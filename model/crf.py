# -*- encoding: utf-8 -*-
'''
@File    :   crf.py
@Time    :   2022/4/1
@Author  :   Sparklingdeng
@Version :   1.2
'''

import numpy as np
import torch
import torch.nn as nn
from transformers import XLMRobertaModel, BertModel, AutoModel, AutoModelForMaskedLM
from configparser import ConfigParser

train_method = "cn_PLM_crf"
cfg = ConfigParser()
cfg.read("config/Chinese_Tibetan_Config.ini", encoding='utf-8')
batch_size = cfg.getint(train_method, "batch_size")  # 所有的参数都能用get去读成文本
lr = cfg.getfloat(train_method, "lr")
warmup_rate = cfg.getfloat(train_method, "warmup_rate")
weight_decay = cfg.getfloat(train_method, "weight_decay")
patience = cfg.getint(train_method, "patience")
seed = cfg.getint(train_method, "seed")
n_epochs = cfg.getint(train_method, "n_epochs")
logdir = cfg.get(train_method, "logdir")
language = cfg.get(train_method, "language")
train_set = cfg.get(train_method, "train_location")
valid_set = cfg.get(train_method, "valid_location")
model_name = cfg.get(train_method, "model")
pretrained_vector = cfg.get(train_method, "pretrained_vector")
train_type = cfg.get(train_method, "train_type")  # 对于bool值，更推荐getboolean，支持0和1转换为bool值


def argmax(vec):
    # return the argmax as a python int
    _, idx = torch.max(vec, 1)
    return idx.item()


# Compute log sum exp in a numerically stable way for the forward algorithm
def log_sum_exp(vec):
    max_score = vec[0, argmax(vec)]
    max_score_broadcast = max_score.view(1, -1).expand(1, vec.size()[1])
    return max_score + \
           torch.log(torch.sum(torch.exp(vec - max_score_broadcast)))


def log_sum_exp_batch(log_tensor, axis=-1):  # shape (batch_size,n,m)
    return torch.max(log_tensor, axis)[0] + \
           torch.log(torch.exp(log_tensor - torch.max(log_tensor, axis)[0].view(log_tensor.shape[0], -1, 1)).sum(axis))


class Bert_BiLSTM_CRF(nn.Module):
    def __init__(self, tag_to_ix, hidden_dim=768):
        super(Bert_BiLSTM_CRF, self).__init__()
        self.tag_to_ix = tag_to_ix
        self.tagset_size = len(tag_to_ix)
        self.train_type = train_type
        self.model = model_name
        # self.hidden = self.init_hidden()
        if self.model == 'bert':
            self.bert = AutoModel.from_pretrained('model/bert-base-chinese')
        elif self.model == 'CINO':
            self.bert = AutoModel.from_pretrained('model/CINO_base')
        elif self.model == 'Roberta':
            self.bert = AutoModel.from_pretrained('model/roberta-base-bo')
        elif self.model == 'fasttext':
            self.embedding = nn.Embedding.from_pretrained(torch.from_numpy(np.load(pretrained_vector)),
                                                          freeze=False)
            hidden_dim = 300
        self.lstm = nn.LSTM(bidirectional=True, num_layers=2, input_size=hidden_dim, hidden_size=hidden_dim // 2,
                            batch_first=True)
        self.transitions = nn.Parameter(torch.randn(
            self.tagset_size, self.tagset_size
        ))
        self.hidden_dim = hidden_dim
        self.start_label_id = self.tag_to_ix['<CLS>']
        self.end_label_id = self.tag_to_ix['<SEP>']
        self.fc = nn.Linear(hidden_dim, self.tagset_size)

        # fasttext_embedding = TokenEmbedding('./model/sgns.renmin.bigram')
        # embeds = fasttext_embedding[self.vocab.idx_to_token]
        # self.embedding.weight.data.copy_(embeds)
        # self.embedding.weight.requires_grad = False
        # for param in self.embedding.parameters():
        #     param.requires_grad = True
        # for param in self.bert.parameters():
        #     param.requires_grad = True

        # self.bert.eval()  # 知用来取bert embedding

        self.transitions.data[self.start_label_id, :] = -10000
        self.transitions.data[:, self.end_label_id] = -10000

        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.transitions.to(self.device)

    def init_hidden(self):
        return (torch.randn(2, 1, self.hidden_dim // 2),
                torch.randn(2, 1, self.hidden_dim // 2))

    def _forward_alg(self, feats):
        '''
        this also called alpha-recursion or forward recursion, to calculate log_prob of all barX
        '''

        # T = self.max_seq_length
        T = feats.shape[1]
        batch_size = feats.shape[0]

        # alpha_recursion,forward, alpha(zt)=p(zt,bar_x_1:t)
        log_alpha = torch.Tensor(batch_size, 1, self.tagset_size).fill_(-10000.).to(self.device)  # [batch_size, 1, 16]
        # normal_alpha_0 : alpha[0]=Ot[0]*self.PIs
        # self.start_label has all of the score. it is log,0 is p=1
        log_alpha[:, 0, self.start_label_id] = 0

        # feats: sentances -> word embedding -> lstm -> MLP -> feats
        # feats is the probability of emission, feat.shape=(1,tag_size)
        for t in range(1, T):
            log_alpha = (log_sum_exp_batch(self.transitions + log_alpha, axis=-1) + feats[:, t]).unsqueeze(1)

        # log_prob of all barX
        log_prob_all_barX = log_sum_exp_batch(log_alpha)
        return log_prob_all_barX

    def _score_sentence(self, feats, label_ids):
        T = feats.shape[1]
        batch_size = feats.shape[0]

        batch_transitions = self.transitions.expand(batch_size, self.tagset_size, self.tagset_size)
        batch_transitions = batch_transitions.flatten(1)

        score = torch.zeros((feats.shape[0], 1)).to(self.device)
        # the 0th node is start_label->start_word,the probability of them=1. so t begin with 1.
        for t in range(1, T):
            score = score + \
                    batch_transitions.gather(-1, (label_ids[:, t] * self.tagset_size + label_ids[:, t - 1]).view(-1, 1)) \
                    + feats[:, t].gather(-1, label_ids[:, t].view(-1, 1)).view(-1, 1)
        return score

    def _bert_enc(self, x):
        """
        x: [batchsize, sent_len]
        enc: [batch_size, sent_len, 768]
        """
        with torch.no_grad():
            encoded_layer = self.bert(x, return_dict=False)
            # print(encoded_layer)
            # print(encoded_layer[0].shape)

        # enc = encoded_layer[-1]
        # print(enc.shape)
        return encoded_layer[0]

    def _viterbi_decode(self, feats):
        '''
        Max-Product Algorithm or viterbi algorithm, argmax(p(z_0:t|x_0:t))
        '''

        # T = self.max_seq_length
        T = feats.shape[1]
        batch_size = feats.shape[0]

        # batch_transitions=self.transitions.expand(batch_size,self.tagset_size,self.tagset_size)

        log_delta = torch.Tensor(batch_size, 1, self.tagset_size).fill_(-10000.).to(self.device)
        log_delta[:, 0, self.start_label_id] = 0.

        # psi is for the vaule of the last latent that make P(this_latent) maximum.
        psi = torch.zeros((batch_size, T, self.tagset_size), dtype=torch.long)  # psi[0]=0000 useless
        for t in range(1, T):
            # delta[t][k]=max_z1:t-1( p(x1,x2,...,xt,z1,z2,...,zt-1,zt=k|theta) )
            # delta[t] is the max prob of the path from  z_t-1 to z_t[k]
            log_delta, psi[:, t] = torch.max(self.transitions + log_delta, -1)
            # psi[t][k]=argmax_z1:t-1( p(x1,x2,...,xt,z1,z2,...,zt-1,zt=k|theta) )
            # psi[t][k] is the path choosed from z_t-1 to z_t[k],the value is the z_state(is k) index of z_t-1
            log_delta = (log_delta + feats[:, t]).unsqueeze(1)

        # trace back
        path = torch.zeros((batch_size, T), dtype=torch.long)

        # max p(z1:t,all_x|theta)
        max_logLL_allz_allx, path[:, -1] = torch.max(log_delta.squeeze(), -1)

        for t in range(T - 2, -1, -1):
            # choose the state of z_t according the state choosed of z_t+1.
            path[:, t] = psi[:, t + 1].gather(-1, path[:, t + 1].view(-1, 1)).squeeze()

        return max_logLL_allz_allx, path

    def neg_log_likelihood(self, sentence, tags):
        feats = self._get_lstm_features(sentence)  # [batch_size, max_len, 16]
        forward_score = self._forward_alg(feats)
        gold_score = self._score_sentence(feats, tags)
        return torch.mean(forward_score - gold_score)

    def _get_lstm_features(self, sentence):
        """sentence is the ids"""
        # self.hidden = self.init_hidden()
        # print(sentence.shape)
        if self.train_type == 'PLM_bilstm_crf':
            embeds = self._bert_enc(sentence)
            # 过lstm
            enc, _ = self.lstm(embeds)
            # print(enc)# [64, 256, 768]
            # print(enc.shape)
            lstm_feats = self.fc(enc)
            return lstm_feats  # [8, 75, 16]
        elif self.train_type == 'bilstm_crf':
            # print(sentence)
            embeds = self.embedding(sentence)
            # print(embeds)
            enc, _ = self.lstm(embeds)  # [64, 256, 768]
            # print(enc.shape)
            lstm_feats = self.fc(enc)
            return lstm_feats  # [8, 75, 16]
        elif self.train_type == 'PLM_crf':
            embeds = self._bert_enc(sentence)
            lstm_feats = self.fc(embeds)
            return lstm_feats  # [8, 75, 16]

    def forward(self, sentence):  # dont confuse this with _forward_alg above.
        # Get the emission scores from the BiLSTM

        lstm_feats = self._get_lstm_features(sentence)  # [8, 180,768]
        # Find the best path, given the features.
        score, tag_seq = self._viterbi_decode(lstm_feats)
        return score, tag_seq

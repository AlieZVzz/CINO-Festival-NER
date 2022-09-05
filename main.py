# -*- encoding: utf-8 -*-
# Author: Sparkling Deng
# Time: 2022/4/1
# Email: Sparklingdeng@outlook.com

import time
import torch
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np
from torch.utils import data
from model.crf import Bert_BiLSTM_CRF
from transformers import get_cosine_schedule_with_warmup
from utils import NerDataset, pad, tag2idx, idx2tag, get_logger, f1_score, TAGS, setup_seed
from configparser import ConfigParser


class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""

    def __init__(self, patience=5, verbose=False, delta=0):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement.
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_f1_min = np.Inf
        self.delta = delta

    def __call__(self, val_f1, model):

        score = val_f1

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_f1, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            logger.info(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_f1, model)
            self.counter = 0

    def save_checkpoint(self, val_f1, model):
        # Saves model when validation loss decrease.
        if self.verbose:
            logger.info(f'Validation f1 increased ({self.val_f1_min:.6f} --> {val_f1:.6f}).  Saving model ...')

        # torch.save(model.state_dict(), 'checkpoint.pt')	# 这里会存储迄今最优模型的参数
        torch.save(model,
                   'checkpoints/' + language + '_' + model_name + '_' + train_type + '_' + str(
                       round(val_f1, 4)) + '_params.pth')
        self.val_f1_min = val_f1


def train(model, iterator, optimizer, scheduler, criterion, device, epoch):
    model.train()
    for i, batch in enumerate(iterator):
        words, x, is_heads, tags, y, seqlens = batch
        x = x.to(device)
        y = y.to(device)
        _y = y  # for monitoring
        if train_type == "PLM_bilstm":
            output = model(x)
            loss = criterion(output, y)
        else:
            loss = model.neg_log_likelihood(x, y)  # logits: (N, T, VOCAB), y: (N, T)

        # logits = logits.view(-1, logits.shape[-1]) # (N*T, VOCAB)
        # y = y.view(-1)  # (N*T,)
        # writer.add_scalar('data/loss', loss.item(), )

        # loss = criterion(logits, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        if i == 0:
            logger.info("=====sanity check======")
            # print(words[0])
            # print(type(words[0]))
            logger.info("words:%s", words[0])
            logger.info("x:%s", x.cpu().tolist()[0][:seqlens[0]])
            # logger.info("tokens:", tokenizer.convert_ids_to_tokens(x.cpu().numpy()[0])[:seqlens[0]])
            logger.info("y:%s", _y.cpu()[0][:seqlens[0]])
            logger.info("tags:%s", tags[0])
            logger.info("seqlen:%s", seqlens[0])
            logger.info("=======================")

        if i % 10 == 0:  # monitoring
            logger.info("epoch %s step %s, loss %s", str(epoch), i, loss.item())


def eval(model, iterator, f, device):
    model.eval()
    recall_list, precision_list, f1_list = [], [], []
    Words, Is_heads, Tags, Y, Y_hat = [], [], [], [], []
    with torch.no_grad():
        for i, batch in enumerate(iterator):
            words, x, is_heads, tags, y, seqlens = batch
            x = x.to(device)
            # y = y.to(device)
            if train_type == "PLM_bilstm":
                y_hat = model(x)
                y_hat = torch.argmax(y_hat, 1)
            else:
                _, y_hat = model(x)  # y_hat: (N, T)

            Words.extend(words)
            Is_heads.extend(is_heads)
            Tags.extend(tags)
            Y.extend(y.numpy().tolist())
            Y_hat.extend(y_hat.cpu().numpy().tolist())

    for tag in saved_metrics:
        recall, precision, f1 = f1_score(Y, Y_hat, tag, tag2idx)
        saved_metrics[tag]['precision'].append(precision)
        saved_metrics[tag]['recall'].append(recall)
        saved_metrics[tag]['f1'].append(f1)
        recall_list.append(recall)
        precision_list.append(precision)
        f1_list.append(f1)
        logger.info("tag:%s  Recall:%s  Precision:%s  f1:%s", tag, recall, precision, f1)

    with open("temp", 'w', encoding='utf-8') as fout:  # get results and save
        for words, is_heads, tags, y_hat in zip(Words, Is_heads, Tags, Y_hat):
            y_hat = [hat for head, hat in zip(is_heads, y_hat) if head == 1]
            preds = [idx2tag[hat] for hat in y_hat]
            assert len(preds) == len(words.split()) == len(tags.split())
            for w, t, p in zip(words.split()[1:-1], tags.split()[1:-1], preds[1:-1]):
                fout.write(f"{w} {t} {p}\n")
            fout.write("\n")

    y_true = np.array(
        [tag2idx[line.split()[1]] for line in open("temp", 'r', encoding='utf-8').read().splitlines() if len(line) > 0])
    y_pred = np.array(
        [tag2idx[line.split()[2]] for line in open("temp", 'r', encoding='utf-8').read().splitlines() if len(line) > 0])
    num_proposed = len(y_pred[y_pred > 1])
    num_correct = (np.logical_and(y_true == y_pred, y_true > 1)).astype(int).sum()
    num_gold = len(y_true[y_true > 1])

    logger.info("num_proposed:%s", num_proposed)
    logger.info("num_correct:%s", num_correct)
    logger.info("num_gold:%s", num_gold)

    final = f + "_epoch_" + time_stamp + '_' + model_name + "{P%.2fR%.2fF%.2f}.txt" % (
        sum(precision_list) / len(precision_list), sum(recall_list) / len(recall_list), sum(f1_list) / len(f1_list))
    with open(final, 'w', encoding='utf-8') as fout:
        result = open("temp", "r", encoding='utf-8').read()
        fout.write(f"{result}\n")
        fout.write(f"precision={np.mean(precision_list)}\n")
        fout.write(f"recall={np.mean(recall_list)}\n")
        fout.write(f"f1={np.mean(f1_list)}\n")

    os.remove("temp")
    logger.info("precision=%.4f", np.mean(precision_list))
    logger.info("recall=%.4f", np.mean(recall_list))
    logger.info("f1=%.4f", np.mean(f1_list))
    return np.mean(precision_list), np.mean(recall_list), np.mean(f1_list)


if __name__ == "__main__":

    train_method = "bo_PLM_bilstm"
    cfg = ConfigParser()
    cfg.read("config/Chinese_Tibetan_Config.ini", encoding='utf-8')
    batch_size = cfg.getint(train_method, "batch_size")
    patience = cfg.getint(train_method, "patience")
    seed = cfg.getint(train_method, "seed")
    lr = cfg.getfloat(train_method, "lr")
    n_epochs = cfg.getint(train_method, "n_epochs")
    warmup_rate = cfg.getfloat(train_method, "warmup_rate")
    weight_decay = cfg.getfloat(train_method, "weight_decay")
    logdir = cfg.get(train_method, "logdir")
    language = cfg.get(train_method, "language")
    train_set = cfg.get(train_method, "train_location")
    valid_set = cfg.get(train_method, "valid_location")
    model_name = cfg.get(train_method, "model")
    train_type = cfg.get(train_method, "train_type")

    setup_seed(seed)
    time_stamp = time.strftime("%m-%d-%H-%M", time.localtime())
    saved_metrics = {}
    for ent in TAGS:
        saved_metrics[ent] = {'precision': [], 'recall': [], 'f1': []}
    early_stopping = EarlyStopping(patience, verbose=True)
    logger = get_logger(
        'log/NER_' + language.strip('"') + '_' + model_name.strip('"') + '_' + train_type.strip('"') + '_' + str(
            time_stamp) + '.log')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    torch.cuda.empty_cache()

    # model = nn.DataParallel(model)

    train_dataset = NerDataset(train_set)
    eval_dataset = NerDataset(valid_set)
    logger.info('Build Data Done')
    model = Bert_BiLSTM_CRF(tag2idx).to(device)
    logger.info('Initial Model Done')
    train_iter = data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=0,
                                 collate_fn=pad)
    eval_iter = data.DataLoader(dataset=eval_dataset, batch_size=batch_size, shuffle=True, num_workers=0,
                                collate_fn=pad)
    logger.info('Load Data Done')

    param_optimizer = list(model.named_parameters())
    no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
         'weight_decay': weight_decay},
        {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}]
    optimizer = optim.AdamW(optimizer_grouped_parameters, lr=lr)
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    total_steps = len(train_iter) * batch_size
    scheduler = get_cosine_schedule_with_warmup(optimizer=optimizer, num_warmup_steps=warmup_rate * total_steps,
                                                num_training_steps=total_steps)

    logger.info('Start Train...,')
    for epoch in range(1, n_epochs + 1):  # 每个epoch对dev集进行测试
        train(model, train_iter, optimizer, scheduler, criterion, device, epoch)
        logger.info(f"=========eval at epoch={epoch}=========")
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        f_name = os.path.join(logdir, str(epoch))
        precision, recall, f1 = eval(model, eval_iter, f_name, device)
        np.save('checkpoints/' + language + '_' + train_type + '_' + model_name + '.npy', saved_metrics)
        early_stopping(f1, model)  # 若满足 early stopping 要求
        if early_stopping.early_stop:
            logger.info("Early stopping")  # 结束模型训练
            break

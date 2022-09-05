import numpy as np
import logging
import torch
from torch.utils.data import Dataset
import collections
from transformers import XLMRobertaTokenizer, XLMRobertaModel, BertTokenizer, AutoTokenizer
from configparser import ConfigParser
import random

train_method = "bo_PLM_bilstm"
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
pretrained_dict = cfg.get(train_method, "pretrained_dict")
model_name = cfg.get(train_method, "model")
train_type = cfg.get(train_method, "train_type")  # 对于bool值，更推荐getboolean，支持0和1转换为bool值

TAGS = ['Festival', 'Item', 'Event', 'Location']
VOCAB = (
    '<PAD>', '<CLS>', '<SEP>', 'O', 'B-Festival', 'M-Festival', 'E-Festival', 'B-Item', 'M-Item', 'E-Item', 'S-Item',
    'B-Event',
    'M-Event', 'E-Event', 'B-Location', 'M-Location', 'E-Location', 'S-Location')
Color_MAP = {'Festival': '#3772FF', 'Item': '#EF709D', 'Event': '#E2EF70', 'Location': '#FFEAAE'}
tag2idx = {tag: idx for idx, tag in enumerate(VOCAB)}
idx2tag = {idx: tag for idx, tag in enumerate(VOCAB)}
MAX_LEN = 256 - 2


def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)


class NerDataset(Dataset):
    def __init__(self, f_path):
        self.model = model_name
        with open(f_path, 'r', encoding='utf-8') as fr:
            entries = fr.read().strip().split('\n\n')
        sents, tags_li = [], []  # list of lists
        for entry in entries:
            words = [line.split()[0] for line in entry.splitlines()]
            tags = ([line.split()[-1] for line in entry.splitlines()])
            if len(words) > MAX_LEN:
                # 先对句号分段
                word, tag = [], []
                for char, t in zip(words, tags):

                    if char != '。':
                        if char != '\ue236':  # 测试集中有这个字符
                            word.append(char)
                            tag.append(t)
                    else:
                        sents.append(["<CLS>"] + word[:MAX_LEN] + ["<SEP>"])
                        tags_li.append(['<CLS>'] + tag[:MAX_LEN] + ['<SEP>'])
                        word, tag = [], []
                        # 最后的末尾
                if len(word):
                    sents.append(["<CLS>"] + word[:MAX_LEN] + ["<SEP>"])
                    tags_li.append(['<CLS>'] + tag[:MAX_LEN] + ['<SEP>'])
                    word, tag = [], []
            else:
                sents.append(["<CLS>"] + words[:MAX_LEN] + ["<SEP>"])
                tags_li.append(['<CLS>'] + tags[:MAX_LEN] + ['<SEP>'])
        self.sents, self.tags_li = sents, tags_li
        if self.model == 'bert':
            bert_model = 'model/roberta-chinese'
            self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
        elif self.model == 'CINO':
            bert_model = 'model/CINO_base'
            self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
        elif self.model == 'Roberta':
            bert_model = 'model/roberta-base-bo'
            self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
        elif self.model == 'bert-base':
            bert_model = 'bert-base-chinese'
            self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
        elif self.model == 'albert':
            bert_model = 'ckiplab/albert-tiny-chinese'
            self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
        elif self.model == 'ernie':
            self.tokenizer = AutoTokenizer.from_pretrained('model/ernie')
        elif self.model == 'fasttext':
            # bert_model = 'model/roberta-chinese'
            # self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
            self.vocab = np.load(pretrained_dict, allow_pickle=True).item()

    def __getitem__(self, idx):

        words, tags = self.sents[idx], self.tags_li[idx]
        # print(words)
        x, y = [], []
        is_heads = []

        for w, t in zip(words, tags):
            # print(w)
            # print(t)
            if self.model == 'fasttext':
                xx = [self.vocab.get(w, 0)]
                is_head = [1]
                t = [t]
            else:
                tokens = self.tokenizer.tokenize(w) if w not in ("<CLS>", "<SEP>") else [w]
                # tokens = w if w not in ("<CLS>", "<SEP>") else [w]
                xx = self.tokenizer.convert_tokens_to_ids(tokens)

                # CINO
                # xx = [xx]
                assert len(tokens) == len(xx), f"len(tokens)={len(tokens)}, len(xx)={len(xx)}"
                # 非 CINO
                is_head = [1] + [0] * (len(tokens) - 1)
                t = [t] + ['<PAD>'] * (len(tokens) - 1)
                # CINO
                # is_head = [1] + [0] * (len(xx) - 1)
                # t = [t] + ['<PAD>'] * (len(xx) - 1)
            # print(xx)
            # 中文没有英文wordpiece后分成几块的情况
            # print(len(w))

            is_heads.extend(is_head)
            yy = [tag2idx[each] for each in t]

            x.extend(xx)
            y.extend(yy)
        assert len(x) == len(y) == len(is_heads), f"len(x)={len(x)}, len(y)={len(y)}, len(is_heads)={len(is_heads)}"

        # seqlen
        seqlen = len(y)

        # to string
        words = " ".join(words)
        tags = " ".join(tags)

        assert len(x) == len(y) == len(is_heads), f"len(x)={len(x)}, len(y)={len(y)}, len(is_heads)={len(is_heads)}"
        return words, x, is_heads, tags, y, seqlen

    def __len__(self):
        return len(self.sents)

    def __vocab__(self):
        return self.vocab


def pad(batch):
    '''Pads to the longest sample'''
    f = lambda x: [sample[x] for sample in batch]
    words = f(0)
    is_heads = f(2)
    tags = f(3)
    seqlens = f(-1)
    maxlen = np.array(seqlens).max()

    f = lambda x, seqlen: [sample[x] + [0] * (seqlen - len(sample[x])) for sample in batch]  # 0: <pad>
    x = f(1, maxlen)
    y = f(-2, maxlen)

    f = torch.LongTensor

    return words, f(x), is_heads, tags, f(y), seqlens


def get_logger(filename, verbosity=1, name=None):
    level_dict = {0: logging.DEBUG, 1: logging.INFO, 2: logging.WARNING}
    formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(level_dict[verbosity])

    fh = logging.FileHandler(filename, "w", encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger


def count_corpus(tokens):
    """Count token frequencies."""
    # Here `tokens` is a 1D list or 2D list
    if len(tokens) == 0 or isinstance(tokens[0], list):
        # Flatten a list of token lists into a list of tokens
        tokens = [token for line in tokens for token in line]
    return collections.Counter(tokens)


def truncate_pad(line, num_steps, padding_token):
    """Truncate or pad sequences."""
    if len(line) > num_steps:
        return line[:num_steps]  # Truncate
    return line + [padding_token] * (num_steps - len(line))  # Pad


def get_tags(path, tag, tag_map):
    begin_tag = tag_map.get("B-" + tag)
    mid_tag = tag_map.get("M-" + tag)
    end_tag = tag_map.get("E-" + tag)
    single_tag = tag_map.get("S-" + tag)
    o_tag = tag_map.get("O")
    begin = -1
    end = 0
    tags = []
    last_tag = 0
    for index, tag in enumerate(path):
        if tag == begin_tag and index == 0:
            begin = 0
        elif tag == begin_tag:
            begin = index
        elif tag == end_tag and last_tag in [mid_tag, begin_tag] and begin > -1:
            end = index
            tags.append([begin, end])
        elif tag == o_tag or tag == single_tag:
            begin = -1
        last_tag = tag
    return tags


def f1_score(tar_path, pre_path, tag, tag_map):
    origin = 0.
    found = 0.
    right = 0.
    for fetch in zip(tar_path, pre_path):
        tar, pre = fetch
        tar_tags = get_tags(tar, tag, tag_map)
        pre_tags = get_tags(pre, tag, tag_map)

        origin += len(tar_tags)
        found += len(pre_tags)

        for p_tag in pre_tags:
            if p_tag in tar_tags:
                right += 1

    recall = 0. if origin == 0 else (right / origin)
    precision = 0. if found == 0 else (right / found)
    f1 = 0. if recall + precision == 0 else (2 * precision * recall) / (precision + recall)
    return recall, precision, f1


def format_result(output, index, result, text, tag, lang):
    # print(text)
    for i in result:
        begin, end = i
        entity_dict = output[index]['entities']
        if lang == 'zh':
            entity_dict.append({
                "start": begin - 1,
                "stop": end,
                "entity": ''.join(text[begin:end + 1]),
                "type": tag,
                "color": Color_MAP.get(tag)
            })
        elif lang == 'dz':
            entity_dict.append({
                "start": begin-1,
                "stop": end,
                "entity": ''.join(text[begin:end+1]),
                "type": tag,
                "color": Color_MAP.get(tag)
            })
        # print(text[begin:end+1])
        # output[index]['entities']['start'] = begin
        # output[index]['entities']['stop'] = end + 1
        # output[index]['entities']['idx'] = text[begin:end + 1]
        # output[index]['entities']['stop'] = tag

    return output

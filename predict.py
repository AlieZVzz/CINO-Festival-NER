import torch
import json
from utils import get_tags, format_result, tag2idx, TAGS, idx2tag
from transformers import BertTokenizer, AutoTokenizer
import langid
import html2text

device = 'cuda' if torch.cuda.is_available() else 'cpu'
bert_model = 'model/bert-base-chinese'

# print(langid.classify('藏历新年是藏族人民传统新年，西藏最隆重的节日之一，寺庙僧侣与俗人共同欢庆的节日。'))
# 载入GPU



test_path = 'data_collect/test.txt'
file = open(test_path, 'r', encoding='utf-8')
input = file.readlines()
file.close()
output = []

for i, input_str in enumerate(input):
    if langid.classify(input_str)[0] == 'dz':
        tokenizer = AutoTokenizer.from_pretrained('model/roberta-base-bo')
        model = torch.load('checkpoints/bo_PLM_bilstm_crf_0.8627439588725075_params.pth', map_location=device)
        lang = 'dz'
        x = tokenizer.encode(input_str)
        # text = tokenizer.decode(x)
        text = input_str
        # text = html2text.html2text(text)

    elif langid.classify(input_str)[0] == 'zh':
        tokenizer = BertTokenizer.from_pretrained(bert_model)
        model = torch.load('checkpoints/cn_PLM_bilstm_crf_0.925024408229689_params.pth', map_location=device)
        lang = 'zh'
        # input_str = html2text.html2text(input_str)
        x = tokenizer.encode(input_str)
        text = tokenizer.decode(x).split(' ')

    else:
        print('wrong language')
        break
    # x = tokenizer.encode(input_str)
    # print(x)
    # text_1 = tokenizer.decode(x)
    # print(html2text.html2text(text_1))
    # text = tokenizer.decode(x).split(' ')
    # print(text)
    output.append({'text': input_str.strip(), "entities": [], "tokenized": text[1:-1]})
    # print(x)
    x = torch.tensor(x).unsqueeze(dim=0)

    x = x.to(device)
    # convert to tensor
    _, predict = model(x)
    paths = predict.to('cpu').tolist()
    print(paths)
    # print(paths[0][1:-1])
    # output = [idx2tag.get(i) for i in predict]
    for tag in TAGS:
        tags = get_tags(paths[0], tag, tag2idx)
        # for z,g in tags:
        #     print(text_1[z:g])

        output = format_result(output, i, tags, text, tag, lang)
with open("output/predict.json", "w+", encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False)

    #     output = format_result(output, i, tags, input_str, tag)
    # with open("output/predict.json", "w+") as f:
    #     json.dump(output, f, ensure_ascii=False)
    # file.close()

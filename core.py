import torch
import json
from utils import get_tags, format_result, tag2idx, TAGS, idx2tag
from transformers import BertTokenizer, AutoTokenizer
import langid


def predict(message_text):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # 载入GPU
    output = []
    message_text = [message_text]
    for i, input_str in enumerate(message_text):
        if langid.classify(input_str)[0] == 'dz':
            tokenizer = AutoTokenizer.from_pretrained('model/roberta-base-bo')
            model = torch.load("checkpoints/bo_PLM_bilstm_crf_0.8433_params.pth", map_location=device)
            lang = 'dz'
            x = tokenizer.encode(input_str)
            # text = tokenizer.decode(x)

            text = [tokenizer.convert_ids_to_tokens(j) for j in x]
            output.append({'text': input_str.strip(), "entities": [], "tokenized": text})
            # text = html2text.html2text(text)

        elif langid.classify(input_str)[0] == 'zh':
            bert_model = 'model/roberta-chinese'
            tokenizer = AutoTokenizer.from_pretrained(bert_model)
            model = torch.load('checkpoints/cn_PLM_bilstm_crf_0.9305245629140657_params.pth', map_location=device)
            lang = 'zh'
            # input_str = html2text.html2text(input_str)
            x = tokenizer.encode(input_str)
            text = [tokenizer.convert_ids_to_tokens(j) for j in x]
            output.append({'text': input_str.strip(), "entities": [], "tokenized": text[1:-1]})

        else:
            print('wrong language')
            break
        # x = tokenizer.encode(input_str)
        # print(x)
        # text_1 = tokenizer.decode(x)
        # print(html2text.html2text(text_1))
        # text = tokenizer.decode(x).split(' ')
        # print(text)

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
    return output


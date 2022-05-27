path = '../data_collect/tibet_data_bio.txt'
res_path = '../data_collect/tibet_data_bmes.txt'


f = open(path, encoding='utf-8')
f1 = open(res_path, "w+", encoding='utf-8')
sentences = []
sentence = []
label_set = set()
cnt_line = 0
for line in f:

    cnt_line += 1
    if len(line) == 0 or line[0] == "\n":
        if len(sentence) > 0:
            sentences.append(sentence)
            # print(sentence)
            sentence = []
        continue
    splits = line.split(' ')
    sentence.append([splits[0], splits[-1][:-1]])
    label_set.add(splits[-1])

if len(sentence) > 0:
    sentences.append(sentence)
    sentence = []
f.close()

# �ļ�ת�� �洢�ļ�
for sen in sentences:
    # print(sen)
    # print(sen)
    i = 0
    for index, word in enumerate(sen):
        char = word[0]
        label = word[1]

        if index < len(sen) - 1:
            if (label[0] == 'B'):
                if sen[index + 1][1][0] == 'I':
                    label = label
                elif sen[index + 1][1][0] == 'B':
                    label = 'S' + label[1:]
                elif sen[index + 1][1][0] == 'O':
                    label = 'S' + label[1:]
            elif (label[0] == 'I'):
                if sen[index + 1][1][0] == 'I':
                    label = 'M' + label[1:]
                if sen[index + 1][1][0] == 'O' or sen[index + 1][1][0] == 'B':
                    label = 'E' + label[1:]
            elif (label[0] == 'O'):
                label = label
        else:
            if (label[0] == 'B'):
                label = 'S' + label[1:]
            elif (label[0] == 'I'):
                label = 'E' + label[1:]
            elif (label[0] == 'O'):
                label = label

        f1.write(f'{char} {label}\n')
    f1.write('\n')
f1.close()

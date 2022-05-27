import re

f = open("../data_collect/藏语all.txt", "r", encoding='utf-8')
line = f.readline()
line = line[:-1]
list2 = []
while line:
    line = f.readline()
    line = line[:-1]
    p5 = re.compile(r'[@||$](.*?)[#]', re.S)
    p6 = re.compile(r'[#](.*?)[*]', re.S)
    p7 = re.findall(p5, line)
    # print(p7)
    p8 = re.findall(p6, line)
    # print(p8)
    list1 = re.sub(r'[[](.*?)[]]', '+', line)
    print(list1)
    sum = 0
    for str in list1.split(' '):

        if str != '+':
            str = str + ' O'
            # print(str)
            list2.append(str)
        else:
            sum += 1
            a = 0
            if (len(p7) > sum - 1):
                for j in p7[sum - 1]:

                    if a == 0:
                        # print(j + ' B-' + p4[sum - 1])
                        list2.append(j + ' B-' + p8[sum - 1])
                    else:
                        # print(j + ' I-' + p4[sum - 1])
                        list2.append(j + ' I-' + p8[sum - 1])
                    a += 1
            else:
                print(p7)
                continue
# print(list)
with open("../data_collect/tibet_data_bio.txt", "w", encoding='utf-8') as w:
    print(list2)
    for i in list2:
        if (i != '　 O'):
            if (i == '。 ' + 'O'):
                w.write('\n')
            else:
                w.write(i)
                w.write('\n')

        else:
            continue

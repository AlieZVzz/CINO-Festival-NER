from sklearn.model_selection import train_test_split

total_list = []
singe_list = []
with open('../data_collect/cn_valid_bmes.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        if i == '\n':
            singe_list.append(i)
            total_list.append(singe_list)
            singe_list = []
        else:
            singe_list.append(i)
# print(total_list)
new_total_list = []
for i in total_list:
    for j in i:
        if j != '\n' and j[2] == 'B' :
            new_total_list.append(i)
print(new_total_list)
x_train, x_test = train_test_split(new_total_list, test_size=0.5)
print(len(x_train))
print(len(x_test))


with open('../data_collect/cn_valid1_bmes.txt', 'w', encoding='utf-8') as f1:
    for i in x_train:
        for j in i:
            f1.write(j)

with open('../data_collect/bo_test1_bmes.txt', 'w', encoding='utf-8') as f2:
    for i in x_test:
        for j in i:
            f2.write(j)

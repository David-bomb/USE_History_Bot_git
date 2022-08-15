import json

with open('dates.txt', encoding='utf-8') as file:
    info = file.readlines()
jsn = []
for k in info:
    i = k.strip()
    if i[0] != '#':
        # print(i.split(' – '))
        jsn.append((i.split(' – ')[0], ' - '.join(i.split(' – ')[1:])))
    else:
        jsn.append(i)
# print(*info)
print(*jsn, sep='\n')

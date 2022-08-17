import json

with open('dates.txt', encoding='utf-8') as file:
    info = file.readlines()
jsn = {}
# lol = 0
for k in info:
    i = k.strip()
    if i[0] != '#':
        # lol += 1
        # print(i.split(' – ')[1][-1], lol)
        jsn[i.split(' – ')[0]] = i.split(' – ')[1]
    # else:
        # jsn.append(i)
# print(*txtDates)
print(jsn)
'''with open("dates.json", "w") as file:
    json.dump(jsn, file)'''
'''with open("dates.json", "r") as read_file:
    JsDates = json.load(read_file)
print(JsDates)'''

import json
with open('dates.txt', encoding='utf-8') as file:
  info = file.readlines()
print(*info)
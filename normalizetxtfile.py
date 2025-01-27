import unicodedata


with open('page_14.txt', 'r', encoding='utf8') as f:
    data = f.read()

data_normalized = unicodedata.normalize('NFC', data)

with open('page_14_normalized.txt', 'w', encoding='utf8') as f:
    f.write(data_normalized)
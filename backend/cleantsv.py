import csv
import re

def is_japanese(text):
    # Returns True if the text contains Hiragana, Katakana, or Kanji
    return bool(re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]', text))

def is_english(text):
    # Returns True if the text contains at least some ascii letters (not just symbols)
    return bool(re.search(r'[A-Za-z]', text))

with open('data/en-ja.tsv', 'r', encoding='utf-8') as infile, \
     open('data/en-ja_clean.tsv', 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerow(['en', 'ja'])  # header

    for row in reader:
        # Try all pairs in each row to find likely en/ja sentences
        candidates = []
        for i in range(len(row)-1):
            en_candidate = row[i].strip()
            ja_candidate = row[i+1].strip()
            if is_english(en_candidate) and is_japanese(ja_candidate):
                candidates.append((en_candidate, ja_candidate))
        # If we found candidates, write the first one (or all if you want)
        if candidates:
            writer.writerow(candidates[0])

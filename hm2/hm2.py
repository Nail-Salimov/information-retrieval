from urllib.request import urlopen
import glob
from bs4 import BeautifulSoup
import re
import pymorphy2


# проверяет русское ли слово
def is_russian_word(word):
    for letter in word:
        e = ord(letter)
        if e not in range(ord('А'), ord('Я') + 1) and e not in range(ord('а'), ord('я') + 1) \
                and e != ord('Ё') and e != ord('ё'):
            return False
    return True


# возвращает слова из html файла
def get_words_from_html(path):
    f = open(path, "r", encoding='utf-8')
    html = f.read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style", "header", "footer"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    # разбить слова построчно
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # отбрасить пустые строки
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # разбить слова по символам (split)
    dirty_words = set(re.split(' |\n|«|»|,|:|–|-|}|{', text))

    clear_words = [w for w in filter(is_russian_word, dirty_words)]
    # word = re.sub('[^0-9А-Яa-я]+', '', str)
    clear_words = [re.sub('[^0-9А-Яa-яёЁ]+', ' ', w).strip() for w in clear_words]
    return_words = set()
    for word in clear_words:
        s = word.split()
        return_words.update(tuple(s))
    return return_words


# возвращает слова из всех html файлов в директории
def get_all_words(directory):
    paths = glob.glob(directory + "/*.html")
    words = set()
    for path in paths:
        html_words = get_words_from_html(path)
        words = words.union(html_words)
    words = [w for w in filter(is_russian_word, words)]
    return words


# создает файл со словами
def create_tokens_file(words):
    with open('tokens.txt', 'a', encoding='utf-8') as file:
        for word in words:
            file.write(word + "\n")


# возвращает словарь вида: лемма - [слова]
def get_lemmas_dict(words):
    morph = pymorphy2.MorphAnalyzer()
    lemmas_dict = dict()
    for word in words:
        p = morph.parse(word)[0]
        lemma = p.normal_form
        if lemma in lemmas_dict:
            l_words = lemmas_dict[lemma]
            l_words.append(word)
            lemmas_dict[lemma] = l_words
        else:
            lemmas_dict[lemma] = [word]

    return lemmas_dict


# создает файл с леммами
def create_lemmas_file(words):
    lemmas_dict = get_lemmas_dict(words)
    with open('lemmas.txt', 'a', encoding='utf-8') as file:
        for lemma in lemmas_dict:
            words = lemmas_dict[lemma]
            s = ' '.join(str(e) for e in words)
            s = lemma + ": " + s
            file.write(s + "\n")


all_words = get_all_words('../html')
create_tokens_file(all_words)
create_lemmas_file(all_words)

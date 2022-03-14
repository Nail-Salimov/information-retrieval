from nltk.tokenize import word_tokenize
import pymorphy2
from bs4 import BeautifulSoup
import re

def is_russian_word(word):
    for letter in word:
        e = ord(letter)
        if (e < 1040 or e > 1071) and (e < 1072 or e > 1078):
            return False
        return True

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

    r = re.compile("[а-яА-Я]+")
    clear_words = [w for w in filter(is_russian_word, dirty_words)]
    # word = re.sub('[^0-9А-Яa-я]+', '', str)
    clear_words = [re.sub('[^0-9А-Яa-я]+', ' ', w).strip() for w in clear_words]
    return_words = set()
    for word in clear_words:
        s = word.split()
        return_words.update(tuple(s))
    return return_words

lemmas_file = open("C:\\Users\\Айдар\\PycharmProjects\\information-retrieval\\hm2\\lemmas.txt", "r", encoding='utf-8')
index = {}
for line in lemmas_file:
    lemma = line.split(':')[0]
    index[lemma] = []

morph = pymorphy2.MorphAnalyzer()
for i in range(1, 115):
    tokens = get_words_from_html("C:\\Users\\Айдар\\PycharmProjects\\html\\html\\" + str(i) + ".html")
    for token in tokens:
        normal_form = morph.parse(token)[0].normal_form
        if normal_form in index:
            index[normal_form].append(i)

inverted_index_file = open("inverted_index.txt", "a", encoding='utf-8')
for i in index:
    inverted_index_file.write(i + ":")
    for num in index[i]:
        inverted_index_file.write(" " + str(num))
    inverted_index_file.write("\n")
inverted_index_file.close()
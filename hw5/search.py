import collections
import functools
import math


def line_to_record(line):
    term_and_tf_idf = line.split(' ')

    return {
        'term': term_and_tf_idf[0],
        'tf': float(term_and_tf_idf[1]),
        'idf': float(term_and_tf_idf[2])
    }


idf = {}
for i in range(0, 114):
    file_ = open('../hm4/term/term/' + str(i) + '.txt', 'r', encoding='utf-8')
    records_ = [line_to_record(line) for line in file_]
    for r_ in records_:
        idf[r_['term']] = r_['idf']


def read_weights(path):
    file = open(path, 'r', encoding='utf-8')
    records = [line_to_record(line) for line in file]
    return {r['term']: r['tf'] * r['idf'] for r in records}


def get_weights(text: str):
    text = text.lower()
    terms = text.split(' ')
    length = len(terms)
    term_to_count = collections.Counter(terms)
    return {t: c / length * idf[t] for t, c in term_to_count.most_common()}


def vec_len(vec):
    return math.sqrt(functools.reduce(lambda x, x1: x + x1, map(lambda x: x * x, vec)))


def similarity(path, search_text):
    doc = read_weights(path)
    search = get_weights(search_text)
    terms = list(set().union(doc, search))
    terms.sort()
    doc_vec = [doc.get(term, .0) for term in terms]
    search_vec = [search.get(term, .0) for term in terms]
    numerator = functools.reduce(lambda x, x1: x + x1, [doc_vec[j] * search_vec[j] for j in range(0, len(terms))])
    enumerator = vec_len(doc_vec) * vec_len(search_vec)
    return numerator / enumerator


def search(search_text):
    return sorted([{'similarity': similarity('../hm4/term/term/' + str(j) + '.txt', search_text), 'index': j} for j
                   in range(0, 114)],
                  key=lambda d: d['similarity'], reverse=True)


if __name__ == '__main__':
    print(search('вайпить андроид'))

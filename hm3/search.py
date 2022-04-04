import pymorphy2


def bool_search(query_string):
    inverted_index_file = open("inverted_index.txt", "r", encoding='utf-8')
    index = {}
    for line in inverted_index_file:
        lemma_and_ids = line.split(': ')
        if len(lemma_and_ids) > 1:
            index[lemma_and_ids[0]] = [int(n) for n in lemma_and_ids[1].split(' ')]

    parts = query_string.split(" ")
    for i in range(1, len(parts), 2):
        if parts[i] != '||' and parts[i] != '&&':
            raise ValueError("query is not correct")

    morph = pymorphy2.MorphAnalyzer()
    lemma = morph.parse(parts[0])[0].normal_form

    if lemma in index:
        result = set(index[lemma])
    else:
        result = set()

    for i in range(2, len(parts), 2):
        lemma = morph.parse(parts[i])[0].normal_form
        documents = set()
        if lemma in index:
            documents = index[lemma]

        if parts[i - 1] == '&&':
            result = result.intersection(documents)
        else:
            result = result.union(documents)

    return result


if __name__ == '__main__':
    print(bool_search('автоматизированный && лоремипсумамено'))

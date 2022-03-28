import  math
import os
import shutil


def read_terms(path):
    word_count = {}
    dic = {}

    f = open(path, "r")
    while True:
        line = f.readline()
        if not line:
            break
        str = line.strip()
        elem = str.split(":", 2)
        term = elem[0]
        pos = elem[1].split()

        for p in pos:
            if p in dic:
                html_dic = dic[p]
                if term in html_dic:
                    count = html_dic[term]
                    html_dic[term] = count + 1
                else:
                    html_dic[term] = 1

            else:
                html_dic = {term: 1}
                dic[p] = html_dic

            if p in word_count:
                count = word_count[p]
                word_count[p] = count + 1
            else:
                word_count[p] = 1

    return dic, word_count


def l_counts(path, term_dic):
    term_to_lem = {}
    f = open(path, "r")
    while True:
        line = f.readline()
        if not line:
            break
        str = line.strip()
        elem = str.split(":", 2)
        lem = elem[0]
        terms = elem[1].split()
        for term in terms:
            term_to_lem[term.lower()] = lem

    lem_dic = {}
    for i in term_dic:
        i_dic = term_dic[i]
        new_i_dic = {}
        for term in i_dic:
             #TODO проверка слово из inverted_term_index есть в lemmas, как термин (не лемма)
            if term in term_to_lem:
                lem = term_to_lem[term]
                if lem in new_i_dic:
                    lem_count = new_i_dic[lem]
                    new_i_dic[lem] = lem_count + i_dic[term]
                else:
                    new_i_dic[lem] = i_dic[term]
        lem_dic[i] = new_i_dic
    return lem_dic

#directory - папка куда сохранятся файлы
def write_term_param(directory, dic, word_count):
    d = directory
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for i in dic:
        path = d + "/" + i + ".txt"
        word_dic = dic[i]
        all_count = word_count[i]
        with open(path, 'a') as file:
            for term in word_dic:
                term_count = word_dic[term]
                tf = term_count / all_count
                idf = math.log(all_count / term_count)
                s = term + " " + str(tf) + " " + str(idf)
                file.write(s + "\n")


dic, word_count = read_terms("inverted_term_index.txt")
l_dic = l_counts("lemmas.txt", dic)
write_term_param("term", dic, word_count)
write_term_param("lem", l_dic, word_count)





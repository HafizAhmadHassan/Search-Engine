from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import doc_index_row
import codecs

def get_dir_name(directory_name):
    onlyfiles = [f for f in listdir(directory_name) if isfile(join(directory_name, f))]
    return onlyfiles


def get_tokens(file, directory_name, ans):
    file_name = directory_name + '/' + file

    with codecs.open(file_name, "r", encoding='utf-8', errors='ignore') as data:
        text = data.read()[700:]
    data.close()

    soup = BeautifulSoup(text, "html.parser")
    result = re.sub(r'[\ \n]{2,}', '', soup.text)
    each_tokens = result.split()

    for token in each_tokens:
        result = re.match("\w+(\.?\w+)*", token)
        if result:
            if re.match("\w+(\.?\w+)*", token).group() == token:
                ans.append(token.lower())


def get_stop_words_list(stop_words):
    with open('F:/BSCS-FAST/Semester 7/Informaiton Retrieval/assignments/assignments/learning/stoplist.txt') as stop_words_file:
        for line in stop_words_file:
            line = line.strip()
            stop_words.append(line)


def filter_ans_from_stop_words(ans, stop_words_filtered_list, stop_words):
    for token in ans:
        if not token in stop_words:
            stop_words_filtered_list.append(token)


def apply_stemming(stop_words_filtered_list):
    stemmer = PorterStemmer()
    stems = [stemmer.stem(token) for token in stop_words_filtered_list]
    return stems


def create_docids_txt_file(files):
    fw = open('docids.txt', 'w')
    for i in range(len(files)):
        fw.write(str(i) + '\t' + files[i])
        fw.write('\n')
    fw.close()


def create_termids_txt_file(stems):
    fw = open('termids.txt', 'w')
    for i in range(len(stems)):
        fw.write(str(i) + '\t' + stems[i])
        fw.write('\n')
        print("creating term id file")
    fw.close()


def get_this_doc_tokens(file, directory_name):
    file_name = directory_name + '/' + file

    with codecs.open(file_name, "r", encoding='utf-8', errors='ignore') as data:
        text = data.read()[700:]
    data.close()

    soup = BeautifulSoup(text, "html.parser")
    result = re.sub(r'[\ \n]{2,}', '', soup.text)
    each_tokens = result.split()

    this_doc_tokens = []
    for token in each_tokens:
        result = re.match("\w+(\.?\w+)*", token)
        if result:
            if re.match("\w+(\.?\w+)*", token).group() == token:
                this_doc_tokens.append(token.lower())

    stop_words = []
    stop_words_filtered_list = []

    get_stop_words_list(stop_words)
    filter_ans_from_stop_words(this_doc_tokens, stop_words_filtered_list, stop_words)

    this_doc_tokens = apply_stemming(stop_words_filtered_list)

    return this_doc_tokens


def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def create_doc_index_objects(files, unique_stems, doc_index):
    doc_index_rows = []
    count = 0
    for i in range(len(files)):
        for j in range(len(unique_stems)):
            if unique_stems[j] in doc_index.get(i):
                token_indexes = list_duplicates_of(doc_index.get(i), unique_stems[j])
                new_row = doc_index_row.doc_index_row(i, j, token_indexes)
                doc_index_rows.append(new_row)
                print("creating doc index objects: ", count)
                count = count + 1
    return doc_index_rows


def create_doc_index_txt_file(doc_index_rows):
    with open('doc_index.txt', 'w') as fp:
        for doc_index_row in doc_index_rows:
            doc_id, tab, term_id, tab = doc_index_row.doc_id, '\t', doc_index_row.term_id, '\t'
            fp.writelines('{} {} {} {}'.format(doc_id, tab, term_id, tab))
            for position in doc_index_row.positions:
                fp.writelines('{} {}'.format(position, '\t'))
            fp.writelines('\n')


import sys
import functions


ans = []


directory_name = "F:/BSCS-FAST/semester 7/Informaiton Retrieval/assignments/assignments/learning\pa1-data/0"
files = functions.get_dir_name(directory_name)

for file in files:
    functions.get_tokens(file, directory_name, ans)

stop_words = []
stop_words_filtered_list = []

unique_ans = set(ans)
unique_ans = list(unique_ans)

functions.get_stop_words_list(stop_words)
functions.filter_ans_from_stop_words(unique_ans, stop_words_filtered_list, stop_words)

stems = functions.apply_stemming(stop_words_filtered_list)

unique_stems = set(stems)
unique_stems = list(unique_stems)

functions.create_docids_txt_file(files)
functions.create_termids_txt_file(unique_stems)

doc_index = {}
for x in range(len(files)):
    doc_index[x] = functions.get_this_doc_tokens(files[x], directory_name)

doc_index_rows = functions.create_doc_index_objects(files, unique_stems, doc_index)
functions.create_doc_index_txt_file(doc_index_rows)


import inverted_list
from collections import defaultdict


dic = {}
dic = defaultdict(list)

with open("doc_index.txt") as file:
    while True:
        line = file.readline()
        if not line:
            break
        line = line.split()
        for pos in line[2 : ]:
            tuple = (int(line[0]), int(pos))
            dic[int(line[1])].append(tuple)

offsets = {}
with open('term_index.txt', 'w') as fp:
    for key in dic:
        offsets[key] = fp.tell()
        doc_list = [int(i[0]) for i in dic[key]]
        pos_list = [int(i[1]) for i in dic[key]]
        fp.writelines('{} {}'.format(key, '\t'))
        doc_temp = 0
        pos_temp = 0
        for doc, pos in zip(doc_list, pos_list):
            print_doc = doc - doc_temp
            if print_doc is 0:
                print_pos = pos - pos_temp
                fp.writelines('{} {} {} {}'.format(print_doc,':', print_pos, '\t'))
            else:
                fp.writelines('{} {} {} {}'.format(print_doc, ':', pos, '\t'))
            doc_temp = doc
            pos_temp = pos
        fp.writelines('\n')

with open('term_info.txt', 'w') as file:
    for key in dic:
        doc_list = [int(i[0]) for i in dic[key]]
        pos_list = [int(i[1]) for i in dic[key]]
        doc_list = set(doc_list)
        file.writelines('{} {} {} {} {} {} {}'.format(key, '\t', offsets[key], '\t', len(pos_list), '\t', len(doc_list)))
        file.writelines('\n')
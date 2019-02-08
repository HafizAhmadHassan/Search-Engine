import re

def get_doc_id(doc_name):
    check = False
    with open('docids.txt') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.split()
            if line[1] == doc_name:
                doc_id =  line[0]
                check = True
                break
    if check:
        return doc_id
    else:
        return -1

def get_term_id(term):
    check = False
    with open('termids.txt') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.split()
            if line[1] == term:
                term_id = line[0]
                check = True
                break

    if check:
        return term_id
    else:
        return -1

def get_doc_info(doc_name):
    doc_id = get_doc_id(doc_name)

    if doc_id == -1:
        print("Given Document doesn't exist in entire corpus")
        return

    dic = {}
    x = 0
    with open('doc_index.txt') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.split()
            if line[0] == doc_id:
                dic[x] = list(map(int, line[2:]))
                x = x + 1

    sum = 0
    for key in dic.keys():
        sum = sum + len(dic[key])

    print('Listing for Document: ', doc_name)
    print('DOCID: ', doc_id)
    print('Distinct Terms: ', len(dic.keys()))
    print('Total Terms: ', sum)

def get_term_info(term):
    term_id = get_term_id(term)
    if term_id == -1:
        print("Given Term doesn't exist in entire corpus")
        return
    with open('term_info.txt', 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.split()
            if line[0] == term_id:
                byte_offset = line[1]
                total_occurences = line[2]
                total_documents = line[3]


    print('Listing for term: ', term)
    print('TERMID: ', term_id)
    print('Number of documents containing term: ', total_documents)
    print('Term frequency in corpus: ', total_occurences)
    print('Inverted list offset: ', byte_offset)


def get_inverted_list_of_term_document(term, doc_name):
    try:
        term_id = get_term_id(term)
        doc_id = get_doc_id(doc_name)

        if doc_id == -1 or term_id == -1:
            print("Given Document or Term doesn't exist in entire corpus")
            return
        with open('doc_index.txt', 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.split()
                if line[0] == doc_id and line[1] == term_id:
                    count = len(line[2:])
                    break
        print('Inverted list for term: ', term)
        print('In document: ', doc_name)
        print('TERMID: ', term_id)
        print('DOCID: ', doc_id)
        print('Term frequency in document: ', count)
        print('positions: ', ', '.join(map(str, line[2:])))
    except:
        print("Document or term doesn't exist")

# get_doc_info('clueweb12-0311wb-44-23878')
# get_term_info('year')
# get_inverted_list_of_term_document('year', 'clueweb12-0311wb-44-23878')
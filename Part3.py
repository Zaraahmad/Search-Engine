from nltk import PorterStemmer

docID = open("F:\\PycharmProjects\\SearchEngine\\files\\docids.txt", mode="r", encoding="utf-8", errors='ignore')
termID = open("F:\\PycharmProjects\\SearchEngine\\files\\termids.txt", mode="r", encoding="utf-8", errors='ignore')
term_info = open("F:\\PycharmProjects\\SearchEngine\\files\\term_info.txt", 'r', encoding='utf8', errors='ignore')
doc_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\doc_index.txt", mode="r", encoding="utf-8", errors='ignore')
term_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\term_index.txt", mode="r", encoding="utf-8", errors='ignore')

docInd = []
termInd = []
drow = 0
trow = 0
term_r = 0

while True:
    sentence = docID.readline()
    if sentence == '':
        break
    docInd.append([])
    docInd[drow] = sentence.split()
    drow += 1

while True:
    sentence = termID.readline()
    if sentence == '':
        break
    termInd.append([])
    termInd[trow] = sentence.split()
    trow += 1

def terminfo(id):
    while True:
        sentence = term_info.readline()
        if sentence == '':
            break
        sentence = sentence.split()
        if sentence[0] == id:
            break
    return sentence


def docinfo(id):
    occurrence = 0
    t_terms = 0
    found = False
    for line in doc_ind:
        sentence = line.split()
        if sentence[0] == id:
            t_terms = t_terms + len(sentence) - 2
            occurrence += 1  # distinct terms
            found = True
        elif found:
            break
    doc_info = [occurrence, t_terms]
    return doc_info


def getDocId(doc_name):
    for i in range(0, drow):
        if docInd[i][1] == doc_name:
            return docInd[i][0]
    return -1

def getTermId(term):
    for i in range(0, trow):
        if termInd[i][1] == term:
            return termInd[i][0]
    return -1

def getTermInfo(offset, ind):
    term_ind.seek(offset-1)
    sentence = term_ind.readline()
    print("sentence " + sentence)
    words = sentence.split()
    docid = []
    for i in range(1, len(words)):
        docid.append(words[i].split(":"))
    st = 0
    count = 0
    positions = []

    cont = True
    for i in range(0, len(docid)):
        if int(docid[i][0]) != 0:
            st = st + int(docid[i][0])
        if st == ind:
            decode = int(docid[i][1])
            while cont:
                positions.append(docid[i][1])
                count += 1
                i += 1
                if i != len(docid):
                    docid[i][1] = str(int(docid[i][1]) + decode)
                    if int(docid[i][0]) != 0:
                        cont = False
                else:
                    cont = False
            break
    positions.append(count)
    return positions


def parseCommand(command):
    docFound = False
    termFound = False
    if command.find("--doc") != -1:
        docFound = True
    if command.find("--term") != -1:
        termFound = True
    sentence = command.split()
    d_name = ""
    t_name = ""
    if docFound and termFound:
        d_name = sentence[3]
        t_name = sentence[1]
        t_id = getTermId(PorterStemmer().stem(t_name))
        d_id = getDocId(d_name)

        if int(d_id) > 0:
            if int(t_id) > 0:
                temp = terminfo(t_id)
                t_offset = temp[1]
                td_info = getTermInfo(int(t_offset), int(d_id))
                print("Inverted list for term: " + t_name)
                print("In document: " + d_name)
                print("TERMID: " + str(t_id))
                print("DOCID: " + str(d_id))
                length = len(td_info)
                if length > 1:
                    print("Term frequency in document: " + str(td_info[length-1]))
                    i = 0
                    pos = []
                    while i < length-1:
                        pos.append(td_info[i])
                        i += 1
                    #print(*pos, sep = ' ')
                    print("Positions: " + str(pos)[1:-1])
                else:
                    print("Term " + t_name + " is not found in document " + d_name)
            else:
                print("This term does not exist in the inverted index.\n")
        else:
            print("This document does not exist in the corpus.\n")
    elif docFound:
        d_name = sentence[1]
        d_id = getDocId(d_name)
        if int(d_id) > 0:
            d_info = docinfo(d_id)
            print("Listing for document: " + d_name)
            print("DOCID: " + str(d_id))
            print("Distinct terms: " + str(d_info[0]))
            print("Total terms: " + str(d_info[1]))
        else:
            print("This document does not exist in the corpus.\n")
    elif termFound:
        t_name = sentence[1]
        t_id = getTermId(PorterStemmer().stem(t_name))
        #print(type(t_id))
        if int(t_id) > 0:
            t_info = terminfo(t_id)
            #print(t_info)
            print("Listing for term: " + t_name)
            print("TERMID: " + str(t_id))
            print("Number of documents containing term: " + t_info[3])
            print("Term frequency in corpus: " + str(t_info[2]))
            print("Inverted list offset: " + str(t_info[1]))
        else:
            print("This term does not exist in the inverted index.\n")


#term = "matters"
# passage clueweb12-0000tw-35-20780

docID.close()
termID.close()
term_info.close()
doc_ind.close()
term_ind.close()

command = input("Enter command.\n")
loop = True
while loop:
    if command == 'exit':
        loop = False
    else:
        docID = open("F:\\PycharmProjects\\SearchEngine\\files\\docids.txt", mode="r", encoding="utf-8", errors='ignore')
        termID = open("F:\\PycharmProjects\\SearchEngine\\files\\termids.txt", mode="r", encoding="utf-8", errors='ignore')
        term_info = open("F:\\PycharmProjects\\SearchEngine\\files\\term_info.txt", 'r', encoding='utf8', errors='ignore')
        doc_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\doc_index.txt", mode="r", encoding="utf-8", errors='ignore')
        term_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\term_index.txt", mode="r", encoding="utf-8", errors='ignore')

        parseCommand(command)

        docID.close()
        termID.close()
        term_info.close()
        doc_ind.close()
        term_ind.close()
        command = input("Enter command.\n")

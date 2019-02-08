from bs4 import BeautifulSoup #for finding relevant word
import os
from nltk import PorterStemmer

term_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\term_index.txt", 'w', encoding='utf8', errors='ignore')
term_inf = open("F:\\PycharmProjects\\SearchEngine\\files\\term_info.txt", 'w', encoding='utf8', errors='ignore')
doc_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\doc_index.txt", 'r', encoding='utf8', errors='ignore')
termID = open("F:\\PycharmProjects\\SearchEngine\\files\\termids.txt", mode="r", encoding="utf-8", errors='ignore')
docInd = []
tid = []
row = 0

#read the whole doc_index file
while True:
    sentence = doc_ind.readline()
    if sentence == '':
        break
    docInd.append([])
    docInd[row] = sentence.split()
    row += 1

#read term id file
while True:
    sentence = termID.readline()
    if sentence == '':
        break
    sentence = sentence.split()
    tid.append(sentence[0])

#print(docInd)
term_occurence = [] #total occurrence of term in corpus
term_in_docs = [] #total no of docs in which term appears
term_frequency = 0
termdoc = 0
for i in range(0, len(tid)):
    term_ind.write(str(tid[i]))
    previousdoc = 0
    term_frequency = 0
    termdoc = 0
    for j in range(0, row):
        if docInd[j][1] == tid[i]:
            termdoc += 1
            for k in range(2, len(docInd[j])):
                term_frequency += 1
                if k > 2:
                    term_ind.write("\t")
                    result = int(docInd[j][0])-int(previousdoc)
                    term_ind.write(str(result))
                    term_ind.write(":")
                    if result == 0:
                        term_ind.write(str(int(docInd[j][k])-int(previouspos)))
                    else:
                        term_ind.write(docInd[j][k])
                    previousdoc = docInd[j][0]
                    previouspos = docInd[j][k]
                elif k == 2:
                    term_ind.write("\t")
                    term_ind.write(str(int(docInd[j][0])-int(previousdoc)))
                    term_ind.write(":")
                    term_ind.write(docInd[j][k])
                    previousdoc = docInd[j][0]
                    previouspos = docInd[j][k]
    term_occurence.append(term_frequency)
    term_in_docs.append(termdoc)
    term_ind.write("\n")
term_ind.close()

term_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\term_index.txt", 'r', encoding='utf8', errors='ignore')
offset = 1
for i in range(0, len(tid)):
    term_inf.write(tid[i])
    term_inf.write("\t")
    term_inf.write(str(offset))
    term_inf.write("\t")
    term_inf.write("\t")
    term_inf.write(str(term_occurence[i]))
    term_inf.write("\t")
    term_inf.write(str(term_in_docs[i]))
    term_inf.write("\n")
    term_ind.readline()
    #offset = 1 + len(term_ind.readline())
    offset = 1 + term_ind.tell()






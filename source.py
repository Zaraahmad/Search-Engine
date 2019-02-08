# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup  # for finding relevant word
import os
from nltk import PorterStemmer
import operator  # for itemgetter
import math  # for log

# In[2]:


termIDs = {}
docIDs = {}
termDF = {}
Queries = {}
# docIND = {}
tDocTerms = {}  # total terms in a document

# In[3]:


Stop_word_file = open("F:\\PycharmProjects\\SearchEngine\\files\\stoplist.txt", 'r', encoding='utf8', errors='ignore')
stopwords = Stop_word_file.readlines()
stopwords = [x.strip() for x in stopwords]  # removes all leading and trailing spaces from string
Stop_word_file.close()


# In[4]:


def processQuery():
    for key, val in Queries.items():
        sentence = Queries[key]
        words = sentence.lower().split()
        # REGEXXXXXXXXXXXX
        symbols = r"!@#$%^&*”“…’‘|~`()_-\"+=/\}{[,].<';:>?"  # use \ before character that are like eof
        for i in range(0, len(symbols)):
            words = [word.replace(symbols[i], "") for word in words]

        temp = []
        for index, w in enumerate(words):
            if w in stopwords:
                temp.append(w)
            else:
                stemmed = PorterStemmer().stem(w)
                words[index] = stemmed

        for t in temp:
            words.remove(t)

        Queries[key] = words


# In[5]:


def parseQueryTopics():
    QT = open("F:\\PycharmProjects\\SearchEngine\\files\\p2\\topics.xml", mode="r", encoding="utf-8", errors='ignore')
    source_code = QT.read()
    soup = BeautifulSoup(source_code, "html.parser")

    for t in soup.findAll('topic'):
        q = t.find('query').text
        Queries[int(t['number'])] = q
    QT.close()
    processQuery()


# In[6]:


def getTermIDs():
    termID = open("F:\\PycharmProjects\\SearchEngine\\files\\termids.txt", mode="r", encoding="utf-8", errors='ignore')
    for line in termID:
        sen = line.split()
        termIDs[int(sen[0])] = sen[1]
    termID.close()


# In[7]:


def getDocIDs():
    docID = open("F:\\PycharmProjects\\SearchEngine\\files\\docids.txt", mode="r", encoding="utf-8", errors='ignore')

    for line in docID:
        sen = line.split()
        docIDs[int(sen[0])] = sen[1]
    docID.close()


# In[8]:


# total terms in a doc
def getDocInfo():
    doc_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\doc_index.txt", mode="r", encoding="utf-8",
                   errors='ignore')

    tCorpusTerms = 0
    did = 1
    for line in doc_ind:
        sen = line.split()
        tCorpusTerms = tCorpusTerms + len(sen) - 2
        if int(sen[0]) == did:
            #         if did == 1:
            #             print(sen[0])
            if did in tDocTerms:
                tDocTerms[did] = tDocTerms[did] + len(sen) - 2
            else:
                tDocTerms[did] = len(sen) - 2
        else:
            did = did + 1
            tDocTerms[did] = len(sen) - 2
    doc_ind.close()
    return tCorpusTerms


# In[9]:


def avgQueryLength():
    avg_qlen = 0
    for val in Queries:
        lst = Queries[val]
        avg_qlen = avg_qlen + len(lst)
    avg_qlen = avg_qlen / len(Queries)
    return avg_qlen


# In[10]:


# In[11]:


def terminfo(id):
    term_info = open("F:\\PycharmProjects\\SearchEngine\\files\\term_info.txt", 'r', encoding='utf8', errors='ignore')
    for line in term_info:
        sentence = line.split()
        if int(sentence[0]) == id:
            break
    term_info.close()
    return sentence


# In[12]:


# term Document info
def getTermInfo(offset, ind):
    term_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\term_index.txt", mode="r", encoding="utf-8",
                    errors='ignore')
    term_ind.seek(offset - 1)
    sentence = term_ind.readline()
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
    term_ind.close()
    return positions


# In[13]:


def OkapiTF():
    oktfFile = open("F:\\PycharmProjects\\SearchEngine\\files\\okapiTFRanked.txt", mode="w", encoding="utf-8",
                    errors='ignore')
    for key, val in Queries.items():
        # rank = 0
        temp_dict = {}
        for i in range(1, len(docIDs) + 1):
            # extract key
            # rank = rank + 1
            cross_prod = []
            doc_len = []
            query_len = []
            for j in range(0, len(val)):  # for all words in a query
                for k, v in termIDs.items():
                    if v == val[j]:
                        temp = terminfo(k)  # for offset
                        t_offset = temp[1]
                        td_info = getTermInfo(int(t_offset), int(i))
                        length = len(td_info)
                        tf = td_info[length - 1]
                        oktf_doc = tf / (tf + 0.5 + (1.5 * tDocTerms[i] / avgDocLen))
                        t = oktf_doc * oktf_doc
                        doc_len.append(t)

                        tf_q = val.count(v)
                        oktf_q = tf_q / (tf_q + 0.5 + (1.5 * len(val) / avg_qlen))
                        t = oktf_q * oktf_q
                        query_len.append(t)

                        oktf = oktf_doc * oktf_q
                        cross_prod.append(oktf)
            numerator = sum(cross_prod)
            d_len = math.sqrt(sum(doc_len))
            q_len = math.sqrt(sum(query_len))
            if d_len > 0 and numerator > 0:
                score = numerator / (d_len * q_len)
            else:
                score = 0
            temp_dict[docIDs[i]] = score
        # converted to list when sorted
        temp_dict = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)

        for i in range(len(temp_dict)):
            oktfFile.write(str(key))
            oktfFile.write("\t")
            oktfFile.write("0")
            oktfFile.write("\t")
            oktfFile.write(temp_dict[i][0])
            oktfFile.write("\t")
            oktfFile.write(str(i + 1))
            oktfFile.write("\t")
            oktfFile.write(str(temp_dict[i][1]))
            oktfFile.write("\t")
            oktfFile.write("run1")
            oktfFile.write("\n")
    oktfFile.close()


# In[14]:


# In[13]:


def TF_IDF():
    TFIDF_file = open("F:\\PycharmProjects\\SearchEngine\\files\\TF_IDFranked.txt", mode="w", encoding="utf-8",
                      errors='ignore')
    for key, val in Queries.items():
        # rank = 0
        temp_dict = {}
        for i in range(1, len(docIDs) + 1):
            # extract key
            # rank = rank + 1
            cross_prod = []
            doc_len = []
            query_len = []
            for j in range(0, len(val)):  # for all words in a query
                for k, v in termIDs.items():
                    if v == val[j]:
                        temp = terminfo(k)  # for offset
                        t_offset = temp[1]
                        td_info = getTermInfo(int(t_offset), int(i))
                        length = len(td_info)
                        tf = td_info[length - 1]
                        oktf_doc = tf / (tf + 0.5 + (1.5 * tDocTerms[i] / avgDocLen))
                        t = oktf_doc * oktf_doc
                        doc_len.append(t)

                        tf_q = val.count(v)
                        oktf_q = tf_q / (tf_q + 0.5 + (1.5 * len(val) / avg_qlen))
                        t = oktf_q * oktf_q
                        query_len.append(t)

                        t_info = terminfo(k)
                        oktf = oktf_doc * oktf_q * math.log10((len(docIDs) / int(temp[3])))  # t_info[2]
                        cross_prod.append(oktf)
            numerator = sum(cross_prod)
            d_len = math.sqrt(sum(doc_len))
            q_len = math.sqrt(sum(query_len))
            if d_len > 0 and numerator > 0:
                score = numerator / (d_len * q_len)
            else:
                score = 0
            temp_dict[docIDs[i]] = score
        # converted to list when sorted
        temp_dict = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)

        for i in range(len(temp_dict)):
            TFIDF_file.write(str(key))
            TFIDF_file.write("\t")
            TFIDF_file.write("0")
            TFIDF_file.write("\t")
            TFIDF_file.write(temp_dict[i][0])
            TFIDF_file.write("\t")
            TFIDF_file.write(str(i + 1))
            TFIDF_file.write("\t")
            TFIDF_file.write(str(temp_dict[i][1]))
            TFIDF_file.write("\t")
            TFIDF_file.write("run1")
            TFIDF_file.write("\n")
    TFIDF_file.close()


# In[14]:


# In[17]:


def BM25():
    BM25_file = open("F:\\PycharmProjects\\SearchEngine\\files\\BM25_ranked.txt", mode="w", encoding="utf-8",
                     errors='ignore')

    k1 = 1.2
    k2 = 120
    b = 0.75

    for key, val in Queries.items():
        temp_dict = {}
        for i in range(1, len(docIDs) + 1):  # for testing i have taken only the first 10 docs
            score = 0
            K_ = k1 * ((1 - b) + (b * tDocTerms[i] / avgDocLen))
            for j in range(0, len(val)):  # for all words in a query
                for k, v in termIDs.items():
                    if v == val[j]:
                        temp = terminfo(k)  # for offset
                        t_offset = temp[1]
                        td_info = getTermInfo(int(t_offset), int(i))
                        length = len(td_info)
                        tf = td_info[length - 1]
                        tf_q = val.count(v)

                        first = (len(docIDs) + 0.5) / (int(temp[3]) + 0.5)
                        second = ((1 + k1) * tf) / (K_ + tf)
                        third = ((1 + k1) * tf_q) / (k2 + tf_q)
                        score = score + (math.log10(first) * second * third)

            temp_dict[docIDs[i]] = score

        # converted to list when sorted
        temp_dict = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)

        for i in range(len(temp_dict)):
            BM25_file.write(str(key))
            BM25_file.write("\t")
            BM25_file.write("0")
            BM25_file.write("\t")
            BM25_file.write(temp_dict[i][0])
            BM25_file.write("\t")
            BM25_file.write(str(i + 1))
            BM25_file.write("\t")
            BM25_file.write(str(temp_dict[i][1]))
            BM25_file.write("\t")
            BM25_file.write("run1")
            BM25_file.write("\n")
    BM25_file.close()


# In[18]:


# In[19]:


def Jelinek_Mercer():
    JM_file = open("F:\\PycharmProjects\\SearchEngine\\files\\JM_ranked.txt", mode="w", encoding="utf-8",
                   errors='ignore')
    lambdaa = 0.6
    for key, val in Queries.items():
        temp_dict = {}
        for i in range(1, len(docIDs) + 1):
            score = 1
            for j in range(0, len(val)):  # for all words in a query
                for k, v in termIDs.items():
                    if v == val[j]:
                        temp = terminfo(k)  # for offset
                        t_offset = temp[1]
                        td_info = getTermInfo(int(t_offset), int(i))
                        length = len(td_info)
                        tf = td_info[length - 1]

                        first = lambdaa * tf / tDocTerms[i]
                        second = (1 - lambdaa) * int(temp[2]) / tCorpusTerms
                        score = score * (first + second)

            temp_dict[docIDs[i]] = score
        # converted to list when sorted
        temp_dict = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)

        for i in range(len(temp_dict)):
            JM_file.write(str(key))
            JM_file.write("\t")
            JM_file.write("0")
            JM_file.write("\t")
            JM_file.write(temp_dict[i][0])
            JM_file.write("\t")
            JM_file.write(str(i + 1))
            JM_file.write("\t")
            JM_file.write(str(temp_dict[i][1]))
            JM_file.write("\t")
            JM_file.write("run1")
            JM_file.write("\n")
    JM_file.close()


# In[20]:


print("Running")
parseQueryTopics()
getTermIDs()
getDocIDs()
tCorpusTerms = getDocInfo()
avgDocLen = tCorpusTerms / len(docIDs)
avg_qlen = avgQueryLength()

command = input("Enter command.\n")
loop = True
while loop:
    if command == 'exit':
        loop = False

    elif command == '--score TF':
        OkapiTF()

    elif command == '--score TF-IDF':
        TF_IDF()

    elif command == '--score BM25':
        BM25()

    elif command == '--score JM':
        Jelinek_Mercer()

    command = input("Enter command.\n")
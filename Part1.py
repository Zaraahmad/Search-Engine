from bs4 import BeautifulSoup #for finding relevant word
import os
from nltk import PorterStemmer

def clean_up_list(word_list):
    clean_word_list = []
    for word in word_list:
        symbols = r"!@#$%^&*”“…’‘|~`()_-\"+=/\}{[,].<';:>?" #use \ before character that are like eof
        for i in range (0, len(symbols)):
            word = word.replace(symbols[i],"")
        if len(word)>0:
            #print(word)
            clean_word_list.append(word)
    return clean_word_list

def tokenizer(directory):
    filenames = [f for f in os.listdir(directory)]
    docID = open("F:\\PycharmProjects\\SearchEngine\\files\\docids.txt", mode="w",encoding="utf-8", errors='ignore')
    termID = open("F:\\PycharmProjects\\SearchEngine\\files\\termids.txt", mode="w", encoding="utf-8", errors='ignore')
    doc_ind = open("F:\\PycharmProjects\\SearchEngine\\files\\doc_index.txt", mode="w", encoding="utf-8", errors='ignore')

    Stop_word_file = open("F:\\PycharmProjects\\SearchEngine\\files\\stoplist.txt", 'r', encoding='utf8', errors='ignore')
    stopwords = Stop_word_file.readlines()
    stopwords = [x.strip() for x in stopwords] #removes all leading and trailing spaces from string

    #Storing document ids
    fileids = {}
    f_id = 1
    t_id = 1
    print("Assigning Doc IDs.\n")
    for file in filenames:
        fileids[file] = f_id
        docID.write(str(f_id))
        docID.write("\t")
        docID.write(file)
        docID.write("\n")
        f_id += 1
    docID.close()
    print("Doc IDs assigned.\n")

    term_id = {}
    print("Writing to files...\n")
    for i in range(0, len(filenames)):
        try:
            #enc = 'iso-8859-15'
            open_file = open(directory + r'\\' + filenames[i], 'r', encoding='utf8', errors='ignore')
            word_list = []
            source_code = open_file.read()
            #print(type(source_code))
            soup = BeautifulSoup(source_code, 'html.parser')#lxml

            for post_text in soup.findAll(['p', 'a', 'title', 'class', 'id', 'div']):
                content = post_text.string #gets only the string and discards html stuff tags
                #print(type(content))
                if content is None:
                    continue
                words = content.lower().split()
                for each_word in words:
                    #print(each_word)
                    word_list.append(each_word)
            clean_word_list = clean_up_list(word_list)

            # kill all script and style elements
#             for script in soup(["script", "style"]):
#                 script.extract() #rip it out
#             text = soup.get_text() # get text
#             # break into lines and remove leading and trailing space on each
#             lines = (line.strip() for line in text.splitlines())
#             # break multi-headlines into a line each
#             chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#             # drop blank lines
#             text = '\n'.join(chunk for chunk in chunks if chunk)
#             words = text.lower().split()
#             for each_word in words:
#                 # print(each_word)
#                 word_list.append(each_word)
#             clean_word_list = clean_up_list(word_list)
# #TRYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
#             [x for x in clean_word_list if x]
            #term ids

            #stem the words in list and store them as keys against tid value
            #make term id file
            for word in clean_word_list:
                word = PorterStemmer().stem(word)
                if word in stopwords:
                    pass
                elif word in term_id:
                    pass
                # elif word == "":
                #     print("yooo")
                #     clean_word_list.remove(word)
                else:
                    term_id[word] = t_id
                    termID.write(str(t_id))
                    termID.write("\t")
                    termID.write(word)
                    termID.write("\n")
                    t_id += 1

            #forward index
            term_position = []
            position = 0
            local_dict = {}
            l_id = 0
            for word in clean_word_list:
                word = PorterStemmer().stem(word)
                position += 1
                if word in stopwords:
                    pass
                elif word in local_dict:
                    idd = local_dict[word]
                    term_position[idd].append(position)
                else:
                    local_dict[word] = l_id
                    term_position.append([])
                    term_position[l_id].append(position)
                    l_id += 1

            x = 0

            while(x < l_id):
                if len(term_position[x]) > 0:
                    #print(term_position[x])
                    doc_ind.write(str(i + 1))
                    doc_ind.write("\t")
                    for key, value in local_dict.items():
                        if value == x:
                            term = key
                    #term = local_dict.keys()[local_dict.values().index(x)]
                    doc_ind.write(str(term_id[term]))
                    doc_ind.write("\t")
                    y = 0
                    #print(len(term_position[x]))
                    while (y < len(term_position[x])):
                        doc_ind.write(str(term_position[x][y]))
                        doc_ind.write("\t")
                        y += 1
                    doc_ind.write("\n")
                    x += 1
            open_file.close()
        except IOError:
            print("File not found or path is incorrect")
    print("Writing done.\n")
    termID.close()
    doc_ind.close()

dir = r"F:\PycharmProjects\SearchEngine\files\corpus"
tokenizer(dir)
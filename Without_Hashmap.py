from collections import defaultdict
import nltk
# nltk.download('punkt')
from bs4 import BeautifulSoup
import os
import string
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

# C:\Users\Eesha Javaid\Desktop\Semester 7\Information Retrieval\Assignments\corpus\check
directory_name = input("Enter the complete directory path separated by / ")
directory_name = directory_name
temp = ''
doc_index = 1
term_index = 1
list_inverted_index = list()
dic_term_name = dict()
dic_termid = dict()
set3 = set()
with os.scandir(directory_name) as entries:
    for entry in entries:
        with open(directory_name + '/' + entry.name, 'r', encoding='utf-8', errors='ignore') as contents:
            soup = BeautifulSoup(contents, "html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        # text = soup.get_text()
        if (soup.head):
            head = soup.head.get_text()
        if (soup.body):
            body = soup.body.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in body.splitlines())
        lines2 = (line.strip() for line in head.splitlines())

        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        chunks2 = (phrase.strip() for line in lines2 for phrase in line.split("  "))

        # drop blank lines
        head = '\n'.join(chunk for chunk in chunks2 if chunk)
        body = '\n'.join(chunk for chunk in chunks if chunk)

        text: str = head + " " + body

        # split into words
        tokens = word_tokenize(text)
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation from each word
        punct = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(punct) for w in tokens]
        # remove remaining tokens that are not alphabetic
        words = [word for word in stripped if word.isalpha()]
        digits = str.maketrans('', '', string.digits)
        stripped1 = [w.translate(digits) for w in words]
        colon = str.maketrans('', '', ":")
        stripped2 = [w.translate(colon) for w in stripped1]
        # stripped2 now contains the words in order
        stop = set()
        f = open('stoplist.txt', 'r')
        for data in f:
            stop.add(data[:-1])

        # stop now contains all the stop words
        # stemming
        porter = PorterStemmer()
        # stemmed = [porter.stem(word) for word in words]
        # print(stripped2)
        word_position = 1  # word position in the document
        previous_term_index = 1
        for word in stripped2:  # original document
            if (word not in stop):  # checking stop words
                stemmed = porter.stem(word)  # stem
                if (stemmed not in dic_term_name):  # checking if already exists
                    dic_term_name[stemmed] = term_index  # adding the word as a key and its id as value
                    term_index += 1  # updating for new word

                get_termid = dic_term_name.get(
                    stemmed)  # getting id of the term that either already exists in the dict or is new
                tuple1 = (get_termid, doc_index, word_position)
                list_inverted_index.append(tuple1)
            word_position += 1  # updates word position whatever the word is(stop word or not)
        doc_index += 1
        soup.reset()

# list_inverted_index contains all words in every document along with their positions

list_inverted_index.sort(key=lambda i: i[2])  # sort by positions
list_inverted_index.sort(key=lambda i: i[1])  # sort by doc_ids
list_inverted_index.sort(key=lambda i: i[0])  # sort by term_ids

prev_doc = 0
prev_term = 0
total_occurences = list()
total_documents = list()

for tuple in list_inverted_index:
    if (tuple.__getitem__(0) != prev_term):  # new term
        if prev_term != 0:
            total_occurences.append(count_position)
            total_documents.append(count_document)
        count_position = 1
        count_document = 1
        prev_term = tuple.__getitem__(0)
        prev_doc = tuple.__getitem__(1)

    else:

        if (tuple.__getitem__(1) != prev_doc):  # new document
            prev_doc = tuple.__getitem__(1)
            count_document += 1
        count_position += 1

total_occurences.append(count_position)
total_documents.append(count_document)
f2 = open("term_info.txt", 'a')
f1 = open("term_index.txt", 'a')
offset = 0
prev_term = 0
prev_doc = 0
print(f1.tell)
for tuple in list_inverted_index:
    if (tuple.__getitem__(0) != prev_term):  # new term

        if(prev_term != 0):
            f1.write("\n")
        f2.write(str(tuple.__getitem__(0)) + " " + str(f1.tell())+ "\n")
        prev_term = tuple.__getitem__(0)
        first_doc = tuple.__getitem__(1)
        first_position = tuple.__getitem__(2)
        prev_doc = tuple.__getitem__(1)

        f1.write( str(prev_term) + " " + str(total_occurences.__getitem__((prev_term - 1))) + " ")
        f1.write(str(total_documents.__getitem__((prev_term - 1))) + " ")
        f1.write(str(first_doc) + "," + str(first_position) + " ")

    else:  # same term
        if (prev_doc != tuple.__getitem__(1)):  # new document
            f1.write(str(tuple.__getitem__(1) - prev_doc) + "," + str(tuple.__getitem__(2)) + " ")
            prev_doc = tuple.__getitem__(1)
            first_position = tuple.__getitem__(2)
        else:  # same document
            f1.write(str(0) + ',' + str((tuple.__getitem__(2) - first_position)) + " ")
            first_position = tuple.__getitem__(2)

f.close()
f1.close()
f2.close()
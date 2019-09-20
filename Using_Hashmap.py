
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

doc_index = 1
term_index = 1
dic_term_name = dict()
dic_termid = dict()
set3 = set()
with os.scandir(directory_name) as entries:
    for entry in entries:
        with open(directory_name + '/' + entry.name, 'r', encoding='utf-8', errors='ignore') as contents:
            soup = BeautifulSoup(contents, "html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # get text
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
        # remove colon
        stripped1 = [w.translate(digits) for w in words]
        colon = str.maketrans('', '', ":")
        stripped2 = [w.translate(colon) for w in stripped1]
        # stripped2 now contains the words in order
        # storing stop words
        stop = set()
        f = open('stoplist.txt', 'r')
        for data in f:
            stop.add(data[:-1])

        # stop now contains all the stop words
        # stemming
        porter = PorterStemmer()

        word_position = 1  # word position in the document
        previous_term_index = 1
        for word in stripped2:  # original document
            if (word not in stop):  # checking stop words
                stemmed = porter.stem(word)  # stem
                if (stemmed not in dic_term_name):  # checking if already exists
                    dic_term_name[stemmed] = term_index  # adding the word as a key and its id as value
                    dic_termid[term_index] = defaultdict(
                        list)  # creating a default dictionary for a word that will contain the list of positions for that specific document
                    term_index += 1  # updating for new word
                get_termid = dic_term_name.get(
                    stemmed)  # getting id of the term that either already exists in the dict or is new
                dic_termid[get_termid][doc_index].append(
                    word_position)  # adding the position of that word in the document
            word_position += 1  # updates word position whatever the word is(stop word or not)
        doc_index += 1

        soup.reset()
    # till now dictionary of inverted index is made

f = open("term_index.txt", 'a')
prev_doc = 0
f1 = open("term_info.txt", 'a')
offset = 0  # for term offsets
for term in dic_termid:
    f1.write(str(term) + " " + str(offset) + "\n")
    total_occurences = 0
    total_documents = 0
    for document in dic_termid[term]:
        total_documents += 1

        for position in dic_termid[term][document]:
            total_occurences += 1
    f.write(str(term) + " " + str(total_occurences) + " " + str(total_documents) + " ")
    for document in dic_termid[term]:
        if (prev_doc == 0):  # first document
            prev_doc = document
            current_doc = document
        else:
            current_doc = document - prev_doc
            prev_doc = document
        index = 0
        for position in dic_termid[term][document]:
            if (position == dic_termid[term][document].__getitem__(0)):
                f.write(str(current_doc) + "," + str(position) + " ")
            else:
                f.write(str(0) + "," + str((position - dic_termid[term][document].__getitem__(index - 1))) + " ")
            index += 1

    f.write("\n")
    offset = f.tell()

    current_doc = prev_doc = 0
f.close()
f1.close()

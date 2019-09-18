import nltk
# nltk.download('punkt')
from bs4 import BeautifulSoup
import html
from nltk.corpus import stopwords
import os
import string
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

# C:\Users\Eesha Javaid\Desktop\Semester 7\Information Retrieval\Assignments\corpus\check
directory_name = input("Enter the complete directory path separated by / ")
directory_name = directory_name
word_count = 0
temp = ''
doc_index = 1
term_index = 1
dic_term = dict()
set3 = set()
with os.scandir(directory_name) as entries:
    for entry in entries:
        print(entry.name)
        with open(directory_name + '/' + entry.name, 'r', encoding='utf-8', errors='ignore') as contents:
            soup = BeautifulSoup(contents, "html.parser")

        # kills all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
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

        # concatenation
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
        # remove colons
        colons = str.maketrans('', '', ":")
        stripped2 = [w.translate(colons) for w in stripped1]

        # store stop words
        stop = set()
        f = open('stoplist.txt', 'r')
        for data in f:
            stop.add(data[:-1])

        words = [w for w in stripped2 if not w in stop]

        # stemming
        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in words]
        # document file writing
        f1 = open("docids.txt", 'a')
        str1 = str(doc_index) + "\t" + entry.name + '\n'
        f1.write(str1)
        doc_index += 1
        # term file writing
        f2 = open("termids.txt", 'a', encoding='utf-8', errors='ignore')
        for word in stemmed:
            if (word not in set3):  # finding unique words
                set3.add(word)
                word_count += 1
                f2.write(str(word_count) + "\t" + word + "\n")
        soup.reset()

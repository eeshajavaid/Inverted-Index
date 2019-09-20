import string
from nltk.stem.porter import PorterStemmer

term = input("Enter the term you wish to find in the corpus")
print(term)
porter = PorterStemmer()
stem = porter.stem(term)
term_id=0
linelist = [line.rstrip('\n') for line in open("termids.txt")]
for line in linelist:
    if line.find(stem) != -1:  # word exists in that line
        term_id = line.split(None, 1)[0]  #  get the first word of that line (term id)
        break
flag=0

lineoffset = [line.rstrip('\n') for line in open("term_info.txt")]
for line in lineoffset:
    term1 = line.split(None, 1)[0]
    if term1 == term_id:
        offset = line.split(None,1)[1]
        flag=1
        break
if(flag==0):
    print("Term not found in Corpus")
else:
    f = open("term_index.txt", 'r')
    f.seek(int(offset))
    list = f.readline()
    line= list.split(" ")
    print(line)
    print("Listing for term: " +term)
    print("TERMID: " +line.__getitem__(0) )
    print("Number of documents containing term: " +line.__getitem__(2))
    print("Term frequency in corpus: "+line.__getitem__(1))
    f.close()








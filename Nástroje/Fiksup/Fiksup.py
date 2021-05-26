from tabulate import tabulate
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')
file = open('C:/[CESTA ZDE]/Extrahovane komentare - The Sun.txt', encoding="utf8")
with file as fp:
   line = fp.readline()
   cnt = 1
   while line:
       #print(line.strip())
       line = fp.readline()
       fixed = tool.correct(line.strip())
       print(fixed)
       cnt += 1
file = open('C:/[CESTA ZDE]/Extrahovane komentare - The Sun - Opravena Gramatika.txt', encoding="utf8")
positiveVocabulary = open('C:/[CESTA ZDE]/bing-positive-words.txt')
negativeVocabulary = open('C:/[CESTA ZDE]/bing-negative-words.txt')
class Sentence:
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.words = []
        self.numOfPositivWords = 0
        self.numOfNegativWords = 0
        self.opinion = 'NA'
    def setopinion(self):
        s = 0
        if self.numOfPositivWords or self.numOfNegativWords != 0:
            s = self.numOfPositivWords / (self.numOfPositivWords + self.numOfNegativWords)
            if s > 0.5:
                self.opinion = 1
            else:
                self.opinion = 0
def preprocessdata(file, positiveVocabulary, negativeVocabulary):
    positiveTerms = []
    for line in positiveVocabulary:
        positiveTerms.append(line.strip())
    negativeTerms = []
    for line in negativeVocabulary:
        negativeTerms.append(line.strip())
    sentences = []
    i = 1
    for line in file:
        sen = Sentence(i, line.strip())
        sentences.append(sen)
        i = i + 1
    for sentence in sentences:
        sentence.words = sentence.text.lower().replace('.', '').replace(',', '').split()
    return sentences, positiveTerms, negativeTerms
def executeclassification():
    for sentence in sentences:
        for word in sentence.words:
            if word in positiveTerms:
                sentence.numOfPositivWords = sentence.numOfPositivWords + 1
                continue
            if word in negativeTerms:
                sentence.numOfNegativWords = sentence.numOfNegativWords + 1
                continue
        sentence.setopinion()

def printresults():
    table = []
    for sentence in sentences:
        result = [sentence.id, sentence.numOfPositivWords, sentence.numOfNegativWords, sentence.opinion]
        table.append(result)
    print(tabulate(table, headers=["ID", "Number of positive words", "Number of negative words", "Opinion"]))
sentences, positiveTerms, negativeTerms = preprocessdata(file, positiveVocabulary, negativeVocabulary)
executeclassification()
printresults()
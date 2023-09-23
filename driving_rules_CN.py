from jieba import posseg
from jieba.analyse import extract_tags
import PyPDF2
import re
import argparse
from googletrans import Translator

LOCAL_PATH = 'manuals/'
ALL_SENTENCES = []
ALL_POSSIBLE_RULES = []
ALL_POSSIBLE_RULES_KEYWORDS = []

def read_manual_chinese(file_name='CA_driving_handbook_chinese.pdf', rule_file=str()):
    pdfFile = open(LOCAL_PATH + file_name, 'rb')
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfReader(pdfFile)

    for i in range(38, 120): # TODO: identify start and end page for different pdfs
        # add all text in the pdf into ALL_SENTENCES
        page = pdfReader.pages[i]
        text = page.extract_text().replace("\n","")
        # cut sentences
        newText = cut_sent_CN(text)
        for line in newText:
            ALL_SENTENCES.append(line)
        
        # from ALL_SENTENCES, find all Possible rules
    extract_if_then()
    extract_keyword()


# this function helps to cut Chinese text into sentences by using Chinese punctuations
def cut_sent_CN(sent):
    sent = re.sub('([。！？\?，])([^”’])', r"\1\n\2", sent)  # check punctuations for single character
    # Check ellipsis
    # sent = re.sub('(\.{6})([^”’])', r"\1\n\2", sent)  
    # sent = re.sub('(\…{2})([^”’])', r"\1\n\2", sent)  
    sent = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', sent)
    sent = sent.rstrip()
    return sent.split("\n")

# update ALL_POSSIBLE_RULES
def extract_if_then(): #TODO: check if there a causation between two sentences
    count = 1
    for i in range(len(ALL_SENTENCES) - 1):
        # find all sentences with "if"
        if "如果" in ALL_SENTENCES[i]: 
            # drop the word "if"
            newIF = re.split("如果",ALL_SENTENCES[i])
            # the next sentence will be THEN sentence, drop all useless characters
            newTHEN = re.split("則|請|您|您的", ALL_SENTENCES[i+1])
            newTHEN = newTHEN[1] if len(newTHEN) > 1 else newTHEN[0]
            # drop commas and periods, then append [#, if sentence, then sentence] into ALL_POSSIBLE_RULES
            if newIF != "" and newTHEN != "":
                ALL_POSSIBLE_RULES.append([count, newIF[1][:-1], newTHEN[:-1]])
                count += 1

# update ALL_POSSIBLE_RULES_KEYWORDS
def extract_keyword():
    for count, IF, THEN in ALL_POSSIBLE_RULES:
        # find key word in chinese sentences by using jieba.analyse.extract_tags
        IF_Keyword = ', '.join(extract_tags(IF, topK = 20))
        THEN_Keyword = ', '.join(extract_tags(THEN, topK = 20))
        if IF_Keyword != "" and THEN_Keyword != "":
            ALL_POSSIBLE_RULES_KEYWORDS.append([count, IF_Keyword, THEN_Keyword])
        
# print IF-THEN keywords
def defaultOutput():
    for count, IF, THEN in ALL_POSSIBLE_RULES_KEYWORDS:
        printRule(count, IF, THEN)

# print full IF-THEN sentences
def fullOutput():
    for count, IF, THEN in ALL_POSSIBLE_RULES:
        printRule(count, IF, THEN)

def POSOutput():
    for count, IF, THEN in ALL_POSSIBLE_RULES_KEYWORDS:
        # analyze every word's Part-Of-Speech tag for all IF-THEN sentences
        IF_POS = ", ".join(['%s/%s' % (word, flag) for word, flag in posseg.cut(IF)])
        THEN_POS = ", ".join(['%s/%s' % (word, flag) for word, flag in posseg.cut(THEN)])
        printRule(count, IF_POS, THEN_POS)

def englishOutput():
    # using google translator
    translator = Translator()
    for count, IF, THEN in ALL_POSSIBLE_RULES_KEYWORDS:
        try:
            translated_IF = translator.translate(IF, src='zh-tw', dest='en').text
            translated_THEN = translator.translate(THEN, src='zh-tw', dest='en').text
        except Exception as e:
            print(f"Error translating text: {e}")
            continue  # skip to the next iteration or handle the error as appropriate

        printRule(count, translated_IF, translated_THEN)

def fullEnglishOutput():
    # using google translator
    translator = Translator()
    for count, IF, THEN in ALL_POSSIBLE_RULES:
        try:
            translated_IF = translator.translate(IF, src='zh-tw', dest='en').text
            translated_THEN = translator.translate(THEN, src='zh-tw', dest='en').text
        except Exception as e:
            print(f"Error translating text: {e}")
            continue  # skip to the next iteration or handle the error as appropriate

        printRule(count, translated_IF, translated_THEN)

def printRule(count, sent1, sent2):
    print("#" + str(count) + ": IF: (" + sent1 + ") THEN:(" + sent2 + ")")

if __name__ == "__main__": #TODO: read file name in case there's multiple pdfs
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', '--full', action='store_true', help='Read full IF-THEN sentences instead of keyword')
    parser.add_argument('-E','--eng', action='store_true', help='Read keywords in English')
    parser.add_argument('-P','--pos', action='store_true', help='Read Keywords\' Part-Of-Speech tags')
    parser.add_argument('-FE', '--fulleng', action='store_true', help='Read full IF-THEN sentences in English')
    args = parser.parse_args()
    
    read_manual_chinese()
    
    if args.eng:
        englishOutput()
    elif args.pos:
        POSOutput()
    elif args.full:
        fullOutput()
    elif args.fulleng:
        fullEnglishOutput()
    else:
        defaultOutput()
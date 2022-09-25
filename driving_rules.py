# importing required modules
import argparse
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from io import StringIO
from driving_rules1.high_level import extract_text
from driving_rules1.converter import TextConverter
from driving_rules1.layout import LAParams
from driving_rules1.pdfdocument import PDFDocument
from driving_rules1.pdfinterp import PDFResourceManager, PDFPageInterpreter
from driving_rules1.pdfpage import PDFPage
from driving_rules1.pdfparser import PDFParser
from typing import Tuple, List
import PyPDF2
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
# from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain, pretty_goal_tree
import re
import logging

LOCAL_TEXT_PATH = 'manual_text/'
LOCAL_PATH = 'manuals/'
IF_ = 'if'
THEN = 'then'
NEVER = 'never'
BC = 'BECAUSE'

AND = ' and '
THAT = ' that '
ANDS = [AND, THAT]

OR = ' or '
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP']
SUBJECTS = ['NN', 'NNP', 'NNS']

TO_BE = ['is', 'am', 'are', 'was', 'were', 'be', 'being', 'been']
TO_HAVE = ['have', 'has', 'had', 'having']
NOTS = ['not', 'never']

RE_SPLITTERS = '[:,.]'
CONJS = [AND, OR]
MAX_WORDS = 25  # Sometimes sentences don't get split well...

KEY_PHRASES = ['blind spot', 'traffic light', 'traffic signal', 'safety belt', 'blind spot']


# def read_manual(state: str = 'MA', file_name='MA_Drivers_Manual.pdf'):
#     """
#     File located at
#     MA: https://driving-tests.org/wp-content/uploads/2020/03/MA_Drivers_Manual.pdf
#     CA: https://www.dmv.ca.gov/portal/file/california-driver-handbook-pdf/
#     """
#
#     if state == 'CA':
#         file_name = 'CA_driving_handbook.pdf'
#     txt_file_name = file_name.replace(".pdf", ".txt")
#
#     pdfFile = open(LOCAL_PATH + file_name, 'rb')
#     # creating a pdf reader object
#     # pdfReader = PyPDF2.PdfFileReader(pdfFile)
#     pdfReader = extract_text('manuals/MA_Drivers_Manual.pdf')
#     print(repr(pdfReader))
#     print(pdfReader)
#
#
#     # printing number of pages in pdf file
#     MAX_PAGES = pdfReader.numPages
#     # MAX_PAGES = 87
#     START_PAGE = 84  # This starts from the rules of the road for MA.
#     END_PAGE = MAX_PAGES - 1  # START_PAGE+40 # MAX_PAGES
#     all_rules = []
#
#     """
#     For Mass 82-124
#     """
#     txt_file_object = open(LOCAL_TEXT_PATH + txt_file_name, "w")
#
#     for page in range(START_PAGE, END_PAGE):
#         # pageObj = pdfReader.getPage(page)
#         pageObj = pdfReader.getPage(page)
#         pageText = pageObj.extractText()
#         txt_file_object.write(pageText)
#         # if page == START_PAGE:
#         #     print(pageText)
#         all_rules.extend(extract_if_then(pageText))
#     txt_file_object.close()
#     # closing the pdf file object
#     print("Found %d potential rules" % len(all_rules))
#     pdfFile.close()
#     return all_rules


def read_manual(state: str = 'MA', file_name='MA_Drivers_Manual.pdf'):
    output_string = StringIO()
    with open('manuals/MA_Drivers_Manual.pdf', 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # MAX_PAGES = pdfReader.numPages
        MAX_PAGES = 87
        START_PAGE = 84  # This starts from the rules of the road for MA.
        END_PAGE = MAX_PAGES - 1  # START_PAGE+40 # MAX_PAGES
        all_rules = []

        print("hi", PDFPage.create_pages(doc))
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            # x = output_string.getvalue()
            # all_rules.extend(extract_if_then(x))

    print(output_string.getvalue())


def extract_if_then(page_text: str):
    """
    Check for rule keywords in text
    """
    rule_counter = 0
    rules = []
    counter = 0

    # sometimes in reading the pdf we will get non-ascii characters
    new_val = page_text.encode("ascii", "ignore")
    updated_text = new_val.decode()
    sentences = updated_text.split('.')
    for sentence in sentences:
        tokens = word_tokenize(sentence.lower())
        if IF_ in tokens and len(tokens) < MAX_WORDS:
            words = [word for word in tokens if word.isalpha()]
            # TODO: check sentence
            rule = extract_rule(sentence)
            if not 'None' in str(rule):  # and containsNumber(sentence):
                logging.debug("Root it %s" % sentence.strip())
                logging.debug("  Rule is:  %s" % rule)
                counter += 1
                rules.append(rule)
    return rules


def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False


def extract_rule(sentence) -> str:
    """
    Tries to extract an IF/THEN rule from a sentence.  Returns it in the form: IF(if triples), THEN(then triples)
    """
    logging.debug("What is the sentence %s" % sentence)
    if_then = re.split(RE_SPLITTERS, sentence)
    # sometimes if is the last part:
    try:
        if_clause, then_clause = set_if_clause(if_then)

        if_triples = make_triples_from_phrase(if_clause)
        then_triples = make_triples_from_phrase(then_clause)
        return 'IF %s, THEN %s' % (if_triples, then_triples)
    except TypeError:
        print("error")


def set_if_clause(clauses) -> Tuple:
    """
    Sets the if clause and the then clause for a rule.
    - If there are two parts, then it will return the if then
    """
    logging.debug("I'm here with %s" % clauses)
    if len(clauses) == 2:
        if IF_ in clauses[0].lower():
            return tuple(clauses)
        else:
            return clauses[1], clauses[0]
    elif len(clauses) == 1:  # It didn't get separated
        logging.debug("Didn't split on regex, trying to split on if or then keyword")
        if IF_ in clauses[0]:
            all_tokens = clauses[0].split(IF_)
            then_clause = all_tokens[0]
            full_if = ""
            for part in all_tokens[1::]:
                full_if += part.strip() + ' '
            return full_if.strip(), then_clause.strip()
    else:  # put the commas back together
        full_then = ""
        for item in clauses[1::]:
            full_then += item
        return clauses[0], full_then


def make_triples_from_phrase(phrase: str, full_phrase: str = ""):
    """
    Struggled with this one. So I think we need to find all the occurences
    Keeping a full phrase in case....
    """
    logging.debug("  Making triples for %s" % phrase)
    if AND in phrase or OR in phrase or THAT in phrase:
        tokens = word_tokenize(phrase)
        for token in tokens:
            if token == AND.strip():
                parts = phrase.split(AND, 1)
                return "AND(%s, %s)" % (make_triples_from_phrase(parts[0]), make_triples_from_phrase(parts[1]))
            elif token == THAT.strip():
                parts = phrase.split(THAT, 1)
                return "AND(%s, %s)" % (make_triples_from_phrase(parts[0]), make_triples_from_phrase(parts[1]))
            elif token == OR.strip():
                parts = phrase.split(OR, 1)
                return "OR(%s, %s)" % (make_triples_from_phrase(parts[0]), make_triples_from_phrase(parts[1]))
    else:
        return make_one_triple(phrase)


def make_conjs(sentences):
    """
    Makes a conjunction from sentences.
    """
    conjs = ''

    for sentence in sentences:
        current_triple = make_one_triple(sentence)
        if current_triple is not None:
            conjs += str(current_triple)
            # Add a comma if it's not the last one.
            if sentences.index(sentence) != len(sentences) - 1:
                conjs += ', '
    return conjs


def make_one_triple(sentence: str) -> str:
    """
    Makes a single triple, that should be returned as a string.
    """
    neg = False
    relation = 'isA'
    obj = None

    if 'not' in sentence or 'never' in sentence:
        neg = True

    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    logging.debug("is it? %s" % sentence)
    # sentence_cleaned = sent_tokenize(sentence)[0]
    # print(tags)

    try:
        sentence_cleaned = sent_tokenize(sentence)[0]
        start = get_subject(tags)

        # TODO: This might be a phrase
        subject_phrase = get_noun_phrase_if_exists(start[0],
                                                   sentence_cleaned)  # make_noun_phrase(get_noun_phrase(tags))
        subject = subject_phrase if subject_phrase != "" else start[0]

        truncated_tags = tags[tags.index(start)::]
        # print(truncated_tags)

        if has_in(truncated_tags):
            relation = has_in(truncated_tags)[0]
            obj = get_object(truncated_tags[truncated_tags.index(has_in(truncated_tags))::])[0]
            object_phrase = get_noun_phrase_if_exists(obj, sentence_cleaned)
            return '(%s, %s, %s)' % (subject, relation, obj if object_phrase == "" else obj)
        # Otherwise can SVO or SPO (last NN->)
        elif has_verb(tags):  # Changed from truncated
            verb = has_verb(tags)[0][0]
            logging.debug("found verb %s" % verb)
            if verb_before_subject(tags):
                obj = subject
                subject = 'self'
            else:
                obj = get_object(truncated_tags[truncated_tags.index(has_verb(truncated_tags)[0])::])[0]
                object_phrase = get_noun_phrase_if_exists(obj, sentence_cleaned)
                obj = obj if object_phrase == "" else object_phrase
            if verb in TO_BE:
                logging.debug("Found an isA type verb")
                return '(%s, %s, %s)' % (subject, 'isA', obj)
            elif verb in TO_HAVE:
                logging.debug("Found an hasA type verb")
                return '(%s, %s, %s)' % (subject, 'hasA', obj)
            else:
                relation = verb
        if neg:
            return 'NOT(%s, %s, %s)' % (subject, relation, obj)
        else:
            return '(%s, %s, %s)' % (subject, relation, obj)
    except TypeError:
        logging.debug("Could not make a triple for text %s" % sentence)
    except IndexError:
        logging.debug("Sentence: %s is blank" % sentence)


def has_in(tags):
    for tag in tags:
        if 'IN' == tag[1]:
            return tag
    return None


def get_object(tags):
    for tag in tags:
        if tag[1] in SUBJECTS:
            return tag
    return tags[-1]


def get_subject(tags):
    """
    A subject could be a string.
    """
    for tag in tags:
        if tag[1] in SUBJECTS:
            return tag


def get_noun_phrase(tags):
    """
    Returns a noun phrase (if exists).  Returns none if the len is <= 1: a single token.
    """
    last_noun = False
    phrase = []
    for tag in tags:
        if tag[1] in SUBJECTS and last_noun:
            phrase.append(tag)
        elif tag[1] in SUBJECTS:
            last_noun = True
            phrase = [tag]
        else:
            last_noun = False
            if phrase and len(phrase) > 1:
                return phrase
    if len(phrase) > 1:
        return phrase
    else:
        return None


def get_noun_phrase_if_exists(start, sentence) -> str:
    for phrase in KEY_PHRASES:
        if start in phrase and phrase in sentence:
            return phrase
    else:
        return ""


def make_noun_phrase(list_of_tokens) -> str:
    """
    From a list of tokens it makes a string phrase
    """
    phrase_str = ""
    for token in list_of_tokens:
        phrase_str += token[0] + ' '
    return phrase_str.strip()


def verb_before_subject(tags) -> bool:
    if tags.index(has_verb(tags)[0]) < tags.index(get_subject(tags)):  # if verb before subject, then it is the object
        return True
    else:
        return False


def has_verb(tags) -> List:
    """
    Returns a list of the verbs
    """
    verbs = None
    for tag in tags:
        if tag[1] in VERBS:
            if verbs:
                verbs.append(tag)
            else:
                verbs = [tag]
    return verbs


def parse_manual(state: str = 'MA'):
    rules = read_manual(state)
    for rule in rules:
        print(rule)


if __name__ == "__main__":
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('--v', '--verbose', action='store_true')
    parser.add_argument('--state', nargs='?', default='MA',
                        help='Name of the state to parse.  Options are CA (California) and MA (Massachusetts) the default.')

    args = parser.parse_args()
    if args.v:  # Set verbose messages if you want them.
        logging.getLogger().setLevel(logging.DEBUG)

    state = 'CA' if args.state.startswith('C') or args.state.startswith('c') else 'MA'
    # TODO: Add an option for writing out to file.
    parse_manual(state)


def high_level():
    return None

import nltk
import spacy
from langdetect import detect
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from pymystem3 import Mystem
import en_core_web_sm


ERROR_PHRASES = {'Необоснованное обобщение': ['всем известно что', 'все знают что',
                                              'все считают так', 'все считают что', 'известно всем',
                                              'everybody knows', 'everyone knows'],
                 'Призыв к очевидности': ['очевидно', 'obviously', 'apparently'],
                 'Мнимое доказательство': [],
                 'Переход на личности': ['мне приятно'],
                 'Отсылка к авторитету': ['как говорил'],
                 'Какнасчетизм': ['как насчет', 'what about']
                 }

CONJ = {'and': ['и', 'но', 'это', 'and', 'but'], 'not': ['not', 'не']}


def tokenize(s):
    mystem = Mystem()
    lem_tags = mystem.analyze(s.lower())
    res = []
    for word in lem_tags:
        if len(word) > 1:
            try:
                res.append((word['analysis'][0]['lex'], word['analysis'][0]['gr'].split("=")[0].split(",")[0]))
            except:
                res.append((word['text'], 'UKNWN'))
        # else:
        #     res.append(word['text'])
    return res


def tokenize_eng(s):
    lemmatizer = WordNetLemmatizer()
    word_list = word_tokenize(s)
    lemm_list = [lemmatizer.lemmatize(word) for word in word_list]
    return nltk.pos_tag(lemm_list)


def tokenize_spacy(s):
    # download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(s)
    res = []
    for token in doc:
        lexeme = doc.vocab[token.text]
        if "n't" in lexeme.text:
            lexeme.text.replace("n't", "not")
        res.append((lexeme.text.replace("n't", "not"), token.pos_))
    return res


def and_not_filter(tokens):
    for i in range(1, len(tokens) - 1):
        if tokens[i][0] in CONJ['and']:
            if (i < len(tokens) - 2) and (tokens[i + 1][0] in CONJ['not']):
                if tokens[i + 2][0] == tokens[i - 1][0]:
                    return 'Противоречие'
            elif tokens[i + 1][0] == 'не' + tokens[i - 1][0]:
                return 'Противоречие'
            elif 'не' + tokens[i + 1][0] == tokens[i - 1][0]:
                return 'Противоречие'
            elif (tokens[i + 1][0] == tokens[i - 1][0]) and (i > 1) and (tokens[i - 2][0] in CONJ['not']):
                return 'Противоречие'
    return None


def phrase_filter(s):
    for error_type in ERROR_PHRASES.keys():
        for unit in ERROR_PHRASES[error_type]:
            if unit in s:
                return error_type
    return None


def antonym_finder(word):
    # nltk.download('wordnet')
    antonyms = []
    number_of_ant = 5
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
        if len(set(antonyms)) >= number_of_ant:
            break
    return list(set(antonyms))


def antonyms_filter(tokens):
    for i in range(1, len(tokens) - 1):
        if tokens[i][0] in CONJ['and']:
            if tokens[i - 1][0] in antonym_finder(tokens[i + 1][0]):
                return 'Противоречие'
    return None


def check_negation_contradiction(antonym_tracker, neg_doc1, neg_doc2):
    temp_var = neg_doc1 + neg_doc2 + antonym_tracker
    return 1 if (temp_var % 2 != 0) and (temp_var < 3) else 0


def check_values(t1):
    checklist_more = ['more than ', 'greater than ', 'above', 'больше']
    checklist_less = ['less than ', 'lesser than ', 'below', 'меньше']
    for phrase in checklist_more:
        idx = t1.find(phrase)
        if idx != -1:
            num1 = t1[idx + len(phrase): t1.find(' ', idx + len(phrase))]
            num1 = int(num1) if num1.isdigit() else num1

            for phrase2 in checklist_less:
                idx = t1.find(phrase2)
                if idx != -1:
                    num2 = t1[idx + len(phrase2): t1.find(' ', idx + len(phrase2))]
                    num2 = int(num2) if num2.isdigit() else num1
                    if num1 > num2:
                        return ["Численное противоречие"]
    return None


def contradictions_filter(s):
    antony = list()
    antonym_tracker = 0

    neg_doc1 = 0
    neg_doc2 = 0
    verb1 = ""
    verb2 = ""

    synonyms = []
    antonyms = []

    def ant_syn(word):
        from nltk.corpus import wordnet
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

    nlp = en_core_web_sm.load()
    doc1 = nlp(s)
    doc2 = nlp(s)

    for token in doc1:
        if token.dep_ == "neg":
            neg_doc1 = 1
            verb1 += "NOT "
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            verb1 += token.lemma_ + ' и '
            ant_syn(token.lemma_)
            for anton in antonyms:
                antony.append(anton)

    for token in doc2:
        if token.dep_ == "neg":
            neg_doc2 = 1
            verb2 += "NOT "
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            verb2 += token.lemma_ + ' '
            if token.lemma_ in antony:
                antonym_tracker = 1

    contr_tracker = check_negation_contradiction(antonym_tracker, neg_doc1, neg_doc2)

    if contr_tracker == 1:
        return f"{verb1.upper()[:-3]} не могут быть совершенны одновременно"

    return None


def numeric_errors_filter(doc1):
    return check_values(doc1)


def error_finder(sentence, lang=None):
    from mistake.models import Mistake
    s = sentence.message + ' '
    errors = []
    if lang is None:
        lang = detect(s)
    if lang not in ['ru', 'en']:
        return [f'Неизвестный язык:{lang}']
    phrase_type_error = phrase_filter(s)
    if phrase_type_error is not None:
        errors.append(Mistake.objects.create(type=phrase_type_error, sentence=sentence))
    if lang == 'ru':
        tokens = tokenize(s)
    else:
        tokens = tokenize_spacy(s)
    and_not_filter_res = and_not_filter(tokens)
    if and_not_filter_res is not None:
        errors.append(Mistake.objects.create(type=and_not_filter_res, sentence=sentence))
    if lang == 'en':
        antonyms_filter_res = antonyms_filter(tokens)
        if antonyms_filter_res is not None:
            errors.append(Mistake.objects.create(type=antonyms_filter_res, sentence=sentence))
        contradictions_filter_res = contradictions_filter(s)
        if contradictions_filter_res is not None:
            errors.append(Mistake.objects.create(type=contradictions_filter_res, sentence=sentence))
    numeric_errors_filter_res = numeric_errors_filter(s)
    if numeric_errors_filter_res is not None:
        errors.append(Mistake.objects.create(type=numeric_errors_filter_res, sentence=sentence))
    return errors if len(errors) > 0 else ['Ошибок не найдено']


# s = 'more than 5 less than 3 '
# # print(s)
# # print(tokenize(s))
# print(error_finder(s, lang='en'))



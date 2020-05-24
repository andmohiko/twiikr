import re

import numpy as np
import MeCab


nmc = MeCab.Tagger('-Ochasen')
nmw = MeCab.Tagger("-Owakati")


def get_wakati(text):
    return nmw.parse(text).strip()


def get_words(text, pos_list=[], form="asitis"):
    word_list = []
    inflection_index = inflection(form)
    for chunk in nmc.parse(text).splitlines()[:-1]:
        morpheme = chunk.split('\t')
        morpheme = parts_of_speech(morpheme, pos_list)
        if morpheme == None:
            continue
        word_list.append(morpheme[inflection_index])
    return word_list


def parts_of_speech(morpheme, pos_list):
    if pos_list == []:
        return morpheme
    else:
        for pos in pos_list:
            if morpheme[3].startswith(pos):
                return morpheme


def inflection(form):
    if form == "asitis":
        return 0
    elif form == "origin":
        return 2
    else:
        return "error in form"


def make_corpus(series):
    corpus_spaced = [0] * len(series)
    for i, words in enumerate(series):
        try:
            corpus_spaced[i] = get_wakati(words)
        except TypeError:
            print(i, words)
            corpus_spaced[i] = "nopositon"
    return corpus_spaced


def split_words(corpus_spaced):
    corpus_splitted = [0] * len(corpus_spaced)
    for i, c in enumerate(corpus_spaced):
        corpus_splitted[i] = c.split()
    return corpus_splitted


def join_words(corpus_splitted):
    corpus_joined = [0] * len(corpus_splitted)
    for i, c in enumerate(corpus_splitted):
        corpus_joined[i] = " ".join(c)
    return corpus_joined


def remove_stopwords(corpus_splitted, stopwords):
    na_idx = []
    for i, c in enumerate(corpus_splitted):
        corpus_splitted[i] = [word for word in c if word not in stopwords]
        if corpus_splitted[i] == []:
            na_idx.append(i)
    return corpus_splitted, na_idx

# -*- coding: utf-8 -*-


import os
import sys
import re
import codecs
from itertools import izip_longest


# class SentenceParser(object):
#     #ustawia pierwotny stan obiektu
#     #self - referencja na biezacy obiekt (jawnie, inaczej niz w Javie)
#     def __init__(self):
#         pass
#
#     def parse(self):

def make_pairs(values):
    return list(izip_longest(values[::2], values[1::2], fillvalue=""))

def is_ends_with_shortcut(text):
    return " " in text[-4:]

def parse_sentences(content):
    r = re.compile(r'([.!?]|\n)+')
    parts = r.split(content)
    pairs = make_pairs(parts)
    buffor = "" #skladujemy rzeczy ktore moga byc zdaniem (talerz)
    ends_with_shortcut = False
    results = []

    for part, separator in pairs:

        if separator == ".":
            #Patrzymy:
            #0. Czy ma cos na talerzu? Jesli tak to przetwarzamy kolejny part (jestesmy w nim)
            #1. Jesli koncze sie skrotem to kontynuujemy
            # Tak czy siak dodajemy cos na talerz
            if buffor and (part.strip() and (part.strip()[0].isupper() or not ends_with_shortcut)):
                results.append(buffor)
                buffor = ""

            buffor += part + separator
            ends_with_shortcut = is_ends_with_shortcut(part)
        # Wiemy ze mamy [!?\n], dajemy na talerz i od razu sciagamy
        else:
            results.append(buffor+part+separator)
            buffor = ""
            ends_with_shortcut = False #jak konczy sie np. wykrzyknikiem

        #niezaleznie dla ktorego warunku
        #chcemy wiedziec
        #ends_with_shortcut = is_ends_with_shortcut(part)

    results.append(buffor)
    return filter(bool, results)

def list_unique_counter(content, pattern):
    r = re.compile(pattern)
    list = r.findall(content)
    counts = 0
    if list:
        unique_words = set(list)
        counts = len(unique_words)

    return counts

# from (year - day - month) to (day - month - year)
def convert_data_format(dates_in_format_YDM):
    converted_dates = []
    for single_date in range(len(dates_in_format_YDM)):
        converted_dates += [((dates_in_format_YDM[single_date][1]),
                             (dates_in_format_YDM[single_date][2]),
                             (dates_in_format_YDM[single_date][0]))]
    return converted_dates

def counts_unique_dates(dates_in_format_DMY, dates_in_format_YDM):
    all_dates = dates_in_format_DMY + convert_data_format(dates_in_format_YDM)
    unique_words = 0

    if all_dates:
        unique_words = set(all_dates)
        counts = len(unique_words)

    return counts


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    ### section P ###
    pattern_section_p = r'<P>([\W|\w]*)</P>'
    r = re.compile(pattern_section_p)
    section_P = r.findall(content)
    #################

    #AUTOR
    autor_pattern = re.search(r'<META NAME="AUTOR" CONTENT="(\D*)">',content)
    autor = autor_pattern.group(1)

    #SECTION DESCRIPTION
    section_description_pattern = re.search(r'<META NAME="DZIAL" CONTENT="(.*)"',content)
    section_description = section_description_pattern.group(1)

    #KEY WORDS
    key_words = re.findall(r'<META NAME="KLUCZOWE_\d+" CONTENT="(.+)">', content)

    #EMAILS
    email_pattern = r'([\w-]+)(\.\w+)*@(\w+)(-\w+)*\.[a-zA-Z0-9]+(-\w+)*(\.[a-zA-Z]+(-\w+)*)*'
    #email_counts = list_unique_counter(content, email_pattern)
    email_counts = list_unique_counter(' '.join(section_P), email_pattern)

    #SHORTCUTS
    shortcut_pattern = r'(\s[a-zA-Z]{1,3}\.)'
    shortcut_counts = list_unique_counter(' '.join(section_P), shortcut_pattern)

    #FLOATS
    float_pattern = r' (?:-?(?:(?:\d+\.\d?)|(?:\d*\.\d+))(?:[eE][+-]\d+)?)'
    float_counts = list_unique_counter(' '.join(section_P), float_pattern)

    #INTEGERS
    integer_pattern = r'\s(([-]{,1}([1-9]\d{1,3}|[1-2]\d{4}|3[0-1]\d{3}|32[0-6]\d{2}|327[0-5]\d|3276[0-7]))|-32768|\d)\s'
    integer_counts = list_unique_counter(' '.join(section_P), integer_pattern)

    #SENTENCES
    sentences_counts = len(parse_sentences(' '.join(section_P)))

    # sentences_pattern = r'([\dA-ZĄĆĘŃÓŚŁŻŹ]([A-ZĄĆĘŃÓŚŁŻŹa-ząćęńóśżłź\s,\|\)\/\-\+\=\(\*&^%\$#@!\d]*|(\s[a-zA-Z]{1,3}\.\s))+)'
    # r = re.compile(sentences_pattern)
    # sentences_list = r.findall(' '.join(section_P))
    # sentences_counts = len(sentences_list)

    ###DATES
    # day - month - year
    # pattern6 = r'((31[-./](01|03|05|07|08|10|12)[-./]\d\d\d\d)|(((0[1-9])|(1[0-9])|2[0-9])[-./]((0[1-9])|(1[0-2]))[-./]\d\d\d\d)|(30[./](01|03|04|05|06|07|08|09|10|11|12)[-./]\d\d\d\d))'
    # r = re.compile(pattern6)
    # data = r.findall(' '.join(section_P))

    pattern7 = r'((31-(01|03|05|07|08|10|12)-\d\d\d\d)|(((0[1-9])|(1[0-9])|2[0-9])-((0[1-9])|(1[0-2]))-\d\d\d\d)|(30-(01|03|04|05|06|07|08|09|10|11|12)-\d\d\d\d))'
    r = re.compile(pattern7)
    data = r.findall(' '.join(section_P))

    pattern8 = r'((31.(01|03|05|07|08|10|12).\d\d\d\d)|(((0[1-9])|(1[0-9])|2[0-9]).((0[1-9])|(1[0-2])).\d\d\d\d)|(30.(01|03|04|05|06|07|08|09|10|11|12).\d\d\d\d))'
    r = re.compile(pattern8)
    data += r.findall(' '.join(section_P))

    pattern8 = r'((31/(01|03|05|07|08|10|12)/\d\d\d\d)|(((0[1-9])|(1[0-9])|2[0-9])/((0[1-9])|(1[0-2]))/\d\d\d\d)|(30/(01|03|04|05|06|07|08|09|10|11|12)/\d\d\d\d))'
    r = re.compile(pattern8)
    data += r.findall(' '.join(section_P))

    # year - day - month
    # pattern7 = r'(\d\d\d\d[-./]31[-./](01|03|05|07|08|10|12)|(\d\d\d\d[-./]((0[1-9])|(1[0-9])|2[0-9])[-./]((0[1-9])|(1[0-2])))|(\d\d\d\d[./]30[-./](01|03|04|05|06|07|08|09|10|11|12)))'
    # r = re.compile(pattern7)
    # data2 = r.findall(' '.join(section_P))

    pattern9 = r'(\d\d\d\d-31-(01|03|05|07|08|10|12)|(\d\d\d\d-((0[1-9])|(1[0-9])|2[0-9])-((0[1-9])|(1[0-2])))|(\d\d\d\d-30-(01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(pattern9)
    data2 = r.findall(' '.join(section_P))

    pattern10 = r'(\d\d\d\d.31.(01|03|05|07|08|10|12)|(\d\d\d\d.((0[1-9])|(1[0-9])|2[0-9]).((0[1-9])|(1[0-2])))|(\d\d\d\d.30.(01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(pattern10)
    data2 += r.findall(' '.join(section_P))

    pattern11 = r'(\d\d\d\d/31/(01|03|05|07|08|10|12)|(\d\d\d\d/((0[1-9])|(1[0-9])|2[0-9])/((0[1-9])|(1[0-2])))|(\d\d\d\d/30/(01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(pattern11)
    data2 += r.findall(' '.join(section_P))

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor: ", autor)
    print("dzial: ", section_description)
    print("slowa kluczowe:", key_words)
    print("liczba zdan: ", sentences_counts)
    print("liczba skrotow: ", shortcut_counts)
    print("liczba liczb calkowitych z zakresu int: ", integer_counts)
    print("liczba liczb zmiennoprzecinkowych: ", float_counts)
    print("liczba dat: ", counts_unique_dates(data,data2))
    print("liczba adresow email:", email_counts)
    print("\n")


try:
    path = os.path.join(os.getcwd(), "1993-01") #sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)



for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)

# assert parse_sentence("Ala ma kota.") == ['Ala ma kota.']
# assert parse_sentence("Ala ma kota. Kot ma Ale.") == ['Ala ma kota.', ' Kot ma Ale.']
# assert parse_sentence("Ala ma kota?! Pies ma asd 0.5 Kot ma Ale!!!") == ['Ala ma kota!', ' Pies ma asd 0.5 Kot ma Ale!']
# assert parse_sentence("Ala ma kota zl. ") == ['Ala ma kota zl. ']
# assert parse_sentence("Ala ma kota zl. asdaasa. ") == ['Ala ma kota zl. asdaasa. ']
# assert parse_sentence("Ala ma@wp.pl kota zl.\n SADAsas ") == ['Ala ma@wp.pl kota zl\n', ' SADAsas ']
#
# print parse_sentence("Ala ma@wp.pl kota zl??!\n SADAsas ")

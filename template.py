# -*- coding: utf-8 -*-
import os
import sys
import re
import codecs
from itertools import izip_longest


def multiple_replace(text, mapping):
    for old, new in mapping.items():
        text = text.replace(old, new)
    return text

def without_empty(values):
    """Pozbywa się z listy częsci, które składają się np. z samych spacji"""
    return [value for value in values if value.strip()]

def replace_emails(text, emails, placeholder="email"):
	# izip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
	#dict(izip_longest('ABCD', 'xy', fillvalue='-')) --> {'A': 'x', 'C': '-', 'B': 'y', 'D': '-'}
    mapping = dict(izip_longest(emails, (), fillvalue=placeholder))
    return multiple_replace(text, mapping)

def _get_safe_parts(text):
    """Ta funkcja dużo uprasza, bo przepuszczając przez nią tekst już nie musimy
    przejmować !, ? czy \n. Zostaje nam tylko kropka do obsługi.
    """
    return without_empty(re.split('[!?\n]+', text))

def is_ends_with_shortcut(text):
    return " " in text[-4:]

def parse_sentences(text, emails=None):
    if emails:
        text = replace_emails(text, emails)

    buffor = ''
    results = []
    ends_with_shortcut = False

    for long_part in _get_safe_parts(text):
        for part in without_empty(long_part.split('.')):
            if buffor and (part.strip()[0].isupper() or not ends_with_shortcut):
                results.append(buffor)
                buffor = ""

            buffor += part + '.'  # nie zawsze ta kropka ma sens
            ends_with_shortcut = is_ends_with_shortcut(part)

    results.append(buffor)
    return without_empty(results)

def list_unique_counter(content, pattern):
    r = re.compile(pattern)
    list = r.findall(content)
    counts = 0
    if list:
        unique_words = set(list)
        counts = len(unique_words)

    return counts

def counts_unique_dates(dates_in_format_DMY, dates_in_format_YDM):
    all_dates = clean_empty_tuples_for_date(dates_in_format_DMY) + usuwaniePustychRDM(dates_in_format_YDM)
    counts = 0
    if all_dates:
        unique_words = set(all_dates)
        counts = len(unique_words)

    return counts

# day - month - year
def clean_empty_tuples_for_date(tuples_list):
    new_tuples_list = []
    for i in tuples_list:  #dla kazdej daty
        for j in range(len(i)): #dla kazdego elementu krotki
            if i[j]!= u'':
                day = i[j]
                month = i[j+1]
                year = i[j+2]
                new_tuples_list += [(day,month,year)]
                break
    return new_tuples_list

# year - day - month
def usuwaniePustychRDM(tuples_list):
    new_tuples_list = []
    for i in tuples_list:  #dla kazdej daty
        tmp = []
        for j in range(len(i)): #dla kazdego elementu krotki
            if i[j]!= u'':
                tmp += [i[j]]
        new_tuples_list += [(tmp[1],tmp[2],tmp[0])]
    return new_tuples_list


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    ### SECTION P ###
    pattern_section_p = r'<P>([\W|\w]*)</P>'
    r = re.compile(pattern_section_p)
    section_P = r.findall(content)
    section_P = ' '.join(section_P)

    pattern_section_p_content = r'[^</>](?:\s*\w*[@.,ółżę)ąńśź(ć-]*)*[^<>]'
    r = re.compile(pattern_section_p_content)
    section_P = r.findall(section_P)
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
    email_pattern = r'((?:[\w-]+)(?:\.\w+)*@(?:\w+)(?:-\w+)*\.[a-zA-Z0-9]+(?:-\w+)*(?:\.[a-zA-Z]+(?:-\w+)*)*)'
    email_counts = list_unique_counter(' '.join(section_P), email_pattern)
    r = re.compile(email_pattern)
    email_list = r.findall(' '.join(section_P))

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
    sentences_counts = len(parse_sentences(' '.join(section_P), email_list))

    ###DATES
    # month - year - day
    myd_first_pattern = r'(?:(?:(31)-(01|03|05|07|08|10|12)-(\d\d\d\d))|(?:((?:0[1-9])|(?:1[0-9])|2[0-9])-((?:0[1-9])|(?:1[0-2]))-(\d\d\d\d))|(?:(30)-(01|03|04|05|06|07|08|09|10|11|12)-(\d\d\d\d)))'
    r = re.compile(myd_first_pattern)
    data = r.findall(' '.join(section_P))

    myd_second_pattern = r'(?:(?:(31).(01|03|05|07|08|10|12).(\d\d\d\d))|(?:((?:0[1-9])|(?:1[0-9])|2[0-9]).((?:0[1-9])|(?:1[0-2])).(\d\d\d\d))|(?:(30).(01|03|04|05|06|07|08|09|10|11|12).(\d\d\d\d)))'
    r = re.compile(myd_second_pattern)
    data += r.findall(' '.join(section_P))

    myd_third_pattern = r'(?:(?:(31)/(01|03|05|07|08|10|12)/(\d\d\d\d))|(?:((?:0[1-9])|(?:1[0-9])|2[0-9])/((?:0[1-9])|(?:1[0-2]))/(\d\d\d\d))|(?:(30)/(01|03|04|05|06|07|08|09|10|11|12)/(\d\d\d\d)))'
    r = re.compile(myd_third_pattern)
    data += r.findall(' '.join(section_P))

    # year - day - month
    ydm_first_pattern = r'(?:(?:(\d\d\d\d)-(31)-(01|03|05|07|08|10|12))|(?:(\d\d\d\d)-((?:0[1-9])|(?:1[0-9])|2[0-9])-(?:(0[1-9])|(1[0-2])))|(?:(\d\d\d\d)-(30)-(01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(ydm_first_pattern)
    data2 = r.findall(' '.join(section_P))

    ydm_second_pattern = r'(?:(?:(\d\d\d\d).(31).(01|03|05|07|08|10|12))|(?:(\d\d\d\d).((?:0[1-9])|(?:1[0-9])|2[0-9]).(?:(0[1-9])|(1[0-2])))|(?:(\d\d\d\d).(30).(01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(ydm_second_pattern)
    data2 += r.findall(' '.join(section_P))

    ydm_third_pattern = r'(?:(?:(\d\d\d\d)/(31)/(01|03|05|07|08|10|12))|(?:(\d\d\d\d)/((?:0[1-9])|(?:1[0-9])|2[0-9])/(?:(0[1-9])|(1[0-2])))|(?:(\d\d\d\d)/(30)/(01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(ydm_third_pattern)
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
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)

tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)


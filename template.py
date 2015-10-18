# -*- coding: utf-8 -*-


import os
import sys
import re
import codecs

def list_unique_counter(content, pattern):
    r = re.compile(pattern)
    list = r.findall(content)
    counts = 0
    if list:
        unique_words = set(list)
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
    key_words = re.findall(r'<META NAME="KLUCZOWE_\d+" CONTENT="(.*)">', content)

    #EMAILS
    email_pattern = r'([\w-]+)(\.\w+)*@(\w+)(-\w+)*\.[a-zA-Z0-9]+(-\w+)*(\.[a-zA-Z]+(-\w+)*)*'
    email_counts = list_unique_counter(content, email_pattern)

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
    sentences_pattern = r'([\dA-ZĄĆĘŃÓŚŁŻŹ]([A-ZĄĆĘŃÓŚŁŻŹa-ząćęńóśżłź\s,\|\)\/\-\+\=\(\*&^%\$#@!\d]*|(\s[a-zA-Z]{1,3}\.\s))+)'
    r = re.compile(sentences_pattern)
    sentences_list = r.findall(' '.join(section_P))
    sentences_counts = len(sentences_list)

    #DATES
    ###########################################
    def poprawnaDataDMR(listaDMR):
        lista=[]
        for i in listaDMR:
            if(u'0'<i[1]<=u'12'): #jesli miesiac ok
                if(i[1]==u'02' or i[1]==u'02'):
                    if(i[0]==u'28'):
                        lista+=[(i)] #jesli luty
                elif(i[0]<=u'31'):
                    lista+=[(i)] #jesli inne miesiace
        return lista

    def poprawnaDataRDM(listaRDM):
        lista=[]
        for i in listaRDM:
            if(u'0'<i[2]<=u'12'): #jesli miesiac ok
                if(i[2]==u'02' or i[2]==u'02'):
                    if(i[1]==u'28'):
                        lista+=[(i)] #jesli luty
                elif(i[1]<=u'31'):
                    lista+=[(i)] #jesli inne miesiace
        return lista

    def kon(listaRDM):
        i=[]
        for j in range(len(listaRDM)):
            i+=[((listaRDM[j][1]),(listaRDM[j][2]),(listaRDM[j][0]))]
        return i

    def liczbaDat(data, data2):
        liczba=0
        lista = data+kon(data2)
        ilosc=0
        for i in range(len(lista)):
            if lista:
                element = lista.pop()
                liczba=liczba+1
                ilosc=lista.count(element)
                for j in range(ilosc):
                    lista.remove(element)
        return liczba

    # day - month - year
    pattern6 = r'((31[-./](01|03|05|07|08|10|12)[-./]\d\d\d\d)|(((0[1-9])|(1[0-9])|2[0-9])[-./]((0[1-9])|(1[0-2]))[-./]\d\d\d\d)|(30[./](01|03|04|05|06|07|08|09|10|11|12)[-./]\d\d\d\d))'
    r = re.compile(pattern6)
    data = r.findall(' '.join(section_P))

    # year - day - month
    pattern7 = r'(\d\d\d\d[-./]31[-./](01|03|05|07|08|10|12)|(\d\d\d\d[-./]((0[1-9])|(1[0-9])|2[0-9])[-./]((0[1-9])|(1[0-2])))|(\d\d\d\d[./]30[-./](01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(pattern7)
    data2 = r.findall(' '.join(section_P))
    ###########################################


    fp.close()
    print("nazwa pliku:", filepath)
    print("autor: ", autor)
    print("dzial: ", section_description)
    print("slowa kluczowe:", key_words)
    print("liczba zdan: ", sentences_counts)
    print("liczba skrotow: ", shortcut_counts)
    print("liczba liczb calkowitych z zakresu int: ", integer_counts)
    print("liczba liczb zmiennoprzecinkowych: ", float_counts)
    print("liczba dat: ", liczbaDat(data,data2))
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





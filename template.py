# -*- coding: utf-8 -*-

__author1__ = 'Kamil'
__author2__ = 'Grzegorz'

import os
import sys
import re
import codecs

def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    def liczbaRoznychElementowListy(lista):
        liczba=0
        ilosc=0
        for i in range(len(lista)):
            if lista:
                element = lista.pop()
                liczba=liczba+1
                ilosc=lista.count(element)
                for j in range(ilosc):
                    lista.remove(element)
        return liczba


    ######### email ####################
    pattern = r'([\w-]+)(\.\w+)*@(\w+)(-\w+)*\.[a-zA-Z0-9]+(-\w+)*(\.[a-zA-Z]+(-\w+)*)*'

#     .@q.q.q.q.pl
# q@@qp._
# sq_12@p-.pl
# qwerty.qwerty25@gmail._
# qwerty.qwerty.12@co-m.f-888e.co-m.p-l.p-l
# qwerty@student.agh.edu.pl
# qwerty@student.agh.edu..pl
# qwerty..qwerty.12@fke.com
# qwerty.qwerty.12@.fke.com
# .qwerty.qwerty.12@fke.com
# qwerty.qwerty.12@fke.com.
# qwerty.qwerty.12.@fke.com

    r = re.compile(pattern)
    m = r.findall(content)
    emaile = liczbaRoznychElementowListy(m)
    ######################################


    pattern2 = r'<META NAME="AUTOR" CONTENT="(\D*)">'   #moj kod
    r = re.compile(pattern2)
    autor = r.findall(content)

    pattern3 = r'<META NAME="DZIAL" CONTENT="(.*)">'   #moj kod
    r = re.compile(pattern3)
    dzial = r.findall(content)

    pattern3 = r'<META NAME="KLUCZOWE_\d*" CONTENT="(\D*)">'   #moj kod (slowo kluczowe jako cyfra!)
    r = re.compile(pattern3)
    kluczowe = r.findall(content)


    ########## sekcja P ###############
    pattern4 = r'<P>([\W|\w]*)</P>'   #moj kod
    r = re.compile(pattern4)
    sekcjaP = r.findall(content)
    #########################################



    ########### skroty ##################
    pattern5 = r'(\s[a-zA-Z]{1,3}\.)'
    r = re.compile(pattern5)
    skr = r.findall(' '.join(sekcjaP))
    skrotyLiczba = liczbaRoznychElementowListy(skr)
    #####################################

    ########### daty ####################### dorobic ze daty sa poprawne
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


    pattern6 = r'((31[-./](01|03|05|07|08|10|12)[-./]\d\d\d\d)|(((0[1-9])|(1[0-9])|2[0-9])[-./]((0[1-9])|(1[0-2]))[-./]\d\d\d\d)|(30[./](01|03|04|05|06|07|08|09|10|11|12)[-./]\d\d\d\d))'
    r = re.compile(pattern6)
    data = r.findall(' '.join(sekcjaP))
   # print(data.group(1))



    pattern7 = r'(\d\d\d\d[-./]31[-./](01|03|05|07|08|10|12)|(\d\d\d\d[-./]((0[1-9])|(1[0-9])|2[0-9])[-./]((0[1-9])|(1[0-2])))|(\d\d\d\d[./]30[-./](01|03|04|05|06|07|08|09|10|11|12)))'
    r = re.compile(pattern7)
    data2 = r.findall(' '.join(sekcjaP))
    ###########################################



    #r'(-?((\d+\.?\d?)|(\d*\.?\d+))(e[+-]\d+)?)'

    ########## liczby zmiennoprzecinkowe ##############
    pattern7 = r' (?:-?(?:(?:\d+\.\d?)|(?:\d*\.\d+))(?:[eE][+-]\d+)?)'
    r = re.compile(pattern7)
    zmiennoprzecinkowe = r.findall(' '.join(sekcjaP))

    liczbyzm = liczbaRoznychElementowListy(zmiennoprzecinkowe)
    ####################################################

    ########## liczby calkowite ##############
    pattern7 = r'\s(([-]{,1}([1-9]\d{1,3}|[1-2]\d{4}|3[0-1]\d{3}|32[0-6]\d{2}|327[0-5]\d|3276[0-7]))|-32768|\d)\s'
    r = re.compile(pattern7)
    calk = r.findall(' '.join(sekcjaP))

    liczbyca = liczbaRoznychElementowListy(calk)
    ####################################################

    ########## zdania ##############
    pattern8 =r'([\dA-ZĄĆĘŃÓŚŁŻŹ]([A-ZĄĆĘŃÓŚŁŻŹa-ząćęńóśżłź\s,\|\)\/\-\+\=\(\*&^%\$#@!\d]*|(\s[a-zA-Z]{1,3}\.\s))+)'
    #r'([\dA-ZĄĆĘŃÓŚŁŻŹ](?:[A-ZĄĆĘŃÓŚŁŻŹa-ząćęńóśżłź\s,\|\)\/\-\+\=\(\*\&\^\%\$\#\@\!\d]*(?:\s[a-zA-Z]{1,3}\.\s)?)[\.!?\n]+\s)'
     # r'[\dA-ZĄĆĘŃÓŚŁŻŹ]([A-ZĄĆĘŃÓŚŁŻŹa-ząćęńóśżłź\s,\|\)\/\-\+\=\(\*\&\^\%\$\#\@\!\d])*[\.!?\n]+\s'
        #r'[A-ZĄĆĘŃÓŚŁŻŹ][a-ząćęńóśżłź\s,\|\)\/\-\+\=\(\*\&\^\%\$\#\@\!\d]*'
    r = re.compile(pattern8)
    zda = r.findall(' '.join(sekcjaP))
   # zdania = liczbaRoznychElementowListy(zda)
    print("aaa")
    print(zda)
    print("aaa")
    ####################################################






    fp.close()
    print("nazwa pliku:", filepath)
    print("autor:",autor[0])
    print("dzial:",dzial[0])
    print("slowa kluczowe:",', '.join(kluczowe))
    print("liczba zdan:")
    print("liczba skrotow:",skrotyLiczba)
    print("liczba liczb calkowitych z zakresu int:",liczbyca)
    print("liczba liczb zmiennoprzecinkowych:",liczbyzm)
    print("liczba dat:",liczbaDat(data,data2))
    print("liczba adresow email:",emaile)
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





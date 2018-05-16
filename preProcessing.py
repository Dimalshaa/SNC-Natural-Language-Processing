# -*- coding: cp1252 -*-
import os
import re

def zgradiListoDatotek(path):
    datoteke = os.listdir(path)

    for i in range(0, len(datoteke)):
        print("Datoteka: " + datoteke[i])


    return datoteke

def preberiDatoteko(dat):
    with file(dat) as f:
        string = f.read()

    return string


#popraviBesedilo -> odstrani locila, stevilke in vsa druga locila,
#spremeni velike crke v male.
def popraviBesedilo(besedilo):
    izhod = ""
    
    for char in besedilo:
        if char.isalpha():
            if char.isupper():
                izhod+=char.lower()
            else:    
                izhod+=char
        elif char.isspace():
            izhod+=char
        elif char=="�":
            izhod+=char
        elif char=="'":
            izhod+=char
        
    return izhod

def shraniDatoteko(path, filename, besedilo):
    dat = path + filename   
    file_out  = open(dat, 'w')

    file_out.write(besedilo)

     

if __name__ == "__main__":
    #path -> mapa kjer se nahajajo datoteke za obdelavo
    #path_izhod -> mapa v katero bomo shranjevali popravljene datoteke
    #path = "./suicide-notes-database/completers/"
    #path_izhod = "./suicide-notes-database/completers-pp/"

    path = "./suicide-notes-database/completers/"
    path_izhod = "./suicide-notes-database/completers-pp/"
    
    datoteke = zgradiListoDatotek(path)

    for i in range(0, len(datoteke)):
        filename = path + datoteke[i]
        besedilo = preberiDatoteko(filename)
        popravljeno_besedilo = popraviBesedilo(besedilo)
        shraniDatoteko(path_izhod, datoteke[i], popravljeno_besedilo)
       

    path = "./suicide-notes-database/elicitors/"
    path_izhod = "./suicide-notes-database/elicitors-pp/"
    
    datoteke = zgradiListoDatotek(path)

    for i in range(0, len(datoteke)):
        filename = path + datoteke[i]
        besedilo = preberiDatoteko(filename)
        popravljeno_besedilo = popraviBesedilo(besedilo)
        shraniDatoteko(path_izhod, datoteke[i], popravljeno_besedilo)

    path = "./suicide-notes-database/TESTER/C/"
    path_izhod = "./suicide-notes-database/TESTER/C-pp/"
    
    datoteke = zgradiListoDatotek(path)

    for i in range(0, len(datoteke)):
        filename = path + datoteke[i]
        besedilo = preberiDatoteko(filename)
        popravljeno_besedilo = popraviBesedilo(besedilo)
        shraniDatoteko(path_izhod, datoteke[i], popravljeno_besedilo)

    path = "./suicide-notes-database//TESTER/E/"
    path_izhod = "./suicide-notes-database/TESTER/E-pp/"
    
    datoteke = zgradiListoDatotek(path)

    for i in range(0, len(datoteke)):
        filename = path + datoteke[i]
        besedilo = preberiDatoteko(filename)
        popravljeno_besedilo = popraviBesedilo(besedilo)
        shraniDatoteko(path_izhod, datoteke[i], popravljeno_besedilo)
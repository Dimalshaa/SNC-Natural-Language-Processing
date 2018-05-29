# SNC-Natural-Language-Processing
Suicide Note Classification Using Natural Language Processing

### Člani skupine

- Denis Ekart
- Dejan Orter
- Gregor Kovačevič
- Alen Verk
- Dejan Rupnik

### Ime in opis projekta

Skozi projekt, ki smo si ga izbrali, se bomo osredotočali na razpoznavo poslovilnih pisem samomorilcev, bolj natančno- na razpoznavo pristnih pisem te narave, od pisem, ki to niso oziroma so le-ta lažna. V pomoč nam bo znanstveni članek Suicide Note Classification Using Natural Language Processing: A Content Analysis [http://journals.sagepub.com/doi/pdf/10.4137/BII.S4706]. Predvideva se, da se s pomočjo procesiranja naravnega jezika in algoritmov pristna pisma ločijo od lažnih v večini primerov. Postopek analiziranja pisem poteka v več korakih, prvi izmed njih je razčlemba besedila, sledi označevanje ključnih besed in povezava ključnih besed s posameznimi koncepti iz tega področja. Takšno besedilo se doda v množico besedil za strojno učenje, ki poteka pod nadzorom uporabnika (dodajanje tag-ov v besedilo). Naučena programska oprema je nato sama zmožna ločevati med pristnimi in ostalimi pismi.  

Testne množice bomo pridobili s pomočjo naslednjih virov:

1. https://russelljohn.net/journal/2008/03/a-collection-of-suicide-notes/ ,
2. https://www.researchgate.net/publication/305280412_SUICIDE_NOTE_THE_LAST_WORDS ,
3. https://www.sciencedirect.com/science/article/pii/S135311319990175X ,
4. https://www.historicmysteries.com/suicide-notes/ .

Lažna pisma bomo sestavili sami.



## Implementacija

### Parts-Of-Speech
Uporabljene nestandardne knjižnice: 

1. LXML [http://lxml.de/]

2. NLTK [https://www.nltk.org/]


Skripta podpira obdelavo korpusov v <u>.txt</u> in <u>.xml</u> formatu. Funkcija `readFiles` kot parameter sprejme pot do direktorija iz katerega nato prebere tektovno vsebino.

Primer uporabe:

```python
data = readFiles("./suicide-notes-database/elicitors")
```

Spremenljivka `data`, ki jo vrača zgoraj omenjena funkcija, je dvodimenzionalna tabela. `data[0][4]` nam, na primer, pove vsebino petega besedila v prvi datoteki izbranega direktorija. Ta oblika zapisa se pojavi samo pri obdelavi XML datotek (ker iščemo po paragrafih). Pri navadnih tekstovnih datotekah je celotna vsebina datoteke shranjena v `data[0][0]`.

Funkcija `partsOfSpeechTaggingMultiprocessed` poskrbi za tokenizacijo in označevanje besed glede na pomen v povedi. Dodana je tudi podpora za več nitno delovanje. Za celoten seznam in pomene določenih označb si poglejte: https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging. 

Uporablja se kot metoda razreda `PartsOfSpeechTagger`, kot parametra pa podamo podatke, ki jih želimo procesirati s parts-of-speech in parameter `number_of_processes`, s katerim povemo, na koliko nitih želimo, da se program izvaja. Ker je ta način izvajanja primeren za delo nad večjim številom korpusev, podatkov ne dodaja v spremenljivko, temveč rezultate izpisuje v datoteke. Rezultate lahko uporabimo za merjenje povprečij in ostale statistike, kjer ID dokumenta ni pomemben (za primere, kjer potrebujemo podatek, kateri slovar pripada kateremu pismu, si poglejte podpoglavje "Pridobivanje statistike za posamezno pismo").



Primer uporabe:

```txt
./some_text_file_content.txt

I am now convinced that my condition is too chronic, and therefore a cure is doubtful. All of a sudden all will and determination to fight has left me. I did desperately want to get well. But it was not to be–I am defeated and exhausted physically and emotionally. Try not to grieve. Be glad I am at least free from the miseries and loneliness I have endured for so long.
```

```python
data = readFiles("./suicide-notes-database/completers-pp/", ".//post")
pos = PartsOfSpeechTagger("./suicide-notes-database/parts_of_speech/")

# multi threaded tagger
pos.partsOfSpeechTaggingMultiprocessed(data, 6)
```

Rezultat:

```json
[('I', 'PRP'), ('am', 'VBP'), ('now', 'RB'), ('convinced', 'JJ'), ('that', 'IN'), ('my', 'PRP$'), ('condition', 'NN'), ('is', 'VBZ'), ('too', 'RB'), ('chronic', 'JJ'), (',', ','), ('and', 'CC'), ('therefore', 'RB'), ('a', 'DT'), ('cure', 'NN'), ('is', 'VBZ'), ('doubtful', 'JJ'), ('.', '.'), ('All', 'DT'), ('of', 'IN'), ('a', 'DT'), ('sudden', 'JJ'), ('all', 'DT'), ('will', 'MD'), ('and', 'CC'), ('determination', 'NN'), ('to', 'TO'), ('fight', 'NN'), ('has', 'VBZ'), ('left', 'VBN'), ('me', 'PRP'), ('.', '.'), ('I', 'PRP'), ('did', 'VBD'), ('desperately', 'RB'), ('want', 'VB'), ('to', 'TO'), ('get', 'VB'), ('well', 'RB'), ('.', '.'), ('But', 'CC'), ('it', 'PRP'), ('was', 'VBD'), ('not', 'RB'), ('to', 'TO'), ('be\xe2\x80\x93I', 'VB'), ('am', 'VBP'), ('defeated', 'VBN'), ('and', 'CC'), ('exhausted', 'VBN'), ('physically', 'RB'), ('and', 'CC'), ('emotionally', 'RB'), ('.', '.'), ('Try', 'VB'), ('not', 'RB'), ('to', 'TO'), ('grieve', 'VB'), ('.', '.'), ('Be', 'NNP'), ('glad', 'JJ'), ('I', 'PRP'), ('am', 'VBP'), ('at', 'IN'), ('least', 'JJS'), ('free', 'JJ'), ('from', 'IN'), ('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC'), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN'), ('so', 'RB'), ('long', 'RB'), ('.', '.')]
```

POMEMBNO: Pred zagonom omenjene funkcije, je treba pognati metodo `downloadLexicons`, ki s spleta naloži vse potebne leksikone in ostale datoteke, ki jih NLTK potrebuje za delovanje.



#### Branje rezultatov Parts-of-Speech

Za branje rezultatov, ki jih vrača `partsOfSpeechTaggingMultiprocessed`, uporabimo razred `PartsOfSpeechReader`.

Primer uporabe:

```python
# reader : statistics
pos_reader = PartsOfSpeechReader(
    "./suicide-notes-database/parts_of_speech/",
    "./suicide-notes-database/parts_of_speech_statistics/"
	)
pos_data = pos_reader.readAnalyzedData()
pos_reader.partsOfSpeechStatistics(pos_data)
statistics = pos_reader.getMedianStatistics()
```

Zgornja koda sešteje vse pojavitve tag-ov, parts-of-speech datotek. kot rezultat (spremenljivka `statistics`) vrne slovar povprečnih pojavitev določenih označb. Torej, koliko glagolov, ločil, samostalnikov itd., vsebuje povprečno pismo.

Primer rezultatov:

```json
PRP$  :  2.07936507937
VBG  :  1.4126984127
VBD  :  3.19047619048
VBN  :  1.68253968254
POS  :  0.0634920634921
''  :  0.015873015873
VBP  :  4.55555555556
WDT  :  0.206349206349
JJ  :  4.44444444444

...
```



Slovar označb smo normalizirali na značke, prikazane spodaj, a je poljubno razširljiv:

```python
# normalize dictionary
dict = { 
    	"CC" : 0, "DT" : 0, "EX" : 0, "IN" : 0,	
    	"JJ" : 0, "JJS" : 0, "MD" : 0, "NN" : 0,	
    	"NNS" : 0, "PDT" : 0, "PRP" : 0, "PRP$" : 0, 
    	"RB" : 0, "TO" : 0,	"VB" : 0, "VBD" : 0, 
    	"VBG" : 0, "VBN" : 0, "VBP" : 0, "VBZ" : 0, 
    	"WDT" : 0
	}
```



***OPOZORILO: Obe funkciji, `partsOfSpeechTaggingMultiprocessed` in `partsOfSpeechStatistics`, ob zagonu pobrišeta vsebino podanih direktorijev!***

Podrobnejši primer uporabe je prikazan v `partsOfSpeech.py` v `"__main__"`.



#### Pridobivanje statistike za posamezno pismo

Pridobi statistiko za vsako posamezno pismo in pri tem ohrani ime pisma (za to poskrbi funkcija `getFileByFileStatistics`):

```python
full_data_completers = []
folder_path = "./suicide-notes-database/completers-pp/"
pos_folder_path = "./suicide-notes-database/parts_of_speech/"
statistics_folder_path = "./suicide-notes-database/parts_of_speech_statistics/"
paragraph_tag_name = ".//post"
full_data_completers = getFileByFileStatistics(folder_path, pos_folder_path, 		statistics_folder_path, paragraph_tag_name)

## print 1st letter's pos dictionary
print full_data_completers[1][0][1][0]
```



### Feature selection

Uporabljene nestandardne knjižnice:

1. sklearn [http://scikit-learn.org/stable/modules/classes.html]

Skripta podpira obdelavo korpusov v <u>.txt</u> formatu. Funkcija `buildCorpus` kot parameter sprejme pot enega direktorija ali več direktorijev v array-u npr.: `.\completeres` ali `[.\completers, .\elictors]`.

Primer uporabe:

```python
corpus = buildCorpus(['.\suicide-notes-database\completers', '.\suicide-notes-database\elicitors'])
corpus = buildCorpus('.\suicide-notes-database\completers')
```
Spremenljivka `corpus` je tipa `list` in vsak element predstavlja celotno vsebino datoteke.

Funkcija `bagOfWords` poskrbi za izdelavo slovarja-vocabulary kourpusa. Prav tako pa pove frekvenco besed v posameznem elementu korpusa glede na slovar.

#### Splošna statistika

Funkcija splosnaStatistika kot vhodni parameter sprejme pot do direktorija kjer se nahajo pisma. 

Primer klica: 

```
statistika = splosnaStatistika('./suicide-notes-database/completers')
```

Kot izhod pa dobimo array z statistiko v obliki

imeDatoteke1.txt|st.besed|st.znakov|st.crk|st.stavkov
imeDatoteke2.txt|st.besed|st.znakov|st.crk|st.stavkov

Primer izhoda:

------STATISTIKA-------

1.txt|195|242|682|20|

10.txt|71|103|253|6|

11.txt|34|49|117|4|

12.txt|42|61|180|7|

13.txt|92|106|309|11|



### Pre-processing

Pripravi korpuse na nadaljno uporabo. Iz teksta odstrani ločila, številke ter vse ostale ne standardne znake. Poskrbi za pretvorbo velikih črk v male črke.

Primer uporabe:

```python
    path = "./suicide-notes-database/raw/genuine/"
    path_izhod = "./suicide-notes-database/raw/genuine-predobdelana/"
```

Za uporabo samo nastavimo spremenljivko "path" na mapo (direktorij), kjer se nahajajo vhodni korpusi za obdelavo. V spremenljivko "path_izhod" zapišemo direktorij v katerega se bodo shranili pre obdelani korpusi.

Vhod:

```text
    The act of taking my own life is not something that I do without a lot of thought. I don't believe that people should take their own lives without deep and thoughtful reflection over a considerable period of time. I do believe strongly, however, that the right to do so is one of the most fundamental rights anyone in a free society should have. For me much of the world makes no sense, but my feelings about what I am doing ring loud and clear to an inner ear and to a place where there is no self, only calm. Love always, Wendy.
```

Izhod:

```text
	the act of taking my own life is not something that i do without a lot of thought i don't believe that people should take their own lives without deep and thoughtful reflection over a considerable period of time i do believe strongly however that the right to do so is one of the most fundamental rights anyone in a free society should have for me much of the world makes no sense but my feelings about what i am doing ring loud and clear to an inner ear and to a place where there is no self only calm love always wendy
```

### Readability

<u>Besedilo naj se ne pre-procesira pred izvajanjem testa</u>

####Teorija

#####Flesch score

`RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)` 

**RE** = Readability Ease 

**ASL** = Average Sentence Length (i.e., the number of words divided by the number of sentences) 

**ASW** = Average number of syllables per word (i.e., the number of syllables divided by the number of words) 

<u>Višji je RE manjša je kompleksnost besedila</u>. Pričakovan izhod je med [0 - 100] vendar pa se zaradi napak v formatiranju lahko pojavijo napake. Te bomo normalizirali na pričakovane vrednosti(tj. 0 - 100)

*Mutilacije RE se lahko zgodijo zaradi nepravilnega formatiranja besedila (npr. manjkajo ločila,...)*



##### Flesch-Kincaid level

`RL=0.39 x ( TW / TS ) + 11.8 x ( TSYL / TW ) - 15.59`

**TW** = Total Words

**TS** = Total Sentences

**TSYL** = Total Syllables

<u>Rezultat ustreza razrednem nivoju v ZDA. Optimalno je med **[0 - 12]**, ekstremne vrednosti pa sežjo med **[-3,4   - 13+]**. Rezultat je, tako kot pri RE odvisen od pravilnega formatiranja besedila.</u>



Nad korpusom izvede teste bralnosti teksta, po Flesch-ovi metodi in po metodi Flesch-Kincaid.

Flesch metoda vrne oceno bralnosti teksta(readability score), katera je decimalno število med 0 in 100.

Flesch-Kincaid metoda vrne nivo bralnosti teksta (readability grade level), katera je decimalno število med 0 in 10.

Primer klica:

```python
#klic
results=readibility_test(".", "*.txt")

#iteracija med rezultati
for result in results:
    print "Ime datoteke "+result[0]
    print "Flesch score "+str(result[1])
    print "Flesch-Kincaid grade "+str(result[2])
```

Primer rezultata:

```
Ime datoteke .\1.txt
Flesch score 69.45625
Flesch-Kincaid grade 6.36638888889

Ime datoteke .\2.txt
Flesch score 83.8535714286
Flesch-Kincaid grade 5.04142857143

Ime datoteke .\3.txt
Flesch score 99.0157142857
Flesch-Kincaid grade 1.18761904762

Ime datoteke .\4.txt
Flesch score 79.4342857143
Flesch-Kincaid grade 7.39682539683
```



Opis funkcije `readability_test`:

Vhod: 

- `root:str` - root direktorij za iskanje dokumentov
- `file_pattern:string` - regex vzorec za izbiro datotek (npr. "*", "\*.txt",...)

Izhod:

Array generator objektov (evalvacija se zgodi komaj ob dostopanju do vrednosti - nepomembno za končnega uporabnika)

`(file_path:str, flesch_readability_ease_score:num[0-100], flesch_kincaid_grade_level:num[0-10])`

### CSV Maker

Združi dve vhodni csv datoteki v eno izhodno.
**Program išče datoteke na pathu:**

./ml-database 

Primer uporabe:

```python
    fileToJoin1 = "learning_set_elicitors.csv"
    fileToJoin2 = "learning_set_completers.csv"
    outputFile = "learning_set.csv"

    joinFiles(fileToJoin1, fileToJoin2 , outputFile)
```

Zgornji primer bi pomeni, da hočemo združiti datoteki learning_set_elicitors.csv in learning_set_completers.csv, ki sta na pathu ./ml-database
(./ml-database/learning_set_elicitors.csv, ..) v izhodno datoteko learning_set.csv.

filetoJoin1 in fileToJoin2 sta vhodni datoteki. outputFile je izhodna datoteka, katero hočemo generirati.
joinFiles(vhodna_dat1, vhodna_dat2, izhodna_dat) je klic funkcije, ki opravi združitev. 
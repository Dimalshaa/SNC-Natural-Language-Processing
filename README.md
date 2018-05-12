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

Funkcija `partsOfSpeechTagging` poskrbi za tokenizacijo in označevanje besed glede na pomen v povedi. Za celoten seznam in pomene določenih označb si poglejte: https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging. 

Primer uporabe:

```txt
./some_text_file_content.txt

I am now convinced that my condition is too chronic, and therefore a cure is doubtful. All of a sudden all will and determination to fight has left me. I did desperately want to get well. But it was not to be–I am defeated and exhausted physically and emotionally. Try not to grieve. Be glad I am at least free from the miseries and loneliness I have endured for so long.
```

```python
pos = PartsOfSpeechTagger("./suicide-notes-database/results")
pos.partsOfSpeechTagging(data)
#pos.data_tagged
```

Rezultat:

```python
[('I', 'PRP'), ('am', 'VBP'), ('now', 'RB'), ('convinced', 'JJ'), ('that', 'IN'), ('my', 'PRP$'), ('condition', 'NN'), ('is', 'VBZ'), ('too', 'RB'), ('chronic', 'JJ'), (',', ','), ('and', 'CC'), ('therefore', 'RB'), ('a', 'DT'), ('cure', 'NN'), ('is', 'VBZ'), ('doubtful', 'JJ'), ('.', '.'), ('All', 'DT'), ('of', 'IN'), ('a', 'DT'), ('sudden', 'JJ'), ('all', 'DT'), ('will', 'MD'), ('and', 'CC'), ('determination', 'NN'), ('to', 'TO'), ('fight', 'NN'), ('has', 'VBZ'), ('left', 'VBN'), ('me', 'PRP'), ('.', '.'), ('I', 'PRP'), ('did', 'VBD'), ('desperately', 'RB'), ('want', 'VB'), ('to', 'TO'), ('get', 'VB'), ('well', 'RB'), ('.', '.'), ('But', 'CC'), ('it', 'PRP'), ('was', 'VBD'), ('not', 'RB'), ('to', 'TO'), ('be\xe2\x80\x93I', 'VB'), ('am', 'VBP'), ('defeated', 'VBN'), ('and', 'CC'), ('exhausted', 'VBN'), ('physically', 'RB'), ('and', 'CC'), ('emotionally', 'RB'), ('.', '.'), ('Try', 'VB'), ('not', 'RB'), ('to', 'TO'), ('grieve', 'VB'), ('.', '.'), ('Be', 'NNP'), ('glad', 'JJ'), ('I', 'PRP'), ('am', 'VBP'), ('at', 'IN'), ('least', 'JJS'), ('free', 'JJ'), ('from', 'IN'), ('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC'), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN'), ('so', 'RB'), ('long', 'RB'), ('.', '.')]
```

POMEMBNO: Pred zagonom omenjene funkcije, je treba pognati metodo `downloadLexicons`, ki s spleta naloži vse potebne leksikone in ostale datoteke, ki jih NLTK potrebuje za delovanje.

Dodana je tudi podpora za več nitno delovanje. Uporablja se isto, kot `PartsOfSpeechTagger`, le da tu vnesemo še dodatni parameter `number_of_processes`, s katerim podamo, na koliko nitih želimo, da se program izvaja. Ker je ta način izvajanja primeren za delo nad večjim številom korpusev, podatkov ne dodaja v `self.data_tagged`, temveč rezultate izpisuje v datoteke.

```python
pos = PartsOfSpeechTagger()
pos.partsOfSpeechTaggingMultiprocessed(data, 6)
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
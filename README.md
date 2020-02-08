# SNC-Natural-Language-Processing
Suicide Note Classification Using Natural Language Processing

### Team members

- Dennis Eckart
- Dejan Orter
- Gregor Kovachevich
- Allen Verk
- Dejan Rupnik

### The name and description of the project

Through the project we have chosen, we will focus on recognizing the suicide letters of suicide, more specifically on identifying genuine letters of this nature, from letters that are not or are false. Suicide Note Classification Using Natural Language Processing: A Content Analysis [http://journals.sagepub.com/doi/pdf/10.4137/BII.S4706] will help us. It is assumed that through natural language processing and algorithms, genuine letters are separated from false ones in most cases. The process of analyzing the letters is done in several steps, the first of which is the parsing of the text, followed by the tagging of the keywords and the linking of the keywords with the respective concepts in the field. Such text is added to a plethora of machine learning texts that are controlled by the user (adding tags to the text).  

Test sets will be obtained using the following resources:

1. https://russelljohn.net/journal/2008/03/a-collection-of-suicide-notes/,
2. https://www.researchgate.net/publication/305280412_SUICIDE_NOTE_THE_LAST_WORDS,
3. https://www.sciencedirect.com/science/article/pii/S135311319990175X,
4. https://www.historicmysteries.com/suicide-notes/.

We will compose false letters ourselves.



## Implementation

### Parts-Of-Speech
Non-standard libraries used: 

1. LXML [http://lxml.de/]

2. NLTK [https://www.nltk.org/]


The script supports corpus processing in <u> .txt </u> and <u> .xml </u> formats. The `readFiles` function takes the path to the directory from which it then reads the text content.

Application example:

`` python
data = readFiles ("./ suicide-notes-database / elicitors")
``

The `data` variable returned by the function mentioned above is a two-dimensional table. `data [0] [4]`, for example, tells us the contents of the fifth text in the first file of the selected directory. This format only occurs when processing XML files (because we search for paragraphs). For plain text files, the entire contents of the file are stored in `data [0] [0]`.

The `partsOfSpeechTaggingMultiprocessed` function arranges for the tokenization and marking of words according to the meaning in the sentence. Support for multi-threaded operation is also added. For a full list and meanings of specific designations, see: https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging.

It is used as the method of the `PartsOfSpeechTagger` class, and as the parameter we specify the data we want to process with parts-of-speech and the parameter` number_of_processes`, which tells us how many threads we want the program to execute. Because this method of execution is suitable for working on a large number of corpora, it does not add data to a variable but outputs the results to files. The results can be used to measure averages and other statistics where the ID of the document is not important (for cases where we need to know which dictionary belongs to which letter, see the section "Getting statistics for each letter").



Application example:

`` `txt
./some_text_file_content.txt

I am now convinced that my condition is too chronic, and therefore a cure is doubtful. All of a sudden all will and determination to fight has left me. I did desperately want to get well. But it wasn't to be – I was defeated and exhausted physically and emotionally. Try not to grieve. Be hungry I am at least free from the miseries and loneliness I have endured for so long.
``

`` python
data = readFiles ("./ suicide-notes-database / completers-pp /", ".//post")
pos = PartsOfSpeechTagger ("./ suicide-notes-database / parts_of_speech /")

# multi threaded tagger
pos.partsOfSpeechTaggingMultiprocessed (data, 6)
``

Result:

`` `json
[('I', 'PRP'), ('am', 'VBP'), ('now', 'RB'), ('convinced', 'JJ'), ('that', 'IN') , ('my', 'PRP $'), ('condition', 'NN'), ('is', 'VBZ'), ('too', 'RB'), ('chronic', 'JJ' ), (',', ','), ('and', 'CC'), ('therefore', 'RB'), ('a', 'DT'), ('girls', 'NN' ), ('is', 'VBZ'), ('doubtful', 'JJ'), ('.', '.'), ('All', 'DT'), ('of', 'IN' ), ('a', 'DT'), ('sudden', 'JJ'), ('all', 'DT'), ('will', 'MD'), ('and', 'CC' ), ('determination', 'NN'), ('to', 'TO '), (' fight ',' NN '), (' has ',' VBZ '), (' left ',' VBN '), (' me ',' PRP '), ('. ',' . '), (' I ',' PRP '), (' did ',' VBD '), (' desperately ',' RB '), (' want ',' VB '), (' to ',' TO '), (' get ',' VB '), (' well ',' RB '), ('. ','. '), (' But ',' CC '), (' it ',' PRP '), (' was', 'VBD'), ('not', 'RB'), ('to', 'TO'), ('be \ xe2 \ x80 \ x93I', 'VB'), ('am', 'VBP'), ('defeated', 'VBN'), ('and', 'CC'), ('exhausted', 'VBN'), ('physically', 'RB'), ('and', 'CC'), ('emotionally', 'RB '), ('. ','. '), (' Try ',' VB '), (' not ',' RB '), (' to ',' TO '), (' grieve ',' VB '), ('. ','. '), (' Be ',' NNP '), (' hunger ',' JJ '), (' I ',' PRP '), (' am ',' VBP '), (' at ',' IN '), (' least ',' JJS '), (' free ',' JJ '), (' from ',' IN '), (' the ',' DT '), (' miseries ',' NNS '), (' and ',' CC '), (' loneliness ',' NN '), (' I ',' PRP '), (' have ',' VBP '), (' endured ',' VBN '), (' for ',' IN '), (' so ',' RB '), (' long ',' RB '), ('. ',' . ')]), ('not', 'RB'), ('to', 'TO'), ('grieve', 'VB'), ('.', '.'), ('Be', 'NNP' ), ('hunger', 'JJ'), ('I', 'PRP'), ('am', 'VBP'), ('at', 'IN'), ('least', 'JJS' ), ('free', 'JJ'), ('from', 'IN'), ('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC' ), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN' ), ('so', 'RB'), ('long', 'RB'), ('.', '.')]), ('not', 'RB'), ('to', 'TO'), ('grieve', 'VB'), ('.', '.'), ('Be', 'NNP' ), ('hunger', 'JJ'), ('I', 'PRP'), ('am', 'VBP'), ('at', 'IN'), ('least', 'JJS' ), ('free', 'JJ'), ('from', 'IN'), ('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC' ), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN' ), ('so', 'RB'), ('long', 'RB'), ('.', '.')]('Be', 'NNP'), ('Hunger', 'JJ'), ('I', 'PRP'), ('am', 'VBP'), ('at', 'IN'), ('least', 'JJS'), ('free', 'JJ'), ('from', 'IN'), ('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC'), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN'), ('so', 'RB'), ('long', 'RB'), ('.', '.')]('Be', 'NNP'), ('Hunger', 'JJ'), ('I', 'PRP'), ('am', 'VBP'), ('at', 'IN'), ('least', 'JJS'), ('free', 'JJ'), ('from', 'IN'), ('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC'), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN'), ('so', 'RB'), ('long', 'RB'), ('.', '.')]('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC'), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN'), ('so', 'RB'), ('long', 'RB'), ('.', '.')]('the', 'DT'), ('miseries', 'NNS'), ('and', 'CC'), ('loneliness', 'NN'), ('I', 'PRP'), ('have', 'VBP'), ('endured', 'VBN'), ('for', 'IN'), ('so', 'RB'), ('long', 'RB'), ('.', '.')]
``

IMPORTANT: The `downloadLexicons` method must be run before running the mentioned function, which downloads all the necessary lexicons and other files that NLTK needs to operate.



#### Reading Parts-of-Speech Results

We use the `PartsOfSpeechReader` class to read the results returned by` partsOfSpeechTaggingMultiprocessed`.

Application example:

`` python
# reader: statistics
pos_reader = PartsOfSpeechReader (
    "./suicide-notes-database/parts_of_speech/",
    "./suicide-notes-database/parts_of_speech_statistics/"
	)
pos_data = pos_reader.readAnalyzedData ()
pos_reader.partsOfSpeechStatistics (pos_data)
statistics = pos_reader.getMedianStatistics ()
``

The above code summarizes all occurrences of tag, parts-of-speech files. returns the dictionary of average occurrences of certain labels as a result (the `statistics` variable). So how many verbs, punctuation, nouns, etc., does the average letter contain.

Example results:

`` `json
PRP $: 2.07936507937
VBG: 1.4126984127
VBD: 3.19047619048
VBN: 1.68253968254
POS: 0.0634920634921
'': 0.015873015873
VBP: 4.55555555556
WDT: 0.206349206349
JJ: 4.44444444444

...
``



We've normalized the tag dictionary to the badges shown below, but it's optional:

`` python
# normalize dictionary
dict = { 
    	"CC": 0, "DT": 0, "EX": 0, "IN": 0,	
    	"JJ": 0, "JJS": 0, "MD": 0, "NN": 0,	
    	"NNS": 0, "PDT": 0, "PRP": 0, "PRP $": 0, 
    	"RB": 0, "TO": 0, "VB": 0, "VBD": 0, 
    	"VBG": 0, "VBN": 0, "VBP": 0, "VBZ": 0, 
    	"WDT": 0
	}
``



*** WARNING: Both the `partsOfSpeechTaggingMultiprocessed` and` partsOfSpeechStatistics` functions delete the contents of the specified directories at startup! ***

A more detailed use case is shown in `partsOfSpeech.py` in` `__main __ ''.



#### Retrieve statistics for each letter

Retrieves statistics for each individual letter while maintaining the name of the letter (provided by the `getFileByFileStatistics` function):

`` python
full_data_completers = []
folder_path = "./suicide-notes-database/completers-pp/"
pos_folder_path = "./suicide-notes-database/parts_of_speech/"
statistics_folder_path = "./suicide-notes-database/parts_of_speech_statistics/"
paragraph_tag_name = ".//post"
full_data_completers = getFileByFileStatistics (folder_path, pos_folder_path, statistics_folder_path, paragraph_tag_name)

## print 1st letter's pos dictionary
print full_data_completers [1] [1] [2]
``



### Feature selection

Non-standard libraries used:

1. sclearn [http://scikit-learn.org/stable/modules/classes.html]

The script supports corpus processing in <u> .txt </u> format. The `buildCorpus` function takes the path of one directory or multiple directories in an array, for example:`. \ Completeres` or `[. \ Completers,. \ Elictors]`.

Application example:

`` python
corpus = buildCorpus (['. \ suicide-notes-database \ completers', '. \ suicide-notes-database \ elicitors'])
corpus = buildCorpus ('. \ suicide-notes-database \ completers')
``
The `corpus` variable is of the` list` type and each element represents the entire contents of the file.

The `bagOfWords` function arranges for the creation of vocabulary vocabulary. It also tells the frequency of words in each corpus element according to the dictionary.

#### General Statistics

GeneralStatistics takes the path to the directory where the letters are located as the input parameter. 

Call example: 

``
statistics = generalStatistics ('./ suicide-notes-database / completers')
``

As an output, we get an array with statistics in the form

filename1.txt | st.besed | st.signs | st.crk |
filename2.txt | st.besed | st.signs | st.crk |

Example output:

------ STATISTICS -------

1.txt | 195 | 242 | 682 | 20 |

10.txt | 71 | 103 | 253 | 6 |

11.txt | 34 | 49 | 117 | 4 |

12.txt | 42 | 61 | 180 | 7 |

13.txt | 92 | 106 | 309 | 11 |



### Pre-processing

Prepare the corps for further use. Removes punctuation, numbers, and any non-standard characters from the text. Arrange for upper case to lower case letters.

Application example:

`` python
    path = "./suicide-notes-database/raw/genuine/"
    path_exit = "./suicide-notes-database/raw/genuine-preprocessed/"
``

For use, we just set the "path" variable to the directory (directory) where the input corpus for processing are located. In the "path_exit" variable, write the directory where the pre-processed corpora will be stored.

Entrance:

`` text
    The act of taking my own life is not something that I do without a lot of thought. I do not believe that people should take their own lives without deep and thoughtful reflection over a considerable period of time. I do believe strongly, however, that the right to do so is one of the most fundamental rights anyone in a free society should have. For me, much of the world makes no sense, but my feelings about what I am doing ring loud and clear to the inner ear and to a place where there is no self, only calm. Love always, Wendy.
``

Exit:

`` text
	the act of taking my own life is not something that I do without a lot of thought and don't believe that people should take their own lives without a deep and thoughtful reflection over a considerable period of time and do believe strongly however that the right to do so is one of the most fundamental rights anyone in a free society should have for me much of the world makes no sense but my feelings about what i am doing ring loud and clear to the inner ear and to a place where there is no self only calm love always wendy
``

### Readability

<u> Text should not be pre-processed before running the test </u>

#### Theory

##### Flesch score

`RE = 206,835 - (1,015 x ASL) - (84.6 x ASW)` 

** RE ** = Readability Ease 

** ASL ** = Average Sentence Length (ie, number of words divided by number of sentences) 

** ASW ** = Average number of syllables per word (ie, number of syllables divided by number of words) 

<u> The higher the RE, the lower the complexity of the text </u>. The expected output is between [0 - 100], but formatting errors can cause errors. These will be normalized to expected values ​​(ie 0-100)

* RE mutations can occur due to incorrect text formatting (eg missing punctuation, ...) *



##### Flesch-Kincaid level

`RL = 0.39 x (TW / TS) + 11.8 x (TSYL / TW) - 15.59`

** TW ** = Total Words

** TS ** = Total Sentences

** TSYL ** = Total Syllables

<u> The result corresponds to the US grade level. It is optimally between ** [0 - 12] **, and extreme values ​​range between ** [- 3,4 - 13 +] **. As with RE, the result depends on the correct formatting of the text. </u>



Performs text readability tests above the corpus, using the Flesch method and the Flesch-Kincaid method.

The Flesch method returns a readability score, which is a decimal number between 0 and 100.

The Flesch-Kincaid method returns a readability grade level, which is a decimal number between 0 and 10.

Call example:

`` python
#call
results = readability_test (".", "* .txt")

#iteration between results
for result in results:
    print "File Name" + result [0]
    print "Flesch score" + str (result [1])
    print "Flesch-Kincaid Grade" + str (result [2])
``

Example result:

``
File name. \ 1.txt
Flesch score 69.45625
Flesch-Kincaid grade 6.36638888889

File name. \ 2.txt
Flesch score 83.8535714286
Flesch-Kincaid grade 5.04142857143

File name. \ 3.txt
Flesch score 99.0157142857
Flesch-Kincaid grade 1.18761904762

File name. \ 4.txt
Flesch score 79.4342857143
Flesch-Kincaid grade 7.39682539683
``



Description of `readability_test` function:

Entrance: 

- `root: str` - The root directory for searching documents
- `file_pattern: string` - regex file selection pattern (eg" * "," \ *. txt ", ...)

Exit:

Array object generator (evaluation happens only when accessing the value - irrelevant to the end user)

`(file_path: str, flesch_readability_ease_score: num [0-100], flesch_kincaid_grade_level: num [0-10])`

### CSV Maker

Combine two input csv files into one output.
** The program looks for files on the path: **

./ml-database 

Application example:

`` python
    fileToJoin1 = "learning_set_elicitors.csv"
    fileToJoin2 = "learning_set_completers.csv"
    outputFile = "learning_set.csv"

    joinFiles (fileToJoin1, fileToJoin2, outputFile)
``

The above example would mean that we want to combine the learning_set_elicitors.csv and learning_set_completers.csv files on the path ./ml-database
(./ml-database/learning_set_elicitors.csv, ..) to the learning_set.csv output file.

filetoJoin1 and fileToJoin2 are input files. outputFile is the output file we want to generate.
joinFiles (input_dat1, input_dat2, output_dat) is the function call that performs the merge. 

import partsOfSpeech as pos
import readabilityTests as rt
from partsOfSpeech import downloadLexicons
from partsOfSpeech import readFiles
from partsOfSpeech import PartsOfSpeechTagger
from partsOfSpeech import PartsOfSpeechReader
import nltk
import csv




if __name__ == "__main__":
    #downloadLexicons()
    
    csv_attributes = ["Attribute", "Completers Mean (SD)", "Elicitors Mean (SD)"]
    #cvs_mean_pos = [[key , completer_mean, elicitor_mean], ...]
    cvs_mean_pos = []

       
    #### LEARNING SET
    ### COMPLETERS
    data = readFiles("./suicide-notes-database/completers-pp/", ".//post")
    pos = PartsOfSpeechTagger("./suicide-notes-database/parts_of_speech/")

    # multi threaded tagger
    pos.partsOfSpeechTaggingMultiprocessed(data, 6)

    
    # reader : statistics
    pos_reader = PartsOfSpeechReader(
        "./suicide-notes-database/parts_of_speech/",
        "./suicide-notes-database/parts_of_speech_statistics/"
        )
    pos_reader.partsOfSpeechStatistics( pos_reader.readAnalyzedData() )
    statistics_completers = pos_reader.getMedianStatistics()

    ### ELICITORS
    data = readFiles("./suicide-notes-database/elicitors-pp/", ".//post")
    pos = PartsOfSpeechTagger("./suicide-notes-database/parts_of_speech/")

    # multi threaded tagger
    pos.partsOfSpeechTaggingMultiprocessed(data, 6)

    # reader : statistics
    pos_reader = PartsOfSpeechReader(
        "./suicide-notes-database/parts_of_speech/",
        "./suicide-notes-database/parts_of_speech_statistics/"
        )
    pos_reader.partsOfSpeechStatistics( pos_reader.readAnalyzedData() )
    statistics_elicitors = pos_reader.getMedianStatistics()


    for key in statistics_elicitors:
        cvs_mean_pos.append([key, statistics_completers[key], statistics_elicitors[key]])
        print key, " : ", statistics_completers[key]



    with open("medians.csv", 'wb') as fs:
        wr = csv.writer(fs, quoting=csv.QUOTE_NONE) #, delimiter='|', quotechar='',escapechar='\\')
        wr.writerow(csv_attributes)
        for tag in cvs_mean_pos:
            wr.writerow(tag)

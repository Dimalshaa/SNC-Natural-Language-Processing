import partsOfSpeech as pos
import readabilityTests as rt
from partsOfSpeech import downloadLexicons
from partsOfSpeech import readFiles
from partsOfSpeech import PartsOfSpeechTagger
from partsOfSpeech import PartsOfSpeechReader
import nltk
import csv

def fleschMediana(path):
    results=rt.readibility_test(path, "*.txt")
    sumOfValuesFLESCH = 0
    sumOfValuesKINCAID = 0

    #iteracija med rezultati
    counter = 0
    for result in results:
        sumOfValuesFLESCH += float(result[1])
        sumOfValuesKINCAID += float(result[2])
        counter += 1


    meanFLESCH = sumOfValuesFLESCH / counter
    meanKINCAID = sumOfValuesKINCAID / counter

    return meanFLESCH, meanKINCAID


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
    
    ###Flesch-ova metoda in metoda Flesch-Kincaid -> COMPLETERS
    flesch_completers, kincaid_completers = fleschMediana("./suicide-notes-database/completers-pp/")

    ###Flesch-ova metoda in metoda Flesch-Kincaid -> ELICITORS
    flesch_elicitors, kincaid_elicitors = fleschMediana("./suicide-notes-database/elicitors-pp/")


    cvs_mean_pos.append(["Flesch score", flesch_completers, flesch_elicitors])
    cvs_mean_pos.append(["Flesch-Kincaid grade", kincaid_completers, kincaid_elicitors])

    for key in statistics_elicitors:
        cvs_mean_pos.append([key, statistics_completers[key], statistics_elicitors[key]])



    with open("medians.csv", 'wb') as fs:
        wr = csv.writer(fs, quoting=csv.QUOTE_NONE) #, delimiter='|', quotechar='',escapechar='\\')
        wr.writerow(csv_attributes)
        for tag in cvs_mean_pos:
            wr.writerow(tag)

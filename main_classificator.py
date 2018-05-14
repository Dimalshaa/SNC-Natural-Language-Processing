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

"""
saves CVS file of means for completers and elicitors
"""
def saveMeanStatisticsCSV(output_csv_filename, pos_completers_folder, pos_elicitors_folder, pos_folder_path, statistics_folder_path, 
    paragraph_tag_name, readibility_completers_folder, readibility_elicitors_folder):
    
    csv_attributes = ["Attribute", "Completers Mean (SD)", "Elicitors Mean (SD)"]
    #cvs_mean_pos = [[key , completer_mean, elicitor_mean], ...]
    cvs_mean_pos = []

    ### POS statistics
    pos = PartsOfSpeechTagger(pos_folder_path)
    pos_reader = PartsOfSpeechReader(
        pos_folder_path,
        statistics_folder_path
        )
  
    ### COMPLETERS
    data = readFiles(pos_completers_folder, paragraph_tag_name)
    pos.partsOfSpeechTaggingMultiprocessed(data, 6)
    pos_reader.partsOfSpeechStatistics( pos_reader.readAnalyzedData() )
    statistics_completers = pos_reader.getMedianStatistics()

    ### ELICITORS
    data = readFiles(pos_elicitors_folder, paragraph_tag_name)
    pos.partsOfSpeechTaggingMultiprocessed(data, 6)
    pos_reader.partsOfSpeechStatistics( pos_reader.readAnalyzedData() )
    statistics_elicitors = pos_reader.getMedianStatistics()
    
    ### Flesch-ova metoda in metoda Flesch-Kincaid -> COMPLETERS
    flesch_completers, kincaid_completers = fleschMediana(readibility_completers_folder)

    ### Flesch-ova metoda in metoda Flesch-Kincaid -> ELICITORS
    flesch_elicitors, kincaid_elicitors = fleschMediana(readibility_elicitors_folder)

    cvs_mean_pos.append(["Flesch score", flesch_completers, flesch_elicitors])
    cvs_mean_pos.append(["Flesch-Kincaid grade", kincaid_completers, kincaid_elicitors])

    for key in statistics_elicitors:
        cvs_mean_pos.append([key, statistics_completers[key], statistics_elicitors[key]])

    with open(output_csv_filename, 'wb') as fs:
        wr = csv.writer(fs, quoting=csv.QUOTE_NONE) #, delimiter='|', quotechar='',escapechar='\\')
        wr.writerow(csv_attributes)
        for tag in cvs_mean_pos:
            wr.writerow(tag)



if __name__ == "__main__":
    #downloadLexicons()
    
    saveMeanStatisticsCSV("means.csv", "./suicide-notes-database/completers-pp/", "./suicide-notes-database/elicitors-pp/",
        "./suicide-notes-database/parts_of_speech/", "./suicide-notes-database/parts_of_speech_statistics/", ".//post",
        "./suicide-notes-database/completers/", "./suicide-notes-database/elicitors/")


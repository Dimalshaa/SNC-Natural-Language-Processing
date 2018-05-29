import partsOfSpeech as pos
import readabilityTests as rt
import featureSelection as fss
from partsOfSpeech import downloadLexicons
from partsOfSpeech import readFiles
from partsOfSpeech import PartsOfSpeechTagger
from partsOfSpeech import PartsOfSpeechReader
from partsOfSpeech import getFileByFileStatistics
import nltk
import csv
from emotionAnalysis import getEmotionsForCorpus
from array import array



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

def averageStat(path):
    stats = fss.splosnaStatistika(path)

    numWords = 0
    numSigns = 0
    numChars = 0
    numSentences = 0

    counter = len(stats)

    for i in range(0, len(stats)):
        stat = stats[i].split("|")

        numWords += float(stat[1])
        numSigns += float(stat[2])
        numChars += float(stat[3])
        numSentences += float(stat[4])

    meanWords = float(numWords / counter)
    meanSigns = float(numSigns / counter)
    meanChars = float(numChars / counter)
    meanSentences = float(numSentences / counter)

    return meanWords, meanSigns, meanChars, meanSentences


"""
saves CVS file of indiviual letter attribute values, for completers and elicitors
"""
def singleFileStatisticsCSV(completers_folder_pp, elicitors_folder_pp, statistics_folder, pos_folder, out_completers_filename,
                            out_elictors_filename, regular_completers_folder, regular_elicitors_folder, unique_emotions):

    full_data_completers = []
    full_data_elicitors = []

    stats_completers = fss.splosnaStatistika(regular_completers_folder)
    stats_elicitors = fss.splosnaStatistika(regular_elicitors_folder)


    stat = stats_completers[len(stats_completers)-1].split("|")

    #print(stats_completers[len(stats_completers)-1])     
    #print(stat)
    paragraph_tag_name = ".//post"
    full_data_completers = getFileByFileStatistics(completers_folder_pp, pos_folder, statistics_folder, paragraph_tag_name)
    full_data_elicitors = getFileByFileStatistics(elicitors_folder_pp, pos_folder, statistics_folder, paragraph_tag_name)

    num_completers = len(full_data_completers)
    num_elicitors = len(full_data_elicitors)

    csv_out_completers = []
    csv_out_elicitors = []
    csv_attributes = []

    results=rt.readibility_test(regular_completers_folder, "*.txt")
    results_2=rt.readibility_test(regular_elicitors_folder, "*.txt")

    res_flesch_completers = []
    res_kincaid_completers = []  

    res_flesch_elicitors = []
    res_kincaid_elicitors = [] 

    res_emotio_completers = []
    res_emotio_elicitors = []

    csv_attributes.append("Ime_dat")

    for result in results:
        res_flesch_completers.append(result[1])
        res_kincaid_completers.append(result[2])

    for result in results_2:
        res_flesch_elicitors.append(result[1])
        res_kincaid_elicitors.append(result[2])   


    arr = array('f', [0]*len(unique_emotions))
    for result in getEmotionsForCorpus('./suicide-notes-database/completers-pp/', '*.txt'):
        for emo in result[1]:
            arr_index = int(unique_emotions.index(str(emo[0]))) 
            arr[arr_index] = float(emo[1])

        res_emotio_completers.append(arr)
        arr = array('f', [0]*len(unique_emotions))


    for i in range(0, num_completers):
        output = []
        path = full_data_completers[i][0][0]
        words = path.split("/")
        filename = words[-1]                # -1 = last element
        
        output.append(filename)
        
        dictionary = full_data_completers[i][0][1][0]
        for key in dictionary:
            if i == 0:
                csv_attributes.append(key)
                
            output.append(dictionary[key]) 
   
        if i == 0:
            csv_attributes.append("Flesch")
            csv_attributes.append("Kincaid")
            csv_attributes.append("Num_words")
            csv_attributes.append("Num_signs")
            csv_attributes.append("Num_chars")
            csv_attributes.append("Num_sentence")

        output.append(str(res_flesch_completers[i]))
        output.append(str(res_kincaid_completers[i]))

        stat = stats_completers[i].split("|")

        for j in range(1, (len(stat)-1)):
            output.append(stat[j])
        

        values_arr = res_emotio_completers[i]
        for k in range(0, len(values_arr)):
            output.append(values_arr[k])

        csv_out_completers.append(output)


    for emotion in unique_emotions:
        csv_attributes.append(emotion) 

    #print(csv_attributes)    
    #print(output)
    with open(out_completers_filename, 'wb') as fs:
        wr = csv.writer(fs, quoting=csv.QUOTE_NONE)
        wr.writerow(csv_attributes)
        for tag in csv_out_completers:
           wr.writerow(tag)


    ################      ELICITORS       ##########################      
     
     
    arr_2 = array('f', [0]*len(unique_emotions))
    for result in getEmotionsForCorpus('./suicide-notes-database/elicitors-pp/', '*.txt'):
        for emo in result[1]:
            arr_index = int(unique_emotions.index(str(emo[0]))) 
            arr_2[arr_index] = float(emo[1])

        res_emotio_elicitors.append(arr_2)
        arr_2 = array('f', [0]*len(unique_emotions))     
        

    for i in range(0, num_elicitors):
        output_2 = []
        path_2 = full_data_elicitors[i][0][0]
        words_2 = path_2.split("/")
        filename_2 = words_2[-1]                # -1 = last element
        
        output_2.append(filename_2)
        
        dictionary_2 = full_data_elicitors[i][0][1][0]
        for key in dictionary_2:
            output_2.append(dictionary_2[key])

        output_2.append(str(res_flesch_elicitors[i]))
        output_2.append(str(res_kincaid_elicitors[i]))

        stat_2 = stats_elicitors[i].split("|")

        for j in range(1, (len(stat_2)-1)):
            output_2.append(stat_2[j])


        values_arr_2 = res_emotio_elicitors[i]
        for k in range(0, len(values_arr_2)):
            output_2.append(values_arr_2[k])    

        csv_out_elicitors.append(output_2)


    with open(out_elictors_filename, 'wb') as fs:
        wr = csv.writer(fs, quoting=csv.QUOTE_NONE)
        wr.writerow(csv_attributes)
        for tag in csv_out_elicitors:
           wr.writerow(tag)        
    

"""
saves CVS file of means for completers and elicitors
"""
def saveMeanStatisticsCSV(output_csv_filename, pos_completers_folder, pos_elicitors_folder, pos_folder_path, statistics_folder_path, 
    paragraph_tag_name, readibility_completers_folder, readibility_elicitors_folder, unique_emotions):
    
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

    ### EMOTIONS COMPLETERS
    arr = array('f', [0]*len(unique_emotions))
    for result in getEmotionsForCorpus('./suicide-notes-database/completers-pp/', '*.txt'):
        for emo in result[1]:
            arr_index = int(unique_emotions.index(str(emo[0]))) 
            arr[arr_index] += float(emo[1])

    ### EMOTIONS ELICITORS
    arr_2 = array('f', [0]*len(unique_emotions))
    for result in getEmotionsForCorpus('./suicide-notes-database/elicitors-pp/', '*.txt'):
        for emo in result[1]:
            arr_index = int(unique_emotions.index(str(emo[0]))) 
            arr_2[arr_index] += float(emo[1])


    cvs_mean_pos.append(["Flesch", flesch_completers, flesch_elicitors])
    cvs_mean_pos.append(["Kincaid", kincaid_completers, kincaid_elicitors])

    for key in statistics_elicitors:
        cvs_mean_pos.append([key, statistics_completers[key], statistics_elicitors[key]])

    meanWordsCompleters, meanSignsCompleters, meanCharsCompleters, meanSentencesCompleters = averageStat(readibility_completers_folder)
    meanWordsElicitors, meanSignsElicitors, meanCharsElicitors, meanSentencesElicitors = averageStat(readibility_elicitors_folder)

    cvs_mean_pos.append(["Num_words", meanWordsCompleters, meanWordsElicitors])
    cvs_mean_pos.append(["Num_signs", meanSignsCompleters, meanSignsElicitors])
    cvs_mean_pos.append(["Num_chars", meanCharsCompleters, meanCharsElicitors])
    cvs_mean_pos.append(["Num_sentence", meanSentencesCompleters, meanSentencesElicitors])

    ### normalization emotions
    len_uniqe = len(unique_emotions)
    for i in range(0, len_uniqe):
        arr[i] = arr[i]/len_uniqe
        arr_2[i] = arr_2[i]/len_uniqe
        cvs_mean_pos.append([unique_emotions[i], arr[i], arr_2[i]])    

    with open(output_csv_filename, 'wb') as fs:
        wr = csv.writer(fs, quoting=csv.QUOTE_NONE) #, delimiter='|', quotechar='',escapechar='\\')
        wr.writerow(csv_attributes)
        for tag in cvs_mean_pos:
            wr.writerow(tag)
    
def createStacionarDictionary(allEmotions):
    new_list = list(set(allEmotions))

    return new_list

def getAllEmotions(elicitors, completers):
    tmp_list = []
    
    for result in getEmotionsForCorpus(elicitors,'*.txt'):
        for emo in result[1]:
            print emo[0]
            print emo[1]
        tmp_list.extend(result[2])

    for res in getEmotionsForCorpus(completers, '*.txt'):
        print(res[0])
        for emo in res[1]:
            print emo[0]
            print emo[1]
        tmp_list.extend(res[2])
        print("----------------")

    return tmp_list    

if __name__ == "__main__":
    #downloadLexicons()

    # directories path names
    
    learning_completers = "./suicide-notes-database/completers/"
    learning_elicitors = "./suicide-notes-database/elicitors/"
    learning_completers_pp = "./suicide-notes-database/completers-pp/"
    learning_elicitors_pp = "./suicide-notes-database/elicitors-pp/"

    uniqueEmotions = [u'ambiguous-hope', u'love', u'distress', u'earnestness', u'coolness', u'closeness', u'gladness', u'satisfaction', u'shame', u'comfortableness', u'fulfillment', u'anger', u'eagerness', u'liking', u'stir', u'hate', u'happiness', u'ambiguous-expectation', u'confidence', u'devotion', u'umbrage', u'thing', u'positive-concern', u'peace', u'indifference', u'favor', u'fury', u'stupefaction', u'tranquillity', u'easiness', u'tumult', u'covetousness', u'panic', u'shamefacedness', u'negative-fear', u'forlornness', u'negative-concern', u'compassion', u'confusion', u'horror', u'regard', u'fearlessness', u'depression', u'lost-sorrow', u'embarrassment', u'bang', u'reverence', u'humility', u'huffiness', u'fondness', u'nausea', u'elation', u'regret-sorrow', u'forgiveness', u'jitteriness', u'grief', u'benevolence', u'sadness', u'defeatism', u'calmness', u'triumph', u'misery', u'security', u'scare', u'affection']
    print(uniqueEmotions)

    """

    listEmotionsLearning = []
    listEmotionsLearning = getAllEmotions(learning_elicitors_pp, learning_completers_pp)

    listEmotionsTesters = []
    listEmotionsTesters = getAllEmotions(tester_elicitors_pp, tester_completers_pp)

    listAll = listEmotionsLearning + listEmotionsTesters
    uniqueEmotions = createStacionarDictionary(listAll)
    print(uniqueEmotions)
    """
     
    
    saveMeanStatisticsCSV("ml-database/means.csv", learning_completers_pp, learning_elicitors_pp,
        "./suicide-notes-database/parts_of_speech/", "./suicide-notes-database/parts_of_speech_statistics/", ".//post",
        learning_completers, learning_elicitors, uniqueEmotions)
    
    
    
    singleFileStatisticsCSV(learning_completers_pp, learning_elicitors_pp,
        "./suicide-notes-database/parts_of_speech_statistics/", "./suicide-notes-database/parts_of_speech/",
        "ml-database/learning_set_completers.csv", "ml-database/learning_set_elicitors.csv",
        learning_completers, learning_elicitors, uniqueEmotions)

    

    
    


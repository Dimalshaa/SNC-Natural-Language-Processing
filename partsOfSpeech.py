#1. Tokenization - prepares text for analysis like word checking, 
# ambiguity checking and disambiguation.
#2. Add speech tags.

import glob, os, os.path
import lxml.etree
import nltk 
from multiprocessing import Process, Manager, Value
import math
import json
import pickle
import codecs
import uuid
import ast

"""
outputs file contents as string
"""
def textFileParser(filename):
    data = []
    with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as text_file:
        data= text_file.read().replace('\n', '')
    return [data]

"""
outputs file contents as string
""" 
def xmlFileParser(filename, paragraph_tag_name) : 
    from lxml.etree import tostring
    from itertools import chain
    root = lxml.etree.parse(filename).getroot()
    buffer = root.findall(paragraph_tag_name)
    output = []
    for b in buffer:
        output.append(b.text.encode('utf8'))
    
    return output

"""
gets string "folder_path" and reads all files in a given directory
supports .xml and .txt files 
outputs an array of content from those files
"""
def readFiles(folder_path, paragraph_tag_name):
    filenames = os.listdir(folder_path)
    data = []

    for i in range(0, len(filenames)):
        filename, file_extension = os.path.splitext(filenames[i]) #gets file extension
        if file_extension == ".txt":
            data.append(textFileParser(folder_path + "\\" + filenames[i]))
        elif file_extension == ".xml":
            data.append(xmlFileParser(folder_path + "\\" + filenames[i], paragraph_tag_name))
        else:
            print("File ", filenames[i], " uses unsupported file format!")

    """ for i in data:
        print(len(i)) """

    return data
    
"""
similar to readFiles, only this one work for a single file
outputs data AND filename
supports .xml and .txt files
"""
def readSingleFile(full_file_path, paragraph_tag_name):
    data = []

    filename, file_extension = os.path.splitext(full_file_path) #gets file extension
    if file_extension == ".txt":
       data.append([full_file_path, textFileParser(full_file_path)])
    elif file_extension == ".xml":
        data.append([full_file_path, xmlFileParser(full_file_path, paragraph_tag_name)])
    else:
        print("File ", full_file_path, " uses unsupported file format!")

    return data

"""
downloads all lexicons and other files, used by nltk
"""
def downloadLexicons(): 
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('brown')
    nltk.download('cmudict')
    
"""
deletes all files in a given directory, with selected file extension
"""
def deleteFilesInDirectory(path, file_extension):
    filelist = glob.glob(os.path.join(path, file_extension))
    for f in filelist:
        os.remove(f)
    print "[deleteFilesInDirectory] Deleted ", len(filelist), " files"

"""
returns parts of speech statistics for each specific file
parameters: preprocessed files folder path, PartsOfSpeechReader constructor params
"""
def getFileByFileStatistics(folder_path, pos_folder_path, statistics_folder_path, paragraph_tag_name):
    full_data_completers = []
    filenames = os.listdir(folder_path)
    for i in range(0, len(filenames)):
        full_data_completers.append(readSingleFile(folder_path + filenames[i], paragraph_tag_name))

    pos = PartsOfSpeechTagger(pos_folder_path)
    pos_reader = PartsOfSpeechReader(
        pos_folder_path,
        statistics_folder_path
    )
        
    for fd in full_data_completers:
        fd[0][1][0] = pos.partsOfSpeechTagging(fd[0][1][0])
        fd[0][1][0] = pos_reader.partsOfSpeechSingleFileStatistics(fd[0][1][0])

    return full_data_completers


class PartsOfSpeechTagger:
    def __init__(self, results_folder_path):
        self.results_folder_path = results_folder_path

    ### single thread method
    def partsOfSpeechTagging(self, data):
        tokenized = nltk.word_tokenize(data.decode('utf-8'))
        return nltk.pos_tag(tokenized)

    ### multi thread methods
    def tagger(self, data, processID):
        print("[PartsOfSpeechTagger] Process initialized")
        for paragraph in data:
            tokenized = nltk.word_tokenize(paragraph.decode('utf-8'))
            json_string = json.dumps(nltk.pos_tag(tokenized), ensure_ascii=False) 
            filename = self.results_folder_path + str(uuid.uuid1()) +".json"
            with open(filename, 'w') as outfile:
                json.dump(json_string, outfile) 
        
        return True

    def partsOfSpeechTaggingMultiprocessed(self, data, number_of_processes):
        deleteFilesInDirectory(self.results_folder_path, "*.json")

        data_count = 0
        for corpus in data:
            for paragraph in corpus:
                data_count += 1

        data_per_process = math.ceil(data_count / float(number_of_processes))
        process_clusters = [] # array of data split into chunks, so we can divide them among multiple threads
        temp_list = []
        counter = 0

        # splits data into process_clusters
        for corpus_index in range(0, len(data)):
            for paragraph_index in range(0, len(data[corpus_index])):
                temp_list.append(data[corpus_index][paragraph_index])
                if(len(temp_list) >= data_per_process):
                    process_clusters.append(temp_list)
                    temp_list = []
        if len(temp_list) != 0:
            process_clusters.append(temp_list)

        processes = []  # processes queue
        for i in range(0, number_of_processes):   
            if(i >= len(process_clusters)):
                break
            processes.append(Process(target = self.tagger, args = (process_clusters[i], i, )))
            processes[i].start()
            
        for k in range(0, len(processes)):
            processes[k].join() 


class PartsOfSpeechReader():
    def __init__(self, pos_folder_path, statistics_folder_path):
        self.pos_folder_path = pos_folder_path
        self.statistics_folder_path = statistics_folder_path

    # get data as an array
    def readAnalyzedData(self):
        filenames = os.listdir(self.pos_folder_path)
        output = []
        for i in range(0, len(filenames)):
            with open(self.pos_folder_path + filenames[i]) as json_data_encrypted:
                note = json.load(json_data_encrypted)
                output.append(note)
        return output
 
    # save to file
    def save_obj(self, obj):
        with open(self.statistics_folder_path + str(uuid.uuid1()) + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    # save dictionaries of selected notes into a statistics files folder
    def partsOfSpeechStatistics(self, pos_data):
        deleteFilesInDirectory(self.statistics_folder_path, "*.pkl")

        notes = pos_data
        for note in notes:
            note = ast.literal_eval(note)
            # normalize dictionary
            dict = {"CC" : 0, "DT" : 0, "EX" : 0, "IN" : 0,	
                "JJ" : 0, "JJS" : 0, "MD" : 0, "NN" : 0,	
                "NNS" : 0, "PDT" : 0, "PRP" : 0, "PRP$" : 0, 
                "RB" : 0, "TO" : 0,	"VB" : 0, "VBD" : 0, 
                "VBG" : 0, "VBN" : 0, "VBP" : 0, "VBZ" : 0, 
                "WDT" : 0
                }
            for tagged_word in note:
                if tagged_word[1] in dict:
                    dict[tagged_word[1]] += 1.0

            self.save_obj(dict)

            """
            for tag in dict:
                print tag, ' : ', dict[tag]
            """
        return

    def partsOfSpeechSingleFileStatistics(self, note):
        # normalize dictionary
        dict = {"CC" : 0, "DT" : 0, "EX" : 0, "IN" : 0,	
                "JJ" : 0, "JJS" : 0, "MD" : 0, "NN" : 0,	
                "NNS" : 0, "PDT" : 0, "PRP" : 0, "PRP$" : 0, 
                "RB" : 0, "TO" : 0,	"VB" : 0, "VBD" : 0, 
                "VBG" : 0, "VBN" : 0, "VBP" : 0, "VBZ" : 0, 
                "WDT" : 0
                }

        for tagged_word in note:
            if tagged_word[1] in dict:
                dict[tagged_word[1]] += 1.0

        return dict

    # load from file
    def load_obj(self):
        filenames = os.listdir(self.statistics_folder_path)
        output = []
        for i in range(0, len(filenames)):
            with open(self.statistics_folder_path + filenames[i], 'rb') as f:
                output.append(pickle.load(f))
        return output

    # gets median values
    def getMedianStatistics(self):
        dictionaries = self.load_obj()
        results = {}
        for d in dictionaries:
            for key in d:
                if key in results:
                    results[key] += d[key]
                else:
                    results[key] = d[key]
        
        for key in results:
            print key, " : ", results[key]
            results[key] /= len(dictionaries)
            print key, " : ", results[key]
        
        return results



if __name__ == "__main__":
    #downloadLexicons()

    """
    full_data_completers = []
    folder_path = "./suicide-notes-database/completers-pp/"
    pos_folder_path = "./suicide-notes-database/parts_of_speech/"
    statistics_folder_path = "./suicide-notes-database/parts_of_speech_statistics/"
    paragraph_tag_name = ".//post"
    full_data_completers = getFileByFileStatistics(folder_path, pos_folder_path, statistics_folder_path, paragraph_tag_name)
    """


    """
    ### Tako dobis slovar! ;TODO: delete this comment + line: 
    print full_data_completers[1][0][1][0]

    """

    """
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

    """

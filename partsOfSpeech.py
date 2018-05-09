#1. Tokenization - prepares text for analysis like word checking, 
# ambiguity checking and disambiguation.
#2. Add speech tags.

import os
import lxml.etree
import nltk 
from multiprocessing import Process, Manager, Value
import math
import json

"""
outputs file contents as string
"""
def textFileParser(filename):
    data = []
    with open(filename, 'r') as text_file:
        data=text_file.read().replace('\n', '')
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
downloads all lexicons and other files, used by nltk
"""
def downloadLexicons(): 
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

class PartsOfSpeechTagger:
    def __init__(self, results_folder_path):
        self.data_tagged = []
        self.results_folder_path = results_folder_path

    ### single thread method
    def partsOfSpeechTagging(self, data):
        for corpus in data:
            for paragraph in corpus:
                tokenized = nltk.word_tokenize(paragraph.decode('utf-8'))
                self.data_tagged.append(nltk.pos_tag(tokenized))

    ### multi thread methods
    def tagger(self, data, processID):
        print("[PartsOfSpeechTagger] Process initialized")
        output = []
        for paragraph in data:
            tokenized = nltk.word_tokenize(paragraph.decode('utf-8'))
            output.append(nltk.pos_tag(tokenized))
            
        json_string = json.dumps(output, ensure_ascii=False) 
        filename = self.results_folder_path + "test" + str(processID)  
        with open(filename, 'w') as outfile:
            json.dump(json_string, outfile) 

        return True

    def partsOfSpeechTaggingMultiprocessed(self, data, number_of_processes):
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



if __name__ == "__main__":
   # downloadLexicons()
    data = readFiles("./suicide-notes-database/trash_files", ".//post")
    
    pos = PartsOfSpeechTagger("./suicide-notes-database/results/")
    #pos.partsOfSpeechTagging(data)
    #print(len(pos.data_tagged))

    #multithreaded
    pos.partsOfSpeechTaggingMultiprocessed(data, 6)
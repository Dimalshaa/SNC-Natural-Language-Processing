import pandas as pd

def joinFiles(fileName1, fileName2, outputFilename):

    path1 = "./ml-database/" + fileName1
    path2 = "./ml-database/" + fileName2
    outputPath = "./ml-database/" + outputFilename

    a = pd.read_csv(path1)
    b = pd.read_csv(path2)

    df = pd.DataFrame(a)
    rowsFile1 = len(df.index)
    listFile1 = ["False"] * rowsFile1

    df2 = pd.DataFrame(b)
    rowsFile2 = len(df2.index)
    listFile2 = ["True"] * rowsFile2

    df['Authentic'] = listFile1
    df2['Authentic'] = listFile2
    new = a.merge(b, how='outer')

    #print(new)
    new.to_csv(outputPath, index=False)
    return 0

if __name__ == "__main__":
    fileToJoin1 = "learning_set_elicitors.csv"
    fileToJoin2 = "learning_set_completers.csv"
    outputFile = "learning_set.csv"

    joinFiles(fileToJoin1, fileToJoin2 , outputFile)

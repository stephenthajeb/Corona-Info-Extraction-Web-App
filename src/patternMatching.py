import re
from nltk import tokenize
from collections import defaultdict
import sys
sys.path.append("../test")

def readFile(filename):
    f = open(filename,"r")
    text = f.read()
    return text

#================================================Using BM Algorithm==================================================================
#Preprocessing
def buildLast(pattern):
  last = [-1 for i in range(128)]#Initalize all char
  for i in range(len(pattern)):#Revalue char that is in pattern
    last[ord(pattern[i])] = i;
  return last

#Return the first idx to found pattern, idx starts from 0, return -1 if not found
def bmMatch(casePattern,caseText):
    pattern = casePattern.lower()
    text = caseText.lower()  
    patternLength = len(pattern)
    textLength = len(text)
    table = buildLast(pattern)
    if (patternLength > textLength):
        return -1
    for i in range(textLength-patternLength+1):
        numOfSkips = 0
        for j in range(patternLength-1,-1,-1):
            if (pattern[j] != text[i+j]):
                if text[i+j] in table:
                    numOfSkips = table[text[i+j]]
                    break
                else:
                    numOfSkips = patternLength
                    break
        if (numOfSkips==0): #pattern is found
            return i
    return -1


#================================================Using KMP Algorithm==================================================================
#Preprocessing
def borderFunction (pattern):
    length = len(pattern)
    #Initialize the border table 
    b = [0 for i in range(length)]
    lps = 0 #variable to store previous longest prefix that is also suffix
    i = 1  # b[0] is always 0, start calculating from b[1]
    while (i < length):
        if (pattern[i] == pattern[lps]):
            lps+=1 #updating lps
            b[i] = lps
            i+=1
        else:
            if (lps!=0):
                lps = b[lps-1] #shorten the lps, since the current lps is not valid
            else:
                b[i] = 0
                i +=1
    return b    

#return the first idx in text where pattern match subtext, idx start from 0
def kmpMatch(casePattern,caseText):
    pattern = casePattern.lower()
    text = caseText.lower()  
    patternLength = len(pattern)
    textLength = len(text)
    b = borderFunction(pattern)
    i = 0
    j = 0
    while (i < textLength):
        if (pattern[j] == text[i]):
            if (j == patternLength-1):
                return i-patternLength+1
            i +=1 # move the next character for both text and pattern
            j +=1 
        elif (j > 0):
            j = b[j-1] #move back the patten to left according to border function
        else:
            i +=1
    return -1
# print(kmpMatch("abc","abaabaabbAbc"))
    

#=========================================================== Using Regex =========================================================================
# #Searching for the keyword and return the last occurance matching index
def regexMatching(pattern,sentence): 
    #Index version
    expression = re.compile(rf"{pattern}",re.IGNORECASE)
    # matchIdx = []
    for match in expression.finditer(sentence):
        return match.span()[0]
    return -1

#=========================================================== Extracting ===================================================================
# #Extract information about the number of people that are involve or related to a certain topic or keyword
def extractNumeric(sentence):
    expression = re.compile(r"(?:^(?:\d+(?:\.\d+)*)(?:\,\d+)?(?:[\%]| ratus| ribu| juta| milyar| hundreds?| thousands?| millions?)? )|(?:\d{1,3}(?:\.\d+)*)(?:\,\d+)?(?:[\%]| ratus| ribu| juta| milyar| hundreds?| thousands?| millions?)?[\. ,]",re.IGNORECASE)
    matchIdx = []
    for match in expression.finditer(sentence):
        matchIdx.append(match.span())
    return matchIdx


# #Extract date information
def extractDate(sentence):
    expression = re.compile(r"(?:Sen(?:in)?|Sel(?:asa)?|Rabu?|Kam(?:is)?|Jum(?:at)?|Sab(?:tu)?|Minggu|Sun(?:day)?|Mon(?:day)?|Tue(?:sday)|Wed(?:nesday)?|Thur(?:sday)|Fri(?:day)?|Sat(?:urday)?)?(?:, | \()?(?:(?:[\d]{1,2}[\/-][\d]{1,2}[\/-][\d]{4})|(?:\d{1,2}(?:-\d{1,2})? (?:Jan(?:nuari)?|Feb(?:ruari)?|Mar(?:et)?|Apr(?:il)?|Mei|Juni?|Juli?|Agus(?:tus)?|Ags|Sept(?:ember)?|Sep|Okt(?:ober)?|Nov(?:ember)?|Des(?:ember)?) \d{4})|(?: yang lalu| lalu| kemarin))\)?",re.IGNORECASE)
    matchIdx = []
    for match in expression.finditer(sentence):
        matchIdx.append(match.span())
    return matchIdx

#Function to return the closest numeric or date data to a keyword
def closestToKeyword (firstIdx,wantedData,pattern):
    distance = []
    for position in wantedData:
        if (wantedData == []):
            return []
        if position[0] < firstIdx:
            distance.append(abs(position[1]-firstIdx))
        else:
            distance.append(abs(position[0]-(len(pattern)-1+firstIdx)))
    return (wantedData[distance.index(min(distance))])

#Extract based on algorithm
def foundIdx(pattern,sentence,algo):
    idx = -1
    if(algo == "KMP"):
        idx = kmpMatch(pattern,sentence)
    elif (algo=="BM"):
        idx = bmMatch(pattern,sentence)
    else:
        idx = regexMatching(pattern,sentence)
    return idx

#Extrac by input multiple files in the test folder
def extractInfoFromNews(files,pattern,algo):
    output = []
    for single_file in files :
        news = readFile("../test/"+single_file)
        sentences = tokenize.sent_tokenize(news)
        foundNewsDate = 0
        for sentence in sentences:
            keyword = foundIdx(pattern,sentence,algo)
            if (foundNewsDate == 0):
                news_date = extractDate(sentence)
                if (news_date!=[]):
                    news_date = sentence[news_date[0][0]:news_date[0][1]]
                    foundNewsDate =1
            print(keyword)
            if (keyword != -1):    
                # print("Keyword : ",end="")
                # print(keyword)
                date = extractDate(sentence)
                numeric = extractNumeric(sentence)
                # print("Ini kalimat :",end="")
                # print(sentence) 
                if (date == [] and foundNewsDate==1):#Asumsi semua artikel pasti ada newsDate
                    date = news_date     
                else:
                    dateRange = closestToKeyword(keyword,date,pattern)
                    date = sentence[dateRange[0]:dateRange[1]]
                if (numeric != []):
                    numericRange = closestToKeyword(keyword,numeric,pattern)
                    numeric = sentence[numericRange[0]:numericRange[1]]   
                if (numeric == []):
                    numeric = "Tidak ditemukan"
                print("Ini tanggal :",end="")
                print(date)
                print("Ini jumlah :",end="")
                print(numeric)
                subSentence = re.split(pattern,sentence,flags=re.IGNORECASE)
                # print(subSentence)
                output.append((date,numeric,subSentence,single_file))
    return output
import json, requests, urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter 

allKural = []
df = pd.DataFrame()

for i in range(0,1330):
    print(i)
    text = ""
    html = urllib.request.urlopen("http://www.gokulnath.com/kural/"+str(i+1)).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("   "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    #print(text)
    list1 = []
    list1 = text.strip().split("\n")
    
    kural = {}
      
    kural['tamilExp'] = list1[(list1.index('சாலமன் பாப்பையா உரை:'))+1]
    kural['tamilKural'] = list1[25]
    
    kural['englishkural'] = list1[(list1.index('Transliteration'))-3]
    kural['englishExp'] = list1[(list1.index('Transliteration'))-1]
    kural['englishTransliteration'] = list1[(list1.index('Transliteration'))+1]
    
    kural['paalNo'] = list1[(list1.index('பால்/Section/Paal'))+1]
    kural['paal'] = list1[(list1.index('பால்/Section/Paal'))+2]
    kural['adhigaramNo'] = list1[(list1.index('அதிகாரம்/Chapter/Adhigaram'))+1]
    kural['adhigaram'] = list1[(list1.index('அதிகாரம்/Chapter/Adhigaram'))+2]   
    allKural.append(kural)

df1 = pd.DataFrame(allKural)
print(df1)

#count the words
kurals = df1['tamilKural']
k1 = []
for i in kurals:
    k1.append(i.split())
kuralwords = [item for sublist in k1 for item in sublist]  #flatten the list of lists
kuralWordCounts = Counter(kuralwords)

#write the list of tamil words to a csv
outfile="tamilwords.csv"
out=open(outfile,"w",encoding="UTF-16")
for i in kuralwords:
    out.write(i+"\n")
out.close()

#translated english kurals
enKurals = df1['englishkural']
enk1 = []
for i in enKurals:
    enk1.append(i.split())
enkuralwords = [item for sublist in enk1 for item in sublist]
enkuralWordCounts = Counter(enkuralwords)

import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
filtered_words = [word for word in enkuralwords if word not in stopwords.words('english')]

#write the list of english words to a csv
outfile="englishwords.csv"
out=open(outfile,"w",encoding="UTF-16")
for i in filtered_words:
    out.write(i+"\n")
out.close()

#paste the words from the csv file in a word cloud generator like http://www.wordclouds.com/
#வாழ்க தமிழ் வளர்க தமிழ்

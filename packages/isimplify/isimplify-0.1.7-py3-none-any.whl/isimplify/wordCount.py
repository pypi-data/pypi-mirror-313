from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from collections import Counter
# Download stopwords if not already done
nltk.download('stopwords')
nltk.download('punkt')

custom_words_to_remove=["and","that"]
def removeStopWords(text):
    #text=  "This is an example sentence, demonstrating stop word removal."
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    filtered_words = [word for word in filtered_words if word.isalnum()]
    return filtered_words
    

def countWordFrequency(content):
    count = Counter(content)
    return count
def removeCustomwords(words):
      words = set(words)
      filtered_words = [word for word in words if word not in custom_words_to_remove]
      return filtered_words




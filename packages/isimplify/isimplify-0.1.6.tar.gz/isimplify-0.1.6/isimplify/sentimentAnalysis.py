from transformers import pipeline

def sentimentAnalysis(text):
    model_name="distilbert-base-uncased-finetuned-sst-2-english"
    print("------sentiment alalysis on ------")
    print(text)
    sentiment_analysis = pipeline("sentiment-analysis",model=model_name)
    result = sentiment_analysis(text[:512])[0]
    print("sentiment:--",result)
    return result 



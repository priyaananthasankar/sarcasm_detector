Polarity Classifier for Sarcasm Detection

A Polarity Classifier which will determine the contextual or situational polarity of a sentence and classify it accordingly.

Installation Instructions: (Write down any required installation instructions if any)

1. Install ntlk:
    sudo pip3 install -U nltk

2. Install TextBlob: (Sentiment Analysis)
    pip install -U textblob

3. Download nltk corpus called "opinion_lexicon" which is Liu's positive/negative words lexicon
    nltk.download("opinion_lexicon")

4. Download nltk Part of Speech Tagger
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_treebank_pos_tagger')



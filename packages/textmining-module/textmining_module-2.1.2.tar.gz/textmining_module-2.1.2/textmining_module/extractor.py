import pandas as pd
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from yake import KeywordExtractor
from collections import Counter
import re

def extract_keywords_to_dataframe(data, text_column, method='yake', n=3, stopword_language='english'):
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    spacy_nlp = spacy.load('en_core_web_sm')  # Make sure you have downloaded this model

    def extract_keywords(text):
        if not text or text.isspace():
            return []

        if method == 'frequency':
            words = re.findall(r'\w+', text.lower())
            stop_words = set(nltk.corpus.stopwords.words(stopword_language))
            filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
            most_common = [word for word, freq in Counter(filtered_words).most_common(n)]
            return most_common

        elif method == 'yake':
            kw_extractor = KeywordExtractor(lan=stopword_language, n=n)
            extracted_keywords = kw_extractor.extract_keywords(text)
            return [kw[0] for kw in extracted_keywords][:n]

        elif method == 'tf-idf':
            vectorizer = TfidfVectorizer(stop_words=stopword_language)
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_array = vectorizer.get_feature_names_out()
            tfidf_sorting = tfidf_matrix.toarray().flatten().argsort()[::-1]
            return [feature_array[i] for i in tfidf_sorting][:n]

        elif method == 'pos':
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            selected_words = [word for word, tag in pos_tags if tag.startswith('NN')]  # Nouns
            return selected_words[:n]

        elif method == 'ner':
            doc = spacy_nlp(text)
            return [ent.text for ent in doc.ents][:n]

        else:
            raise ValueError("Invalid method. Choose from 'frequency', 'yake', 'tf-idf', 'pos', or 'ner'.")

    # Apply keyword extraction to each row in the DataFrame
    data['Keywords'] = data[text_column].apply(lambda text: extract_keywords(text))
    return data

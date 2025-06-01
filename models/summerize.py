import math
import re
import nltk
from nltk.stem import WordNetLemmatizer
import spacy

# Download if not already downloaded
nltk.download('wordnet')

# Initialize spaCy and lemmatizer
nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()

def summarize_text(text: str) -> str:
    # Clean and process text with spaCy
    doc = nlp(text)
    sentences = list(doc.sents)
    total_sentences = len(sentences)

    stop_words = nlp.Defaults.stop_words

    # Create frequency matrix
    freq_matrix = {}
    for sent in sentences:
        freq_table = {}
        words = [token.text.lower() for token in sent if token.text.isalnum()]
        for word in words:
            word = lemmatizer.lemmatize(word)
            if word not in stop_words:
                freq_table[word] = freq_table.get(word, 0) + 1
        freq_matrix[sent[:15]] = freq_table

    # Term Frequency (TF)
    tf_matrix = {}
    for sent, freq_table in freq_matrix.items():
        tf_table = {}
        total_words = len(freq_table)
        for word, count in freq_table.items():
            tf_table[word] = count / total_words
        tf_matrix[sent] = tf_table

    # Sentence count per word
    word_in_sent_count = {}
    for freq_table in freq_matrix.values():
        for word in freq_table:
            word_in_sent_count[word] = word_in_sent_count.get(word, 0) + 1

    # Inverse Document Frequency (IDF)
    idf_matrix = {}
    for sent, freq_table in freq_matrix.items():
        idf_table = {}
        for word in freq_table:
            idf_table[word] = math.log10(total_sentences / float(word_in_sent_count[word]))
        idf_matrix[sent] = idf_table

    # TF-IDF Matrix
    tf_idf_matrix = {}
    for sent in tf_matrix:
        tf_idf_table = {}
        for word in tf_matrix[sent]:
            tf_idf_table[word] = tf_matrix[sent][word] * idf_matrix[sent].get(word, 0.0)
        tf_idf_matrix[sent] = tf_idf_table

    # Sentence scoring
    sentence_scores = {}
    for sent, tfidf_table in tf_idf_matrix.items():
        total_score = sum(tfidf_table.values())
        count = len(tfidf_table)
        if count != 0:
            sentence_scores[sent] = total_score / count

    # Calculate average score
    avg_score = sum(sentence_scores.values()) / len(sentence_scores)

    # Generate summary
    summary = ''
    for sent in sentences:
        if sentence_scores.get(sent[:15], 0) >= (1.3 * avg_score):
            summary += ' ' + sent.text

    return summary.strip()


text = """
Natural language processing (NLP) is a field of artificial intelligence that gives machines the ability to read, understand and derive meaning from human languages. It is a component of artificial intelligence (AI).
The evolution of NLP is shaped by advancements in machine learning and deep learning. Common NLP tasks include text classification, machine translation, sentiment analysis, and speech recognition.
NLP powers applications like chatbots, translation tools, and virtual assistants. It helps organizations make sense of unstructured text data, extract insights, and improve customer interactions.
"""

summary = summarize_text(text)
print("Summary:\n", summary)
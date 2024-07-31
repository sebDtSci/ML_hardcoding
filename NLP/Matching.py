import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "?", "(", ")", ""])

texte = str(input())
questions = [str(input()) for _ in range(5)]
answers = str(input())
answers = answers.split(';')
texte = texte.split('.')

def simple_tokenizer(text: str) -> list:
    return re.findall(r'\b\w+\b', text.lower())

def simple_lemmatizer(word):
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('s'):
        return word[:-1]
    return word

def cleaner(sentence: str) -> str:
    tokens = simple_tokenizer(sentence)
    lem = [simple_lemmatizer(word) for word in tokens if word not in stop_words]
    return " ".join(lem)

def vectorize_text(texts):
    return vectorizer.fit_transform(texts)

def find_best_matching_sentence(question, tfidf_matrix, sentences, sentence_vectors):
    question_words = cleaner(question).split()
    question_vectors = vectorizer.transform(question_words)
    scores = np.zeros(sentence_vectors.shape[0])

    for word_vector in question_vectors:
        word_scores = cosine_similarity(word_vector, sentence_vectors).flatten()
        scores += word_scores
    
    best_sentence_index = scores.argmax()
    return sentences[best_sentence_index]

def match_questions_to_answers(questions, textes, answers):
    textes_clean = [cleaner(sentence) for sentence in textes]
    questions_clean = [cleaner(question) for question in questions]
    answers_clean = [cleaner(answer) for answer in answers]

    sentence_vectors = vectorize_text(textes_clean)
    best_sentences = [find_best_matching_sentence(question, sentence_vectors, textes, sentence_vectors) for question in questions_clean]

    duplicate_indices = [idx for idx, val in enumerate(best_sentences) if best_sentences.count(val) > 1]
    for idx in duplicate_indices:
        segments = best_sentences[idx].split(',')
        segment_vectors = vectorize_text([cleaner(segment) for segment in segments])
        best_segment = find_best_matching_sentence(questions[idx], segment_vectors, segments, segment_vectors)
        best_sentences[idx] = best_segment

    results = {}
    for i, question in enumerate(questions):
        best_sentence = best_sentences[i]
        for answer in answers:
            if set(cleaner(answer).split()).issubset(set(cleaner(best_sentence).split())):
                results[question] = answer
                break

    return results

results = match_questions_to_answers(questions, texte, answers)

for question, answer in results.items():
    print(f"Question: {question}")
    print('-> ',answer)
    
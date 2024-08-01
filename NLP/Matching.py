import re

stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "?", "(", ")", ""])

texte = str(input())
questions = [str(input()) for _ in range(5)]
answers = str(input())
answers = answers.split(';')
texte = texte.split('.')

def simply(text: list, answers: list) -> list:
    return [sentence for sentence in text if any(answer in sentence for answer in answers)]

texte = simply(texte, answers)

def simple_tokenizer(text: str) -> list:
    return re.findall(r'\b\w+\b', text.lower())

def simple_lemmatizer(word: str) -> str:
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('s'):
        return word[:-1]
    return word

def cleaner(sentence: str) -> str:
    tokens = simple_tokenizer(sentence)
    lem = [simple_lemmatizer(word) for word in tokens if word not in stop_words]
    return " ".join(lem)

def calculate_scores(question_words: set, sentence: str) -> tuple:
    sentence_words = set(cleaner(sentence).split())
    match_count = sum(1 for word in question_words if word in sentence_words)
    complete_match = question_words.issubset(sentence_words)
    return (complete_match, match_count)

def match_questions_to_answers(questions: list, sentences: list, answers: list) -> dict:
    results = {}
    assigned_sentences = set()

    for i, question in enumerate(questions):
        question_words = set(cleaner(question).split())
        potential_matches = [
            (sentence, calculate_scores(question_words, sentence))
            for sentence in sentences
        ]

        potential_matches.sort(key=lambda x: (x[1][0], x[1][1]), reverse=True)
        
        for sentence, _ in potential_matches:
            if sentence not in assigned_sentences:
                assigned_sentences.add(sentence)
                for answer in answers:
                    answer_words = set(cleaner(answer).split())
                    sentence_words = set(cleaner(sentence).split())
                    if answer_words.issubset(sentence_words):
                        results[question] = answer
                        break
                break
    for i, question in enumerate(questions):
        if question not in results:
            results[question] = "No clear answer found"

    return results

results = match_questions_to_answers(questions, texte, answers)

for question, answer in results.items():
    print(f"Question: {question}")
    print('-> ',answer)
    
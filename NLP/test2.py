import re

stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", "hasn", "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "?", "(", ")", ""])

texte = str(input())
questions = [str(input()) for _ in range(5)]
answers = str(input())
answers = answers.split(';')
texte = texte.split('.')

def simply(text: list, answers: list) -> list[str]:
    return [sentence for sentence in text if any(answer in sentence for answer in answers)]

texte = simply(texte, answers)

def simple_tokenizer(text: str) -> list[str]:
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


def match_sentences(texte: list[str], questions: list[str]) -> list[tuple]:
    results = []
    sentences = []
    
    cleaned_texte = [cleaner(sentence) for sentence in texte]

    for question in questions:
        cleaned_question = cleaner(question)
        question_set = set(cleaned_question.split())
        best_score = 0
        best_sentence = ""
        
        for sentence in cleaned_texte:
            sentence_set = set(sentence.split())
            common_words = question_set.intersection(sentence_set)
            score = len(common_words) / len(question_set)
            
            if score > best_score:
                best_score = score
                best_sentence = sentence

        results.append((question, best_sentence, best_score))
        sentences.append(best_sentence)
        

    return results, sentences

# def get_answer(sentences: str, answers: list[str]) -> list[str]:
#     return [answer for answer in answers if any(cleaner(answer) in sentence for sentence in sentences)]

def get_answers_ordered_by_questions(results: list[tuple[str, str, float]], answers: list[str]) -> list[list[str]]:
    ordered_answers = []

    for question, sentence, _ in results:
        matching_answers = [answer for answer in answers if cleaner(answer) in cleaner(sentence)]
        if matching_answers not in ordered_answers:
            ordered_answers.append(matching_answers)

    return ordered_answers

results, sentences = match_sentences(texte, questions)

ordered_answers = get_answers_ordered_by_questions(results, answers)

for answer in ordered_answers:
    print(answer[0])
    
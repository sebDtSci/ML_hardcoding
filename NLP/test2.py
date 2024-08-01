import re

# Define stop words to be excluded during cleaning
stop_words = {'the', 'is', 'a', 'an', 'and', 'to', 'of', 'for', 'in', 'which', 'on', 'as'}

# Input text, questions, and answers
texte = "The kangaroo is a marsupial from the family Macropodidae (macropods, meaning 'large foot'). In common use the term is used to describe the largest species from this family, especially those of the genus Macropus, red kangaroo, antilopine kangaroo, eastern grey kangaroo and western grey kangaroo. Kangaroos are endemic to Australia. Kangaroos have large, powerful hind legs, large feet adapted for leaping, a long muscular tail for balance, and a small head. Like most marsupials, female kangaroos have a pouch called a marsupium in which joeys complete postnatal development. Larger kangaroos have adapted much better than smaller Macropods[which?] to land clearing for pastoral agriculture and habitat changes brought to the Australian landscape by humans. Many of the smaller Macropods are rare and endangered species, whilst the larger species of Kangaroos prosper to become relatively plentiful. The kangaroo is an unofficial symbol of Australia and appears as an emblem on the Australian coat of arms and on some of its currency and is used by some of Australia's well known organisations, including Qantas and the Royal Australian Air Force. The kangaroo is important to both Australian culture and the national image, and consequently there are numerous popular culture references. Wild kangaroos are shot for meat, leather hides, and to protect grazing land. Although controversial, harvesting kangaroo meat has some environmental advantages to limit over-grazing and the meat has perceived health benefits for human consumption compared with traditional meats due to the low level of fat on kangaroos."
questions = [
    "Which family does the kangaroo belong to?",
    "What happens in the marsupium?",
    "What is the marsupium?",
    "Which are some of Australia's well known organizatins for which the kangaroo appears as a symbol or emblem?",
    "What are the environmental advantages of harvesting kangaroo meat?"
]
answers = [
    "Macropodidae",
    "joeys complete postnatal development",
    "female kangaroos have a pouch called a marsupium",
    "Qantas and the Royal Australian Air Force",
    "limit over-grazing"
]
texte = texte.split('.')

def simply(text: list, answers: list) -> list:
    """Filter sentences containing any of the answers."""
    return [sentence for sentence in text if any(answer in sentence for answer in answers)]

texte = simply(texte, answers)

def simple_tokenizer(text: str) -> list:
    """Tokenize the input text into words."""
    return re.findall(r'\b\w+\b', text.lower())

def simple_lemmatizer(word: str) -> str:
    """Perform simple lemmatization of words."""
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('s'):
        return word[:-1]
    return word

def cleaner(sentence: str) -> str:
    """Clean and lemmatize a sentence."""
    tokens = simple_tokenizer(sentence)
    lem = [simple_lemmatizer(word) for word in tokens if word not in stop_words]
    return " ".join(lem)

def calculate_scores(question_words: set, sentence: str) -> tuple:
    """Calculate matching scores between question words and a sentence."""
    sentence_words = set(cleaner(sentence).split())
    match_count = sum(1 for word in question_words if word in sentence_words)
    complete_match = question_words.issubset(sentence_words)
    return (complete_match, match_count)

def match_questions_to_answers(questions: list, sentences: list, answers: list) -> dict:
    """Match each question to the best answer based on sentences."""
    results = {}
    assigned_sentences = set()

    for i, question in enumerate(questions):
        question_words = set(cleaner(question).split())
        potential_matches = [
            (sentence, calculate_scores(question_words, sentence))
            for sentence in sentences
        ]

        # Find the best matching sentence for the question
        potential_matches.sort(key=lambda x: (x[1][0], x[1][1]), reverse=True)
        
        for sentence, _ in potential_matches:
            if sentence not in assigned_sentences:
                assigned_sentences.add(sentence)
                # Instead of breaking early, ensure we match the best possible answer
                for answer in answers:
                    answer_words = set(cleaner(answer).split())
                    sentence_words = set(cleaner(sentence).split())
                    if answer_words.issubset(sentence_words):
                        results[question] = answer
                        break
                break

    # Handle any questions not matched above
    for i, question in enumerate(questions):
        if question not in results:
            results[question] = "No clear answer found"

    return results

results = match_questions_to_answers(questions, texte, answers)

# Print results to verify
for question, answer in results.items():
    print(f"Question: {question}\nRéponse: {answer}\n")

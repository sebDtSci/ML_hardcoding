import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()
nlp = spacy.load("en_core_web_sm")


texte = str(input())
questions = [str(input()) for _ in range(4)]
answers = str(input())

answers = answers.split(';')

def cleaner(sentence: str) -> str:
    doc = nlp(sentence)
    lem = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(lem)

textes = texte.split(".")
textes_clean = [cleaner(sentence) for sentence in textes]
questions_clean = [cleaner(question) for question in questions]
answers_clean = [cleaner(answer) for answer in answers]

tfidf_matrix = vectorizer.fit_transform(textes_clean)
tfidf_feature_names = vectorizer.get_feature_names_out()

def find_best_matching_sentence(question):
    question_tfidf = vectorizer.transform([question])
    cosine_similarities = cosine_similarity(question_tfidf, tfidf_matrix).flatten()
    most_similar_sentence_index = cosine_similarities.argmax()
    return textes[most_similar_sentence_index]

matched_sentences = [find_best_matching_sentence(question) for question in questions_clean]

results = {}
for i, question in enumerate(questions):
    best_sentence = matched_sentences[i]
    for answer in answers:
        if cleaner(answer) in cleaner(best_sentence):
            results[question] = answer
            break

for question, answer in results.items():
    # print(f"Question: {question}")
    print(f"Answer: {answer}")
    
    
    
# texte = "Zebras are several species of African equids (horse family) united by their distinctive black and white stripes. Their stripes come in different patterns, unique to each individual. They are generally social animals that live in small harems to large herds. Unlike their closest relatives, horses and donkeys, zebras have never been truly domesticated. There are three species of zebras: the plains zebra, the Grévy's zebra and the mountain zebra. The plains zebra and the mountain zebra belong to the subgenus Hippotigris, but Grévy's zebra is the sole species of subgenus Dolichohippus. The latter resembles an ass, to which it is closely related, while the former two are more horse-like. All three belong to the genus Equus, along with other living equids. The unique stripes of zebras make them one of the animals most familiar to people. They occur in a variety of habitats, such as grasslands, savannas, woodlands, thorny scrublands, mountains, and coastal hills. However, various anthropogenic factors have had a severe impact on zebra populations, in particular hunting for skins and habitat destruction. Grévy's zebra and the mountain zebra are endangered. While plains zebras are much more plentiful, one subspecies, the quagga, became extinct in the late 19th century – though there is currently a plan, called the Quagga Project, that aims to breed zebras that are phenotypically similar to the quagga in a process called breeding back."

# questions = ["Which Zebras are endangered?","What is the aim of the Quagga Project?","Which animals are some of their closest relatives?","Which are the three species of zebras?","Which subgenus do the plains zebra and the mountain zebra belong to?"]

# answers = ["subgenus Hippotigris","the plains zebra, the Grévy's zebra and the mountain zebra","horses and donkeys","aims to breed zebras that are phenotypically similar to the quagga","Grévy's zebra and the mountain zebra"]
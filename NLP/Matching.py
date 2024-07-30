import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
stop_words = stopwords.words('english')
new_SW = ["?"]
stop_words.extend(new_SW)
stop_words = set(stop_words)
lemmatizer = WordNetLemmatizer()

texte = "Zebras are several species of African equids (horse family) united by their distinctive black and white stripes. Their stripes come in different patterns, unique to each individual. They are generally social animals that live in small harems to large herds. Unlike their closest relatives, horses and donkeys, zebras have never been truly domesticated. There are three species of zebras: the plains zebra, the Grévy's zebra and the mountain zebra. The plains zebra and the mountain zebra belong to the subgenus Hippotigris, but Grévy's zebra is the sole species of subgenus Dolichohippus. The latter resembles an ass, to which it is closely related, while the former two are more horse-like. All three belong to the genus Equus, along with other living equids. The unique stripes of zebras make them one of the animals most familiar to people. They occur in a variety of habitats, such as grasslands, savannas, woodlands, thorny scrublands, mountains, and coastal hills. However, various anthropogenic factors have had a severe impact on zebra populations, in particular hunting for skins and habitat destruction. Grévy's zebra and the mountain zebra are endangered. While plains zebras are much more plentiful, one subspecies, the quagga, became extinct in the late 19th century – though there is currently a plan, called the Quagga Project, that aims to breed zebras that are phenotypically similar to the quagga in a process called breeding back."

questions = ["Which Zebras are endangered?","What is the aim of the Quagga Project?","Which animals are some of their closest relatives?","Which are the three species of zebras?","Which subgenus do the plains zebra and the mountain zebra belong to?"]

answers = ["subgenus Hippotigris","the plains zebra, the Grévy's zebra and the mountain zebra","horses and donkeys","aims to breed zebras that are phenotypically similar to the quagga","Grévy's zebra and the mountain zebra"]

textes = texte.split(".")

def cleaner(sentence:str)->str:
    w_token = word_tokenize(sentence)
    filtred = [w for w in w_token if not w.lower() in stop_words]
    lem = [lemmatizer.lemmatize(w) for w in filtred]
    return ",".join(lem)
    

dict = {cleaner(sentence): answer for sentence in textes for answer in answers}
sentence_clean = [cleaner(sentence) for sentence in textes]
question_clean = [cleaner(question) for question in questions]

def DIY_tokenize(text):
    return text.lower().replace('.', '').split()

def vocabulary(texts):
    vocabulary = set()
    for text in texts:
        words = DIY_tokenize(text)
        vocabulary.update(words)
    return list(vocabulary)

def vectorizer(text, vocabulary):
    vector = [0] * len(vocabulary)
    words = DIY_tokenize(text)
    for word in words:
        if word in vocabulary:
            index = vocabulary.index(word)
            vector[index] += 1
    return vector        


def cosine_similarity(vec1, vec2):
    dot_product = sum([vec1[i] * vec2[i] for i in range(len(vec1))])
    magnitude_vec1 = math.sqrt(sum([vec1[i]**2 for i in range(len(vec1))]))
    magnitude_vec2 = math.sqrt(sum([vec2[i]**2 for i in range(len(vec2))]))
    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0
    return dot_product / (magnitude_vec1 * magnitude_vec2)

vocabulary = vocabulary(textes + answers)

text_vectors = [vectorizer(text, vocabulary) for text in sentence_clean]
question_vectors = [vectorizer(question, vocabulary) for question in question_clean]

print(text_vectors)
print(question_vectors)

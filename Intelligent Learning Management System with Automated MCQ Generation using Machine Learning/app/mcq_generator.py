import random

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize


REQUIRED_NLTK_RESOURCES = {
    'punkt': 'tokenizers/punkt',
    'stopwords': 'corpora/stopwords',
    'wordnet': 'corpora/wordnet',
}


def ensure_nltk_data():
    for package_name, resource in REQUIRED_NLTK_RESOURCES.items():
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(package_name)
    return True


ensure_nltk_data()


class MCQGenerator:
    def __init__(self):
        ensure_nltk_data()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def _extract_keywords(self, sentence):
        words = word_tokenize(sentence)
        keywords = []
        seen = set()

        for word in words:
            normalized = word.lower()
            if not normalized.isalpha():
                continue
            if len(normalized) < 3:
                continue
            if normalized in self.stop_words:
                continue
            if normalized in seen:
                continue

            seen.add(normalized)
            keywords.append(word)

        return keywords[:8]

    def generate_mcqs(self, text, num_questions=5):
        sentences = sent_tokenize(text)
        mcqs = []

        for sentence in sentences[:num_questions]:
            keywords = self._extract_keywords(sentence)
            if not keywords:
                continue

            correct_answer = random.choice(keywords)
            question = sentence.replace(correct_answer, "______", 1)

            distractors = [kw for kw in keywords if kw != correct_answer][:3]
            while len(distractors) < 3:
                filler = random.choice(keywords)
                if filler != correct_answer and filler not in distractors:
                    distractors.append(filler)

            options = [correct_answer] + distractors
            random.shuffle(options)

            mcqs.append({
                'question': question,
                'options': options,
                'correct_answer': correct_answer,
                'explanation': f"This tests understanding of the word '{correct_answer}' in context."
            })

        return mcqs

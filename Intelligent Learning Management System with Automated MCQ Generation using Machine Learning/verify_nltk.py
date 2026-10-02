import nltk
from app.mcq_generator import MCQGenerator

text = 'Machine learning helps computers learn from data. It improves predictions.'
result = MCQGenerator().generate_mcqs(text, 1)
print(result)
print('NLTK OK')

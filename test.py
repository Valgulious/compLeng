import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

document = open(r"test.txt").read()


def preprocess(document):
	sentences = nltk.sent_tokenize(document)

	# стоп-слова которые мы считать не будем
	stop_words = stopwords.words('russian')
	print(stop_words)
	# расширим набор дополнительным списком слов
	stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', ',', '«', '»', '.', 'т.д', 'т.п', '!'])

	words = sum(1 for sent in sentences
				for word in nltk.word_tokenize(sent)
				if word not in stop_words
				)
	cnt = 0
	for sent in sentences:
		cnt += 1
		wrds = nltk.word_tokenize(sent)
		wrds_without = [word for word in wrds if not word in stop_words]
		print(sent)
		print(wrds)
		print(wrds_without)
	print('ИТОГ------------:')
	return (len(sentences), words)


print(preprocess(document))

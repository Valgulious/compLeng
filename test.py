import nltk
import pymorphy2

# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
morph = pymorphy2.MorphAnalyzer()

# стоп-слова которые мы считать не будем
stop_words = stopwords.words('russian')
print(stop_words)
# расширим набор дополнительным списком слов
stop_words.extend(
	['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', ',', '«', '»', '.', 'т.д', 'т.п', '!', ':'])


# document = open(r"test.txt").read()
#
#
# def preprocess(document):
# 	sentences = nltk.sent_tokenize(document)
#
# 	# стоп-слова которые мы считать не будем
# 	stop_words = stopwords.words('russian')
# 	print(stop_words)
# 	# расширим набор дополнительным списком слов
# 	stop_words.extend(
# 		['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', ',', '«', '»', '.', 'т.д', 'т.п', '!'])
#
# 	words = sum(1 for sent in sentences
# 				for word in nltk.word_tokenize(sent)
# 				if word not in stop_words
# 				)
# 	cnt = 0
# 	for sent in sentences:
# 		cnt += 1
# 		wrds = nltk.word_tokenize(sent)
# 		wrds_without = [word for word in wrds if not word in stop_words]
# 		print(sent)
# 		print(wrds)
# 		print(wrds_without)
# 	print('ИТОГ------------:')
# 	return (len(sentences), words)
#
#
# print(preprocess(document))


class Text:

	def __init__(self, filename, percent):
		self.filename = filename
		self.percent = percent

		document = open(self.filename, 'r').read()
		sentences = nltk.sent_tokenize(document)
		sents = []
		words_for_count = []
		i = 0
		while i < len(sentences):
			wrds = nltk.word_tokenize(sentences[i])
			wrds_without = [word for word in wrds if not word in stop_words]
			wrds_without_inf = []
			for word in wrds_without:
				wrds_without_inf.append(morph.parse(word)[0].normal_form)
			sents.append(Sentence(i, 0, sentences[i], wrds_without_inf))
			words_for_count.extend(wrds_without_inf)
			i += 1

		counter = Counter(words_for_count)
		words_set = counter.most_common()
		words = []
		for word in words_set:
			words.append(Word(word[0], word[1]))

		self.sentences = sents
		self.words = words


class Sentence:

	def __init__(self, position, score, sentence, words):
		self.position = position
		self.score = score
		self.sentence = sentence
		self.words = words


class Word:

	def __init__(self, word, score):
		self.word = word
		self.scale = score


text = Text("test.txt", 100)

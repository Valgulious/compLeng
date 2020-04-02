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

def swap_positions(list, pos1, pos2):
	list[pos1], list[pos2] = list[pos2], list[pos1]
	return list


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
			sents.append(Sentence(i, 0, sentences[i], set(wrds_without_inf)))
			words_for_count.extend(wrds_without_inf)
			i += 1

		counter = Counter(words_for_count)
		words_set = counter.most_common()
		words = []
		for word in words_set:
			words.append(Word(word[0], word[1]))

		self.sentences = sents
		self.words = words

	def scored_sentences(self):
		for sent in self.sentences:
			for word in self.words:
				if word.word in sent.words:
					sent.score += word.score

	def sorted_sentences_by_score(self):
		for i in range(len(self.sentences) - 1):
			for j in range(len(self.sentences) - i - 1):
				if self.sentences[j].score < self.sentences[j + 1].score:
					self.sentences[j], self.sentences[j + 1] = self.sentences[j + 1], self.sentences[j]


class Sentence:

	def __init__(self, position, score, sentence, words):
		self.position = position
		self.score = score
		self.sentence = sentence
		self.words = words


class Word:

	def __init__(self, word, score):
		self.word = word
		self.score = score


text = Text("test.txt", 100)
text.scored_sentences()
text.sorted_sentences_by_score()
for sent in text.sentences:
	print(sent.score)

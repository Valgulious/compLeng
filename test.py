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


class Text:

	def __init__(self, _filename, _percent):
		_filename_split = filename.split(".")
		new_filename = ""
		for i in range(len(_filename_split) - 1):
			new_filename += _filename_split[i]

		self.filename = new_filename
		self.percent = _percent

		document = open(_filename, 'r').read()
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

	def referat(self):
		referat_filename = self.filename + "_referat.txt"
		referat_file = open(referat_filename, "w")
		count = (self.percent * len(self.sentences)) / 100

		sentences = []
		for i in range(int(count)):
			sentences.append(self.sentences[i])

		for i in range(len(sentences) - 1):
			for j in range(len(sentences) - i - 1):
				if sentences[j].position > sentences[j + 1].position:
					sentences[j], sentences[j + 1] = sentences[j + 1], sentences[j]

		referat = ""
		for sent in sentences:
			referat += sent.sentence + "\n"

		referat_file.write(referat)
		return referat_filename


class Sentence:

	def __init__(self, _position, _score, _sentence, _words):
		self.position = _position
		self.score = _score
		self.sentence = _sentence
		self.words = _words


class Word:

	def __init__(self, _word, _score):
		self.word = _word
		self.score = _score


print("Введите имя файла")
filename = input()
print("Введите, сколько процентов от исходного текста оставить")
percent = input()
text = Text(filename, int(percent))
text.scored_sentences()
text.sorted_sentences_by_score()
print("Зареферированный текст находится в файле " + text.referat())

# shannon.py - Generates discrete sources per Shannon's approximations.
# Paper at: http://cm.bell-labs.com/cm/ms/what/shannonday/shannon1948.pdf
# 
# 
# A process generates the following sequences where each symbol is chosen with an
# associated probability.  The 0th-order approximation chooses each symbol with
# equal probability. The 1st-order symbols are chosen independently with the
# probability they appear in the text.  2nd-order approximations depend on the
# preceeding symbol.

import random

def main():

	# open text
	file_name = "text.txt"
	f = open (file_name, "r")
	text = f.read()
	print "'{}' opened...\n".format(file_name)
	
	# get frequency of each word in text
	words = dict()
	text_words = text.split (' ')
	for word in text_words:
		w = word.lower()
		if w not in words:
			words[w] = 0
		words[w] += 1
	
	# calculate transition frequency for each word
	word_trans = dict()
	for i in range (len (text_words) - 1):
		w = text_words[i].lower()
		if w not in word_trans:
			word_trans[w] = dict()
			for k in words.keys():
				word_trans[w][k] = 0
		x = text_words[i + 1].lower()
		word_trans[w][x] += 1

	
	# normalize word counts
	total_words = sum (words.itervalues())
	for k, v in words.iteritems():
		words[k] = float(v) / total_words
	
	# normalize word transitions
	for i, j in word_trans.iteritems():
		total = sum (j.itervalues())
		for k, v in word_trans[i].iteritems():
			word_trans [i][k] = float (v) / total
		
	# get frequencies for each letter
	num_letters = 0
	letters = dict()
	for c in text:
		c = c.lower()
		num_letters += 1
		if c not in letters:
			letters[c] = 0
		letters[c] += 1

	# build digram matrix
	digram = dict()
	for i in range (len (text) - 1):
		c = text[i].lower()
		if c not in digram:
			digram[c] = dict()
			for k in letters.keys():
				digram[c][k] = 0
		t = text[i + 1].lower()
		digram[c][t] += 1
	
	# build trigram matrix
	trigram = dict()
	for i in range (len(text) - 2):
		c = text[i].lower()
		if c not in trigram:
			trigram[c] = dict()
			for k in letters.keys():
				trigram[c][k] = dict()
				for l in letters.keys():
					trigram[c][k][l] = 0
		d = text[i + 1].lower()
		e = text[i + 2].lower()
		trigram[c][d][e] += 1
			
	# normalize digram values
	for i, j in digram.iteritems():
		# i is current letter
		# j is list of transition frequencies
		row = str (i)
		total = sum (j.itervalues())
		for k, v in j.iteritems():
			digram [i][k] = float(v) / total
	
	# normalize trigram values
	for k, v in trigram.iteritems():
		for l, w in v.iteritems():
			total = sum (w.itervalues())
			if total != 0:
				for m, x in w.iteritems():
					prob = float(x) / total
					trigram[k][l][m] = prob

	# normalize letter probabilities
	print "Letter probabilities:"
	for k, v in letters.iteritems():
		print "{char} {val:5}".format (char=k, val=v), 
		letters[k] = float(v) / num_letters
		print " {:5>04.3f}".format(letters[k]*100.0)

	print "\n{} letters found.".format(num_letters)
	print "{} words found.".format(len(text_words))
	print ""

	
	print "Character Aprroximations:"

	# print 0th-order
	string = list()
	num_chars = 100
	for i in range (num_chars):
		r = random.randint(0, len(letters) - 1)
		c = letters.keys()[r]
		string.append (c)
	print "0th-order:"
	print "".join (string)
	print ""

	# print first-order approximation
	string = list()
	num_chars = 100
	for i in range (num_chars):
		p = random.random()
		# print "p:", p
		cum = 0.0
		for k, v in letters.iteritems():
			# print "c:", cum
			cum += v
			if p < cum:
				string.append (k)
				break
	print "1st-order:"
	print "".join(string)
	print ""

	# print digram approximation
	string = string [-1:] # keep first
	num_chars = 100
	for i in range (1, num_chars):
		c = string [i - 1]
		p = random.random()
		cum = 0.0
		for k, v in digram[c].iteritems ():
			cum += v
			if p < cum:
				string.append (k)
				break
	print "digram:"
	print "".join (string)
	print ""

	# print trigram approximations
	string = string [-2:]
	num_chars = 100
	for i in range (2, num_chars):
		c = string [i - 2]
		d = string [i - 1]
		p = random.random()
		cum = 0.0
		for k, v in trigram[c][d].iteritems ():
			cum += v
			if p < cum:
				string.append (k)
				break
	print "trigram:"
	print "".join (string)
	print "\n"
	
	print "Word Approximations:"
	# print 0th-order word approximation
	string = list()
	words_length = 0
	while words_length < num_chars:
		r = random.randint (0, len(words) - 1)
		w = words.keys()[r]
		string.append (w)
		words_length += len(w) + 1
	print "0th-order"
	print " ".join (string)
	print ""

	# print 1st-order words
	string = list()
	words_length = 0
	while words_length < num_chars:
		p = random.random()
		cum = 0.0
		for k, v in words.iteritems():
			cum += v
			if p < cum:
				string.append (k)
				words_length += len (k) + 1
				break
	print "1st-order:"
	print " ".join(string)
	print ""

	# print 2nd-order words
	string = ["the"] # just to be safe
	words_length = 0
	while words_length < num_chars:
		w = string [-1]
		p = random.random()
		cum = 0.0
		for k, v in word_trans[w].iteritems():
			cum += v
			if p < cum:
				string.append (k)
				words_length += len(k) + 1
				break
	print "2nd-order:"
	print " ".join(string)
	print ""


if __name__ == "__main__":
	main()

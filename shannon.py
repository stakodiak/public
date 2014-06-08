"""
Generates discrete sources per Shannon's approximations.
Paper at: http://cm.bell-labs.com/cm/ms/what/shannonday/shannon1948.pdf


A process generates the following sequences where each symbol is chosen
with an associated probability.  The 0th-order approximation chooses
each symbol with equal probability. The 1st-order symbols are chosen
independently with the probability they appear in the text.  2nd-order
approximations depend on the preceeding symbol.
"""
import random
import sys
import textwrap

def main():
    # open text
    file_name = "text.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
    f = open(file_name, "r")
    text = f.read()
    print "'{}' opened...\n".format(file_name)

    # get frequency of each word in text
    words = dict()
    text_words = text.split(' ')
    for word in text_words:
        w = word.lower()
        if w not in words:
            words[w] = 0
        words[w] += 1

    # calculate transition frequency for each word
    word_2nd = dict()
    for i in range(len(text_words) - 1):
        w = text_words[i].lower()
        if w not in word_2nd:
            word_2nd[w] = dict()
            for k in words.keys():
                word_2nd[w][k] = 0
        x = text_words[i + 1].lower()
        word_2nd[w][x] += 1

    # normalize word counts
    total_words = sum(words.itervalues())
    for k, v in words.iteritems():
        words[k] = float(v) / total_words

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
    for i in range(len(text) - 1):
        c = text[i].lower()
        if c not in digram:
            digram[c] = dict()
            for k in letters.keys():
                digram[c][k] = 0
        t = text[i + 1].lower()
        digram[c][t] += 1

    # build trigram matrix
    trigram = dict()
    for i in range(len(text) - 2):
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

    # build tetragram matrix
    tetragram = dict()
    for i in range(len(text) - 3):
        c = text[i].lower()
        if c not in tetragram:
            tetragram[c] = dict()
            for k in letters.keys():
                tetragram[c][k] = dict()
                for l in letters.keys():
                    tetragram[c][k][l] = dict()
                    for m in letters.keys():
                        tetragram[c][k][l][m] = 0
        d = text[i + 1].lower()
        e = text[i + 2].lower()
        f = text[i + 3].lower()
        tetragram[c][d][e][f] += 1

    # build ngram matrix
    n = 7
    ngram = dict()
    if len(sys.argv) == 3:
        n = int(sys.argv[2])
    for i in range(len(text) - (n - 1)):
        h = text[i + (n - 1)].lower()
        key = text[i:i + (n - 1)].lower()
        if key not in ngram:
            ngram[key] = dict()
        if h not in ngram[key]:
            ngram[key][h] = 0
        ngram[key][h] += 1

    # normalize digram values
    for i, j in digram.iteritems():
        # i is current letter
        # j is list of transition frequencies
        total = sum(j.itervalues())
        for k, v in j.iteritems():
            digram[i][k] = float(v) / total

    # normalize trigram values
    for k, v in trigram.iteritems():
        for l, w in v.iteritems():
            total = sum(w.itervalues())
            if total != 0:
                for m, x in w.iteritems():
                    prob = float(x) / total
                    trigram[k][l][m] = prob

    # normalize tetragram values
    for k, v in tetragram.iteritems():
        for l, w in v.iteritems():
            for m, x in w.iteritems():
                total = sum(x.itervalues())
                if total != 0:
                    for o, y in x.iteritems():
                        prob = float(y) / total
                        #print "{} -> {} / {}".format(prob, float(y), total)
                        tetragram[k][l][m][o] = prob

    # normalize ngram values
    for k, v in ngram.iteritems():
        total = sum(v.itervalues())
        for l, w in v.iteritems():
            ngram[k][l] = float(w) / total

    # normalize letter probabilities
    print "Letter probabilities:"
    for k, v in letters.iteritems():
        print "{char} {val:5}".format(char=k, val=v),
        letters[k] = float(v) / num_letters
        print " {:5>04.3f}".format(letters[k]*100.0)

    print "\n{} letters found.".format(num_letters)
    print "{} words found.".format(len(text_words))
    print ""


    print "Character Aprroximations:"

    # print 0th-order
    string = list()
    num_chars = 100
    for i in range(num_chars):
        r = random.randint(0, len(letters) - 1)
        c = letters.keys()[r]
        string.append(c)
    print "0th-order:"
    print "".join(string)
    print ""

    # print first-order approximation
    string = list()
    num_chars = 100
    for i in range(num_chars):
        p = random.random()
        # print "p:", p
        cum = 0.0
        for k, v in letters.iteritems():
            # print "c:", cum
            cum += v
            if p < cum:
                string.append(k)
                break
    print "1st-order:"
    print "".join(string)
    print ""

    # print digram approximation
    string = string[-1:] # keep first
    num_chars = 100
    for i in range(1, num_chars):
        c = string[i - 1]
        p = random.random()
        cum = 0.0
        for k, v in digram[c].iteritems():
            cum += v
            if p < cum:
                string.append(k)
                break
    print "digram:"
    print "".join(string)
    print ""

    # print trigram approximations
    string = string[-2:]
    num_chars = 100
    for i in range(2, num_chars):
        c = string[i - 2]
        d = string[i - 1]
        p = random.random()
        cum = 0.0
        for k, v in trigram[c][d].iteritems():
            cum += v
            if p < cum:
                string.append(k)
                break
    print "trigram:"
    print "".join(string)
    print ""

    # print tetragram approximations
    string = string[-3:]
    for i in range(3, num_chars):
        c = string[i - 3]
        d = string[i - 2]
        e = string[i - 1]
        p = random.random()
        cum = 0.0
        for k, v in tetragram[c][d][e].iteritems():
            cum += v
            if p < cum:
                string.append(k)
                break
    print "tetragram:"
    print "".join(string)
    print ""

    # print ngram approximation

    # find good starting key
    start = random.randint(0, len(ngram.keys()) - 2)
    while not ngram.keys()[start].startswith('. '):
        start = random.randint(0, len(ngram.keys()) - 2)
    find = ngram.keys()[start][2:]
    keys = ngram.keys()
    for i in range(len(keys)):
        k = keys[i]
        if k.startswith(find):
            find = i
            break
    start = keys[find]

    # start is the beginning of a sentence
    string = list(start)
    num_chars = 500
    for i in range(num_chars):
        if len(string) > num_chars:
            break
        index = i + n - 1
        c = "".join(string[i:index])
        p = random.random()
        cum = 0.0
        for k, v in ngram[c].iteritems():
            cum += v
            if p < cum:
                string.append(k)
                break
    print "ngram:", "(n = {})".format(n)
    string = "".join(string)
    string = textwrap.TextWrapper(width=100).wrap(string)
    print '\n'.join(string)
    print ""

    print ""
    print "Word Approximations:"
    # print 0th-order word approximation
    string = list()
    num_chars = 100
    words_length = 0
    while words_length < num_chars:
        r = random.randint(0, len(words) - 1)
        w = words.keys()[r]
        string.append(w)
        words_length += len(w) + 1
    print "0th-order"
    print " ".join(string)
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
                string.append(k)
                words_length += len(k) + 1
                break
    print "1st-order:"
    print " ".join(string)
    print ""


if __name__ == "__main__":
    main()

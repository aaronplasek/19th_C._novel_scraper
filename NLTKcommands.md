*USEFUL Natural Language Tool Kit (NLTK) COMMANDS & NOTES*
======================

Useful commands----

[1] `len(set([word.lower() for word in text if word.isalpha()]))` Outputs vocabulary of text without double-counting the same word with different caplitalized letters (e.g., That & that, etc.)

[2] `len([word.lower() for word in text if word.isalpha()]))` Outputs all words of text in lower case

[3] `raw('text')` Outputs all chars in text, including spaces and puncuation

[4] `sents('text')` Outputs all sentences in text, where each sentence is a list of words

[4.5] `words('text')` outputs list of words for NLTK'd corpus (see #7)

[5] `nltk.FreqDist([w.lower() for w in text])` Outputs frequency distribution

[6] to making an concordance (example):

    `>>> emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))`

    `>>> emma.concordance("surprize")`

[7] loading a plain text corpus into nltk (example):
 	
  `>>> from nltk.corpus import PlaintextCorpusReader`
  
  `>>> corpus_root = '/usr/share/dict'` #directory where corpus is
  
  `>>> wordlists = PlaintextCorpusReader(corpus_root, '.*')` #can be list of filenames of texts in corpus or pattern match using re
  
  `>>> wordlists.fileids()`
  
  `['README', 'connectives', 'propernames', 'web2', 'web2a', 'words']`
  
  `>>> wordlists.words('connectives')`
  
  `['the', 'of', 'and', 'to', 'a', 'in', 'that', 'is', ...]`

*Syntax notes about python & NLTK----

[A] the expressions [f(x) for ...] (e.g., [f(x) for x in text]) and [x.f for ...] (e.g., [w.upper () for w in text]) is a common way to write python for loops where "f(x)" is a function that acts on every "x" throughout the list/array/string "text". 

[B]

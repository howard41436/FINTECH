import os
from nltk.tag import StanfordNERTagger as NERTagger
from nltk.tag import StanfordPOSTagger as POSTagger
ner_jar = 'StanfordNLP/jars/stanford-ner.jar'
ner_model = 'StanfordNLP/models/english.all.3class.distsim.crf.ser.gz'
pos_jar = 'StanfordNLP/jars/stanford-postagger.jar'
pos_model = 'StanfordNLP/models/english-bidirectional-distsim.tagger'
ner_tagger = NERTagger(ner_model, ner_jar)
pos_tagger = POSTagger(pos_model, pos_jar)
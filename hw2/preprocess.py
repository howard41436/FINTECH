import pdftotext, sys, re, os
from collections import Counter
import pickle
delimeters = [';', ',', '\\*', '\n', '\\.', '\\s', '\\(', '\\)', '"', '\'', '’']
delimeters_str = '|'.join(delimeters)
def remove_capitalize(text):
	first_word = False
	ret = ''
	for ch in text:
		if ch == '.':
			first_word = True
		if first_word == True and ord('A') <= ord(ch) <= ord('Z') or ord('a') <= ord(ch) <= ord('z'):
			ch = ch.lower()
			first_word = False
		ret += ch
	return ret
def preprocess(prefix, year):
	with open('pdfs/{}/{}_{}.pdf'.format(prefix, prefix, year), 'rb') as f:
		pdf = pdftotext.PDF(f)
	text = '\n\n'.join(pdf)
	if not os.path.exists('txts/{}'.format(prefix)):
		os.mkdir('txts/{}'.format(prefix))
	with open('txts/{}/{}_{}.txt'.format(prefix, prefix, year), 'w') as f:
		f.write(text)
	word_list = []
	text2 = re.split(delimeters_str, text)
	i, l = 0, len(text2)
	while i < l - 1:
		if text2[i] == '':
			i += 1
			continue
		if ord('A') <= ord(text2[i][0]) <= ord('Z'):
			j = 1
			new_word = text2[i]
			while i + j < l and (text2[i + j] == '' or ord('A') <= ord(text2[i + j][0]) <= ord('Z')):
				if text2[i + j] != '':
					new_word += ' ' + text2[i + j]
				j += 1
			if new_word != text2[i]:
				word_list.append(new_word)
			i += j
		else:
			i += 1
			continue
	for w in word_list:
		text = text.replace(w, '')
	text = remove_capitalize(text)
	word_list += list(filter(lambda x: x != '' and len(x) >= 3 and (not x.isdigit()), re.split(delimeters_str, text)))
	for w in word_list:
		if len(w) < 3:
			print('error')
	word_dic = Counter(word_list)
	word_sorted_list = sorted(word_dic.items(), key = lambda x: x[1], reverse = True)
	if not os.path.exists('pickles/{}'.format(prefix)):
		os.mkdir('pickles/{}'.format(prefix))
	with open('pickles/{}/{}_{}.pickle'.format(prefix, prefix, year), 'wb') as f:
		pickle.dump(word_sorted_list, f)

prefix = sys.argv[1]
if len(sys.argv) > 2:
	year = sys.argv[2]
	preprocess(prefix, year)
else:
	file_list = os.listdir('pdfs/{}'.format(prefix))
	for f in file_list:
		year = f.split('_')[-1].split('.')[0]
		preprocess(prefix, year)
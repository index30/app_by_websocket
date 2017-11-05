import MeCab
import os
import re
from gensim.models import word2vec

m = MeCab.Tagger("-Owakati")
txt_path = os.listdir('data/txt_file')
txt_path.remove('.DS_Store')
print(txt_path)

with open("data/text1.text8", 'w') as text8:
    for txt in txt_path:
        with open(os.path.join('data/txt_file', txt), 'r') as test1:
            lines = test1.readlines()
            for line in lines:
                line = line.replace('\n', '')
                line = re.sub(r'[,.、。「」]+', '', line)
                l = m.parse(line)
                text8.write(l)

sentences = word2vec.Text8Corpus('data/text1.text8')
#model = word2vec.Word2Vec(sentences, min_count=1, size=200)
model = word2vec.Word2Vec(sentences,
                          sg=1,
                          size=200,
                          min_count=1,
                          window=10,
                          hs=1,
                          negative=0)
print(model.most_similar(['国語']))
print(model.most_similar(['英語']))
print(model.most_similar(['うどん']))
print(model.most_similar(['カレー']))
print(model.similarity('カレー', '料理'))
print(model.similarity('カレー', 'ロシア'))

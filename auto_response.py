import MeCab
from gensim.models import word2vec
import numpy as np

class DefaultResponse():
    def __init__(self):
        pass

    #word2vecを使いたい(方針)
    def wakati_node_parse(self, message):
        m = MeCab.Tagger("-Ochasen")
        parse_txt = m.parseToNode(message)
        part_speech = ['名詞']
        node_dic = {part_speech[0]:[]}
        while parse_txt:
            node = parse_txt.surface
            node_fea = parse_txt.feature.split(",")
            # パース失敗や, 名詞と出ているのに認識しないバグ有り(調査中)
            if node_fea[0] == part_speech[0]:
                node_dic[part_speech[0]] = node_dic[part_speech[0]] + [node]

            parse_txt = parse_txt.next
        return node_dic

    def response_genre(self, word):
        topic = ['スポーツ', '料理', '政治']
        topic_counter = [0,0,0]
        model = word2vec.Word2Vec.load("model/for_conversation.model")
        for w in word:
            topic_counter[0] = topic_counter[0] + model.similarity(w, topic[0])
            topic_counter[1] = topic_counter[1] + model.similarity(w, topic[1])
            topic_counter[2] = topic_counter[2] + model.similarity(w, topic[2])

        result = [g/len(word) for g in topic_counter]
        return topic[np.argmax(np.array(result))]

    def parse_response(self, message):
        wakati_node = self.wakati_node_parse(message)
        noun = wakati_node["名詞"]
        genre = self.response_genre(noun)
        if message == "なんでも":
            return_mes = "そういうのはよくないです"
            return return_mes
        elif genre=="料理":
            return_mes = "いいですね!!おいしそう..."
            return return_mes
        else:
            return_mes = "それはりょうりですか??わたししらないです"
            return return_mes

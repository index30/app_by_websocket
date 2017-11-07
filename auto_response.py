import MeCab
from gensim.models import word2vec
import numpy as np

class DefaultResponse():
    def __init__(self):
        pass

    def wakati_node_parse(self, message):
        m = MeCab.Tagger("-Ochasen")
        parse_txt = m.parseToNode(message)
        part_speech = ['名詞']
        node_dic = {part_speech[0]:[]}
        while parse_txt:
            node = parse_txt.surface
            node_fea = parse_txt.feature.split(",")
            if node_fea[0] == part_speech[0]:
                node_dic[part_speech[0]] = node_dic[part_speech[0]] + [node]
            parse_txt = parse_txt.next
        return node_dic

    def return_genre_sentence(self, word):
        dish_genre = ['中華', 'インド', '和食', '洋食']
        corr_sentence = ['まーボーどうふ', 'カレー', 'うどん', 'ハンバーグ']
        match_list = [corr_sentence[i] for (i, g) in enumerate(dish_genre) if g in word]
        return match_list

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

    def return_template(self, mes, genre):
        if mes == "なんでも":
            return_mes = "そういうのはよくないです"
            return return_mes
        elif genre=="料理":
            return_mes = "いいですね!!おいしそう..."
            return return_mes
        elif genre == "例外":
            return_mes = "よくわかりませんでした...もういちどおねがいできますか?"
            return return_mes
        elif genre == "未知":
            return_mes = "そのたんごはしらないです...ごめんなさい"
            return return_mes
        else:
            return_mes = "それはりょうりですか??"
            return return_mes

    def remove_empty_ele(self, target):
        return [l for l in target if l != '']

    def parse_response(self, message):
        wakati_node = self.wakati_node_parse(message)
        noun = self.remove_empty_ele(wakati_node["名詞"])
        if noun:
            try:
                match = self.return_genre_sentence(noun)
                if match:
                    return "それでは"+"か".join(match)+"はいかがでしょう?"
                else:
                    genre = self.response_genre(noun)
                    return self.return_template(message, genre)
            except:
                return self.return_template(message, "未知")
        else:
            return self.return_template(message, "例外")

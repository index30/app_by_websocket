import MeCab

class DefaultResponse():
    def __init__(self):
        pass

    #word2vecを使いたい(方針)
    def wakati_node_parse(self, message):
        m = MeCab.Tagger("-Owakati")
        parse_txt = m.parseToNode(message)
        part_speech = ["名詞"]
        node_dic = {part_speech[0]:[]}
        while parse_txt:
            node = parse_txt.surface
            node_fea = parse_txt.feature.split(",")
            if node_fea[0] != "BOS/EOS" and node_fea[0] == part_speech[0]:
               node_dic[part_speech[0]] = node_dic[part_speech[0]] + [node]
            parse_txt = parse_txt.next
        return node_dic

    def parse_response(self, message):
        # wakati_node = self.wakati_node_parse(message)
        if message == "なんでも":
            return_mes = "そういうのはよくないです"
            return return_mes
        else:
            return_mes = "いいですね!!おいしそう..."
            return return_mes

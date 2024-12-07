import jieba
def get_word_indices(tokens, token_list):
    word_indices = []
    index = 0
    for token in tokens:
        word_indices.append(index)
        index += len(token)
        while index < len(token_list) and token_list[index] == '[]':
            index += 1
    return word_indices

sentence = "我来自中国"
token_list = ['我','[]','[]','来','自','[]','中','国','[]']

# 使用jieba进行分词
tokens = list(jieba.cut(sentence))

# 获取每个词占有的列表中字符的索引
word_indices = get_word_indices(tokens, token_list)

print("分词结果：", tokens)
print("每个词占有的列表中字符的索引：", word_indices)
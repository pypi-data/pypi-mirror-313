import sentencepiece as spm

# 构建BPE模型并保存
def train_and_save_model(input_text_file, model_prefix, vocab_size):
    spm.SentencePieceTrainer.Train(
        f'--input={input_text_file} --model_prefix={model_prefix} --vocab_size={vocab_size} --model_type=bpe'
    )

# 加载保存的模型并使用
def load_and_use_model(model_path, input_sentence):
    sp = spm.SentencePieceProcessor()
    sp.load(model_path)

    # 使用模型进行文本处理
    encoded_text = sp.encode_as_pieces(input_sentence)
    decoded_text = sp.decode_pieces(encoded_text)

    return encoded_text, decoded_text

def load_and_print_vocab(model_path):
    sp = spm.SentencePieceProcessor()
    sp.load(model_path)
    # 获取词表大小
    vocab_size = sp.get_piece_size()
    # 打印词表
    print(f"Vocabulary Size: {vocab_size}")
    # 打印每个词汇
    vocab_dict = {}
    print("Vocabulary:")
    for i in range(vocab_size):
        piece = sp.id_to_piece(i)
        print(f"{piece}: {i}")
        vocab_dict[piece] = i
    return vocab_dict

if __name__ == '__main__':
    # 示例文本
    # text_file = './example.txt'
    # # 构建并保存BPE模型
    model_prefix = 'example_model'
    # vocab_size = 1000
    # train_and_save_model(text_file, model_prefix, vocab_size)

    # 加载保存的模型并使用
    loaded_model_path = f'{model_prefix}.model'
    # input_sentence = "SentencePiece is easy to use and powerful."
    # encoded_text, decoded_text = load_and_use_model(loaded_model_path, input_sentence)
    # # 打印结果
    # print("Original Text:", input_sentence)
    # print("Encoded Text:", encoded_text)
    # print("Decoded Text:", decoded_text)
    load_and_print_vocab(loaded_model_path)

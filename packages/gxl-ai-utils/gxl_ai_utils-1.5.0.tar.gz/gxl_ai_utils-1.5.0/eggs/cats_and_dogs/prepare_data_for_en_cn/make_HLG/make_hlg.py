from gxl_ai_utils.utils import utils_file

def make_hlg():
    """"""
    input_words = '/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_en_cn/make_arpa/data_res/words_lines.txt'
    input_tokens = '/home/work_nfs7/yhliang/online_sys/wenet/examples/onlinesys/data/dict/lang_char.txt'
    arpa_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/prepare_data_for_en_cn/make_arpa/data_res/output.arpa"
    output_dir = './data_res'
    utils_file.makedir_sil(output_dir)
    utils_file.do_make_HLG(input_words, input_tokens, arpa_path, output_dir)

if __name__ == '__main__':
    make_hlg()
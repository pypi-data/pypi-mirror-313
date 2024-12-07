from gxl_ai_utils.utils import utils_file

if __name__ == "__main__":
    """"""
    token_file = "/home/work_nfs7/yhliang/online_sys/wenet/examples/onlinesys/data/dict/lang_char.txt"
    word_file = "/home/work_nfs4_ssd/yhliang/LanguageModel/lang/lang_test616_mix0.1_pruned_5e-11/words.txt"
    arpa_path = '/home/work_nfs14/xlgeng/new_workspace/wenet_gxl_aishell/examples/aishell/s0/LM_training/data/output_all_data_temp.arpa'
    output_dir = "./output_data_2/"
    utils_file.do_make_HLG(word_file, token_file, arpa_path, output_dir)

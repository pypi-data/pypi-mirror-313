import os
from typing import List

from WerInfo_Object import WerInfo
from gxl_utils import get_wer_path_table, do_extract_nouns_jieba
from gxl_ai_utils.utils import utils_file


def get_hot_word_for_speechio():
    down = 2
    stage = 3
    type = "long"
    res_dict = {}
    output_path = f"./data/hot_word/d{down}s{stage}/{type}.scp"
    utils_file.makedir_for_file(output_path)
    wer_table = get_wer_path_table(f"./data/wer_path_d{down}s{stage}.json")
    # for i in range(27):
    #     wer_path = wer_table.get_value_by_row_index_col_key(i, 'common')
    #     print(wer_path)
    #     wer_info_list:List[WerInfo] = WerInfo.do_load_info_list_from_wer_path(wer_path)
    #     _, noun_dict = do_extract_nouns_jieba(wer_info_list)
    #     sorted_items = sorted(noun_dict.items(), key=lambda item: item[1], reverse=True)
    #     sorted_items = [item for item in sorted_items if len(item[0]) > 1]
    #     sorted_items = sorted_items[:80]
    #     sorted_noun_dict = {item[0]: item[1] for item in sorted_items}
    #     words_list = list(sorted_noun_dict.keys())
    #     string_i = f'识别内容可能包含如下关键词：{"、".join(words_list)}'
    #     res_dict[f'speechio_{i}'] = string_i
    # utils_file.write_dict_to_scp(res_dict, output_path)
    # type = 'medium'
    # res_dict = {}
    # output_path = f"./data/hot_word/d{down}s{stage}/{type}.scp"
    # utils_file.makedir_for_file(output_path)
    # for i in range(27):
    #     wer_path = wer_table.get_value_by_row_index_col_key(i, 'common')
    #     print(wer_path)
    #     wer_info_list: List[WerInfo] = WerInfo.do_load_info_list_from_wer_path(wer_path)
    #     _, noun_dict = do_extract_nouns_jieba(wer_info_list)
    #     sorted_items = sorted(noun_dict.items(), key=lambda item: item[1], reverse=True)
    #     sorted_items = [item for item in sorted_items if len(item[0]) > 1]
    #     sorted_items = sorted_items[:40]
    #     sorted_noun_dict = {item[0]: item[1] for item in sorted_items}
    #     words_list = list(sorted_noun_dict.keys())
    #     string_i = f'识别内容可能包含如下关键词：{"、".join(words_list)}'
    #     res_dict[f'speechio_{i}'] = string_i
    # utils_file.write_dict_to_scp(res_dict, output_path)
    # type = 'short'
    # res_dict = {}
    # output_path = f"./data/hot_word/d{down}s{stage}/{type}.scp"
    # utils_file.makedir_for_file(output_path)
    # for i in range(27):
    #     wer_path = wer_table.get_value_by_row_index_col_key(i, 'common')
    #     print(wer_path)
    #     wer_info_list: List[WerInfo] = WerInfo.do_load_info_list_from_wer_path(wer_path)
    #     _, noun_dict = do_extract_nouns_jieba(wer_info_list)
    #     sorted_items = sorted(noun_dict.items(), key=lambda item: item[1], reverse=True)
    #     sorted_items = [item for item in sorted_items if len(item[0]) > 1]
    #     sorted_items = sorted_items[:20]
    #     sorted_noun_dict = {item[0]: item[1] for item in sorted_items}
    #     words_list = list(sorted_noun_dict.keys())
    #     string_i = f'识别内容可能包含如下关键词：{"、".join(words_list)}'
    #     res_dict[f'speechio_{i}'] = string_i
    # utils_file.write_dict_to_scp(res_dict, output_path)
    type = 'exact'
    res_dict = {}
    output_dir = f"./data/hot_word/d{down}s{stage}/{type}/"
    utils_file.makedir(output_path)
    # for i in range(27):
        # wer_path = wer_table.get_value_by_row_index_col_key(i, 'common')
        # print(wer_path)
        # wer_info_list: List[WerInfo] = WerInfo.do_load_info_list_from_wer_path(wer_path)
        # _, noun_dict = do_extract_nouns_jieba(wer_info_list)
        # sorted_items = sorted(noun_dict.items(), key=lambda item: item[1], reverse=True)
        # sorted_items = [item for item in sorted_items if len(item[0]) > 1]
        # sorted_items = sorted_items[:400]
        # sorted_noun_dict = {item[0]: item[1] for item in sorted_items}
        # WerInfo.do_handle_info_list(wer_info_list)
        # exact_words_dict = {}
        # for info in wer_info_list:
        #     err_word_dict = info.diff_dict
        #     for k, v in err_word_dict.items():
        #         if k in noun_dict:
        #             if k in exact_words_dict:
        #                 exact_words_dict[k] += 1
        #             else:
        #                 exact_words_dict[k] = 1
        # sorted_exact_items = sorted(exact_words_dict.items(), key=lambda item: item[1], reverse=True)
        # filter_exact_items = [item for item in sorted_exact_items if len(item[0]) > 1]
        # sorted_filtered_exact_dict = {item[0]: item[1] for item in filter_exact_items}
        #
        # utils_file.print_dict(sorted_filtered_exact_dict)
        # utils_file.logging_print(f'以上是speechio_{i}的关键词')

    for j in [10,20,30,40,50,60,70,80,100,150,10000]:
        res_dict = {}
        for i in range(27):
            output_scp_path = f"{output_dir}speechio_{i}.scp"
            speechio_dict = utils_file.load_dict_from_scp(output_scp_path)
            output_dir_now = os.path.join(output_dir, f"scp")
            utils_file.makedir(output_dir_now)
            type = 'item_{}'.format(j)
            output_path = f"{output_dir_now}/{type}.scp"
            sorted_items = sorted(speechio_dict.items(), key=lambda item: item[1], reverse=True)
            sorted_items = sorted_items[:j]
            sorted_noun_dict = {item[0]: item[1] for item in sorted_items}
            words_list = list(sorted_noun_dict.keys())
            string_i = f'识别内容可能包含如下关键词：{"、".join(words_list)}'
            res_dict[f'speechio_{i}'] = string_i
        utils_file.write_dict_to_scp(res_dict, output_path)


if __name__ == '__main__':
    get_hot_word_for_speechio()

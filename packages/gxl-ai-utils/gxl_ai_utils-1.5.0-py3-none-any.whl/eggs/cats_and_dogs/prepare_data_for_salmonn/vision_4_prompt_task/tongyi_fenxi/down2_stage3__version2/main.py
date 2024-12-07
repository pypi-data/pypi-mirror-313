"""
首先定义存储单元<WerInfo>
"""
from WerInfo_Object import WerInfo
from gxl_ai_utils.utils import utils_file
from Gxl2DTable import Gxl2DTable

"""
从wer_path_dict 中得到每个speechio的wer_path
"""


def get_wer_path_table(wer_path_info_path):
    wer_path_info_path = wer_path_info_path
    # dict_temp1 = {'speechio': ['common', 'short', 'long', 'repeat', 'messy', 'encourage']}
    # dict_temp2 = utils_file.load_dict_from_json(wer_path_info_path)
    # dict_temp1.update(dict_temp2)

    wer_table = Gxl2DTable.load_from_json(wer_path_info_path)
    return wer_table

from gxl_utils import do_extract_nouns_jieba, do_extract_nouns_thulac

def handle_speechio_(i, wer_table):
    print(f'handling speechio {i}')
    fake_big_dict_to_json = {}
    common_wer_path = wer_table.get_value_by_row_index_col_key(i, 'common')
    # 读取info_list
    common_info_list = WerInfo.do_load_info_list_from_wer_path(common_wer_path)
    # 对common_info_list进行处理
    WerInfo.do_handle_info_list(common_info_list)
    item_dict_to_json = {}
    fake_big_dict_to_json['speechio_' + str(i)] = item_dict_to_json
    # 得到noun_dict
    noun_set, noun_dict = do_extract_nouns_jieba(common_info_list)
    sorted_items = sorted(noun_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_items = sorted_items[:400]
    sorted_noun_dict = {item[0]: item[1] for item in sorted_items if len(item[0]) > 1}
    item_dict_to_json['noun_dict'] = sorted_noun_dict
    for partition in ['short', 'long', 'repeat', 'messy', 'encourage']:
        partition_wer_path = wer_table.get_value_by_row_index_col_key(i, partition)
        partition_info_list = WerInfo.do_load_info_list_from_wer_path(partition_wer_path)
        # 对partition_info_list进行处理
        WerInfo.do_handle_info_list(partition_info_list)
        res_dict1, res_dict2, total_num = WerInfo.do_diff_analysis(common_info_list, partition_info_list,
                                                                   sorted_noun_dict)
        utils_file.logging_print(total_num)
        item_dict_to_json[partition] = {}
        item_dict_to_json[partition]['res_dict1'] = res_dict1
        item_dict_to_json[partition]['res_dict2'] = res_dict2
        item_dict_to_json[partition]['total_num'] = total_num
    return fake_big_dict_to_json



def get_big_info_json(down:int, stage:int):
    """
    耗费时间的信息只需要得到一次,然后存下来, 就不用每次分析重新生成一遍
    :return:
    """
    # big_dict_to_json = utils_file.load_dict_from_json('data/big_diff_info_d2s2.json')
    big_dict_to_json = {}
    wer_table = get_wer_path_table(f"./data/wer_path_d{down}s{stage}.json")
    for i in range(27):
        if i == 25:
            print(f'not handle speechio_{i}')
            continue
        key = 'speechio_' + str(i)
        if key in big_dict_to_json:
            utils_file.logging_print(f'key {key} already in big_dict_to_json, skipping')
            continue
        fake_big_dict_to_json = handle_speechio_(i, wer_table)
        big_dict_to_json.update(fake_big_dict_to_json)
        utils_file.write_dict_to_json(big_dict_to_json, f'data/big_diff_info_d{down}s{stage}.json')
    print(big_dict_to_json)


def add_wer_info_to_final_res_xlsx(final_res_xlsx_path,wer_table):
    """"""
    res_list1 = []
    res_list2 = []
    for input_num in range(0, 27):
        if input_num == 25:
            print(f'not handle speechio_{input_num}')
            continue
        utils_file.logging_print(f'start analysis speechio_{input_num}')
        dataset_name = f'speechio_{input_num}'
        # 首先得到common的info_list
        common_wer_path = wer_table.get_value_by_row_index_col_key(input_num, 'common')
        wer_common, replace_common, delete_common, insert_common = utils_file.get_wer_all_from_wer_file(common_wer_path)
        replace_common, delete_common, insert_common = int(replace_common), int(delete_common), int(insert_common)
        print(wer_common, replace_common, delete_common, insert_common )
        # 然后得到short对应的info_list ,和common进行对比分析
        for partition in ['short', 'long', 'repeat', 'messy', 'encourage']:
            wer_path = wer_table.get_value_by_row_index_col_key(input_num, partition)
            wer_partition, replace_partition, delete_partition, insert_partition = utils_file.get_wer_all_from_wer_file(
                wer_path)
            replace_partition, delete_partition, insert_partition = int(replace_partition), int(delete_partition), int(insert_partition)
            print(wer_partition, replace_partition, delete_partition, insert_partition)
            res_list1.append(f"{wer_partition}/{wer_common}={wer_partition / wer_common:.2f};{partition}/common")
            temp_item = 'S:{},D:{},I:{}'.format(f'{replace_partition}/{replace_common}={replace_partition / replace_common:.2f}', f'{delete_partition}/{delete_common}={delete_partition / delete_common:.2f}',
                                                f'{insert_partition}/{insert_common}={insert_partition / insert_common:.2f}')
            res_list2.append(temp_item)
    res_dict = utils_file.load_data_from_xlsx(final_res_xlsx_path)
    for i, key in enumerate(res_dict.keys()):
        value_list = res_dict[key]
        value_list.insert(1, res_list1[i])
        value_list.insert(2, res_list2[i])
        res_dict[key] = value_list

    output_file_path =final_res_xlsx_path
    utils_file.write_dict_to_xlsx(res_dict, output_file_path, cols_pattern=True)

def main(down:int, stage:int):
    wer_table = get_wer_path_table(f"./data/wer_path_d{down}s{stage}.json")
    input_json_path = f"data/big_diff_info_d{down}s{stage}.json"
    big_dict_to_json = utils_file.load_dict_from_json(input_json_path)
    desc_path = 'data/desc.scp'
    max_list_length = -1
    desc_dict = utils_file.load_dict_from_scp(desc_path)
    big_res_dict = {}  # col pattern
    for i in range(27):
        if i == 25:
            print(f'not handle speechio_{i}')
            continue
        print(f'handling speechio {i}')
        dataset_name = f'speechio_{i}'
        big_res_dict[dataset_name] = ["short"]
        big_res_dict[desc_dict[dataset_name]] = ["long"]
        big_res_dict[f'{dataset_name}.'] = ["repeat"]
        big_res_dict[f'{dataset_name}..'] = ["messy"]
        big_res_dict[f'{dataset_name}...'] = ["encourage"]
        for partition in ['short', 'long', 'repeat', 'messy', 'encourage']:
            item_dict = big_dict_to_json['speechio_' + str(i)][partition]
            total_num = item_dict['total_num']
            the_res_dict = item_dict['res_dict1']
            the_res_dict2 = item_dict['res_dict2']
            num_res_dict = sum([item['frequency'] for item in the_res_dict.values()])
            num_res_dict2 = sum([item['frequency'] for item in the_res_dict2.values()])
            err_words_right = the_res_dict.keys()
            print(err_words_right)
            err_words_right_dict = {}
            for err_word in err_words_right:
                err_words_right_dict[err_word] = the_res_dict[err_word]['errs'][0]['err_left']
            print(err_words_right_dict)

            err_words_error = the_res_dict2.keys()
            print(err_words_error)
            utils_file.logging_print(
                f'speechio_{i} {partition} right num:{num_res_dict}, error num:{num_res_dict2},total:{total_num}')
            if partition == 'short':
                the_key = dataset_name
            elif partition == 'long':
                the_key = desc_dict[dataset_name]
            elif partition == 'repeat':
                the_key = f'{dataset_name}.'
            elif partition == 'messy':
                the_key = f'{dataset_name}..'
            elif partition == 'encourage':
                the_key = f'{dataset_name}...'
            else:
                the_key = dataset_name
            list_i = big_res_dict[the_key]
            list_i.append(f'提升词汇的次数:{num_res_dict}')
            list_i.append(f'未提升词的次数:{num_res_dict2}')
            list_i.append(f'提升比例:{num_res_dict / (num_res_dict + num_res_dict2)}')
            list_i.append(f'正确词汇->common不正确的词汇:')
            for key, value in err_words_right_dict.items():
                list_i.append(f'{key}->{value}')
            big_res_dict[the_key] = list_i
            if max_list_length < len(list_i):
                max_list_length = len(list_i)
        for key, value_list in big_res_dict.items():
            if len(value_list) < max_list_length:
                for i in range(0, max_list_length - len(value_list)):
                    value_list.append("")
        output_file_path = f"data/final_analysis_result_d{down}s{stage}.xlsx"
        utils_file.write_dict_to_xlsx(big_res_dict, output_file_path, cols_pattern=True)
        add_wer_info_to_final_res_xlsx(output_file_path, wer_table)


if __name__ == '__main__':
    get_big_info_json(down=8,stage=3)
    main(down=8,stage=3)
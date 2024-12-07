from gxl_ai_utils.utils import utils_file

from align import do_align
from mingmingshiti import do_fenci


def my_print(*args):
    print(*args, flush=True)


def get_respresent_str(lab_list, rec_list):
    str_list = []
    for i, item in enumerate(lab_list):
        if item == "[]":
            str_list.append(rec_list[i])
        else:
            str_list.append(item)
    str_i = "".join(str_list)
    return str_i


class Info:
    def __init__(self, key, wer, lab_str, rec_str):
        lab_str = lab_str.replace("lab: ", '')
        rec_str = rec_str.replace("rec: ", '')
        self.key = key
        self.wer = wer
        self.lab = lab_str
        self.rec = rec_str
        self.lab_list, self.rec_list = do_align(lab_str, rec_str)
        self.str_represent = get_respresent_str(self.lab_list, self.rec_list)
        self.words, self.words_index = do_fenci(self.str_represent)
        self.diff_dict = compare_lab_rec_diff(self)
        self.lab_without_blank = self.lab.replace(" ", "")

    def __str__(self):
        return f'{self.key} {self.wer} {self.lab} {self.rec}'

    def show_info(self):
        my_print("-" * 100)
        my_print('key: ', self.key)
        my_print('wer: ', self.wer)
        my_print('lab: ', self.lab)
        my_print('rec: ', self.rec)
        my_print('lab_list: ', self.lab_list)
        my_print('rec_list: ', self.rec_list)
        my_print('str_represent: ', self.str_represent)
        my_print('words: ', self.words)
        my_print('words_index: ', self.words_index)
        # my_print('diff_dict: ')
        # utils_file.print_dict(self.diff_dict)
        my_print("-" * 100)


def read_info_from_file(file_path):
    info_list = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("utt:"):
                key = lines[i].split()[1]
                wer = float(lines[i + 1].split()[1])
                lab_str = lines[i + 2].strip()
                rec_str = lines[i + 3].strip()
                info = Info(key, wer, lab_str, rec_str)
                info_list.append(info)
                i += 5
            else:
                i += 1
    return info_list


from mingmingshiti import extract_nouns


def read_data():
    """"""
    # for index, partition in enumerate(['common','short','long','repeat','messy','encourage']):
    #     print("handling {}".format(partition))
    #     for i in range(27):
    #         key = f'speechio_{i}'
    #         res = input(f"请输入speechio_{i}的{partition}的wer path\n:")
    #         if key not in res_dict:
    #             res_dict[key] = []
    #         res_dict[key].append(res)
    #         print(f"输入内容为：{res}，是否重新输入（Y/*）")
    #         if input() == 'Y':
    #             key = f'speechio_{i}'
    #             res = input(f"请输入speechio_{i}的{partition}的wer path\n:")
    #             print(f"输入内容为：{res}")
    #             if key not in res_dict:
    #                 res_dict[key] = []
    #             res_dict[key][index] = res
    # res_dict = utils_file.load_data_from_xlsx(output_path2,return_cols=False)
    # utils_file.write_dict_to_json(res_dict, output_path)

    # output_path = "./data/wer_paths.json"
    # output_path2 = "./data/wer_paths.xlsx"
    # res_dict = utils_file.load_dict_from_json(path=output_path)
    # res_dict2 = {}
    # output_dir = "./data/wer_paths_store/"
    # for key in res_dict:
    #     if key == "speechio":
    #         continue
    #     print(f'handle {key}')
    #     for index, path in enumerate(res_dict[key]):
    #         if key not in res_dict2:
    #             res_dict2[key] = []
    #         output_path_i = path.replace("/home/work_nfs8/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v15/5_epoch",output_dir)
    #         utils_file.makedir_for_file(output_path_i)
    #         utils_file.copy_file(path, f"{output_dir}/{key}_{index}.txt")
    #         res_dict2[key].append(output_path_i)
    # utils_file.write_dict_to_json(res_dict2, "./data/wer_path_d2s3.json")
    # utils_file.write_dict_to_xlsx(res_dict2, "./data/wer_paths2.xlsx", cols_pattern=False)

    # res_dict = utils_file.load_dict_from_json('./data/wer_path_d2s3.json')
    # for key,value in res_dict.items():
    #     if key == 'speechio':
    #         continue
    #     print(f'{key}:{value}')
    #     new_values= []
    #     for path_i in value:
    #         path_2 = path_i.replace("./data/wer_paths_store//","./data/wer_paths_store/")
    #         new_values.append(path_2)
    #     res_dict[key] = new_values
    # utils_file.write_dict_to_json(res_dict, "./data/wer_path_d2s3.json")
    # utils_file.write_dict_to_xlsx(res_dict, "./data/wer_paths2.xlsx", cols_pattern=False)


def get_word_index_by_char_index(char_index, words_index_list):
    for i, word_list in enumerate(words_index_list):
        if char_index in word_list:
            return i
    return -1


def compare_lab_rec_diff(info: Info):
    res_dict = {
    }
    str_i = info.str_represent
    lab_list, rec_list = info.lab_list, info.rec_list
    if len(lab_list) != len(rec_list):
        print("lab_list和rec_list长度不一致")
        print(lab_list)
        print(rec_list)
        exit(0)
    words_list, words_index_list = do_fenci(str_i)
    for i in range(len(lab_list)):
        if lab_list[i] != rec_list[i]:
            word_index = get_word_index_by_char_index(i, words_index_list)
            word_involved = words_list[word_index]
            if word_involved in res_dict:
                continue
            word_index_involved = words_index_list[word_index]
            try:
                word_chars_lab = [lab_list[i] for i in word_index_involved]
                word_chars_rec = [rec_list[i] for i in word_index_involved]
            except:
                print(word_index_involved)
                info.show_info()
                continue
            word_lab = "".join(word_chars_lab)
            word_rec = "".join(word_chars_rec)
            if '[]' in word_chars_lab:
                tag = "insert"
            elif '[]' in word_chars_rec:
                tag = "delete"
            else:
                tag = "replace"
            res_dict[word_involved] = {
                "lab": word_lab,
                "rec": word_rec,
                "tag": tag,
            }
    return res_dict


def showing():
    info_list = read_info_from_file("./data/wer_paths_store/test_step_44268_speechio_short-prompt_2/speechio_6/wer")
    print(len(info_list))
    str_list = []
    for info in info_list:
        str_list.append(info.lab.replace(" ", ""))
        print(info.lab.replace(" ", ""))
    # for info in info_list:
    #     info.show_info()


from Gxl2DTable import Gxl2DTable

wer_path_info_path = "./data/wer_paths2.json"
dict_temp1 = {'speechio': ['common', 'short', 'long', 'repeat', 'messy', 'encourage']}
dict_temp2 = utils_file.load_dict_from_json(wer_path_info_path)
dict_temp1.update(dict_temp2)
wer_table = Gxl2DTable.load_from_json(dict_temp1)


def do_diff_analysis(info_list1, info_list2, res_dict):
    """"""
    my_res_dict = {}
    my_res_dict2 = {}
    # 得到keys
    keys = [item.key for item in info_list1]
    info_list1_dict = {item.key: item for item in info_list1}
    info_list2_dict = {item.key: item for item in info_list2}
    total_err_word = 0
    for key in utils_file.tqdm(keys, total=len(keys), desc="analysising", disable=False):
        """"""
        if not key in info_list2_dict:
            utils_file.logging_print(f'{key} not in info_list2_dict, skipping')
            continue
        info1 = info_list1_dict[key]
        info2 = info_list2_dict[key]
        diff_dict1 = info1.diff_dict
        diff_dict2 = info2.diff_dict
        if len(diff_dict1) == 0 and len(diff_dict2) == 0:
            continue
        err_word_in_1 = list(diff_dict1.keys())
        err_word_in_2 = list(diff_dict2.keys())
        for err_word in err_word_in_1:
            if err_word in res_dict:
                total_err_word += 1
                if err_word in err_word_in_2:
                    err_item = {"key": key, "right": err_word, 'err_left': diff_dict1[err_word]['rec'],
                                'err_right': diff_dict2[err_word]['rec'], 'lab': info1.lab_without_blank}
                    my_res_dict2[err_word] = {
                        "frequency": my_res_dict2[err_word]["frequency"] + 1 if err_word in my_res_dict2 else 1,
                        "errs": my_res_dict2[err_word]["errs"] + [err_item] if err_word in my_res_dict2 else [err_item],
                    }
                else:
                    err_item = {"key": key, "right": err_word, 'err_left': diff_dict1[err_word]['rec'],
                                'err_right': err_word, 'lab': info1.lab_without_blank}
                    my_res_dict[err_word] = {
                        "frequency": my_res_dict[err_word]["frequency"] + 1 if err_word in my_res_dict else 1,
                        "errs": my_res_dict[err_word]["errs"] + [err_item] if err_word in my_res_dict else [err_item],
                    }
    return my_res_dict, my_res_dict2, total_err_word


def analysis_for_one_speechio(input_num: int):
    """"""
    desc_path = 'data/desc.scp'
    max_list_length = -1
    desc_dict = utils_file.load_dict_from_scp(desc_path)
    big_res_dict = {}  # col pattern
    for input_num in range(0, 27):
        utils_file.logging_print(f'start analysis speechio_{input_num}')
        dataset_name = f'speechio_{input_num}'
        big_res_dict[dataset_name] = ["short"]
        big_res_dict[desc_dict[dataset_name]] = ["long"]
        big_res_dict[f'{dataset_name}.'] = ["repeat"]
        big_res_dict[f'{dataset_name}..'] = ["messy"]
        big_res_dict[f'{dataset_name}...'] = ["encourage"]

        # 首先得到common的info_list
        wer_path = wer_table.get_value_by_row_index_col_key(input_num, 'common')
        info_list = read_info_from_file(wer_path)
        lab_without_blank_list = [item.lab_without_blank for item in info_list]
        # 得到命名实体的集合
        res_set, res_dict = extract_nouns(lab_without_blank_list)
        sorted_items = sorted(res_dict.items(), key=lambda item: item[1], reverse=True)
        sorted_items = sorted_items[:400]
        res_dict = {item[0]: item[1] for item in sorted_items if len(item[0]) > 1}

        # 然后得到short对应的info_list ,和common进行对比分析
        for partition in ['short', 'long', 'repeat', 'messy', 'encourage']:
            wer_path = wer_table.get_value_by_row_index_col_key(input_num, partition)
            info_list_short = read_info_from_file(wer_path)
            the_res_dict, the_res_dict2, total = do_diff_analysis(info_list, info_list_short, res_dict)
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
                f'speechio_{input_num} {partition} right num:{num_res_dict}, error num:{num_res_dict2},total:{total}')
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
        output_file_path = "data/final_res2.xlsx"
        utils_file.write_dict_to_xlsx(big_res_dict, output_file_path, cols_pattern=True)


def add_wer_info():
    """"""
    res_list1 = []
    res_list2 = []
    for input_num in range(0, 27):
        utils_file.logging_print(f'start analysis speechio_{input_num}')
        dataset_name = f'speechio_{input_num}'
        # 首先得到common的info_list
        common_wer_path = wer_table.get_value_by_row_index_col_key(input_num, 'common')
        wer_common, replace_common, delete_common, insert_common = utils_file.get_wer_all_from_wer_file(common_wer_path)
        print(wer_common, replace_common, delete_common, insert_common )
        # 然后得到short对应的info_list ,和common进行对比分析
        for partition in ['short', 'long', 'repeat', 'messy', 'encourage']:
            wer_path = wer_table.get_value_by_row_index_col_key(input_num, partition)
            wer_partition, replace_partition, delete_partition, insert_partition = utils_file.get_wer_all_from_wer_file(
                wer_path)
            print(wer_partition, replace_partition, delete_partition, insert_partition)
            res_list1.append(wer_partition / wer_common)
            temp_item = 'S:{},D:{},I:{}'.format(replace_partition / replace_common, delete_partition / delete_common,
                                                insert_partition / insert_common)
            res_list2.append(temp_item)
    res_dict = utils_file.load_data_from_xlsx('./data/final_res2 (1).xlsx')
    for i, key in enumerate(res_dict.keys()):
        value_list = res_dict[key]
        value_list.insert(1, res_list1[i])
        value_list.insert(2, res_list2[i])
        res_dict[key] = value_list

    output_file_path = "data/final_res2 (2).xlsx"
    utils_file.write_dict_to_xlsx(res_dict, output_file_path, cols_pattern=True)


if __name__ == '__main__':
    add_wer_info()

from gxl_ai_utils.utils import utils_file


def pop_first_item_in_dict(dict_info):
    first_key = next(iter(dict_info))
    return first_key, dict_info.pop(first_key)


class Gxl2DTable:

    def __init__(self):
        self.table_name = None
        self.col_head_list = None
        self.row_head_list = None
        self.dict_info = {}

    @staticmethod
    def load_from_xlsx(file_path):
        gxl2dtable = Gxl2DTable()
        gxl2dtable.dict_info = utils_file.load_data_from_xlsx(file_path, return_cols=False)
        gxl2dtable.init_info()
        return gxl2dtable

    @staticmethod
    def load_from_json(file_path, col_pattern=False):
        """
        默认按照行存储
        :param col_pattern:
        :param file_path:
        :return:
        """

        if isinstance(file_path, dict):
            dict_info = file_path
        else:
            dict_info = utils_file.load_dict_from_json(file_path)
        gxl2dtable = Gxl2DTable()
        if col_pattern:
            table_name, row_key_list = pop_first_item_in_dict(dict_info)
            new_dict = {}
            keys = dict_info.keys()
            new_dict[table_name] = keys
            for i in range(len(row_key_list)):
                new_dict[row_key_list[i]] = [dict_info[key][i] for key in keys]

            gxl2dtable.dict_info = new_dict
            gxl2dtable.init_info()
            return gxl2dtable
        gxl2dtable.dict_info = dict_info
        gxl2dtable.init_info()
        return gxl2dtable

    def init_info(self):
        self.table_name, self.col_head_list = pop_first_item_in_dict(self.dict_info)
        self.row_head_list = list(self.dict_info.keys())

    def get_value_by_key(self, row_key, col_key):
        col_index = self.col_head_list.index(col_key)
        return self.dict_info[row_key][col_index]

    def get_value_by_index(self, row_index, col_index):
        row_key = self.row_head_list[row_index]
        return self.dict_info[row_key][col_index]

    def get_value_by_rowkey_col_index(self, row_key, col_index):
        return self.dict_info[row_key][col_index]

    def get_value_by_row_index_col_key(self, row_index, col_key):
        col_index = self.col_head_list.index(col_key)
        row_key = self.row_head_list[row_index]
        return self.dict_info[row_key][col_index]

    def get_dict_info(self):
        res_dict = {self.table_name: self.col_head_list}
        for i in range(len(self.row_head_list)):
            res_dict[self.row_head_list[i]] = self.dict_info[self.row_head_list[i]]
        return res_dict

    def write_to_xlsx(self, file_path):
        utils_file.write_dict_to_xlsx(self.get_dict_info(), file_path, cols_pattern=False)

    def write_to_json(self, file_path):
        utils_file.write_dict_to_json(self.get_dict_info(), file_path)

    def insert_row_index(self, row_head, row_list, row_index):
        self.dict_info[row_head] = row_list
        self.row_head_list.insert(row_index, row_head)

    def insert_col_index(self, col_head, col_list, col_index):
        self.col_head_list.insert(col_index, col_head)
        for i in range(len(col_list)):
            self.dict_info[self.row_head_list[i]].insert(col_index, col_list[i])

    def show_self(self):
        print('-----------------start--------------------')
        str = ""
        for col_head in self.col_head_list:
            str += f"{col_head}\t\t"
        first_line = f"{self.table_name}\t{str}\n"
        print(first_line)
        for row_head in self.row_head_list:
            str = ""
            for i in range(len(self.dict_info[row_head])):
                str += f"{self.dict_info[row_head][i]}\t\t"
            print(f"{row_head}\t{str}")
        print('-----------------end--------------------')
    def show_col_head(self):
        for col_head in self.col_head_list:
            print(col_head)

    def show_row_head(self):
        for row_head in self.row_head_list:
            print(row_head)

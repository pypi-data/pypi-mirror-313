from gxl_ai_utils.utils import utils_file
def do_handle():
    """"""
    hb_text_path = "/home/work_nfs8/xlgeng/new_workspace/bsmu_template/wenet_SALMONN/examples/librispeech/salmonn/data/test_huawei_accent/text_hb"
    js_text_path = "/home/work_nfs8/xlgeng/new_workspace/bsmu_template/wenet_SALMONN/examples/librispeech/salmonn/data/test_huawei_accent/text_js"
    xian_text_path = "/home/work_nfs8/xlgeng/new_workspace/bsmu_template/wenet_SALMONN/examples/librispeech/salmonn/data/test_huawei_accent/text_xian"
    hpy_text_path = "/home/work_nfs14/xlgeng/new_workspace/wenet_gxl_salmonn/examples/aishell/salmonn/exp/salmonn_v14/0_epoch/test_step_18564/huawei_accent/text"
    # 得到hpy_little_text
    js_hpy_path = "./data/test_huawei_accent/js_hpy"
    xian_hpy_path = "./data/test_huawei_accent/xian_hpy"
    hb_hpy_path = "./data/test_huawei_accent/hb_hpy"
    utils_file.makedir_for_file(js_hpy_path)
    utils_file.copy_file(hb_hpy_path, "./data/test_huawei_accent/hb_text")
    utils_file.copy_file(xian_hpy_path, "./data/test_huawei_accent/xian_text")
    utils_file.copy_file(js_hpy_path, "./data/test_huawei_accent/js_text")
    big_hpy_text_dict = utils_file.load_dict_from_scp(hpy_text_path)
    hb_dict = utils_file.load_dict_from_scp(hb_text_path)
    js_dict = utils_file.load_dict_from_scp(js_text_path)
    xian_dict = utils_file.load_dict_from_scp(xian_text_path)
    hb_hpy_dict = {}
    js_hpy_dict = {}
    xian_hpy_dict = {}
    for k, v in big_hpy_text_dict.items():
        if k in hb_dict:
            hb_hpy_dict[k] = v
        if k in js_dict:
            js_hpy_dict[k] = v
        if k in xian_dict:
            xian_hpy_dict[k] = v
    utils_file.write_dict_to_scp(hb_hpy_dict, hb_hpy_path)
    utils_file.write_dict_to_scp(js_hpy_dict, js_hpy_path)
    utils_file.write_dict_to_scp(xian_hpy_dict, xian_hpy_path)

if __name__ == "__main__":
    do_handle()


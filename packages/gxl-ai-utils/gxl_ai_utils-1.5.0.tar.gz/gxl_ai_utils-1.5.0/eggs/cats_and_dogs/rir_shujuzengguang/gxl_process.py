from gxl_ai_utils.utils import utils_file

def test_do_get_row_scp():
    """"""
    wav_dir = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/wav_row"
    wav_scp_path = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/scp/wav.scp"
    wav_dict = utils_file.do_get_scp_for_wav_dir(wav_dir)
    utils_file.write_dict_to_scp(wav_dict, wav_scp_path)
    text_scp_path = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/scp/text"
    text_dict = {}
    for key, wav_path in  wav_dict.items():
        text_dict[key] = "我是耿雪龙"
    utils_file.write_dict_to_scp(text_dict, text_scp_path)

def test_do_get_fbank_k2():
    """"""
    fbank_dir = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/k2/fbank"
    manifest_dir = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/k2/manifest"
    wav_scp_path = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/scp/wav.scp"
    text_scp_path = "/Users/xuelonggeng/Desktop/xlgeng_workspace/gxl_ai_utils/eggs/cats_and_dogs/rir_shujuzengguang/data/scp/text"
    utils_file.do_make_data4icefall(wav_scp_path, text_scp_path, fbank_dir=fbank_dir, manifest_dir=manifest_dir)



from gxl_ai_utils.utils import utils_file

def main():
    """"""
    aishell_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474388291.nohup"
    test_net_1_path = '/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474366751.nohup'
    test_meeting_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474379990.nohup"
    aishell2_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474394176.nohup"
    test_net_2_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474553662.nohup"
    speechio_1_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474572191.nohup"
    speechio_4_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474612859.nohup"
    speechio_3_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474617134.nohup"
    speechio_2_path = "/home/work_nfs8/xlgeng/new_workspace/yzli_template/wenet/examples/aishell/s0/output/run_res/run_gxl_1714474621289.nohup"
    hpy_data_dict = {
        'aishell1': aishell_path,
        'aishell2': aishell2_path,
        'test_net_1': test_net_1_path,
        'test_net_2': test_net_2_path,
        'test_meeting': test_meeting_path,
        'speechio_1': speechio_1_path,
        'speechio_2': speechio_2_path,
        'speechio_3': speechio_3_path,
        'speechio_4': speechio_4_path
    }
    output_dir_root = "./data_output"
    utils_file.makedir_sil(output_dir_root)
    for key, hpy_path in hpy_data_dict.items():
        lines = utils_file.load_list_file_clean(hpy_path)
        hype_text_lines = []
        for line in lines:
            items = line.strip().split()
            if len(items) < 5:
                continue
            hype_text_lines.append(f'{items[3]} {"".join(items[4:])}')
        temp_output_dir = f'{output_dir_root}/{key}'
        utils_file.makedir_sil(temp_output_dir)
        utils_file.write_list_to_file(hype_text_lines, f'{temp_output_dir}/hype_text')
    scp_dir = '/home/work_nfs8/xlgeng/data/scp_test'
    for key in hpy_data_dict.keys():
        text_true = f'{scp_dir}/{key}/text'
        text_hpy = f'{output_dir_root}/{key}/hype_text'
        utils_file.do_compute_wer(text_true, text_hpy,f'{output_dir_root}/{key}')
if __name__ == '__main__':
    main()
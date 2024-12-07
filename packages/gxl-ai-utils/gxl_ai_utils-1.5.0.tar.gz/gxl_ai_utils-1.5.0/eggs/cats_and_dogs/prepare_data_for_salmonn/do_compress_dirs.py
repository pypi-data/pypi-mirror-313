from gxl_ai_utils.utils import utils_file

input_dir = "/mnt/disk1/yhdai/data_zipformer/batch03"
dir_path_list, _ = utils_file.do_listdir(input_dir, return_path=True
                                         )
runner = utils_file.GxlDynamicThreadPool()
for dir_path in dir_path_list:
    runner.add_task(utils_file.do_compress_directory_to_tar_gz, [dir_path])
runner.run()

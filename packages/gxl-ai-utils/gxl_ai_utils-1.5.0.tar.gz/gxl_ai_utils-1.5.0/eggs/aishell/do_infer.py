from gxl_ai_utils.gxl_infer_wenet.gxl_infer import GxlInterfacer

gxl_interfacer = GxlInterfacer('infer_config.yaml')
from gxl_ai_utils.utils import utils_file, utils_data

if __name__ == '__main__':
    gxl_interfacer.run_infer()

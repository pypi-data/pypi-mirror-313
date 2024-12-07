import random
import numpy as np
import pyroomacoustics as pyr
# import gpuRIR
import os
import torchaudio
import soundfile as sf
import tqdm


def MC_RIR_generate(clean):
    target_sr = 16000

    # limit_rir_point = int(limit_rir_time * target_sr)

    while True:
        room_x = round(random.uniform(5, 8), 1)
        room_y = round(random.uniform(3, 5), 1)
        room_z = round(random.uniform(3, 4), 1)
        room_dim = [room_x, room_y, room_z]

        rt60_tgt = round(random.uniform(0.2, 1.2), 2)
        try:
            e_absorption, max_order = pyr.inverse_sabine(rt60_tgt, room_dim) #0.1614901799818631 95
        except Exception:
            print("Not able to generate rt60: %f, room_x is %f, room_y is %f, room_z is %f. Regenerating..." % (
            rt60_tgt, room_x, room_y, room_z))
            continue
        else:
            break

    while True:
        room = pyr.ShoeBox(room_dim, absorption=e_absorption, fs=target_sr, max_order=max_order)
        mic_location_x = room_x / 2.0
        mic_location = np.array([mic_location_x, 1.0, 1.5])
        room.add_microphone(mic_location)

        target_location_x = round(random.uniform(1, room_x - 1), 2)
        target_location_y = round(random.uniform(1, room_y - 1), 2)
        target_location_z = 1.5
        target_location = [target_location_x, target_location_y, target_location_z]

        try:
            room.add_source(target_location, signal=clean)
        except Exception:
            print("Source should be inside the room. Regenerating...")
            continue
        else:
            break

    rir_target = room.compute_rir()
    room.image_source_model()
    room.simulate()
    target = room.mic_array.signals
    rt60 = room.measure_rt60()

    return target, rir_target, room, rt60


# def gpusimulate(self, signal, rir, room):
#     if rir.ndim < 3:
#         rir = np.expand_dims(rir, axis=0)
#     rir = rir.astype(np.float32)
#     signal = signal.astype(np.float32)
#     signal = gpuRIR.simulateTrajectory(signal, rir)
#     signal = signal.T
#     return signal


def generate_signal(target_path, rirtarget_path):
    target, sr = sf.read(target_path)
    new_target, rir_target, room, rt60 = MC_RIR_generate(target)
    # target_mic = gpusimulate(target, rir_target, room)
    sf.write(rirtarget_path, new_target.T, sr)


from gxl_ai_utils.utils import utils_file

def little_handle(wav_dict,output_dir):
    for key in tqdm.tqdm(wav_dict.keys(),desc="handle_wav_scp",total=len(wav_dict)):
        wav_path = wav_dict[key]
        if key.endswith('.wav'):
            new_wav_name = key
        else:
            new_wav_name = key + '.wav'
        new_wav_path = os.path.join(output_dir, new_wav_name)
        generate_signal(wav_path, new_wav_path)


def handle_wav_scp(wav_scp_path,output_dir):
    utils_file.makedir_sil(output_dir)
    wav_dict = utils_file.load_dict_from_scp(wav_scp_path)
    wav_dict_list = utils_file.do_split_dict(wav_dict,7)
    # runner = utils_file.GxlFixedThreadPool(7)
    # for wav_dict_i in wav_dict_list:
    #     runner.add_thread(little_handle,[wav_dict_i,output_dir])
    # runner.start()
    little_handle(wav_dict_list[0],output_dir)



if __name__ == "__main__":
    import pdb; pdb.set_trace()
    now = utils_file.do_get_now_time()
    input_scp_path= "/home/work_nfs8/xlgeng/data/scp_test/aishell/wav.scp"
    handle_wav_scp(input_scp_path, 'data/wav_output/aishell_test')
    utils_file.logging_print('耗时: %s' % (utils_file.do_get_now_time() - now))
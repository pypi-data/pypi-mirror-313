import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor

import psutil
import torch
from funasr_onnx import Fsmn_vad

torch.set_num_threads(1)
vad_models = dict()


class Vad:
    def __init__(self, vad_model_path, num_process=0, batch_size=40, use_cpu=False, device_id=0):
        """
        vad_model_path: vad模型路径
        batch_size: 返回时的batch_size
        num_process: 进程数量
        use_cpu: 是否使用cpu进行推理，默认为False, 即使用gpu进行推理
        """
        self.batch_size = batch_size

        self.use_cpu = use_cpu
        if use_cpu:
            self.vad_model = Fsmn_vad(vad_model_path)
            self.executor = ProcessPoolExecutor(
                max_workers=self.get_optimal_workers() if num_process == 0 else num_process,
                initializer=self.init_model,
                initargs=(self.vad_model,)
            )
        else:
            self.vad_model = Fsmn_vad(vad_model_path, device_id=device_id)

    def __del__(self):
        """
        析构函数，确保进程池正确关闭
        """
        if hasattr(self, 'executor'):
            self.executor.shutdown()

    @staticmethod
    def init_model(model):
        """
        初始化模型
        :param model: 模型实例
        :return:
        """
        pid = multiprocessing.current_process().pid
        vad_models[pid] = model

    @staticmethod
    def vad_process(audio_file):
        """
        vad处理音频文件
        :param audio_file: 音频文件
        :return:
        """
        pid = multiprocessing.current_process().pid
        return vad_models[pid](audio_file)

    @staticmethod
    def get_optimal_workers():
        """
        动态获取workers节点数
        :return:
        """
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 65:
            return cpu_count // 4
        return cpu_count // 2

    def silence_detection(self, audios):
        """
        使用已存在的进程池对音频文件进行静音检测
        :param audios: 音频文件列表
        :return: 静音文件结果 及 有效文件（非静音、以.mp3为后缀）列表
        """
        valid_audios = []
        tmp_ls = []

        if not audios:
            raise ValueError("vad in progress, audios list can't be empty")
        # 若利用cpu多进程进行处理
        if self.use_cpu:
            futures = []
            for input_file in audios:
                futures.append([input_file, self.executor.submit(self.vad_process, input_file)])
            for finish in futures:
                if finish[1].result()[0] and finish[0].endswith(".mp3"):
                    valid_audios.append(finish[0])
                else:
                    tmp_ls.append({"key": os.path.basename(finish[0]).split(".")[0], "text": ""})
        # 使用gpu进行处理
        else:
            for audio in audios:
                res = self.vad_model(audio)
                if res[0] and audio.endswith(".mp3"):
                    valid_audios.append(audio)
                else:
                    tmp_ls.append({"key": os.path.basename(audio).split(".")[0], "text": ""})
        res_ls = [tmp_ls[i:i + self.batch_size] for i in range(0, len(tmp_ls), self.batch_size)]
        return valid_audios, res_ls


if __name__ == "__main__":
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--vad_model_path', type=str, default="../llm_weight/fsmn-vad")
    parser.add_argument('--num_process', type=int, default=1)
    parser.add_argument("--batch_size", type=int, default=20)
    parser.add_argument('--data_path', type=str, default="../dataset/test_data/silence")
    args = parser.parse_args()
    audios = sorted(os.listdir(args.data_path))
    audios = list(map(lambda x: args.data_path + '/' + x, audios))
    vad = Vad(vad_model_path=args.vad_model_path, num_process=args.num_process, batch_size=args.batch_size)
    start_time = time.time()
    result = vad.silence_detection(audios)
    end_time = time.time()
    print("result is: {}".format(result[:2]))
    print("推理速度为 {} ms/条".format((end_time - start_time) * 1000 / len(audios)))

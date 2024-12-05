import os

import librosa
import numpy as np
import torch
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from models import Transfer_Cnn14_16k

classes_num = 2
labels = ["normal", "panting"]


class Voiceprint:
    def __init__(self, voiceprint_model_path, sample_rate=16000, window_size=512, hop_size=160, mel_bins=64, fmin=50,
                 fmax=8000, freeze_base=False, device="cuda:0", batch_size=40):
        self.sample_rate = sample_rate
        self.batch_size = batch_size
        self.device = device
        self.checkpoint = torch.load(voiceprint_model_path)
        self.model = Transfer_Cnn14_16k(sample_rate=sample_rate, window_size=window_size, hop_size=hop_size,
                                        mel_bins=mel_bins, fmin=fmin, fmax=fmax, classes_num=2, freeze_base=freeze_base)
        self.model.load_state_dict(self.checkpoint['model'])
        # 并行
        if 'cuda' in str(device):
            self.model.to(device)
            self.model = torch.nn.DataParallel(self.model)

    @staticmethod
    def move_data_to_device(x, device):
        if 'float' in str(x.dtype):
            x = torch.Tensor(x)
        elif 'int' in str(x.dtype):
            x = torch.LongTensor(x)
        else:
            return x
        return x.to(device)

    def inference(self, audios):
        res_ls = []
        if not audios:
            raise ValueError("voiceprint in progress, audios list can't be empty")
        batch = [audios[i:i + self.batch_size] for i in range(0, len(audios), self.batch_size)]
        for input_files in batch:
            # 逐个加载音频文件，并将其拼接
            waveforms = []
            max_length = 0
            # 第一次遍历获取最大长度
            for file in input_files:
                waveform, _ = librosa.core.load(file, sr=self.sample_rate, mono=True)
                max_length = max(max_length, len(waveform))

            # 第二次遍历进行padding
            tmp_ls = []
            for file in input_files:
                waveform, _ = librosa.core.load(file, sr=self.sample_rate, mono=True)
                # 使用零填充使所有音频长度一致
                if len(waveform) < max_length:
                    waveform = np.pad(waveform, (0, max_length - len(waveform)), 'constant')
                waveforms.append(waveform)
            waveforms = np.array(waveforms)
            waveforms = self.move_data_to_device(waveforms, self.device)
            # 前向传播
            with torch.no_grad():
                self.model.eval()
                batch_output_dict = self.model(waveforms)
            clipwise_output = batch_output_dict['clipwise_output'].data.cpu().numpy()
            for file, output in zip(input_files, clipwise_output):
                sorted_indexes = np.argsort(output)[::-1]
                pred_label = np.array(labels)[sorted_indexes[0]]
                tmp_ls.append({"key": os.path.basename(file).split(".")[0], "label": pred_label})
            if tmp_ls:
                res_ls.append(tmp_ls)
        return res_ls


if __name__ == "__main__":
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--voiceprint_model_path', type=str, default="../llm_weight/PANNs/panns_cnn14_16k.pth")
    parser.add_argument("--batch_size", type=int, default=20)
    parser.add_argument("--data_path", type=str, default="../dataset/test_data/panting")
    args = parser.parse_args()
    audios = sorted(os.listdir(args.data_path))
    audios = list(map(lambda x: args.data_path + '/' + x, audios))
    vp = Voiceprint(voiceprint_model_path=args.voiceprint_model_path,
                    batch_size=args.batch_size)
    start_time = time.time()
    result = vp.inference(audios)
    end_time = time.time()
    print("result is: {}".format(result[:10]))
    print("推理速度为: {}ms/条".format((end_time - start_time) * 1000 / len(audios)))

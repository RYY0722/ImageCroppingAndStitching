import numpy as np
from PIL import Image
import cv2
import glob, os
from pathlib import Path
import shutil

from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import shutil
import json
import matplotlib.pyplot as plt
class StitchAndCalJson(object):
    def __init__(self):
        return
    def stich(self, path, meta):
        with open(path / meta) as json_file:
            data = json.load(json_file)
        # path = self.cp.run(path)
        path = Path(path)
        if (path / 'comb').exists():
            shutil.rmtree(path / 'comb')
        (path / 'comb').mkdir(exist_ok=False)
        i = 0
        files = [file for file in path.glob('*_sr.png')]
        for ID, lsts in data.items():
            totalX, totalY = lsts[-1][1], lsts[-1][3]
            res = np.zeros((totalX, totalY))
            cnt_map = np.zeros((totalX, totalY))
            for lst in lsts:
                x1, x2, y1, y2 = lst
                # name = "{}_{}_{}_sr.png".format(ID, x1, y1)
                img = cv2.imread(str(path / files[i]),cv2.IMREAD_GRAYSCALE)
                i += 1
                try:
                    res[x1:x2, y1:y2] += img
                    cnt_map[x1:x2, y1:y2] += 1
                    # print(lst, 'ok')
                except:
                    print(lst, 'not ok')  
            img = Image.fromarray((res/cnt_map).astype(np.uint8))
            img.save(path / 'comb' / (ID+"_sr.png"))
        
        return
    def cal(self, path):
        psnr_sum = 0
        ssim_sum = 0
        cnt = 0
        hrs = sorted(glob.glob(os.path.join(path, '*_hr.png')))
        srs = sorted(glob.glob(os.path.join(path, '*_sr.png')))
        # assert len(hrs) == len(lrs), 'hr != lr'
        assert len(hrs) == len(srs), 'hr != sr'
        for i in range(len(hrs)):
            hr = cv2.imread(hrs[i],cv2.IMREAD_GRAYSCALE)
            # lr = cv2.imread(lrs[i], cv2.IMREAD_GRAYSCALE)
            sr = cv2.imread(srs[i],cv2.IMREAD_GRAYSCALE)
            _psnr = psnr(hr, sr)
            _ssim = ssim(hr, sr)
            psnr_sum += _psnr
            ssim_sum += _ssim
            cnt += 1
        return {'psnr':psnr_sum/cnt,'ssim':ssim_sum/cnt}
            
            
        return 
    def stichAndCal(self, path, per, patch_width, target_size):
        self.stich(path, per, patch_width, target_size)
        return self.cal(os.path.join(path, 'comb'))
if __name__ == '__main__':
    sac = StitchAndCalJson()
    path = Path(r'D:\Exercise\Python\datasets\six\paired\whole-v2\whole-sr\save_results')
    meta_path = Path(r'D:\Exercise\Python\datasets\six\paired\whole-v2\processed\meta.txt')
    data = sac.stich(path, meta_path)
    # data = sac.cal(path)
    print(data)
        
        
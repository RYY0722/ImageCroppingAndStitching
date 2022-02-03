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
from . import StitchAndCalFlex

class StitchAndCalJson(StitchAndCalFlex):
    def __init__(self):
        super(StitchAndCalJson, self).__init__()
    def stich(self, path, meta, cats):
        with open(path / meta) as json_file:
            data = json.load(json_file)
        # path = self.cp.run(path)
        try:
            data = data['test']
        except:
            pass
        path = Path(path)
        if (path / 'comb').exists():
            shutil.rmtree(path / 'comb')
        (path / 'comb').mkdir(exist_ok=False)
        for cat in cats:
            files = sorted([file for file in path.glob('*_{}.png'.format(cat))])
            i=0
            for ID, lsts in data.items():
                totalX, totalY = lsts[-1][1], lsts[-1][3]
                res = np.zeros((totalX, totalY))
                cnt_map = np.zeros((totalX, totalY))
                # hr = cv2.imread(r'D:\Exercise\Python\datasets\STDR\eehpc\harnet\imgs\{}_hr.png'.format(ID))
                for lst in lsts:
                    x1, x2, y1, y2 = lst
                    # name = "{}_{}_{}_sr.png".format(ID, x1, y1)
                    img = cv2.imread(str(path / files[i]),cv2.IMREAD_GRAYSCALE)
                    i+=1
                    try:
    
                        res[x1:x2, y1:y2] += img
                        # hr_patch = hr[x1:x2, y1:y2]
                        cnt_map[x1:x2, y1:y2] += 1
                        # fig = plt.figure(figsize=(1,2))
                        # fig.add_subplot(1,2,1)
                        # plt.imshow(img)
                        # fig.add_subplot(1,2,2)
                        # plt.imshow(hr_patch)   
                        # print(lst, 'ok')
                    except:
                        print(lst, 'not ok')  
                img = Image.fromarray((res/cnt_map).astype(np.uint8))
                img.save(path / 'comb' / (ID+"_{}.png".format(cat)))
        
        return
   
    def stichAndCal(self, path, meta, cats):
        self.stich(path, meta, cats)
        return self.cal(path / 'comb')
if __name__ == '__main__':
    sac = StitchAndCalJson()
    path = Path(r'D:\Exercise\Python\0models\MultiTask\v2\mul-02-0.3\eval-outer\save_results')
    meta_path = Path(r'D:\Exercise\Python\datasets\six\paired\parts\meta-160s65.txt')
    data = sac.stichAndCal(path, meta_path, ['hr','lr','sr'])
    # data = sac.stich(path, meta_path)
    # data = sac.cal(path)
    print(data)
        
        

import sys
sys.path.append('D:\\')
import numpy as np
from PIL import Image
import cv2
import glob, os
from pathlib import Path
import shutil
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import shutil
class StitchAndCal(object):
    def __init__(self):
        return
    def stich(self, path, per, patch_width, target_size):
        # path = self.cp.run(path)
        path = Path(path)
        if (path / 'comb').exists():
            shutil.rmtree(path / 'comb')
        (path / 'comb').mkdir(exist_ok=False)
        per = per
        width = patch_width
        img_size = target_size
        stride = (img_size - width) // (per-1)
        input_list_bak = sorted([item for item in path.glob("*.png")])
        for ind in range(3):
            input_list = [input_list_bak[i] for i in range(len(input_list_bak)) if i % 3 == ind]
            for i in range(len(input_list)//per**2):
                # create figure
                # fig = plt.figure(figsize=(290, 290))
                
                sub_lst = input_list[i*per**2:(i+1)*per**2]
                img = np.zeros((img_size,img_size))
                cnt_map = np.zeros((img_size,img_size))
                for y in range(per):
                    for x in range(per): # 第j行，第k列
                        # fig.add_subplot(per, per, x*per+y+1 )
                        name = sub_lst[x*per+y]
                        sub = np.asarray(Image.open(name))#.convert("L"))
                        # r, g, b = Image.fromarray(sub).split()
                        # sub = Image.merge("RGB", (r, g, b))
                        offset_x = x * stride
                        offset_y = y * stride
                        # plt.imshow(sub)
                        # plt.axis('off')
                        # plt.title(str(x*per+y+1))
                        try:
                            img[offset_x:offset_x+width, offset_y:offset_y+width] += sub
                            cnt_map[offset_x:offset_x+width, offset_y:offset_y+width] += 1
                        except:
                            pass
                        # ori = img[offset_x:offset_x+width, offset_y:offset_y+width]
                        # tmp = np.zeros((80,80,2))
                        # tmp[:,:,0] = ori; tmp[:,:,1] = sub
                        # img[offset_x:offset_x+width, offset_y:offset_y+width] = np.max(tmp, axis=2)
                # img = Image.fromarray((img/cnt_map).astype(np.uint8)).tobitmap()
                img = Image.fromarray((img/cnt_map).astype(np.uint8))
                # img = img.astype(np.uint8)
                
                # if ind == 2:
                #     img.save(path+'comb/'+str(i).zfill(3)+"_lrsr.png")
                if ind == 1:
                    img.save(path / 'comb' / (str(i).zfill(3)+"_lr.png"))
                elif ind == 0:
                    img.save(path / 'comb' / (str(i).zfill(3)+"_hr.png"))
                elif ind == 2:
                    img.save(path / 'comb' / (str(i).zfill(3)+"_sr.png"))
        return
    def cal(self, path):
        psnr_sum = 0
        ssim_sum = 0
        cnt = 0
        hrs = sorted(glob.glob(os.path.join(path, '*_hr.png')))
        # hrs = [os.path.join(path, file) for file in hrs]
        # lrs = sorted(glob.glob(os.path.join(path, '*_lr.png')))
        # lrs = [os.path.join(path, file) for file in lrs]
        srs = sorted(glob.glob(os.path.join(path, '*_sr.png')))
        # srs = [os.path.join(path, file) for file in srs]
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
    sac = StitchAndCal()
    path = r'D:\Exercise\Python\0models\comb'
    print(path)
    # data = sac.stich(path=path, 
    #                         per=3, patch_width=160, target_size=290)
    data = sac.cal(path)
    print(data)
        
        

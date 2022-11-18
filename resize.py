import os
import cv2

def resize(file_path,out_path,factor=1):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    pic_names = os.listdir(file_path)
    print(pic_names)
    H = 2244
    W = 1275
    new_H = H // factor
    new_W = W // factor
    for pic_name in pic_names:
        img = cv2.imread(os.path.join(file_path,pic_name),cv2.IMREAD_COLOR)
        print("debug here::",img.shape)
        target = cv2.resize(img,(new_W,new_H))
        cv2.imwrite(os.path.join(out_path,pic_name),target)

if __name__ == '__main__':
    resize('flower','new_flower',6)
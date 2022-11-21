import binascii
import cv2
import serial
from PIL import Image
import os
import numpy as np

os.system('sh ./stop_sys_ttyPS0.sh')

def run_action(cmd):
    ser = serial.Serial("/dev/ttyPS0", 9600, timeout=5)
    cnt_err = 0
    while 1:
        test_read = ser.read()
        print('test_read', test_read)
        cnt_err += 1
        if test_read == b'\xa3' or cnt_err == 50:
            break
    
    if cnt_err == 50:
        print('can not get REQ')
    else:
        print('read REQ finished!')
        ser.write(cmd2data(cmd))
        print('send action ok!')
    ser.close()
    
def crc_calculate(package):
    crc = 0
    for hex_data in package:

        b2 = hex_data.to_bytes(1, byteorder='little')
        crc = binascii.crc_hqx(b2, crc)

    return [(crc >> 8), (crc & 255)]    # 校验位两位

def cmd2data(cmd):
    cnt=0
    cmd_list=[]
    for i in cmd:
        cnt+=1
        cmd_list+=[ord(i)]
    cmd_list = [0xff,0xff]+[(cnt+5)>>8,(cnt+5)&255]+[0x01,(cnt+1)&255,0x03]+cmd_list
    cmd_list = cmd_list+crc_calculate(cmd_list)
    return cmd_list

def wait_req():
    ser = serial.Serial("/dev/ttyPS0", 9600, timeout=5)
    while 1:
        test_read=ser.read()
        if test_read== b'\xa3' :
            print('read REQ finished!') 
            break

def angle(dir):
    """根据方向向量计算朝向角。
    Args:
        dir (list): 方向向量。
    Returns:
        float: 朝向角。
    """
    X = dir[:,0]
    Y = dir[:,1]
    theta = np.arctan(Y/X)
    if X < 0 and Y < 0:
        return theta / 3.1415 * 180 - 180
    if X < 0 and Y > 0:
        return theta / 3.1415 * 180 + 180
    return theta / 3.1415 * 180


def angle_dir(angle):
    """根据朝向角计算方向向量
    Returns:
        dir(list):方向向量。
    """
    X = np.cos(angle*3.1415/180)
    Y = np.sin(angle*3.1415/180)
    
    dir = np.concatenate([X,Y],axis=0)
    dir = np.array([dir])
    
    return dir
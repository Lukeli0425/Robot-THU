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
        if test_read== b'\xa3' or cnt_err == 50:
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
    cmd_list=[0xff,0xff]+[(cnt+5)>>8,(cnt+5)&255]+[0x01,(cnt+1)&255,0x03]+cmd_list
    cmd_list=cmd_list+crc_calculate(cmd_list)
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
        
# 场地内测的边长约为294cm x 294cm；内部：
# - 地面上分布有ID为20~42的tag
# - 障碍物上分布有ID为43~71的tag

def load_tag_pos():
    M = 294.1
    def expand(LL):
        LL.append(0)
        a = np.array([
            [0, 0, 0], [5, 0, 0], [5, 5, 0], [0, 5, 0]
        ])
        return a + np.array(LL)
    
    def expand2(LL, face):
        x_dir_LUT = {
            "x": [0,1,0],
            "y": [-1,0,0],
            "-x": [0,-1,0],
            "-y": [1,0,0]
        }
        x_dir = x_dir_LUT[face]
        LL.append(0)
        h = np.array([0,0,-35])
        y = np.array([0, 0, -5])
        x = np.array(x_dir) * 5
        a = np.array([
            np.zeros(3), x, x + y, y
        ]) + h
        return a + np.array(LL)

    tag_poses = {}
    tag_poses['20'] = expand([0.9, 1.2])
    tag_poses['21'] = expand([1.75, 94])
    tag_poses['22'] = expand([1.6, 194.1])
    tag_poses['23'] = expand([0.8, 288.0])
    tag_poses['24'] = expand([94.8, 1.6])
    tag_poses['25'] = expand([92.5, 93.2])
    tag_poses['27'] = expand([94.7, M-5.8])
    tag_poses['28'] = expand([195.0, 1.2])
    tag_poses['29'] = expand([191.6, 92.7])
    tag_poses['30'] = expand([193.6, M-98.0])
    tag_poses['31'] = expand([194.9, M-6.6])
    tag_poses['32'] = expand([M-6, 1.9])
    tag_poses['33'] = expand([M-6.6, M-99.9])
    tag_poses['34'] = expand([M-6, M-6.3])
    tag_poses['35'] = expand([93.6, 47.7])
    tag_poses['36'] = expand([67.3, 174.7])
    tag_poses['37'] = expand([143.3, 156.6])
    tag_poses['38'] = expand([140.4, M-51.4])
    tag_poses['39'] = expand([238.6, M-54.0])
    tag_poses['40'] = expand([235.9, 136.7])
    tag_poses['41'] = expand([238.8, 52.6])
    tag_poses['42'] = expand([52.9, M-53.0])


    tag_poses['43'] = expand2([24.22 + 25, 35.7], 'x')
    tag_poses['44'] = expand2([24.22 + 25, 35.7 + 25], 'y')
    tag_poses['45'] = expand2([59, 112], '-y')
    tag_poses['46'] = expand2([59 + 25, 112], 'x')
    tag_poses['47'] = expand2([59 + 25, 112 + 25], 'y')
    tag_poses['48'] = expand2([59, 112 + 25], '-x')
    tag_poses['49'] = expand2([90.7, M-70.6-25], '-y')
    tag_poses['50'] = expand2([90.7 + 25, M-70.6-25], 'x')
    tag_poses['51'] = expand2([90.7 + 25, M-70.6], 'y')
    tag_poses['52'] = expand2([90.7, M-70.6], '-x')
    tag_poses['53'] = expand2([7.0, M-48 - 25], '-y')
    tag_poses['54'] = expand2([7.0 + 25, M-48 - 25], 'x')
    tag_poses['55'] = expand2([M-85.1-25, 113], '-y')
    tag_poses['56'] = expand2([M-85.1-25, 113+25], '-x')
    tag_poses['57'] = expand2([M-85.1, 113+25], 'y')
    tag_poses['58'] = expand2([M-85.1, 113], 'x')
    tag_poses['59'] = expand2([M-9.1-25, 73.2], '-y')
    tag_poses['60'] = expand2([M-9.1-25, 73.2+25], '-x')
    tag_poses['61'] = expand2([M-9.1, 73.2+25], 'y')
    tag_poses['62'] = expand2([M-6.6-25, M-126.3], '-x')
    tag_poses['63'] = expand2([M-6.6, M-126.3], 'y')
    tag_poses['64'] = expand2([M-6.6-25, M-126.3-25], '-y')
    tag_poses['65'] = expand2([M-62-25, M-17.6-25], '-y')
    tag_poses['66'] = expand2([M-62-25, M-17.6], '-x')
    # tag_poses['67'] = expand2([M-62, M-17.6], 'x')
    tag_poses['67'] = expand2([M-62, M-17.6], 'y')
    tag_poses['68'] = expand2([7.0 + 25, M-48], 'y')
    tag_poses['69'] = expand2([M-114-25, 30.3 + 25], '-x')
    tag_poses['70'] = expand2([M-114, 30.3 + 25], 'y')
    # tag_poses['71'] = expand2([M-114, 30.3], 'y')
    tag_poses['71'] = expand2([M-114, 30.3], 'x')
    return tag_poses


screen_center_relative_pos = [16, -10]
# 按钮相对于TAG左下角的位置（cm）
button_relative_pos = [7, -9]

class ExtraInfoLoader():

    def __init__(self, 
                 tagpos_dict: dict,
                 button_relative_pos: list = [7, -9],
                 screen_center_relative_pos: list = [16, -10],
                 ) -> None:
        """
        params:
        - tagpos_dict: provider by function `load_tag_pos`
        - button_relative_pos: location of button relative to the lower-left corner of the tag
        - screen_center_relative_pos: location of button relative to the lower-left corner of the tag
        """
        self.tagpos_dict = tagpos_dict
        self.button_rloc = button_relative_pos
        self.screen_rloc = screen_center_relative_pos
        
    @staticmethod
    def get_normal(point):
        x = point[1] - point[0]
        y = point[2] - point[1]
        return ExtraInfoLoader.cross_prod(y, x)

    @staticmethod
    def cross_prod(x, y):
        z = np.array([
            x[1] * y[2] - x[2] * y[1],
            x[2] * y[0] - x[0] * y[2],
            x[0] * y[1] - x[1] * y[0]
        ])
        z = z / (((z * z).sum())**0.5)
        return z

    def get_extra_info(self, tag_id: int):
        """
        ### params:
        - tag_id: integer tag id

        ### returns:
        - button_pos: 3D location of the center of the button corresponding to this tag
        - screen_pos: 3D location of the center of the screen corresponding to this tag
        - face: a 3D unit vector representing the facing direction of this tag
        """

        assert isinstance(tag_id, int) and tag_id >= 43 and tag_id <=71, \
            "tag_id must be an integer within [43, 71]"

        tag_loc = self.tagpos_dict[str(tag_id)]
        LL = tag_loc[0,...]

        face = self.get_normal(tag_loc)
        actual_y = np.array([0, 0, -1])
        actial_x = self.cross_prod(face, actual_y)

        # 按钮的坐标
        button_pos = LL + actual_y * self.button_rloc[1] + actial_x * self.button_rloc[0]
        # 屏幕中心的坐标
        screen_pos = LL + actual_y * self.screen_rloc[1] + actial_x * self.screen_rloc[0]

        return button_pos, screen_pos, face
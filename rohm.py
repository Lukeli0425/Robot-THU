# ================ 罗姆楼新场地 ================
# 本文件包含：
# - load_tag_pos: tag的具体坐标
# - obstacles: 所有障碍物坐标（包含大礼堂）
# - ExtraInfoLoader: 获取屏幕和按钮的坐标信息（更正了数据）
# ==============================================

import numpy as np

def load_tag_pos():
    M = 294.1
    def expand(LL):
        LL.append(0)
        a = np.array([
            [.0, .0, .0], [5., 0., 0.], [5., 5., 0.], [0., 5., 0.]
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

    tag_poses['20'] = expand([5, 5])
    tag_poses['21'] = expand([5, 95])
    tag_poses['22'] = expand([5, 195])
    tag_poses['23'] = expand([5, M-10])
    tag_poses['25'] = expand([95, 5])
    tag_poses['24'] = expand([95, 95])
    tag_poses['27'] = expand([95, M-10])
    tag_poses['28'] = expand([195, 5])
    tag_poses['29'] = expand([195, 95])
    tag_poses['30'] = expand([195, 195])
    tag_poses['31'] = expand([195, M-10])
    tag_poses['32'] = expand([M-10, 5])
    tag_poses['33'] = expand([M-10, 195])
    tag_poses['76'] = expand([M-10, M-10])
    tag_poses['77'] = expand([95, 50])
    tag_poses['78'] = expand([70, M-120])
    tag_poses['79'] = expand([145, 155])
    tag_poses['80'] = expand([145, 195])
    tag_poses['85'] = expand([150, M-40])
    tag_poses['81'] = expand([235, 195])
    tag_poses['82'] = expand([235, 145])
    tag_poses['83'] = expand([235, 50])
    tag_poses['84'] = expand([50, 195])

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
    tag_poses['67'] = expand2([M-62, M-17.6], 'y')
    tag_poses['68'] = expand2([7.0 + 25, M-48], 'y')
    tag_poses['69'] = expand2([M-114-25, 30.3 + 25], '-x')
    tag_poses['70'] = expand2([M-114, 30.3 + 25], 'y')
    tag_poses['71'] = expand2([M-114, 30.3], 'x')
    return tag_poses

# 场地内测的边长约为294cm x 294cm；内部：
# - 地面上分布有ID为20~42的tag
# - 障碍物上分布有ID为43~71的tag


# 给选手提供的用于路径规划的数据：
# - [X_min, X_max], [Y_min, Y_max]为场地在x和y两个方向的边界（单位：cm）
# - obstacles为所有障碍物的四个顶脚的平面坐标（单位：cm）

X_min, X_max = 0, 294.1
Y_min, Y_max = 0, 294.1
        
obstacles = [[[24.22, 35.75], [48.22, 35.75], [48.22, 59.75], [24.22, 59.75]], 
             [[59, 112], [83, 112], [83, 136], [59, 136]], 
             [[156.2, 30.3], [180.2, 30.3], [180.2, 54.3], [156.2, 54.3]], 
             [[261.1, 73.2], [285.1, 73.2], [285.1, 97.2], [261.1, 97.2]], 
             [[185.1, 113], [209.1, 113], [209.1, 137], [185.1, 137]], 
             [[263.6, 143.9], [287.6, 143.9], [287.6, 167.9], [263.6, 167.9]], 
             [[90.7, 199.6], [114.7, 199.6], [114.7, 223.6], [90.7, 223.6]], 
             [[7, 222.2], [31, 222.2], [31, 246.2], [7, 246.2]], 
             [[208.2, 252.6], [232.2, 252.6], [232.2, 276.6], [208.2, 276.6]],
             [[180.9, 204.2], [207.2, 204.2], [207.2, 214.2], [180.9, 214.2]]]


# ===== 这两个数据可以直接拿去用 =====
# 屏幕的中心相对于TAG右下角的位置（cm）
screen_center_relative_pos = [17, -5]
# 按钮相对于TAG右下角的位置（cm）
button_relative_pos = [7, -10]


class ExtraInfoLoader():

    def __init__(self, 
                 tagpos_dict: dict,
                 button_relative_pos: list = [7, -10],
                 screen_center_relative_pos: list = [17, -5],
                 ) -> None:
        """
        params:
        - tagpos_dict: provider by function `load_tag_pos`
        - button_relative_pos: location of button relative to the lower-right corner of the tag
        - screen_center_relative_pos: location of button relative to the lower-right corner of the tag
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


# if __name__ == '__main__':
#     # test
#     EIL = ExtraInfoLoader(load_tag_pos())
#     for id in [43, 46, 52, 51, 66, 67, 71]:
#         b, s, f = EIL.get_extra_info(id)
#         print(f'------tag {id}------\nb: {b}\ns: {s}\nf: {f}\n')

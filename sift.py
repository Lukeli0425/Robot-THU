import cv2
import os
from matplotlib import pyplot as plt
'''sift特征点检测+特征匹配'''

# def cross_check(img1, img2):

#     # 创建sift特征检测对象
#     sift = cv2.SIFT_create()

#     # 检测特征点 描述符
#     kp1, des1 = sift.detectAndCompute(img1, None)
#     kp2, des2 = sift.detectAndCompute(img2, None)

#     # 采用match匹配时会包含错误匹配，可以剔除掉一部分
#     BF = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)   # 交叉最佳匹配
#     matches = BF.match(des1, des2)
#     img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, img1)
#     return img3


def knn_match(img1, img2):
    ratio = 0.40

    # 创建sift特征检测对象
    sift = cv2.SIFT_create()

    # 检测特征点 描述符
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    BF = cv2.BFMatcher()
    matches = BF.knnMatch(des1, des2, k=2)  # k邻近匹配
    # 如果两个匹配相距的距离足够大，则认为是一个正确的匹配
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append([m])
    # print("good.size() = ",len(good))
    # img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, img1)
    return len(good)


if __name__ == '__main__':
    pic_names = [i.split('.')[0] for i in os.listdir('new_flower')]
    print('使用神奇的SIFT算法和KNN算法结合判断匹配点数...')
    img2 = cv2.imread('3.jpg', 1)
    for i in pic_names:
        img1 = cv2.imread('./new_flower/%s.jpg'%i, 1)
        good = knn_match(img1, img2)
        print("这是 %s !!!"%i," 匹配数目为:",good)

    # img3 = cross_check(img1, img2)
    
    # plt.imshow(img3)
    # plt.show()



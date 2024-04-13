import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图片
img_name = 'E:\\甲骨文智能识别中原始拓片单字自动分割与识别研究\\1_Pre_test\\h02060.jpg'
img = cv2.imread(img_name)

# 图像灰度化处理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 对图像进行高斯滤波
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# 对图像进行二值化处理
ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 结构元素
kernel = np.ones((3, 3), np.uint8)

# 开运算去除噪声
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# 寻找轮廓
contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 绘制轮廓
contour_img = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 2)

# 显示图像
plt.imshow(contour_img)
plt.show()

# 保存处理后的图像
cv2.imwrite('E:\\甲骨文智能识别中原始拓片单字自动分割与识别研究\\1_Pre_test\\result\\processed_' + img_name, contour_img)
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 假设的图像路径
image_paths = ['h02060.jpg', 'w01637.jpg', 'w01870.jpg']


# 自定义函数实现的简化版本
def find_largest_contour(thresholded_img):
    # 寻找轮廓
    contours, _ = cv2.findContours(thresholded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 根据轮廓面积排序并返回最大轮廓
    return max(contours, key=cv2.contourArea)


def create_bone_mask(img, largest_contour):
    # 创建一个全黑遮罩层
    mask = np.zeros(img.shape, dtype=np.uint8)
    # 将最大轮廓填充为白色
    cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
    return mask


def extract_characters(img, mask):
    # 应用遮罩层提取字符
    return cv2.bitwise_and(img, mask)


def remove_numbers(image, mask):
    # Invert mask to fill everything outside the main contour
    inverted_mask = cv2.bitwise_not(mask)

    # Create a mask for the bottom region of the image where the numbers are
    height, width = image.shape
    number_mask = np.zeros_like(image, dtype=np.uint8)
    bottom_region_height = int(0.2 * height)  # 10% of the image height
    number_mask[-bottom_region_height:] = 255  # Fill the bottom region with white

    # Combine the masks to isolate the numbers
    combined_mask = cv2.bitwise_or(inverted_mask, number_mask)

    # Fill the regions with the background color
    filled_image = cv2.bitwise_or(image, combined_mask)

    return filled_image


# 处理每张图像
for path in image_paths:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Image at path {path} could not be read.")
        continue

    # 应用高斯模糊和Otsu二值化
    blurred = cv2.GaussianBlur(img, (9, 9), 0)
    _, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 寻找最大轮廓
    largest_contour = find_largest_contour(thresholded)
    # 创建甲骨文遮罩层
    mask = create_bone_mask(img, largest_contour)
    # 提取甲骨文字符
    characters = extract_characters(img, mask)
    # 移除图像底部的数字
    final_img = remove_numbers(characters, mask)

    # 显示最终结果
    plt.imshow(final_img, cmap='gray')
    plt.title("Final Image")
    plt.show()

    # 保存处理后的图像到'/mnt/data/'路径下
    output_path = f'processed_{path.split("/")[-1]}'
    cv2.imwrite(output_path, final_img)

# 打印所有处理后图像的路径
processed_image_paths = [f'processed_{path.split("/")[-1]}' for path in image_paths]
print(processed_image_paths)

import numpy as np
from PIL import Image
import os
def convert_images_to_numpy(image_folder, output_folder,size=(128, 128)):
    os.makedirs(output_folder, exist_ok=True)
    for image_name in os.listdir(image_folder):
        if image_name.endswith('.png') or image_name.endswith('.jpg'):
            image_path = os.path.join(image_folder, image_name)
            img = Image.open(image_path).convert('RGB')  # 转换为RGB模式
            img = img.resize((128, 128))  # 如果需要，可以调整图像大小
            img_array = np.array(img)  # 转换为NumPy数组
            output_path = os.path.join(output_folder, f'{os.path.splitext(image_name)[0]}.npy')
            np.save(output_path, img_array)

# 调用该函数将图像转换为.npy格式
convert_images_to_numpy(f'{imgdataceleba}', f'{traindatapathN}')
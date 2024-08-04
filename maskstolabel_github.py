import os
import cv2
import numpy as np

# Set your category names
class_names = ['background', 'cracks']
class_ids = {name: id for id, name in enumerate(class_names)}
# Usually id = 0 is the background, It doesn't need to appear in the annotations
# If you need the 0 in your annotations, change it to false
skip_id_zero = True

# Your mask image path
mask_image_dir = '/share/hel/home/muhammad-liaqat/crackandpot/crackandpot/masks/train'
# Output YOLO txt path
output_dir = '/share/hel/home/muhammad-liaqat/crackandpot/crackandpot/labels/train'

os.makedirs(output_dir, exist_ok=True)

def find_contours(img, class_id):
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if len(img.shape) != 2:
        raise ValueError("The input image must be grayscale")

    mask = np.zeros_like(img, dtype=np.uint8)
    mask[img == class_id] = 255
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

for filename in os.listdir(mask_image_dir):
    if filename.endswith(('.png','.jpg','.JPG')):
        img_path = os.path.join(mask_image_dir, filename)
        # img = cv2.imread(img_path)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        height, width = img.shape[:2]

        label_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.txt')
        with open(label_path, 'a') as f:
            for class_id in range(0, len(class_names)):
                # if skip_id_zero and class_id == 0:
                #     continue
                contours = find_contours(img, class_id)
                for cnt in contours:
                    coords = []
                    for point in cnt:
                        x, y = point[0]
                        x_norm = x / width
                        y_norm = y / height
                        coords.append(f'{x_norm} {y_norm}')
                    if coords:
                        f.write(f'{class_id} ' + ' '.join(coords) + '\n')

print('Label conversion completed @: ', output_dir)
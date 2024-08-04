import cv2
import os

def generate_label_files(image_dir, mask_dir, output_dir):
  """
  Generates label files for YOLOv8 from single-class masks.

  Args:
    image_dir: Path to the directory containing images.
    mask_dir: Path to the directory containing masks.
    output_dir: Path to the directory where label files will be saved.
  """
  for image_name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_name)

    filename, extension = os.path.splitext(image_name)
    extension_lower = extension.lower()
    image_name = f"{filename}{extension_lower}"

    if extension_lower == ".jpg":
        mask_path = os.path.join(mask_dir, image_name.replace(".jpg", ".png"))  # Assuming mask filename pattern
        output_path = os.path.join(output_dir, image_name.replace(".jpg", ".txt"))
    else:
      mask_path = os.path.join(mask_dir, image_name)  # Assuming mask filename pattern
      output_path = os.path.join(output_dir, image_name.replace(".png", ".txt"))

    # Load image and mask
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # Find contours (cracks/potholes) in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Write label file
    with open(output_path, "w") as label_file:
      for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        center_x = (x + w / 2) / image.shape[1]
        center_y = (y + h / 2) / image.shape[0]
        # label_file.write(f"0 {center_x} {center_y} {w / image.shape[1]} {h / image.shape[0]}\n")
        label_file.write("0 {} {} {} {}\n".format(center_x, center_y, w / image.shape[1], h / image.shape[0]))


# Example usage (replace paths with your actual directories)
image_dir = "/share/hel/home/muhammad-liaqat/crackandpot/crackandpot/images/train"
mask_dir = "/share/hel/home/muhammad-liaqat/crackandpot/crackandpot/masks/train"
output_dir = "/share/hel/home/muhammad-liaqat/crackandpot/crackandpot/labels/train"

generate_label_files(image_dir, mask_dir, output_dir)

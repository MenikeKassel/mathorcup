import csv
import os
from PIL import Image

# Define the paths for the images and labels
image_folder = 'E:\\ocdata\\3_Test\\Figures'
label_folder = 'E:\\pythonProject_mathorcup\\yolov9\\runs\\detect\\exp\\labels'
output_csv_path = 'E:\\pythonProject_mathorcup\\2\\result\\result.csv'  # Output CSV file named "11.csv"

# Function to get image size
def get_image_size(image_folder, image_filename):
    for ext in ['.jpg', '.jpeg', '.png']:
        image_path = os.path.join(image_folder, image_filename + ext)
        if os.path.isfile(image_path):
            with Image.open(image_path) as img:
                return img.size
    return None, None

# Function to convert YOLO format to original format
def convert_to_original_format(yolo_annotation, img_width, img_height):
    x_center, y_center, width, height = yolo_annotation[1:5]
    x_min = round((x_center - width / 2) * img_width)
    y_min = round((y_center - height / 2) * img_height)
    x_max = round((x_center + width / 2) * img_width)
    y_max = round((y_center + height / 2) * img_height)
    confidence =  1.0  # Adding default confidence
    return [x_min, y_min, x_max, y_max, confidence]


# Read all label files and convert annotations
converted_annotations = {}
for label_file in os.listdir(label_folder):
    if label_file.endswith('.txt'):
        base_filename = os.path.splitext(label_file)[0]
        label_file_path = os.path.join(label_folder, label_file)
        image_width, image_height = get_image_size(image_folder, base_filename)
        if image_width is not None and image_height is not None:
            with open(label_file_path, 'r') as file:
                annotations = [list(map(float, line.strip().split())) for line in file]
                converted_annotations[base_filename] = [
                    convert_to_original_format(ann, image_width, image_height) for ann in annotations
                ]

# Save the converted annotations to a CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['image_name', 'annotations'])
    for base_filename, anns in converted_annotations.items():
        # Convert each bounding box to a string and then join all with a delimiter (e.g., ";")
        all_anns = '; '.join(['[' + ', '.join(map(str, ann)) + ']' for ann in anns])
        writer.writerow([base_filename, all_anns])

output_csv_path

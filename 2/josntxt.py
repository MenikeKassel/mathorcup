import os
from PIL import Image
import json


def get_image_size(image_folder, image_filename):
    # Check for multiple possible image file extensions
    for ext in ['.jpg', '.jpeg', '.png']:
        image_path = os.path.join(image_folder, image_filename + ext)
        if os.path.isfile(image_path):
            with Image.open(image_path) as img:
                width, height = img.size
                return width, height, ext
    print(f"Image file not found for {image_filename}")
    return None, None, None


def convert_to_yolo_format(annotations, img_width, img_height):
    yolo_annotations = []
    for ann in annotations:
        # Calculate the center x, y coordinates, width and height and normalize them
        x_center = ((ann[0] + ann[2] )/ 2) / img_width
        y_center = ((ann[1] + ann[3] )/ 2) / img_height
        width = (ann[2]-ann[0] ) / img_width
        height = (ann[3] -ann[1] )/ img_height
        # Class label for oracle bone script is 0, change if there are more classes
        class_label = 0
        yolo_annotations.append([class_label, x_center, y_center, width, height])
    return yolo_annotations


def save_to_txt(yolo_annotations, txt_file):
    with open(txt_file, "w") as f:
        for annotation in yolo_annotations:
            line = " ".join(str(coord) for coord in annotation)
            f.write(line + "\n")


# Define the paths for the images and labels
# image_folder = "E:\\ocdata\\2_Train"
# label_folder = "E:\\ocdata\\2_Train"
# output_folder = "E:\\ocdata\\2_Train"
image_folder = "E:\\ocdata_origin\\img"
label_folder = "E:\\ocdata_origin\\train_label"
output_folder = "E:\\ocdata_origin\\img"
# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each JSON file in the label folder
for json_file in os.listdir(label_folder):
    if json_file.endswith('.json'):
        json_path = os.path.join(label_folder, json_file)

        # Open and read the JSON file
        with open(json_path, 'r') as file:
            annotation = json.load(file)

        # Retrieve the corresponding image size and extension
        img_name = annotation['img_name']
        img_width, img_height, img_ext = get_image_size(image_folder, img_name)

        # Skip files if the image was not found
        if img_width is None or img_height is None:
            continue

        # Convert annotations to YOLO format
        yolo_annotations = convert_to_yolo_format(annotation['ann'], img_width, img_height)

        # Create the output text file path
        txt_filename = os.path.splitext(json_file)[0] + '.txt'
        txt_path = os.path.join(output_folder, txt_filename)

        # Save annotations in YOLO format to the text file
        save_to_txt(yolo_annotations, txt_path)

print("Conversion complete.")

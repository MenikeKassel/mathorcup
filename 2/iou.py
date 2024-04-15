def calculate_iou(box1, box2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters:
    box1 : list or tuple, (x1, y1, x2, y2)
    box2 : list or tuple, (x1, y1, x2, y2)

    Returns:
    float
        in the range [0, 1]
    """
    # Determine the coordinates of the intersection rectangle
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The area of intersection
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # The area of both bounding boxes
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # The area of union
    union_area = box1_area + box2_area - intersection_area

    # Compute the IoU
    iou = intersection_area / union_area
    return iou
predicted_boxes = [[112, 111, 143, 169], [204, 49, 230, 114],[207, 128, 228, 167]]
true_boxes = [[102, 102, 146, 173], [201, 50, 224, 113], [200, 117, 229, 174]]

# Assuming the order of the boxes corresponds between predictions and ground truths
ious = [calculate_iou(pred, true) for pred, true in zip(predicted_boxes, true_boxes)]

print("IoUs for each box pair:", ious)

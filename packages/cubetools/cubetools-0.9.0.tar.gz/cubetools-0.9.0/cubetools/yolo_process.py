import numpy as np


def yolo_detection_postprocess(preds, nc, width_radio, height_radio, filter_threshold=0.25, iou_threshold=0.45):
    preds = preds.transpose([1, 0])

    all_boxes = None
    all_scores = None
    all_classes = None
    for cls in range(nc):
        bboxes = preds[preds[:, 4 + cls] > filter_threshold]
        if len(bboxes) > 0:
            boxes = bboxes[:, :4]
            scores = bboxes[:, 4 + cls]
            boxes = xywh2xyxy(boxes)
            boxes, scores = nms(boxes, scores, iou_threshold=iou_threshold)
            classes = np.array([cls] * boxes.shape[0])

            all_boxes = boxes if all_boxes is None else np.append(all_boxes, boxes, axis=0)
            all_scores = scores if all_scores is None else np.append(all_scores, scores, axis=0)
            all_classes = classes if all_classes is None else np.append(all_classes, classes, axis=0)

    if all_boxes is None:
        all_boxes = np.array([])
        all_scores = np.array([])
        all_classes = np.array([])
    else:
        all_boxes[:, 0] *= width_radio
        all_boxes[:, 1] *= height_radio
        all_boxes[:, 2] *= width_radio
        all_boxes[:, 3] *= height_radio

    return all_boxes, all_classes, all_scores


def xywh2xyxy(xywh):
    xyxy = np.copy(xywh)
    xyxy[:, 0] = xywh[:, 0] - xywh[:, 2] / 2
    xyxy[:, 1] = xywh[:, 1] - xywh[:, 3] / 2
    xyxy[:, 2] = xywh[:, 0] + xywh[:, 2] / 2
    xyxy[:, 3] = xywh[:, 1] + xywh[:, 3] / 2
    return xyxy


def nms(boxes, scores, iou_threshold, candidate_size=200):
    """
    Args:
        boxex (N, 4): boxes in corner-form.
        scores (N, 1): scores.
        iou_threshold: intersection over union threshold.
        candidate_size: only consider the candidates with the highest scores.
    Returns:
         picked: a list of indexes of the kept boxes
    """
    picked = []
    indexes = np.argsort(scores)
    indexes = indexes[::-1]
    indexes = indexes[:candidate_size]

    while len(indexes) > 0:
        current = indexes[0]
        picked.append(current)
        if len(indexes) == 1:
            break
        current_box = boxes[current, :]
        indexes = indexes[1:]
        rest_boxes = boxes[indexes, :]
        iou = iou_of(
            rest_boxes,
            np.expand_dims(current_box, axis=0),
        )
        indexes = indexes[iou <= iou_threshold]

    return boxes[picked, :], scores[picked]


def iou_of(boxes0, boxes1, eps=1e-5):
    """Return intersection-over-union (Jaccard index) of boxes.
    Args:
        boxes0 (N, 4): ground truth boxes.
        boxes1 (N or 1, 4): predicted boxes.
        eps: a small number to avoid 0 as denominator.
    Returns:
        iou (N): IoU values.
    """
    overlap_left_top = np.maximum(boxes0[..., :2], boxes1[..., :2])
    overlap_right_bottom = np.minimum(boxes0[..., 2:], boxes1[..., 2:])

    overlap_area = area_of(overlap_left_top, overlap_right_bottom)
    area0 = area_of(boxes0[..., :2], boxes0[..., 2:])
    area1 = area_of(boxes1[..., :2], boxes1[..., 2:])
    return overlap_area / (area0 + area1 - overlap_area + eps)


def area_of(left_top, right_bottom):
    """Compute the areas of rectangles given two corners.
    Args:
        left_top (N, 2): left top corner.
        right_bottom (N, 2): right bottom corner.

    Returns:
        area (N): return the area.
    """
    hw = np.clip((right_bottom - left_top), a_min=0.0, a_max=1.0)
    return hw[..., 0] * hw[..., 1]

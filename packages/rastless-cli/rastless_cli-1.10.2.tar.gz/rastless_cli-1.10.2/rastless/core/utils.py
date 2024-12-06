def merge_bbox_extent(bboxes: list) -> tuple[float, float, float, float]:
    bboxes = tuple(map(tuple, zip(*bboxes, strict=True)))

    return min(bboxes[0]), min(bboxes[1]), max(bboxes[2]), max(bboxes[3])

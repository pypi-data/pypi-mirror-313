# Table2HTML

A Python package that converts table images into HTML format using Object Detection model and OCR.

## Installation

```bash
pip install table2html
```

## Usage

### Initialize
```python
from table2html import Table2HTML

table_config = {
    "model_path": r"table2html\models\det_table_v1.pt",
    "confidence_threshold": 0.25,
    "iou_threshold": 0.7,
}

row_config = {
    "model_path": r"table2html\models\det_row_v0.pt",
    "confidence_threshold": 0.25,
    "iou_threshold": 0.7,
    "task": "detect",
}

column_config = {
    "model_path": r"table2html\models\det_col_v0.pt",
    "confidence_threshold": 0.25,
    "iou_threshold": 0.7,
    "task": "detect",
}

table2html = Table2HTML(table_config, row_config, column_config)
```

### Table Detection
```python
image = cv2.imread(r"table2html\images\sample.jpg")
detection_data = table2html.TableDetect(image)
# Output: [{"table_bbox": Tuple[int]}]

# Visualize table detection (first table)
from table2html.source import visualize_boxes
cv2.imwrite(
    "table_detection.jpg", 
    visualize_boxes(
        image, 
        [detection_data[0]["table_bbox"]], 
        color=(0, 0, 255),
        thickness=1
    )
)
```
Table detection result:

![Table Detection Example](table2html/images/table_detection.jpg)

### Structure Detection
```python
data = table2html.StructureDetect(image)
# Output: {
#   "cells": List[Dict],
#   "num_rows": int,
#   "num_cols": int,
#   "html": str
# }

# Visualize structure detection
from table2html.source import visualize_boxes
cv2.imwrite(
    "structure_detection.jpg", 
    visualize_boxes(
        image, 
        [cell['box'] for cell in data['cells']], 
        color=(0, 255, 0),
        thickness=1
    )
)

# Write HTML output
with open('table.html', 'w') as f:
    f.write(data["html"])
```

Structure detection result:

![Structure Detection Example](table2html/images/structure_detection.jpg)

HTML output: [extracted html](table2html/images/table_0.html).

### Full Pipeline
**Note:** The cell coordinates are relative to the cropped table image.
```python
table_crop_padding = 15
detection_data = table2html(image, table_crop_padding)
# Output: [{
#   "table_bbox": Tuple[int],
#   "cells": List[Dict],
#   "num_rows": int,
#   "num_cols": int,
#   "html": str
# }]

for i, data in enumerate(detection_data):
    table_image = crop_image(image, data["table_bbox"], table_crop_padding)
    cv2.imwrite(
        "table_detection.jpg",
        visualize_boxes(
            image,
            [data["table_bbox"]],
            color=(0, 0, 255),
            thickness=1
        )
    )
    cv2.imwrite(
        "structure_detection.jpg",
        visualize_boxes(
            table_image,
            [cell['box'] for cell in data['cells']],
            color=(0, 255, 0),
            thickness=1
        )
    )

    with open(f"table_{i}.html", "w") as f:
        f.write(data["html"])
```

## Input
- `image`: numpy.ndarray (OpenCV/cv2 image format)

## Outputs
A list of extracted tables in structured:
1. `table_bbox`: Tuple[int] - Bounding box coordinates (x1, y1, x2, y2) of the table
2. `cells`: List[Dict] - List of cell dictionaries, where each dictionary contains:
   - `row`: int - Row index
   - `column`: int - Column index
   - `box`: Tuple[int] - Bounding box coordinates (x1, y1, x2, y2)
   - `text`: str - Cell text content
3. `num_rows`: int - Number of rows in the table
4. `num_cols`: int - Number of columns in the table
5. `html`: str - HTML representation of the table

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

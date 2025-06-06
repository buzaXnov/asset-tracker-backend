import random


def detect(image_bytes: bytes, asset_definitions: list, metadata: dict):
    # Dummy output for testing
    return [
        {
            "bbox": [
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(101, 200),
                random.randint(101, 200),
            ],
            "coordinate_top": [45.815, 15.981],
            "coordinate_bottom": [45.814, 15.982],
            "answers": [
                "Yes" for _ in asset_definitions[0].questions
            ],  # Dummy "Yes" for each question
        }
    ]

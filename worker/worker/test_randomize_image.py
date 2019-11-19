import random
import time
import os

from tasks import randomize_image


def test_randomize_image(monkeypatch):
    dirname = os.path.dirname(__file__)
    with open(f"{dirname}/cat.png", "rb") as input_img, open(
        f"{dirname}/out.png", "rb"
    ) as output_img:
        input_data = input_img.read()
        output_data = output_img.read()

        random.seed(1)
        monkeypatch.setattr(time, "sleep", lambda t: None)

        assert randomize_image(input_data) == output_data

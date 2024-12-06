#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 9:50
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .portrait_main import MortalPortraitMain


class MortalPortrait(MortalPortraitMain):
    def __init__(self, onnx_path=None):
        super().__init__(onnx_path)

    def image(self, image_path, save_path, input_size=(512, 512)):
        self._image(image_path, save_path, input_size)

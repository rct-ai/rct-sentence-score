# coding=utf8
"""================================
@Author: Mr.Chang
@Date  : 2022/5/10 3:16 下午
==================================="""
import os

import torch
from sentence_transformers import SentenceTransformer
from logger import get_logger


def get_model(model_path, device='cpu'):
    LOGGER = get_logger()
    if os.path.exists(model_path):
        qa_model = SentenceTransformer(model_path, device=device)
        return qa_model
    else:
        LOGGER.info(f"{model_path} is not exists")

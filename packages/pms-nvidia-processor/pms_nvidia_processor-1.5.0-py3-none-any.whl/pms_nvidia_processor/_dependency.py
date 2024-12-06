from typing import (
    List,
    Optional,
    Tuple,
    Iterable,
    Literal,
    Dict,
    Any,
    TypeVar,
    Union,
    Generic,
)
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import os
import time
import uvloop
import asyncio
import numpy as np
from loguru import logger
import cv2
import pms_tensorrt as TRT
from pms_inference_engine import IEngineProcessor, EngineIOData, register

InputTypeT = TypeVar("InputTypeT")
OutputTypeT = TypeVar("OutputTypeT")

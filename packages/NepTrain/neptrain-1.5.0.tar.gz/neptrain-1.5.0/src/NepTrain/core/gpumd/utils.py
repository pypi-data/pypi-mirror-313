#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/26 19:39
# @Author  : 兵
# @email    : 1747193328@qq.com
import numpy as np


def read_thermo(filename: str, natoms: int = 1) -> np.ndarray:
    """读取能量用于画图
    """
    data = np.loadtxt(filename)

    energy = data[:,2]

    assert natoms > 0, 'natoms must be positive'

    energy /= natoms
    return energy
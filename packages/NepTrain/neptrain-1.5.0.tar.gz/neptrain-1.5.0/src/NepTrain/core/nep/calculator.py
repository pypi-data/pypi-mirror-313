#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 14:22
# @Author  : 兵
# @email    : 1747193328@qq.com
import contextlib
import os

import numpy as np
from ase import Atoms

from NepTrain.nep_cpu import CpuNep

class Nep3Calculator:

    def __init__(self, model_file="nep.txt"):
        if not isinstance(model_file, str):
            model_file=str(model_file,encoding="utf-8")
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                self.nep3 = CpuNep(model_file)
        self.element_list=self.nep3.get_element_list()
        self.type_dict = {e: i for i, e in enumerate(self.element_list)}




    def get_descriptors(self,structure):
        symbols = structure.get_chemical_symbols()
        _type = [self.type_dict[k] for k in symbols]
        _box = structure.cell.transpose(1, 0).reshape(-1).tolist()
        _position = structure.get_positions().transpose(1, 0).reshape(-1).tolist()
        descriptor = self.nep3.get_descriptor(_type, _box, _position)
        descriptors_per_atom = np.array(descriptor).reshape(-1, len(structure)).T

        return descriptors_per_atom
    def get_structure_descriptors(self, structure):
        descriptors_per_atom=self.get_descriptors(structure)
        return descriptors_per_atom.mean(axis=0)

    def get_structures_descriptors(self,structures:[Atoms]):
        _types=[]
        _boxs=[]
        _positions=[]
        for structure in structures:
            symbols = structure.get_chemical_symbols()
            _type = [self.type_dict[k] for k in symbols]
            _box = structure.cell.transpose(1, 0).reshape(-1).tolist()
            _position = structure.get_positions().transpose(1, 0).reshape(-1).tolist()
            _types.append(_type)
            _boxs.append(_box)
            _positions.append(_position)
        descriptor = self.nep3.get_descriptors(_types, _boxs, _positions)

        return np.array(descriptor)




class DescriptorCalculator:
    def __init__(self, calculator_type="nep",**calculator_kwargs):
        self.calculator_type=calculator_type
        if calculator_type == "nep":
            self.calculator=Nep3Calculator(**calculator_kwargs)
        elif calculator_type == "soap":
            from dscribe.descriptors import SOAP

            self.calculator = SOAP(
                **calculator_kwargs,dtype="float32"
            )
        else:
            raise ValueError("calculator_type must be nep or soap")


    def get_structures_descriptors(self,structures:[Atoms]):

        if len(structures)==0:
            return np.array([])

        if self.calculator_type == "nep":
            return self.calculator.get_structures_descriptors(structures)
        else:

            return  np.array([self.calculator.create_single(structure).mean(0) for structure in structures])
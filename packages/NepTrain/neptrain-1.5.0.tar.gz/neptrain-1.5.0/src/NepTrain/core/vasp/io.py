#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 15:53
# @Author  : 兵
# @email    : 1747193328@qq.com
import os
import subprocess

from ase.calculators.vasp import Vasp
from ase.io import read as ase_read

from NepTrain import Config


class VaspInput(Vasp):


    def __init__(self,*args,**kwargs):

        super(VaspInput,self).__init__(*args,**kwargs)
        self.input_params["setups"] = {"base": "recommended"}
        self.input_params["pp"] = ''

        os.environ[self.VASP_PP_PATH] = os.path.expanduser(Config.get("environ", "potcar_path"))


        # self.converged
    def _run(self, command=None, out=None, directory=None):
        """Method to explicitly execute VASP"""
        if command is None:
            command = self.command
        if directory is None:
            directory = self.directory

        errorcode = subprocess.call(command,
                                    shell=True,
                                    stdout=out,
                                    stderr=out,
                                    cwd=directory)

        return errorcode
if __name__ == '__main__':
    vasp=VaspInput()




    atoms=ase_read("./POSCAR",format='vasp')
    vasp.read_incar("./INCAR")
    vasp.calculate(atoms,('energy'))
    print(vasp.results)
    print(vasp.atoms.info)
    print(atoms.calc.results)
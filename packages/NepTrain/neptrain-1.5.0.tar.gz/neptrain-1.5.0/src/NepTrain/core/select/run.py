#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/13 19:36
# @Author  : 兵
# @email    : 1747193328@qq.com
import os.path

import numpy as np


# from joblib import Parallel, delayed

from NepTrain import utils
from ase.io import read as ase_read
from ase.io import write as ase_write
from .select import select_structures, filter_by_bonds, farthest_point_sampling
from ..gpumd.plot import plot_md_selected
from ..nep import Nep3Calculator
from ..nep.calculator import DescriptorCalculator


def run_select(argparse):

    if utils.is_file_empty(argparse.trajectory_path):
        raise FileNotFoundError(f"An invalid file path was provided: {argparse.trajectory_path}.")
    utils.print_msg("Reading the file, please wait...")

    trajectory=ase_read(argparse.trajectory_path,":",format="extxyz")

    # if argparse.filter:
    # #转移到gpumd的模块
    #     atoms=ase_read(argparse.base_structure,)
    #     good, bad = filter_by_bonds(trajectory, model=atoms)
    #     directory=os.path.dirname(argparse.trajectory_path)
    #     trajectory=good
    #     ase_write(os.path.join(directory, "good_structures.xyz"), good,append=False)
    #     ase_write(os.path.join(directory, "remove_by_bond_structures.xyz"), bad,append=False)
    #     utils.print_msg(f"Bond length filtering activated, {len(bad)} structures filtered out, saved to {os.path.join(directory, 'remove_by_bond_structures.xyz')}.")


    if utils.is_file_empty(argparse.base):
        base_train=[]
    else:
        base_train=ase_read(argparse.base,":",format="extxyz")
    if utils.is_file_empty(argparse.nep):
        utils.print_msg("An invalid path for nep.txt was provided, using SOAP descriptors instead.")
        species=set()
        for atoms in trajectory+base_train:
            for i in atoms.get_chemical_symbols():
                species.add(i)
        kwargs_dict={
            "species":list(species),
            "r_cut":argparse.r_cut,
            "n_max": argparse.n_max,
            "l_max": argparse.l_max

        }

        descriptor =DescriptorCalculator("soap",**kwargs_dict)

    else:
        descriptor =DescriptorCalculator("nep", model_file=argparse.nep)

    utils.print_msg("Start generating structure descriptor, please wait")
    train_structure_des =descriptor.get_structures_descriptors(base_train)
    new_structure_des =descriptor.get_structures_descriptors(trajectory)

    utils.print_msg("Starting to select points, please wait...")

    # train_structure_des = np.array([ descriptor.get_structure_descriptors(i )  for i in base_train])
    #
    # new_structure_des = np.array([ descriptor.get_structure_descriptors(i)  for i in trajectory])
    # train_structure_des =  np.array(Parallel(n_jobs=-1 )(delayed(Nep3Calculator.get_structure_descriptors_nep)(i,argparse.nep) for i in base_train))
    # new_structure_des =  np.array(Parallel(n_jobs=-1 )(delayed(Nep3Calculator.get_structure_descriptors_nep)(i,argparse.nep) for i in trajectory))


    selected_i =farthest_point_sampling(new_structure_des,argparse.max_selected,argparse.min_distance,selected_data=train_structure_des)
    selected_structures =[trajectory[i] for i in selected_i]
    selected_des=new_structure_des[selected_i,:]


    utils.print_msg(f"Obtained {len(selected_structures)} structures." )
    ase_write(argparse.out_file_path, selected_structures)
    png_path=os.path.join(os.path.dirname(argparse.out_file_path),"selected.png")
    plot_md_selected(train_structure_des,
                     new_structure_des,
                     selected_des,
                       png_path ,
                     argparse.decomposition
                     )
    utils.print_msg(f"The point selection distribution chart is saved to {png_path}." )
    utils.print_msg(f"The selected structures are saved to {argparse.out_file_path}." )


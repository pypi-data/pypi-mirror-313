#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 19:56
# @Author  : 兵
# @email    : 1747193328@qq.com
import os.path


import numpy as np
from ase.io import read as ase_read




from NepTrain import utils

from .utils import  read_thermo





def plot_md_selected(train_des,md_des,selected_des, save_path,decomposition="pca"):
    # 画一下图
    from matplotlib import pyplot as plt

    config = [
        # (文件名,图例,图例颜色)

    ]
    if train_des is not None and train_des.size!=0:
        config.append((train_des, "base dataset","gray"))

    if md_des is not None  and md_des.size!=0:
        config.append((md_des, 'new dataset', "#07cd66"))

    if selected_des is not None  and selected_des.size!=0:
        config.append((selected_des,'selected', "red"))

    fit_data = []

    for info in config:

        # atoms_list_des = np.vstack([get_descriptors(i, nep_txt_path) for i in atoms_list])

        atoms_list_des= info[0]
        # print(atoms_list_des.shape)


        fit_data.append(atoms_list_des)
    if decomposition=="pca":
        from sklearn.decomposition import PCA

        reducer = PCA(n_components=2)
    else:
        from umap import UMAP

        reducer = UMAP(n_components=2)

    reducer.fit(np.vstack(fit_data))
    fig = plt.figure()
    for index, array in enumerate(fit_data):
        proj = reducer.transform(array)
        plt.scatter(proj[:, 0], proj[:, 1], label=config[index][1], c=config[index][2])

    plt.legend()
    # plt.axis('off')
    plt.savefig(save_path)
    plt.close(fig)









def plot_energy(thermo_path,natoms=1):
    from matplotlib import pyplot as plt

    potential_energy = read_thermo(thermo_path, natoms)



    fig = plt.figure()
    plt.plot(list(range(len(potential_energy ))), potential_energy)



    plt.savefig(os.path.join(os.path.dirname(thermo_path),"md_energy.png"), dpi=300)
    plt.close(fig)

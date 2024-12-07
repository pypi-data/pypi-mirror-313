# ab-Initio Configuration Sampling tool kit (abICS)
# Copyright (C) 2019- The University of Tokyo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

from __future__ import annotations
from typing import Sequence, Dict

import numpy as np
import os, pathlib, shutil, subprocess, shlex
import time

from pymatgen.core import Structure

from abics.util import expand_cmd_path
from abics.applications.latgas_abinitio_interface.base_trainer import TrainerBase
from abics.applications.latgas_abinitio_interface.util import structure_to_XSF

class AenetTrainer(TrainerBase):
    def __init__(
        self,
        structures: Sequence[Structure],
        energies: Sequence[float],
        generate_inputdir: os.PathLike,
        train_inputdir: os.PathLike,
        predict_inputdir: os.PathLike,
        execute_commands: Dict,
    ):
        self.structures = structures
        self.energies = energies
        self.generate_inputdir = generate_inputdir
        self.train_inputdir = train_inputdir
        self.predict_inputdir = predict_inputdir
        generate_exe = execute_commands["generate"]
        self.generate_exe = [expand_cmd_path(e) for e in shlex.split(generate_exe)]
        self.generate_exe.append("generate.in")
        train_exe = execute_commands["train"]
        self.train_exe = [expand_cmd_path(e) for e in shlex.split(train_exe)]
        self.train_exe.append("train.in")
        assert len(self.structures) == len(self.energies)
        self.numdata = len(self.structures)
        self.is_prepared = False
        self.is_trained = False
        self.generate_outputdir = None

    def prepare(self, latgas_mode = True, st_dir = "aenetXSF"):
        rootdir = os.getcwd()
        xsfdir = os.path.join(rootdir, st_dir)
        
        # prepare XSF files for aenet
        os.makedirs(xsfdir, exist_ok=True)
        os.chdir(xsfdir)
        xsfdir = os.getcwd()
        if latgas_mode:
            for i, st in enumerate(self.structures):
                xsf_string = structure_to_XSF(st, write_force_zero=False)
                xsf_string = (
                    "# total energy = {} eV\n\n".format(self.energies[i]) + xsf_string
                )
                with open("structure.{}.xsf".format(i), "w") as fi:
                    fi.write(xsf_string)
        else:
            for i, st in enumerate(self.structures):
                xsf_string = structure_to_XSF(st, write_force_zero=False)
                xsf_string = (
                    "# total energy = {} eV\n\n".format(self.energies[i]) + xsf_string
                )
                with open("structure.{}.xsf".format(i), "w") as fi:
                    fi.write(xsf_string)

        os.chdir(rootdir)

    def generate_run(self, xsfdir="aenetXSF", generate_dir="generate"):
        # prepare generate
        xsfdir = str(pathlib.Path(xsfdir).resolve())
        if os.path.exists(generate_dir):
            shutil.rmtree(generate_dir)
        shutil.copytree(self.generate_inputdir, generate_dir)
        self.generate_dir = generate_dir
        os.chdir(generate_dir)
        with open("generate.in.head", "r") as fi:
            generate_head = fi.read()
            xsf_paths = [
                os.path.join(xsfdir, "structure.{}.xsf".format(i))
                for i in range(self.numdata)
            ]
            generate = (
                generate_head
                + "\n"
                + "FILES\n"
                + str(self.numdata)
                + "\n"
                + "\n".join(xsf_paths)
                + "\n"
            )
            with open("generate.in", "w") as fi_in:
                fi_in.write(generate)

        # command = self.generate_exe + " generate.in"
        with open(os.path.join(os.getcwd(), "stdout"), "w") as fi:
            #subprocess.run(
            self.gen_proc = subprocess.Popen(
                self.generate_exe, stdout=fi, stderr=subprocess.STDOUT,#, check=True
                )
        self.generate_outputdir = os.getcwd()
        os.chdir(pathlib.Path(os.getcwd()).parent)
        #self.is_prepared = True
        
    def generate_wait(self):
        self.gen_proc.wait()
        timeout = 5.0 # sec
        interval = 0.1 # sec
        t = 0.0
        self.is_prepared = False
        while t < timeout:
            if os.path.exists(os.path.join(self.generate_outputdir, "aenet.train")):
                self.is_prepared = True
                break
            time.sleep(interval)
        if not self.is_prepared:
            raise RuntimeError(f"{self.generate_outputdir}")

    def train(self, train_dir = "train"):
        if not self.is_prepared:
            raise RuntimeError("you have to prepare the trainer before training!")
        if os.path.exists(train_dir):
            shutil.rmtree(train_dir)
        shutil.copytree(self.train_inputdir, train_dir)
        os.chdir(train_dir)
        os.rename(
            os.path.join(self.generate_outputdir, "aenet.train"),
            os.path.join(os.getcwd(), "aenet.train"),
        )
        # command = self.train_exe + " train.in"
        # print(os.getcwd())
        # print(command)
        # print(os.path.exists("train.in"))

        while True:
            # Repeat until test set error begins to rise
            with open(os.path.join(os.getcwd(), "stdout"), "w") as fi:
                subprocess.run(
                    self.train_exe, stdout=fi, stderr=subprocess.STDOUT, check=True
                )
                # try:
                #     subprocess.run(
                #         self.train_exe, stdout=fi, stderr=subprocess.STDOUT, check=True
                #     )
                # except subprocess.CalledProcessError as e:
                #     print(e.stdout)
                #     print(e.stderr)
                #     raise
            with open("stdout", "r") as trainout:
                fullout = trainout.readlines()
                epoch_data = []
                for li in fullout:
                    if "<" in li:
                        epoch_data.append(li)
            with open("epochdat", "w") as epochdatfi:
                epochdat_str = "".join(epoch_data[1:]).replace("<", "")
                epochdatfi.write(epochdat_str)
            epoch_dat_arr = np.loadtxt("epochdat")
            # Find epoch id with minimum test set RMSE
            testRMSE = epoch_dat_arr[:, 4]
            minID = np.argmin(testRMSE)
            if minID == 0:
                minID = np.argmin(testRMSE[1:]) + 1
            num_epoch = len(testRMSE)
            if minID < num_epoch*0.7:  # this "0.7" is a heuristic
                break

        print("Best fit at epoch ID ", minID)
        self.train_outputdir = os.getcwd()
        self.train_minID = minID
        os.chdir(pathlib.Path(os.getcwd()).parent)
        self.is_trained = True

    def new_baseinput(self, baseinput_dir, train_dir=""):
        try:
            assert self.is_trained
        except AssertionError as e:
            e.args += "you have to train before getting results!"

        # Some filesystems may delay making a directory due to cache
        # especially when mkdir just after rmdir, and hence 
        # we should make sure that the old directory is removed and the new one is made.
        # Since `os.rename` is an atomic operation,
        # `baseinput_dir` is removed after `os.rename`.
        if os.path.exists(baseinput_dir):
            os.rename(baseinput_dir, baseinput_dir + "_temporary")
            shutil.rmtree(baseinput_dir + "_temporary")
        os.makedirs(baseinput_dir, exist_ok=False)
        while not os.path.exists(baseinput_dir):
            time.sleep(0.1)

        iflg = False
        for name in ["predict.in", "in.lammps"]:
            if os.path.isfile(os.path.join(self.predict_inputdir, name)):
                iflg = True
                shutil.copyfile(
                    os.path.join(self.predict_inputdir, name),
                    os.path.join(baseinput_dir, name),
                )
        if iflg is False:
            print("Warning: predict.in or in.lammps should be in the predict directory.")


        NNPid_str = "{:05d}".format(self.train_minID)
        NNPfiles = [fi for fi in os.listdir(self.train_outputdir) if NNPid_str in fi]
        for fi in NNPfiles:
            shutil.copyfile(
                os.path.join(self.train_outputdir, fi),
                os.path.join(baseinput_dir, fi),
            )
            # os.rename is guaranteed to be atomic
            os.rename(
                os.path.join(baseinput_dir, fi),
                os.path.join(baseinput_dir, fi[:-6]),
            )

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

from mpi4py import MPI

import shutil
import os, sys
import datetime
import argparse

import numpy as np
import scipy.constants as constants
import toml

from abics.sampling.mc_mpi import RX_MPI_init
from abics.sampling.rxmc import RXParams


def main():
    # Input parser
    parser = argparse.ArgumentParser(
        description="Reorganize abICS RXMC results by temperature"
    )

    parser.add_argument("inputfi", help="toml input file used for abICS run")

    parser.add_argument(
        "skipsteps",
        nargs="?",
        type=int,
        default=0,
        help="number of thermalization steps to skip in energy averaging."
        + " Default: 0",
    )

    args = parser.parse_args()
    inputfi = args.inputfi
    nskip = args.skipsteps
    rxparams = RXParams.from_toml(inputfi)
    nreplicas = rxparams.nreplicas
    comm = RX_MPI_init(rxparams.nreplicas, rxparams.seed)

    param = toml.load(inputfi)
    solver_type = param["sampling"]["solver"]["type"]

    myreplica = comm.Get_rank()

    if myreplica == 0:
        if os.path.exists("Tseparate"):
            shutil.move("Tseparate", "Tseparate.bak.{}".format(datetime.datetime.now()))
        os.mkdir("Tseparate")
    comm.Barrier()

    # Separate structure files
    os.mkdir(os.path.join("Tseparate", str(myreplica)))
    Trank_hist = np.load(os.path.join(str(myreplica), "Trank_hist.npy"))
    os.chdir(str(myreplica))
    for j in range(len(Trank_hist)):
        str_file = f"structure.{j}.vasp"
        if os.path.exists(str_file):
            shutil.copy(
                str_file,
                os.path.join(os.pardir, "Tseparate", str(Trank_hist[j])),
            )

    # Separate energies
    myreplica_energies = np.load("obs_save.npy")
    for Tid in range(nreplicas):
        mask = Trank_hist == Tid
        if myreplica_energies.ndim == 2:
            mask = np.repeat(mask.reshape(-1,1), myreplica_energies.shape[1], axis=1)
        T_energies = np.where(mask, myreplica_energies, 0)
        T_energies_rcvbuf = np.zeros(T_energies.shape, "d")
        comm.Reduce(
            [T_energies, MPI.DOUBLE],
            [T_energies_rcvbuf, MPI.DOUBLE],
            op=MPI.SUM,
            root=Tid,
        )
        if myreplica == Tid:
            np.savetxt(
                os.path.join(os.pardir, "Tseparate", str(Tid), "energies.dat"),
                T_energies_rcvbuf,
            )

    comm.Barrier()

    if myreplica == 0:
        os.chdir(os.path.join(os.pardir, "Tseparate"))
        with open("energies_T.dat", "w") as fi:
            kTs = np.load(os.path.join(os.pardir, "kTs.npy"))
            if solver_type != "potts":
                Ts = kTs / constants.value("Boltzmann constant in eV/K")
            else:
                Ts = kTs
            for Tid in range(nreplicas):
                energies_data = np.loadtxt(os.path.join(str(Tid), "energies.dat"))
                if energies_data.ndim == 1:
                    energy_mean = [np.mean(energies_data[nskip:])]
                else:
                    energy_mean = np.mean(energies_data[nskip:,:],
                                          axis = 0
                    )

                fi.write(f"{Ts[Tid]}")
                for en in energy_mean:
                    fi.write(f"\t{en}")
                fi.write("\n")


if __name__ == "__main__":
    main()

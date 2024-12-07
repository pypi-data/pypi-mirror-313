# (C) Quantum Computing Inc., 2024.
try:
    from .eqcdirect import Dirac3DirectSolver, EqcDirectSolver
except ImportError:
    # eqc-direct is not available
    Dirac3DirectSolver = None
from .qciclient import (Dirac1CloudSolver, Dirac3CloudSolver, QciClientSolver,
                        Dirac3IntegerCloudSolver, Dirac3ContinuousCloudSolver)

__all__ = ["Dirac3DirectSolver", "Dirac1CloudSolver", "Dirac3CloudSolver", 
           "EqcDirectSolver", "QciClientSolver", "Dirac3IntegerCloudSolver",
           "Dirac3ContinuousCloudSolver"]

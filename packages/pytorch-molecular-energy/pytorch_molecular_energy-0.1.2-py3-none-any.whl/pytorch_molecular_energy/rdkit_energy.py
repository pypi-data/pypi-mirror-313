"""PyTorch module for RDKit force field energy calculations."""

from __future__ import annotations

import multiprocessing
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Literal, Optional, Tuple

import numpy as np
import torch
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdForceFieldHelpers import (
    MMFFGetMoleculeForceField,
    MMFFGetMoleculeProperties,
    MMFFHasAllMoleculeParams,
    UFFGetMoleculeForceField,
    UFFHasAllMoleculeParams,
)
from rdkit.Chem.rdmolfiles import MolFromMolFile, MolFromSmiles, MolToSmiles
from rdkit.Chem.rdmolops import AddHs, RemoveAllHs, RemoveHs
from rdkit.ForceField.rdForceField import ForceField  # noqa: F401
from torch import Tensor

R = 0.00198720425864083  # ideal gas constant [kcal / mol / K]


class RDKitEnergy(torch.nn.Module):
    """RDKit force field initialized for a single molecule."""

    def __init__(
        self,
        mol: Mol | Path | str,
        variant: Literal["MMFF94", "MMFF94s", "UFF"] = "UFF",
        temperature: float | None = None,  # kelvin
        n_threads: int | None = None,
        **kwargs,
    ):
        """Initialize the force field for a single molecule.

        Args:
            mol: Molecule passed as RDKit molecule object or Path object pointing to molecule file or SMILES string.
            variant: Name of RDKit supported force field. Defaults to "UFF".
            temperature: Kelvin. If provided, function outputs dimensionless energy or reduced energy.
            n_threads: Number of workers to use for multiprocessing. If None do not use multiprocessing, if 0 use all available CPUs.
                Defaults to None.
            **kwargs: Additional keyword arguments passed on to RDKit's GetForceField method.
        """
        super().__init__()

        if isinstance(mol, str):
            mol = MolFromSmiles(mol, removeHs=False)
        elif isinstance(mol, Path):
            mol = MolFromMolFile(mol, removeHs=False)
        elif not isinstance(mol, Mol):
            raise ValueError("Argument mol must be RDKit molecule, a valid SMILES string, or path to a molecule file.")
        assert mol is not None, "Molecule not valid or could not be loaded."

        if mol.GetNumConformers() == 0:
            raise ValueError("Molecule must have at least one conformer.")

        self.num_total_atoms = mol.GetNumAtoms(onlyExplicit=False)
        self.num_explicit_atoms = mol.GetNumAtoms(onlyExplicit=True)
        self.num_heavy_atoms = mol.GetNumHeavyAtoms()

        # mol = AddHs(mol, addCoords=True)

        self.smiles = MolToSmiles(mol)
        self.name = f"{variant} force field for molecule {self.smiles}."

        if variant == "UFF" and not UFFHasAllMoleculeParams(mol):
            raise ValueError(f"{variant} does not support the molecule.")
        if variant in ["MMFF94", "MMFF94s"] and MMFFHasAllMoleculeParams(mol):
            raise ValueError(f"{variant} does not support the molecule.")

        if n_threads is None:
            self.pool = self.worker_initialize(mol, variant, kwargs, False)
        else:
            shared_arguments = (mol, variant, kwargs, True)
            n_threads = multiprocessing.cpu_count() if n_threads == 0 else n_threads
            self.pool = Pool(n_threads, self.worker_initialize, shared_arguments)

        self.temperature = temperature

    @staticmethod
    def worker_initialize(mol, variant, kwargs, pool=False) -> ForceField:
        if pool:
            # every process will get a different one
            global rdkit_force_field_module  # noqa: W0601

        if variant in ["UFF"]:
            rdkit_force_field_module = UFFGetMoleculeForceField(mol, **kwargs)
        elif variant in ["MMFF94", "MMFF94s"]:
            force_field_properties = MMFFGetMoleculeProperties(mol, variant)
            rdkit_force_field_module = MMFFGetMoleculeForceField(mol, force_field_properties, **kwargs)
        else:
            raise ValueError(f"{variant} is not supported.")

        return rdkit_force_field_module

    @staticmethod
    def get_energy(positions: np.ndarray) -> Tuple[Any, Any]:
        return get_energy(positions, rdkit_force_field_module)

    def forward(self, positions: Tensor) -> Tensor:
        energies, _ = EvaluateEnergy.apply(positions, self.pool)
        # return dimensionless energy if temperature is provided
        if self.temperature is not None:
            energies = energies / (R * self.temperature)
        return energies.reshape(positions.shape[:-2])

    def __repr__(self):
        return self.name

    def __del__(self):
        if hasattr(self, "pool") and hasattr(self.pool, "close"):
            try:
                self.pool.close()
            except ValueError:
                if self.pool.is_alive():
                    self.pool.terminate()
                if self.pool.is_alive():
                    self.pool.kill()
        self.pool = None


class EvaluateEnergy(torch.autograd.Function):
    """Helper class to be used only in RDKitEnergy."""

    @staticmethod
    def forward(positions: Tensor, pool) -> Tensor:
        """Returns the energy and forces of the molecule using the initialized worker pool.

        Args:
            ctx: Context object.
            positions: Coordinates of the atoms in the molecule.
            pool: Initialized worker pool with RDKit Force Fields.

        Returns:
            Tensor: Energy of the molecule.
        """

        pos = positions.detach().cpu().numpy().reshape(-1, positions.shape[-2], 3)

        if isinstance(pool, ForceField):
            outputs = [get_energy(p, pool) for p in pos]
            energies_, forces_ = list(zip(*outputs))
        else:
            outputs = pool.map(RDKitEnergy.get_energy, pos)
            energies_, forces_ = zip(*outputs)

        energies_ = np.stack(energies_, axis=0)
        forces_ = np.stack(forces_, axis=0).reshape(pos.shape)

        energies = torch.from_numpy(energies_).to(positions)
        forces = torch.from_numpy(forces_).to(positions)

        return energies, forces

    @staticmethod
    def backward(ctx, grad_energy: Tensor, grad_forces: Tensor) -> Tensor:
        """Returns the gradient of the energy with respect to the input positions.

        Args:
            ctx: Context object.
            grad_energy: Gradient of the loss with respect to the output of the forward pass.

        Returns:
            Tensor: Gradient of the energy with respect to the input positions.

        Note:
            No gradient of the forces is given.
        """

        (gradient,) = ctx.saved_tensors

        if gradient.ndim == 3 and grad_energy.ndim == 1:
            gradient = grad_energy[:, None, None] * gradient
        else:
            raise NotImplementedError()
        return gradient, None

    @staticmethod
    def setup_context(ctx, inputs, output):
        """Save the input positions and force field in the context for backward pass."""
        _, forces = output
        ctx.save_for_backward(forces)

    @staticmethod
    def vmap(info, in_dims: Tuple[Optional[int]], positions: Tensor, pool) -> Tensor:
        """Define the vmap static method for batching.

        Args:
            info: Information about the vmap operation.
            in_dims: Tuple of Optional[int] that specifies which dimensions are being vmapped over.
            positions: Coordinates of the atoms in the molecule.
            pool: Initialized worker pool with RDKit Force Fields.

        Reference:
            https://pytorch.org/docs/master/notes/extending.func.html#defining-the-vmap-staticmethod
        """

        pos = positions.detach().cpu().numpy().reshape(-1, positions.shape[-2], 3)

        outputs = pool.map(RDKitEnergy.get_energy, pos)
        energies_, forces_ = zip(*outputs)

        energies_ = np.stack(energies_, axis=0).reshape(info.batch_size, -1)
        forces_ = np.stack(forces_, axis=0).reshape(positions.shape)

        energies = torch.from_numpy(energies_).to(positions)
        forces = torch.from_numpy(forces_).to(positions)

        return (energies, forces), (0, 0)


def get_energy(positions: np.ndarray, force_field: ForceField) -> Tuple[Any, Any]:
    expected_shape = (rdkit_force_field_module.NumPoints(), rdkit_force_field_module.Dimension())
    assert positions.shape == expected_shape, f"Expected positions shape {expected_shape}, got {positions.shape}."

    # RDKit force field functions expect positions to be in a (1D) list.
    positions_ = positions.flatten().tolist()

    # Calculate the energy and gradient using the force field.
    energy = force_field.CalcEnergy(positions_)  # kcal / mol
    # Forces point in the opposite direction of the gradient.
    gradient = force_field.CalcGrad(positions_)  # kcal / mol / A

    return energy, gradient

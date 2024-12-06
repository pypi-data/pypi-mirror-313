import pytest
import torch
from rdkit.Chem.AllChem import EmbedMolecule
from rdkit.Chem.rdmolfiles import MolFromSmiles, MolToSmiles
from rdkit.Chem.rdmolops import AddHs

from pytorch_molecular_energy import RDKitEnergy


class TestRDKitEnergy:
    def test___init__(self):
        mol = MolFromSmiles("c1ccccc1CNCC(=O)O")

        with pytest.raises(ValueError):
            RDKitEnergy(mol, n_threads=None)

        with pytest.raises(ValueError):
            RDKitEnergy(mol, n_threads=1)

        mol = AddHs(mol)

        with pytest.raises(ValueError):
            RDKitEnergy(mol, n_threads=1)

        EmbedMolecule(mol)

        energy = RDKitEnergy(mol, n_threads=None)

        assert energy.smiles == MolToSmiles(mol)
        assert energy.num_heavy_atoms == mol.GetNumHeavyAtoms()

        energy = RDKitEnergy(mol, n_threads=1)

        assert energy.smiles == MolToSmiles(mol)
        assert energy.num_heavy_atoms == mol.GetNumHeavyAtoms()

        energy = RDKitEnergy(mol, n_threads=1, temperature=298.15)
        assert energy.temperature == 298.15

    def test_forward(self):
        mol = MolFromSmiles("c1ccccc1CNCC(=O)O")
        mol = AddHs(mol)
        EmbedMolecule(mol)

        # test without workers
        energy_module = RDKitEnergy(mol, n_threads=None)
        positions = torch.from_numpy(mol.GetConformer().GetPositions())
        energy = energy_module(positions)
        assert isinstance(energy, torch.Tensor)
        assert energy.shape == torch.Size([])
        positions = torch.stack([positions] * 7)
        energy = energy_module(positions)
        assert energy.shape == torch.Size([7])

        # test with workers
        energy_module = RDKitEnergy(mol, n_threads=3)
        positions = torch.from_numpy(mol.GetConformer().GetPositions())
        energy = energy_module(positions)
        assert isinstance(energy, torch.Tensor)
        assert energy.shape == torch.Size([])
        positions = torch.stack([positions] * 7)
        energy = energy_module(positions)
        assert energy.shape == torch.Size([7])

    def test_backward(self):
        mol = MolFromSmiles("c1ccccc1CNCC(=O)O")
        mol = AddHs(mol)
        EmbedMolecule(mol)

        # test without workers
        energy_module = RDKitEnergy(mol, n_threads=None)

        positions = torch.from_numpy(mol.GetConformer().GetPositions())
        positions.requires_grad = True
        energy = energy_module(positions)
        energy.backward()
        assert positions.grad is not None
        assert positions.grad.shape == positions.shape

        positions = torch.stack([positions] * 3).detach()
        positions.requires_grad = True
        energy = energy_module(positions)
        energy.sum().backward()
        assert positions.grad is not None
        assert positions.grad.shape == positions.shape

        # test with workers
        energy_module = RDKitEnergy(mol, n_threads=3)

        positions = torch.from_numpy(mol.GetConformer().GetPositions())
        positions.requires_grad = True
        energy = energy_module(positions)
        energy.backward()
        assert positions.grad is not None
        assert positions.grad.shape == positions.shape

        positions = torch.stack([positions] * 3).detach()
        positions.requires_grad = True
        energy = energy_module(positions)
        energy.sum().backward()
        assert positions.grad is not None
        assert positions.grad.shape == positions.shape
        assert positions.grad.shape == positions.shape

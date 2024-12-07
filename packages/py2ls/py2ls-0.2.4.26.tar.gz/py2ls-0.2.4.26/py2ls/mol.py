import os
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem,Draw
from openbabel import openbabel
import matplotlib.pyplot as plt
# import pymol2  # 使用 PyMOL API 进行分子展示

from typing import Any, Dict, Union, List

def load_mol(fpath: str) -> Union[Dict[str, Any], None]:
    """
    Master function to read various molecular structure files and return a consistent molecule dictionary.
    Supports formats: .pdb, .mol, .sdf, .xyz, .gro, and others through RDKit, Pybel, MDAnalysis, and ASE.
    
    Parameters:
    - fpath (str): Path to the molecular file
    
    Returns:
    - mol_dict (Dict[str, Any]): Dictionary with molecule information:
        - 'atoms': List of atom information dictionaries
        - 'bonds': List of bond information dictionaries
        - 'metadata': Metadata for molecule (e.g., file name)
    """
    ext = os.path.splitext(fpath)[-1].lower()  # Get the file extension

    def create_atom_dict(atom) -> Dict[str, Any]:
        """Helper to create a consistent atom dictionary."""
        return {
            'element': atom.atomic_symbol,
            'coords': atom.coords,
            'index': atom.idx,
            'charge': atom.formalcharge
        }
    
    def create_bond_dict(bond) -> Dict[str, Any]:
        """Helper to create a consistent bond dictionary."""
        return {
            'start_atom_idx': bond.GetBeginAtomIdx(),
            'end_atom_idx': bond.GetEndAtomIdx(),
            'bond_type': bond.GetBondTypeAsDouble()
        }

    mol_dict = {
        "atoms": [],
        "bonds": [],
        "metadata": {
            "file_name": os.path.basename(fpath),
            "format": ext
        }
    }

    try:
        # Handling with RDKit (for .mol and .sdf)
        if ext in ['.mol', '.sdf']:
            from rdkit import Chem
            if ext == '.mol':
                mol = Chem.MolFromMolFile(fpath)
                if mol is None:
                    raise ValueError("RDKit failed to parse the .mol file.")
                atoms = mol.GetAtoms()
                bonds = mol.GetBonds()
            elif ext == '.sdf':
                supplier = Chem.SDMolSupplier(fpath)
                mol = next(supplier, None)
                if mol is None:
                    raise ValueError("RDKit failed to parse the .sdf file.")
                atoms = mol.GetAtoms()
                bonds = mol.GetBonds()

            # Populate atom and bond data
            mol_dict["atoms"] = [
                {
                    "element": atom.GetSymbol(),
                    "coords": atom.GetOwningMol().GetConformer().GetAtomPosition(atom.GetIdx()),
                    "index": atom.GetIdx(),
                    "charge": atom.GetFormalCharge()
                }
                for atom in atoms
            ]
            mol_dict["bonds"] = [
                create_bond_dict(bond)
                for bond in bonds
            ]

        # Handling with Pybel (supports multiple formats: .pdb, .mol, .xyz, etc.)
        elif ext in ['.pdb', '.mol', '.xyz', '.sdf']:
            from openbabel import pybel

            mol = next(pybel.readfile(ext[1:], fpath), None)
            if mol is None:
                raise ValueError("Pybel failed to parse the file.")
            # Populate atom and bond data
            mol_dict["atoms"] = [
                {
                    "element": atom.type,
                    "coords": atom.coords,
                    "index": atom.idx,
                    "charge": atom.partialcharge
                }
                for atom in mol.atoms
            ]
            mol_dict["bonds"] = [
                {
                    "start_atom_idx": bond.GetBeginAtomIdx(),
                    "end_atom_idx": bond.GetEndAtomIdx(),
                    "bond_type": bond.GetBondOrder()
                }
                for bond in openbabel.OBMolBondIter(mol.OBMol)
            ]

        # Handling with MDAnalysis (for .pdb, .gro, and trajectory files)
        elif ext in ['.pdb', '.gro', '.xyz', '.xtc', '.dcd', '.trr']:
            import MDAnalysis as mda
            u = mda.Universe(fpath)
            atoms = u.atoms
            mol_dict["atoms"] = [
                {
                    "element": atom.name,
                    "coords": atom.position,
                    "index": atom.id,
                    "charge": atom.charge if hasattr(atom, 'charge') else None
                }
                for atom in atoms
            ]
            mol_dict["bonds"] = [
                {"start_atom_idx": bond[0], "end_atom_idx": bond[1], "bond_type": 1}
                for bond in u.bonds.indices
            ]

        # Handling with ASE (for .xyz, .pdb, and other atomic structure formats)
        elif ext in ['.xyz', '.pdb', '.vasp', '.cif']:
            from ase.io import read as ase_read
            atoms = ase_read(fpath)
            mol_dict["atoms"] = [
                {
                    "element": atom.symbol,
                    "coords": atom.position,
                    "index": i,
                    "charge": None
                }
                for i, atom in enumerate(atoms)
            ]
            # ASE does not explicitly support bonds by default, so bonds are not populated here.

        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    except Exception as e:
        print(f"Error loading molecule from {fpath}: {e}")
        return None

    return mol_dict
 
class DockingConfig:
    def __init__(self, receptor_file, ligand_smiles_list, center=(0, 0, 0), size=(20, 20, 20), output_dir="docking_results"):
        self.receptor_file = receptor_file
        self.ligand_smiles_list = ligand_smiles_list
        self.center = center
        self.size = size
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

def mol_to_pdbqt(mol, output_file):
    """Converts an RDKit Mol object to PDBQT format."""
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("mol", "pdbqt")
    obMol = openbabel.OBMol()
    obConversion.ReadString(obMol, Chem.MolToMolBlock(mol))
    obConversion.WriteFile(obMol, output_file)

def prepare_ligand(smiles, ligand_id):
    """Prepare the ligand file in PDBQT format."""
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.UFFOptimizeMolecule(mol)
    ligand_file = f"ligand_{ligand_id}.pdbqt"
    mol_to_pdbqt(mol, ligand_file)
    return ligand_file

def run_docking(receptor_file, ligand_file, output_file, center, size):
    """Runs Vina docking using the receptor and ligand files."""
    vina_command = [
        "vina",
        "--receptor", receptor_file,
        "--ligand", ligand_file,
        "--center_x", str(center[0]),
        "--center_y", str(center[1]),
        "--center_z", str(center[2]),
        "--size_x", str(size[0]),
        "--size_y", str(size[1]),
        "--size_z", str(size[2]),
        "--out", output_file,
        "--log", output_file.replace(".pdbqt", ".log")
    ]
    subprocess.run(vina_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def parse_vina_output(output_file):
    """Parses Vina output log file to extract docking scores."""
    scores = []
    with open(output_file.replace(".pdbqt", ".log"), 'r') as f:
        for line in f:
            if line.startswith("REMARK VINA RESULT"):
                score = float(line.split()[3])
                scores.append(score)
    return scores

def docking_master_function(config: DockingConfig):
    """Master function to run molecular docking for multiple ligands."""
    receptor_pdbqt = config.receptor_file
    results = {}

    for i, smiles in enumerate(config.ligand_smiles_list):
        ligand_file = prepare_ligand(smiles, ligand_id=i)
        output_file = os.path.join(config.output_dir, f"docked_ligand_{i}.pdbqt")
        
        # Run docking for each ligand
        run_docking(
            receptor_file=receptor_pdbqt,
            ligand_file=ligand_file,
            output_file=output_file,
            center=config.center,
            size=config.size
        )

        # Parse docking results and store them
        scores = parse_vina_output(output_file)
        results[smiles] = scores
        print(f"Ligand {i} (SMILES: {smiles}) docking scores: {scores}")

        # Visualize individual docking result
        visualize_docking(config.receptor_file, output_file, f"{config.output_dir}/ligand_{i}_visualization.png")

        # Clean up intermediate files
        os.remove(ligand_file)

    # Plot binding affinity distribution
    plot_binding_affinities(results, f"{config.output_dir}/binding_affinities.png")
    return results

def visualize_docking(receptor_file, ligand_file, dir_save):
    """Generates a 2D visualization of the docking result using RDKit and Matplotlib."""
    # Load the receptor and ligand molecules
    receptor = Chem.MolFromPDBFile(receptor_file, removeHs=False)
    ligand = Chem.MolFromPDBFile(ligand_file, removeHs=False)

    # Draw the receptor and ligand
    img = Draw.MolToImage(receptor, size=(300, 300))
    img_ligand = Draw.MolToImage(ligand, size=(300, 300))

    # Save images
    img.save(dir_save.replace('.png', '_receptor.png'))
    img_ligand.save(dir_save.replace('.png', '_ligand.png'))
    
    print(f"Saved 2D visualizations to {dir_save.replace('.png', '_receptor.png')} and {dir_save.replace('.png', '_ligand.png')}")


def plot_binding_affinities(results, dir_save):
    """Plots binding affinities for all ligands."""
    ligands = list(results.keys())
    affinities = [min(scores) for scores in results.values()]  # Minimum binding affinity per ligand

    plt.figure(figsize=(10, 6))
    plt.barh(ligands, affinities, color="skyblue")
    plt.xlabel("Binding Affinity (kcal/mol)")
    plt.ylabel("Ligands (SMILES)")
    plt.title("Binding Affinities of Different Ligands")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(dir_save)
    plt.show()
    print(f"Saved binding affinity plot to {dir_save}")
    
# 示例使用
if __name__ == "__main__":
    # 配置
    receptor_file = "receptor.pdbqt"
    ligand_smiles_list = ["CCO", "CCC", "CCN"]  # 示例的配体SMILES列表
    docking_config = DockingConfig(
        receptor_file=receptor_file,
        ligand_smiles_list=ligand_smiles_list,
        center=(10, 10, 10),  # 假设对接中心
        size=(20, 20, 20)     # 假设对接区域大小
    )

    # 运行master function
    docking_results = docking_master_function(docking_config)
    print("Final docking results:", docking_results)

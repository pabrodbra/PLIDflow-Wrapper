from pymol import cmd
import sys

path_pdb = sys.argv[-3]
id_ligand = sys.argv[-2]
path_output = sys.argv[-1]

print sys.argv

# Load PDB
cmd.load(path_pdb)

# loop ligands
cmd.select('ligand', 'resn ' + id_ligand)
cmd.remove('ligand')
cmd.delete('ligand')

# Save new PDB
cmd.save(path_output, "all")

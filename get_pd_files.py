from __future__ import print_function
import sys
import requests
import xmltodict

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	quit()

# Download SMI of LigandID associated to a ProteinID from RSCB
def fetch_smile(pdb_id, ligand_id, output_path):
	url = "http://www.rcsb.org/pdb/rest/ligandInfo?structureId=" + pdb_id
	try:
		ligand_data = requests.get(url)
	except requests.exceptions.RequestException as e:
		eprint("ERROR | " + str(e))

	if(len(ligand_data.text) != 0):
		xml_dict = xmltodict.parse(ligand_data.text)
		ligands_info = xml_dict.get('structureId').get('ligandInfo').get('ligand')
		#print(ligands_info)
		ligand_found = False
		if type(ligands_info) != list:
			ligands_info = [ligands_info]

		for ligand_info in ligands_info:
			#print(ligand_info)
			if ligand_info.get('@chemicalID').lower() == ligand_id:
				ligand_found = True
				f = open(output_path + ligand_id + '.smi', 'w')
				f.write(ligand_info.get('smiles'))
				f.close()
				print('SMI of %s downloaded succesfully!' % ligand_id)
				break

		if ligand_found == False:
			eprint('ERROR | %s is not found on PROTEIN::%s ligands' % (ligand_id, pdb_id))
	else:
		eprint('ERROR | %s is not a valid ID' % pdb_id)


# Download PDB of ProteinID from RSCB
def fetch_pdb(pdb_id, output_path):
	url = "https://files.rcsb.org/download/%s.pdb" % pdb_id
	
	try:
		pdb_data = requests.get(url)
	except requests.exceptions.RequestException as e:
		eprint("ERROR | " + str(e))

	if(len(pdb_data.text) != 0):
		f = open(output_path + pdb_id + '.pdb', 'w')
		f.write(pdb_data.text)
		f.close()
		print('PDB of %s downloaded succesfully!' % pdb_id)
	else:
		eprint('ERROR | %s is not a valid ID' % pdb_id)

############################
########### MAIN ###########
############################

def main():
	pdb_id = sys.argv[1]
	ligand_id = sys.argv[2]
	output_path = sys.argv[3]

	fetch_pdb(pdb_id, output_path)
	fetch_smile(pdb_id, ligand_id, output_path)
		

if __name__ == "__main__":
	if(len(sys.argv) != 4):
		print("ERROR | USE: python get_pd_files.py <PDB file> <Ligand ID> <Output>")
		quit()

	main()

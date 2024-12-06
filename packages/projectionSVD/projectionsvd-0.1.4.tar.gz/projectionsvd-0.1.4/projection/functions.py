import numpy as np
from math import ceil
from projection import shared

##### projectionSVD functions #####
# Read PLINK files
def readPlink(bfile, threads):
	# Find length of fam-file
	N = 0
	with open(f"{bfile}.fam", "r") as fam:
		for _ in fam:
			N += 1
	N_bytes = ceil(N/4) # Length of bytes to describe N individuals

	# Read .bed file
	with open(f"{bfile}.bed", "rb") as bed:
		B = np.fromfile(bed, dtype=np.uint8, offset=3)
	assert (B.shape[0] % N_bytes) == 0, "bim file doesn't match!"
	M = B.shape[0]//N_bytes
	B.shape = (M, N_bytes)

	# Read in full genotypes into 8-bit array
	G = np.zeros((M, N), dtype=np.uint8)
	shared.expandGeno(B, G, threads)
	del B
	return G, M, N

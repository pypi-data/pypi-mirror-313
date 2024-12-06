# cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
import numpy as np
cimport numpy as np
from cython.parallel import prange

# Expand data into full genotype matrix
cpdef void expandGeno(const unsigned char[:,::1] B, unsigned char[:,::1] G, \
		const int t) noexcept nogil:
	cdef:
		int M = G.shape[0]
		int N = G.shape[1]
		int N_b = B.shape[1]
		int i, j, b, bytepart
		unsigned char[4] recode = [2, 9, 1, 0]
		unsigned char mask = 3
		unsigned char byte
	for j in prange(M, num_threads=t):
		i = 0
		for b in range(N_b):
			byte = B[j,b]
			for bytepart in range(4):
				G[j,i] = recode[byte & mask]
				byte = byte >> 2
				i = i + 1
				if i == N:
					break

# Standardize full genotype matrix
cpdef void standardizeE(double[:,::1] E, const unsigned char[:,::1] G, \
		const double[::1] f, const double[::1] d, const int t) noexcept nogil:
	cdef:
		int M = E.shape[0]
		int N = E.shape[1]
		int i, j
	for j in prange(M, num_threads=t):
		for i in range(N):
			if G[j,i] == 9:
				E[j,i] = 0.0
			else:
				E[j,i] = (G[j,i] - 2.0*f[j])/d[j]

# Standardize full genotype matrix (PCAone format)
cpdef void standardizeE_pcaone(double[:,::1] E, const unsigned char[:,::1] G, \
		const double[::1] f, const double[::1] d, const int t) noexcept nogil:
	cdef:
		int M = E.shape[0]
		int N = E.shape[1]
		int i, j
	for j in prange(M, num_threads=t):
		for i in range(N):
			if G[j,i] == 9:
				E[j,i] = 0.0
			else:
				E[j,i] = (G[j,i]/2.0 - f[j])/d[j]

# Standardize batched genotype matrix
cpdef void standardizeL(double[:,::1] E, const unsigned char[:,::1] G, \
		const double[::1] f, const double[::1] d, const int m, const int t) \
		noexcept nogil:
	cdef:
		int M = E.shape[0]
		int N = E.shape[1]
		int i, j, k
	for j in prange(M, num_threads=t):
		k = m + j
		for i in range(N):
			if G[k,i] == 9:
				E[j,i] = 0.0
			else:
				E[j,i] = (G[k,i] - 2.0*f[k])/d[k]

# Standardize batched genotype matrix (PCAone format)
cpdef void standardizeL_pcaone(double[:,::1] E, const unsigned char[:,::1] G, \
		const double[::1] f, const double[::1] d, const int m, const int t) \
		noexcept nogil:
	cdef:
		int M = E.shape[0]
		int N = E.shape[1]
		int i, j, k
	for j in prange(M, num_threads=t):
		k = m + j
		for i in range(N):
			if G[k,i] == 9:
				E[j,i] = 0.0
			else:
				E[j,i] = (G[k,i]/2.0 - f[k])/d[k]		

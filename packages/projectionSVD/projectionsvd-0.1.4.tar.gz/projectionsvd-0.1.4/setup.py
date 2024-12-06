from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
	Extension(
		"projection.shared",
		["projection/shared.pyx"],
		extra_compile_args=['-fopenmp', '-O3', '-g0', '-Wno-unreachable-code'],
		extra_link_args=['-fopenmp'],
		include_dirs=[numpy.get_include()],
		define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
	)
]

setup(
	name="projectionSVD",
	version="0.1.4",
	author="Jonas Meisner",
	author_email="meisnerucph@gmail.com",
	description="Projection into SVD space for genetic data",
	long_description_content_type="text/markdown",
	long_description=open("README.md").read(),
	url="https://github.com/Rosemeis/projectionSVD",
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
	ext_modules=cythonize(extensions),
	python_requires=">=3.10",
	install_requires=[
		"cython>3.0.0",
		"numpy>2.0.0"
	],
	packages=["projection"],
	entry_points={
		"console_scripts": ["projectionSVD=projection.main:main"]
	},
)

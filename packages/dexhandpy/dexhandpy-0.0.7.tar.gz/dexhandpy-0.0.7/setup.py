import glob
import os.path
from distutils.core import setup

__version__ = "0.0.7"

BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


ext_modules = []
try:
    from pybind11.setup_helpers import Pybind11Extension, ParallelCompile, naive_recompile
    ParallelCompile("NPY_NUM_BUILD_JOBS", needs_recompile=naive_recompile, default=4).install()
    source_files = glob.glob('./*.cpp', recursive=True)
    include_dirs = ["./fdexhand/include/*.h", "./fdexhand/include/hand/*.h", "./fdexhand/include/hand/commsocket/*.h", "./fdexhand/include/hand/fourierdexhand/*.h", "./fdexhand/include/hand/rapidjson/*.h"]
    library_dirs = ["./fdexhand/include"]
    runtime_library_dirs = [os.path.abspath("./fdexhand/include")]
    libraries = ["FourierDexHand"]

    ext_modules = [
        Pybind11Extension(
            "dexhandpy.fdexhand",
            source_files,
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            runtime_library_dirs=runtime_library_dirs,
            libraries=libraries,
            cxx_std=14,
            language='c++'
        )
    ]

except ImportError:
    exit(1)

setup(
    name='dexhandpy',  # used by `pip install`
    version=__version__,
    author="Afer Liu",    
    author_email="fei.liu@fftai.com",   
    description= "Fourier dexhand general sdk",
    ext_modules=ext_modules,
    packages=['fdexhand'], # the directory would be installed to site-packages
    setup_requires=["pybind11"],
    install_requires=["pybind11"],
    python_requires='>=3.10',
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
)

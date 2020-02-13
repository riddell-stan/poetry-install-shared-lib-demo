from distutils.extension import Extension
import subprocess
import tempfile

from Cython.Build import cythonize

extensions = [
    Extension(
        "poetry_install_shared_lib_demo.wrappers",
        sources=["poetry_install_shared_lib_demo/wrappers.pyx"],
        libraries=["protobuf"],
    )
]


# poetry-specific method to update call to `setup`
def build(setup_kwargs):
    # install protobuf shared library
    protobuf_src_url ="https://github.com/protocolbuffers/protobuf/releases/download/v3.11.3/protobuf-cpp-3.11.3.tar.gz"
    subprocess.run(["curl", "--silent", "--location", "--remote-name", protobuf_src_url])
    with tempfile.TemporaryDirectory(prefix="poetry_install_shared_lib_demo") as tmpdirname:
        subprocess.run(["tar", "-zvxf", "protobuf-cpp-3.11.3.tar.gz", "-C", tmpdirname])
        src_dir = f"{tmpdirname}/protobuf-3.11.3"
        # {lib, include} will be installed into /usr/local/{lib,include}
        # /usr/local is the default prefix, added here for the reader's benefit
        subprocess.run(["./configure", "--prefix=/usr/local"], cwd=src_dir)
        subprocess.run(["make"], cwd=src_dir)
        subprocess.run(["make", "install"], cwd=src_dir)
    subprocess.run(["ldconfig"])   # refresh shared library cache

    # configure poetry to build our C extension module
    setup_kwargs.update({"ext_modules": cythonize(extensions)})

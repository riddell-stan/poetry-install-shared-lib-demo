from distutils.extension import Extension

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
    setup_kwargs.update({"ext_modules": cythonize(extensions)})

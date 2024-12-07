import re, codecs
from setuptools import setup, Extension

def get_version(version_file):
    """
    Construct the version string without using
        from mhi.pscad import VERSION
    since the import will fail if the module is not installed,
    which it won't be since we are trying to build it. (Catch-22)
    """

    with codecs.open(version_file, 'r') as fp:
        contents = fp.read()

    match = re.search(r"^_VERSION = \((\d+), (\d+), (\d+)\)$", contents, re.M)
    if match is None:
        raise RuntimeError("Unable to find _VERSION")
    version = ".".join(match.groups())

    match = re.search(r"^_TYPE = '([abcf]\d)'$", contents, re.M)
    if match is None:
        raise RuntimeError("Unable to find _TYPE")
    version_type = match.group(1).lower()

    if version_type != 'f0':
        if version_type[0] == 'f':
            version_type = 'p' + version_type[1]
        version += version_type

    return version

version = get_version(r'src/mhi/cosim/__init__.py')

cosim = Extension('_cosim',
                  sources=['src/ext/cosim.c',
                           'src/ext/EmtCoSim/EmtCoSim.c',
                           ],
                  #include_dirs=['src/ext/EmtCoSim',
                  #              ],
                  )

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='mhi-cosim',
      version=version,
      description='MHI Cosimulation Module',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      ext_modules=[cosim],
      ext_package='mhi.cosim',
      package_dir={'': 'src'},
      packages=['mhi.cosim'],
      package_data={'mhi.cosim': ['*.chm']},
      requires=['wheel'],
      python_requires='>=3.6',
      author='Manitoba Hydro International Ltd.',
      author_email='pscad@mhi.ca',
      url='https://www.pscad.com/webhelp-v5-al/index.html',
      license="BSD License",

      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
      ],
      )

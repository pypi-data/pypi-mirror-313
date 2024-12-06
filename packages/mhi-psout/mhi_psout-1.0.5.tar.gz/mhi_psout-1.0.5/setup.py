import codecs, re, site, sys, shutil, os
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

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

VERSION = get_version(r'src\mhi\psout\__init__.py')

with open("README.md") as f:
    long_description = f.read()

if os.path.exists(r'Release\CurveFile.dll'):
    print(r"*** Copying CurveFile.dll to src\mhi\psout ***")
    shutil.copyfile(r'Release\CurveFile.dll', r'src\mhi\psout\CurveFile.dll')

setup(version=VERSION,
      requires=['wheel'],
      tests_require=['matplotlib'],
      package_dir={'': 'src'},
      packages=['mhi.psout'],
      ext_package='mhi.psout',
      ext_modules=[
          Extension(
              name='_psout',
              sources=['PSOut/PSOut.cpp',
                       'PSOut/Closable.cpp',
                       'PSOut/Call.cpp',
                       'PSOut/File.cpp',
                       'PSOut/Trace.cpp',
                       'PSOut/Run.cpp',
                       'PSOut/VarList.cpp',
                       ],
              include_dirs=['PSOut'],
              libraries=['CurveFile',],
              library_dirs=['Release', 'Debug', ],
              )
          ],
      package_data={
          'mhi.psout': ['*.dll', '*.chm'],
          },
      )

import sys
import setuptools
from setuptools import find_packages, setup
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from os.path import join, dirname, realpath

str_version = '0.0.48'



def configuration(parent_package='', top_path=''):
    # this will automatically build the scattering extensions, using the
    # setup.py files located in their subdirectories
    config = Configuration(None, parent_package, top_path)

    pkglist = setuptools.find_packages()
    for i in pkglist:
        config.add_subpackage(i)
    config.add_data_files(join('vvdutils', 'assets', '*.json'))
    config.add_data_files(join('vvdutils', 'assets', '*.jpg'))

    return config


if __name__ == '__main__':
    pass
    setup(
        configuration=configuration,
        name='vvdutils',
        version=str_version,
        description='Commonly used function library by VVD',
        url='https://github.com/zywvvd/utils_vvd',
        author='zywvvd',
        author_email='zywvvd@mail.ustc.edu.cn',
        license='MIT',
        packages=['vvdutils'],
        zip_safe=False,
        install_requires= ['numpy', 'opencv-python', 'numba', 'func_timeout', 'pypinyin','scikit-learn', 'pathlib2', 'tqdm', 'pytest', 'matplotlib', 'pandas', 'flask', 'shapely', 'pyproj', 'bson', 'scikit-image'],
        python_requires='>=3')
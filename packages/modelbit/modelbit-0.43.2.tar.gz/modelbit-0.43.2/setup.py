from setuptools import find_packages, setup  # type: ignore
import sys

with open("README.md", "r") as fh:
  long_description = fh.read()

with open("requirements.txt", "r") as fh:
  required_packages = fh.read().strip().split("\n")

if sys.version_info >= (3, 8):
  required_packages.append("importlib-metadata")  # see _getPipList()

setup(
    name='modelbit',
    description='Modelbit helps you rapidly deploy and manage ML models with modern MLOps features.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.modelbit.com',
    author='Modelbit',
    author_email='tom@modelbit.com',
    license='Modelbit',
    data_files=[('', ['requirements.txt'])],
    packages=find_packages(),
    package_data={"modelbit": ["*.pyi", "*.png", "templates/*.j2", "py.typed"]},
    include_package_data=True,
    entry_points={'console_scripts': ['modelbit=modelbit.cli:main']},
    # Note: Keep these deps in sync with snowpark config
    install_requires=required_packages,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import os
import shutil
import glob
# Helper function to find all .py files, excluding __init__.py
def find_pyx_files(directory):
    pyx_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                pyx_files.append(os.path.join(root, file))
    return pyx_files

# Specify the directories you want to convert to .so
directories = ['rejoai']

# Collect all .py files
pyx_files = []
for directory in directories:
    pyx_files.extend(find_pyx_files(directory))

# Define the extensions
extensions = [Extension(
    pyx.replace('.py', '').replace('/', '.'),
    [pyx]) for pyx in pyx_files]

setup(
    name='rejoai',
    packages=find_packages(),
    version='0.1.7',
    description='my_project',
    author='author',
    license='Proprietary',
    install_requires=[
        'cython',
    ],
    ext_modules=cythonize(extensions,compiler_directives={'language_level': 3}),
)

# Copy __init__.py files to build_package directory
for directory in directories:
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '__init__.py':
                dest_dir = root.replace('rejoai', 'build_package/rejoai')
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy(os.path.join(root, file), os.path.join(dest_dir, file))

# Copy .so files to build_package directory
for so_file in glob.glob('rejoai/**/*.so', recursive=True):
    dest_file = so_file.replace('core', 'build_package/rejoai')
    dest_dir = os.path.dirname(dest_file)
    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(so_file, dest_file)

# Cleanup .c files from core directory
for directory in directories:
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".c"):
                os.remove(os.path.join(root, file))

# Remove the build folder
shutil.rmtree('build', ignore_errors=True)

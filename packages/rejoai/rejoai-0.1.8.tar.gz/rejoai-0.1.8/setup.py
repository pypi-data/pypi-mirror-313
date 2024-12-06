from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import os
import shutil
import glob

def find_pyx_files(directory):
    pyx_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                pyx_files.append(os.path.join(root, file))
    return pyx_files

# Specify the directories you want to convert to .so
directories = ['rejo_ai']

# Collect all .py files
pyx_files = find_pyx_files('rejo_ai')

# Define the extensions with corrected module paths
extensions = [
    Extension(
        f'rejo_ai.{os.path.splitext(os.path.basename(pyx))[0]}',
        [pyx]
    ) for pyx in pyx_files
]

setup(
    name='rejoai',
    packages=find_packages(),
    version='0.1.8',
    description='my_project',
    author='author',
    license='Proprietary',
    setup_requires=['cython'],
    install_requires=['cython'],
    ext_modules=cythonize(
        extensions, 
        compiler_directives={'language_level': 3}
    ),
)

# Copy __init__.py files to build_package directory
for directory in directories:
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '__init__.py':
                dest_dir = root.replace('rejo_ai', 'build_package/rejo_ai')
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy(os.path.join(root, file), os.path.join(dest_dir, file))

# Copy .so files to build_package directory
for so_file in glob.glob('rejo_ai/**/*.so', recursive=True):
    dest_file = so_file.replace('rejo_ai', 'build_package/rejo_ai')
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




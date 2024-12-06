from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import os
import shutil
import glob
import sys

python_version = f"{sys.version_info.major}{sys.version_info.minor}"
package_version = f"0.2.3.post{python_version}"  

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
    version=package_version, 
    description="A brief description",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='author',
    license='Proprietary',
    setup_requires=['cython'],
    install_requires=['cython'],
    ext_modules=cythonize(
        extensions, 
        compiler_directives={'language_level': 3}
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,  # Ensure non-code files are included
    package_data={
        "": ["*.so"],  # Include only .so files
    },
    exclude_package_data={
        "": ["*.py", "*.pyc"],  # Exclude .py and .pyc files
    },

)

# # Copy __init__.py files to build_package directory
# for directory in directories:
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file == '__init__.py':
#                 dest_dir = root.replace('rejo_ai', 'build_package/rejo_ai')
#                 os.makedirs(dest_dir, exist_ok=True)
#                 shutil.copy(os.path.join(root, file), os.path.join(dest_dir, file))

# # Copy .so files to build_package directory
# for so_file in glob.glob('rejo_ai/**/*.so', recursive=True):
#     dest_file = so_file.replace('rejo_ai', 'build_package/rejo_ai')
#     dest_dir = os.path.dirname(dest_file)
#     os.makedirs(dest_dir, exist_ok=True)
#     shutil.move(so_file, dest_file)     
                                                                                                                                                                                                                                                       

# # Cleanup .c files from core directory
# for directory in directories:
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".c"):
#                 os.remove(os.path.join(root, file))

# # Remove the build folder
# shutil.rmtree('build', ignore_errors=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          




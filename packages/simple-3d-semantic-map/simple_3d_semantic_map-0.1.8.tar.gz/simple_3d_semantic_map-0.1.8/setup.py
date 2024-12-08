from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name = 'simple_3d_semantic_map',
    version = '0.1.8',
    packages = find_packages(),
    install_requires = [
    'pyrealsense2==2.54.2',
    'numpy==1.26.4',
    'matplotlib==3.8.3',
    'torch==2.3.0',
    'open3d==0.18.0',
    'opencv-python==4.9.0.80',
    'transformers==4.46.1',
    ],
    long_description=description,
    long_description_content_type='text/markdown',
    license='MIT',
    url = 'https://github.com/Morpheus1024/simple_3D_semantic_map',
    python_requires="==3.9",
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)

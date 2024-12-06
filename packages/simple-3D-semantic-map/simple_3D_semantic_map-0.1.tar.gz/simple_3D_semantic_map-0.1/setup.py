from setuptools import setup, find_packages

setup(
    name = 'simple_3D_semantic_map',
    version = '0.1',
    packages = find_packages(),
    install_requires = [
    'pyrealsense2==2.54.2.5684',
    'numpy==1.26.4',
    'matplotlib==3.8.3',
    'torch==2.3.0',
    'open3d==0.18.0',
    'opencv-python==4.9.0.80',
    'transformers==4.46.1',
    ],
)

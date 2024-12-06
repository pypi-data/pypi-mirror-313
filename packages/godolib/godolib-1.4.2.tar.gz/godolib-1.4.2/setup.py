from setuptools import setup, find_packages

setup(
    name='godolib',
    version='1.4.2',  # Incremented version number to reflect the update
    packages=find_packages(),
    install_requires=[
        'statsmodels',
        'numpy',
        'scikit-learn',
        'pandas',
        'boto3',
        'chardet',
        'psutil',
        'plotly',
        'matplotlib',
        'requests',
        'h5py',
        'tensorflow',
        'nvidia-ml-py3'  # Added pynvml dependency
    ],
    description='Machine/Deep learning and preprocessing oriented library',
    author='Sergio Montes',
    author_email='ss.montes.jimenez@gmail.com',
    url='',  # Add your project URL here, if available
)

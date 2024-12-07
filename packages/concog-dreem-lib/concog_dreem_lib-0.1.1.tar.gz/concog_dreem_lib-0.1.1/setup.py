from setuptools import setup, find_packages

setup(
    name='concog_dreem_lib',
    version='0.1.1',  
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'concog_dreem_lib': ['matlab_functions/*.m'],
    },
    install_requires=[
        'numpy',
        'pandas',
        'mne',
        'scipy',
        'fooof',
        # Note: MATLAB Engine API is not installable via pip
    ],
    python_requires='>=3.6',  
    author='Max Hughes',
    author_email='hugmax12@gmail.com',
    description='Library for LZ complexity, wSMI calculations, and PSD analysis with EEG data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        
    ],
    license='MIT', 
)
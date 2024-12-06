from setuptools import setup, find_packages, find_namespace_packages

VERSION = '0.0.70' 
DESCRIPTION = 'Machine Learning'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="rsp-ml", 
        version=VERSION,
        author="Robert Schulz",
        author_email="schulzr256@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        package_dir={"rsp": "rsp"},
        include_package_data=True,
        package_data={
            #"rsp": ["drl/environment/image/*.png"]
        },
        license="MIT",
        packages=find_packages(),
        #packages=find_namespace_packages(where='rsp'),
        install_requires=[
            'torch',
            'torchvision',
            # 'torchaudio',
            'rsp-common>=0.0.24',
            'numpy',
            'opencv-python',
            # 'gym',
            # 'matplotlib',
            'pandas',
            'seaborn',
            'googledriver'
        ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        url = "https://github.com/SchulzR97/rsp-ml",

        keywords=['python', 'Machine Learning'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",     
        ]
)
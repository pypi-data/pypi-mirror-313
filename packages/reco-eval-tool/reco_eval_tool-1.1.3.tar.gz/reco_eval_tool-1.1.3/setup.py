from setuptools import setup, find_packages

VERSION = '1.1.3' 
DESCRIPTION = 'Reco evaluation tool'
LONG_DESCRIPTION = 'This tool aims to provide a set of evaluation metrics for recommendation'


setup(
        name="reco_eval_tool", 
        version=VERSION,
        author="Minglei Guo",
        author_email="<mingleiguo@microsoft.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
			"pandas",
			"numpy",
			"seaborn",
			"matplotlib",
			"scikit-learn",				  
        ],         
        keywords=['evaluation', 'precision', 'recall', 'F1'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
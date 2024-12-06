from setuptools import setup, find_packages

setup(
    name="lance_converter",          
    version="0.1.1",                      
    packages=find_packages(),             
    install_requires=[                    
        'pyarrow',
        'pandas',
        'tqdm',
        'pillow',
        'lance',
        'lancedb'
    ],
    entry_points={                        
        'console_scripts': [
            'lance_converter = lance_converter.converter:main', 
        ],
    },
    description="A Python package for converting image datasets to Lance format", 
    author="Vipul Maheshwari",                  
    author_email="vim.code.level@gmail.com",  
    classifiers=[                        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
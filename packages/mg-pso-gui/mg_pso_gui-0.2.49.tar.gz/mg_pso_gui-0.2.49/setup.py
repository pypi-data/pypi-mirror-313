from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.2.49'
DESCRIPTION = 'GUI for MG-PSO'
LONG_DESCRIPTION = open('../README.md').read()

# Setting up
setup(
    name="mg-pso-gui",
    version=VERSION,
    author="Robert Cordingly",
    author_email="<rcording@uw.ed>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={
        'mgpsogui': ['*.json', '*.png', 'images/*.png', 'gui/defaults/*.json', 'gui/images/*.png', '*.yaml'],
    },
    include_package_data=True,
    install_requires=['pandas', 
                      'numpy', 
                      'requests',
                      'tk',
                      'customtkinter',
                      'plotly',
                      'csip',
                      'csip-cosu',
                      'kaleido',
                      'pillow'],
    keywords=['python', 'muti-group', 'pso', 'particle', 'swarm', 'optimization', 'gui'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    
    entry_points={
        'setuptools.installation': [
            'eggsecutable=mgpsogui.mgpsogui:open'
        ],
        'console_scripts': [
            'mgpsogui=mgpsogui.mgpsogui:open',
        ],
    }
)
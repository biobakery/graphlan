import setuptools
from setuptools.command.install import install
from io import open
import os

install_requires = ["biopython==1.76", "matplotlib>=1.1", "scipy"]
setuptools.setup(
    name='graphlan',
    version='1.1.3.1',
    author='Francesco Asnicar',
    author_email='f.asnicar@unitn.it',
    url='http://github.com/biobakery/graphlan',
    packages = setuptools.find_packages(),
    scripts=['graphlan.py', 'graphlan_annotate.py'],
    package_dir = {'graphlan' : '' },
    package_data = { 'graphlan' : [
        'src/*'
    ]},
    # entry_points = { "console_scripts" : [ "graphlan.py = graphlan:main",
    #                                        "graphlan_annotate.py = graphlan_annotate:main"
    #                                      ] },
    long_description_content_type='text/markdown',
    long_description=open('readme.md').read(),
    description='GraPhlAn is a software tool for producing high-quality circular representations of taxonomic and phylogenetic trees. GraPhlAn focuses on concise, integrative, informative, and publication-ready representations of phylogenetically- and taxonomically-driven investigation.',
    install_requires=install_requires
)

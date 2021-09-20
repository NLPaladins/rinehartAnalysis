from setuptools import setup, find_packages, Command
import os


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


# Load Requirements
with open('requirements.txt') as f:
    requirements = f.readlines()

# Load README
with open('README.md') as readme_file:
    readme = readme_file.read()

setup_requirements = []
test_requirements = []

COMMANDS = [
    'nlp_main = main:main'
]

data_files = ['nlp_libs/configuration/yml_schema.json']

setup(
    author="jeanmerlet, drkostas, LaneMatthewJ",
    author_email="jmerlet@vols.utk.edu, kgeorgio.vols.utk.edu, mlane42@vols.utk.edu",
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],
    cmdclass={
        'clean': CleanCommand,
    },
    data_files=[('', data_files)],
    description="Rinehart Analysis for the NLP (ECE-617) Project 1.",
    entry_points={'console_scripts': COMMANDS},
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='starter',
    name='starter',
    packages=find_packages(include=['nlp_libs',
                                    'nlp_libs.*']),
    setup_requires=setup_requirements,
    url='https://github.com/NLPaladins/rinehartAnalysis',
    version='0.1.0',
    zip_safe=False,
)

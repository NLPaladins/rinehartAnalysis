# Rinehart Analysis<img src='https://avatars.githubusercontent.com/u/90112108' align='right' width='180' height='104'>

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/NLPaladins/rinehartAnalysis/master/LICENSE)

## Table of Contents

+ [About](#about)
+ [TODO](#todo)
+ [Libraries Overview](#lib_overview) 
+ [Prerequisites](#prerequisites)
+ [Bootstrap Project](#bootstrap)
+ [Running the code from main.py](#run_main)
    + [Configuration](#configuration)
    + [Execution](#execution)
+ [Running the code using Jupyter](#jupyter)
    + [Local Jupyter](#local_jupyter)
    + [Google Collab](#google_collab)
+ [Adding New Libraries](#adding_libs) 
+ [License](#license)

## About <a name = "about"></a>

Rinehart Analysis for NLP (ECE-617) Project 1.

## TODO <a name = "todo"></a>

Read the [TODO](TODO.md) to see the current task list.

## Libraries Overview <a name = "lib_overview"></a>

All the libraries are located under *"\<project root>/nlp_libs"*
- ***ProcessedBook***: Loc: **books/processed_book.py**, Desc: *Book Pre-processor*
- ***Configuration***: Loc: **configuration/configuration.py**, Desc: *Configuration Loader*
- ***ColorizedLogger***: Loc: **fancy_logger/colorized_logger.py**, Desc: *Logger with formatted text capabilities*

## Prerequisites <a name = "prerequisites"></a>

You need to have a machine with Python >= 3.9 and any Bash based shell (e.g. zsh) installed.
Having installed conda is also recommended.

```Shell

$ python3.9 -V
Python 3.9.7

$ echo $SHELL
/usr/bin/zsh

```

## Bootstrap Project <a name = "bootstrap"></a>

All the installation steps are being handled by the [Makefile](Makefile).

If you want to use conda run:
```Shell
$ make install
```

If you want to use venv run:
```Shell
$ make install env=venv
```

## Running the code from main.py <a name = "run_main"></a>

In order to run the code, you will only need to configure the yml file, and either run its
file directly or invoke its console script.

### Modifying the Configuration <a name = "configuration"></a>

You may need to configure the yml file. There is an already configured yml file 
under [confs/proj_1.yml](confs/proj_1.yml).

### Execution <a name = "execution"></a>
First, make sure you are in the correct virtual environment:

```Shell
$ conda activate rinehartAnalysis

$ which python
/home/<your user>/anaconda3/envs/rinehartAnalysis/bin/python
```

Show help:
```Shell
$ python main.py --help
usage: main.py -c CONFIG_FILE -l LOG [-d] [-h]

Rinehart Analysis for NLP (ECE-617) Project 1

Required Arguments:
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        The configuration yml file
  -l LOG, --log LOG     Name of the output log file

Optional Arguments:
  -d, --debug           Enables the debug log messages
  -h, --help            Show this help message and exit
```

Execute the code:
```Shell
$ python main.py -c confs/proj_1.yml -l logs/proj_1.log
```

## Using Jupyter <a name = "jupyter"></a>

In order to run the code, you will only need to configure the yml file, and either run its
file directly or invoke its console script. Refer to [Configuration](#configuration) Section.

### Local Jupyter <a name = "local_jupyter"></a>

First, make sure you are in the correct virtual environment:

```Shell
$ conda activate rinehartAnalysis

$ which python
/home/<your user>/anaconda3/envs/rinehartAnalysis/bin/python
```

To use jupyter, first run `jupyter`:

```shell
jupyter notebook
```
And open the [main.ipynb](main.ipynb).

### Google Collab <a name = "google_collab"></a>

Just Open this [Google Collab Link](https://colab.research.google.com/drive/1evpodmjkOM1_NzyinYWJCz4xVRHAXZb6).

## Adding New Libraries <a name = "adding_libs"></a>

If you want to add a new library (e.g. a Class) in the project you need to follow these steps:
1. Create a new folder under *"\<project root>/nlp_libs"* with a name like *my_lib*
2. Create a new python file inside it with a name like *my_module.py*
3. Paste your code inside it
4. Create a new file name *__init__.py*
5. Paste the follwing code inside it:
   ```python
    """<Library name> sub-package."""
    
    from .<Module name> import <Class Name>
    
    __email__ = "jmerlet@vols.utk.edu, kgeorgio.vols.utk.edu, mlane42@vols.utk.edu"
    __author__ = "jeanmerlet, drkostas, LaneMatthewJ"
    __version__ = "0.1.0"
    ```
6. Open [\<project root>/nlp_libs/\_\_init\_\_.py](nlp_libs/__init__.py)
7. Add the following line: ```from nlp_libs.<Module name> import <Class Name>```
8. (Optional) Rerun `make install` or `python setup.py install` 
 
## License <a name = "license"></a>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



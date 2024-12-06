# The Genovation python toolbox

This python tool-box is supposed to help Genovation associates in their day-to-day work.

# INSTALL

## Pre-requisites

* Windows PowerShell (Terminal on Windows)
  * Console to run `genov` tool box, and its commands
  * How-to from Microsoft: https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows

* Python:
  * `genov` is tested with Python 3.13
  * As of EoY 2024, Python 3.13.0 is available at: https://www.python.org/downloads/
  * Note: starting with Python 3.4, `pip` is by default included

Once installed, you can check in your terminal:
```console
foo@bar:~$ python3 --version
           >> Python 3.13.0
foo@bar:~$ pip3 --version
           >> pip 24.3.1 from /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/pip (python 3.13)
```

Notes:
* On your system, you might have to replace the `python3` with `python`
* To check where is your python installed: `which python3`: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`

## Install Genov

* Simply type in your Terminal: `pip3 install genov`

# Use

## Cheat sheet

## Versions

* 0.0.1, as of 29-Nov-2024: Framework initialized
* 0.0.2, as of 3-Dec-2024: get issues from jira, and persist in an excel spreadsheet

# Contribute

## Dependencies

| Dependencies    | Description                                                                                                            |
|:----------------|:-----------------------------------------------------------------------------------------------------------------------|
| `com-enovation` | The seed toolbox that we use to initialize this toolbox. To decommission as commands are being re-instantiated here... |
| `typer`         | Library for building CLI applications, based on Click                                                                  |
| `tomlkit`       | Library for manipulating configuration file                                                                            |
| `pydash`        | Library for manipulating dictionaries with path...                                                                     |

## Cheat sheet

### Distribution

* build the distribution files and directories: `python3 -m build`
  * Directories `build` and `dist` should be generated
* To install the local build (rather than fetching from pipy), execute the following command from the project root: `rm -rf dist;python3 -m build;pip3 uninstall genov;pip3 install dist/genov-*.tar.gz`
* publish to `pypi`: `python3 -m twine upload --repository pypi dist/*`
  * In case you face an error `No module named twine`, you need first to run `pip install twine`
  * Package viewable at [pypi](https://pypi.org/project/genov)

### Typer

* To get emojis that can be printed by `rich.print()`: run `python -m rich.emoji` in console

### Pycharm configuration

* Unit test configuration, from menu `Run > Edit Configurations...`
  * `Configuration > Target > Script path: ~/PycharmProjects/com_enovation.murex/tests`
  * `Configuration > Working directory: ~/PycharmProjects/com_enovation.murex/`
  * `Configuration > Add content roots to PYTHONPATH: checked`
  * `Configuration > Add source roots to PYTHONPATH: checked`

### Python stuff

* Check we have latest versions:
  * pip: `python3 -m pip install --upgrade pip`
  * build to generate the distribution: `python3 -m pip install --upgrade build`

* Update packages using pip
  * Check all packages are fine: `pip check`
  * List all packages outdated: `pip list --outdated`
  * Update all packages outdated:
    * On Mac: `pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U`
    * On Windows: `pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}`
* A simple example package. You can use [Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/) to write your content.

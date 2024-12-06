# Sphinx extension: TU Delft theme 

## Introduction

The default theme in JupyterBooks is usually not desired and need to be changed by adding custom stylesheets. The **Sphinx-TUDelft-theme** extension provides a simple solution to have a uniform theme across all the books created at Delft University of Technology that matches the TU Delft identity.

## What does it do?

This extension applies styling changes, e.g. using specific fonts, and adding particular colours for admonitions. You can see how the TU Delft theme looks like applied in this [example book](http://teachbooks.io/TU-Delft-Theme-Example/).


## Installation
To install the Sphinx-Image-Inverter, follow these steps:

**Step 1: Install the Package**

Install the `sphinx-tudelft-theme` package using `pip`:
```
pip install sphinx-tudelft-theme
```

**Step 2: Add to `requirements.txt`**

Make sure that the package is included in your project's `requirements.txt` to track the dependency:
```
sphinx-tudelft-theme
```

**Step 3: Enable in `_config.yml`**

In your `_config.yml` file, add the extension to the list of Sphinx extra extensions (**important**: underscore, not dash this time):
```
sphinx: 
    extra_extensions:
        - sphinx_tudelft_theme
```

## Usage

By following the steps above, the theme will be applied automatically. To see the examples of usage visit the [TeachBooks manual](https://teachbooks.io/manual/intro.html).


## Contribute
This tool's repository is stored on [GitHub](https://github.com/TeachBooks/Sphinx-TUDelft-theme). The `README.md` of the branch `Manual` is also part of the [TeachBooks manual](https://teachbooks.io/manual/intro.html) as a submodule. If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/Sphinx-TUDelft-theme). To update the `README.md` shown in the TeachBooks manual, create a fork and open a merge request for the [GitHub repository of the manual](https://github.com/TeachBooks/manual). If you intent to clone the manual including its submodules, clone using: `git clone --recurse-submodulesgit@github.com:TeachBooks/manual.git`.
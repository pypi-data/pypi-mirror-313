# Overview
Business Analysis Core (BACore) is framework around a set of tools for common business analysis work. The main focus of BACore is on documentation and testing. BACore is written in Python and is available through [pypi.org](https://pypi.org/project/bacore/) and on [Github](https://github.com/bacoredev/bacore).

!!! note

    BACore is currently in planning stage of development. The API, CLI and everything else is subject to change.

## Getting Started
There are two main ways to use BACore:

1. Use the common mathematical formulas and functions as basis for writing test cases in your own project.
2. Use BACore on the command line to rapidly set up a documentation and test environments for your project.

### BACore as Lib
To use BACore in your own project install with: `pip install bacore`.

### BACore as CLI
To use BACore on the command line install with: `pip install bacore[cli]`.

Once you have installed BACore, then you can create a new project with: `bacore create project <project_name>`.

Most of the underlying functionality is available through the CLI. BACore CLI is reusing functionality from other
projects such as [Hatch](https://github.com/pypa/hatch).

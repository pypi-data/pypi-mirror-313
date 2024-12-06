# Public Project AllOnIAS3

This project contains the :obj:`~allonias3.s3_path.S3Path` class that allows the user to interact with
its S3 repository in a similar fashion as [pathlib.Path](https://docs.python.org/3/library/pathlib.html)

Even though it is a public package, it is not intended to be used outside
AllOnIA's plateform.

You can find the user documentation at [this URL](https://aleia-team.gitlab.io/public/allonias3)

This is a public project. Everyone is welcome to contribute to it.

## Basic usage

See :ref:`basicusage`

## Installation

```bash
pip install allonias3[boto,datatypehandler]
```

 * By default, :obj:`~allonias3.s3_path.S3Path` will use a Minio client by
   inheriting from :obj:`~allonias3.minio.minio_path.MinioPath`. You can choose to use
   boto instead, by choosing "boto" as an optional dependency and `USE_BOTO=True`
   in your environment variables. Then, :obj:`~allonias3.s3_path.S3Path`
   will inherit from :obj:`~allonias3.boto.boto_path.BotoPath`. In both cases
   the methods will take exactly the same input and return the same output. 
 * Writing and reading data to S3 can be enhanced to support many data types,
   like :obj:`~pandas.DataFrame` to/from *.csv* files, by specifying
   "datatypehandler" as an optional dependency.

## Contributing

This is an open-source project. Everyone is welcome to contribute to it. To do
so, fork the repository, add your features/fixes on your forked repository,
then open a merge request to the original repository.

### Install dependencies using poetry

This project uses [Poetry](https://python-poetry.org/) to manage its
working environment. Install it before coding in the project.

Then, run 

 ```bash 
poetry env use python3.12
poetry install
poetry run pre-commit install
```

This package has two sets of optional libraries, that you can install with

```bash
poetry install -E boto
# or
poetry install -E datatypehandler
# or
poetry install -E datatypehandler -E boto
```

### Testing

Tests are separated into several groups, that can require different packages.

You can run them all using tox:

```bash
poetry run tox
```

You can also run them individually by running commands that you can find
in [tox.ini](tox.ini).

Some tests can not be run un parallel, the "-n 0" args is then require. Refer
to the [tox.ini](tox.ini) file to find which tests are concerned.

#### Coverage

We use `pytest-cov` to display the coverage, so, after run
tests you can check the reports (term, html, xml are enabled), if you want to
improve your coverage, the better thing to do is to check the html report in
your browser:

```bash
open htmlcov/index.html
```

### Lint

To run the linters used by this project, you can run:

```bash
poetry run pre-commit run # Run lint only on staged files

# Manually check conventional commits format:
poetry run pre-commit run gitlint --hook-stage commit-msg --commit-msg-filename .git/COMMIT_EDITMSG
```

### User documentation

The documentation source files are located in [here](docs/source/). If you add
new features, please add them to the documentation as well.

You can buid the documentation locally by doing

```bash
cd docs
make html
```

The produced documentation should then be readable by opening the file in
docs/build/html/index.html in a web browser.


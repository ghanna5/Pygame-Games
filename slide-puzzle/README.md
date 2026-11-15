# Hello Pygame

This is an exercise to verify you have a working Python v.3 and Pygame installation to continue on to the next project in this course.

Below each step are suggestions on how to accomplish the step.

The requirements of this exercise are:

1. Create a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html).
    ```shell
    python3 -m venv env
    ```
1. Activate your newly created virtual environment. Assuming a BASH shell:
    ```shell
    source env/bin/activate
    ```
1. Install Pygame into the virtual environment using pip.
    ```shell
    pip install pygame
    ```
1. Copy [Al Sweigart's Slide Puzzle](https://github.com/asweigart/making-games-with-python-and-pygame/blob/master/slidepuzzle/slidepuzzle.py) into your repository. To download the file directly from the command line:
    ```shell
    wget https://raw.githubusercontent.com/asweigart/making-games-with-python-and-pygame/refs/heads/master/slidepuzzle/slidepuzzle.py
    ```
1. Add Al Sweigart's Slide Puzzle to your repository and commit it.
    ```shell
    git add slidepuzzle.py && git commit slidepuzzle.py -m "Initial import from Al Sweigart's Making Games with Python and Pygame"
    ```
1. Add a shebang and add executable permissions for user, group, and other to `slidepuzzle.py` such that it can be run from the command prompt with the command `./slidepuzzle.py`. Verify that you are able to run `slidepuzzle.py`.
    ```shell
    sed -i '1i#!/usr/bin/env python3' slidepuzzle.py && chmod ugo+x slidepuzzle.py
    ```

1. Freeze the virtual environment using the `pip freeze` command into a file named `requirements.txt`. The file must be named `requirements.txt`. Use the command:
    ```shell
    pip freeze > requirements.txt
    ```
1. Add `requirements.txt` to your repository and commit it.
    ```shell
    git add requirements.txt && git commit requirements.txt -m "Initial add of Python package requirements."
    ```
1. Push your repository back to GitHub.
    ```shell
    git push
    ```

_Do not add and comit your Python virtual environment directory._

## Optional

Although not required, it is highly recommended that you do this.

1. Install pylint into your virtual environment
    ```shell
    pip install pylint
    ```
1. Generate an [RC file](https://en.wikipedia.org/wiki/RUNCOM) for pylint. 
    ```shell
    pylint --generate-rcfile > .pylintrc
    ```
1. Edit the file and change `unsafe-load-any-extension=no` to `unsafe-load-any-extension=yes`.
    ```shell
    sed -i 's/unsafe-load-any-extension=no/unsafe-load-any-extension=yes/g' .pylintrc
    ```
1. Lint `slidepuzzle.py`. You do not need to make any changes, just make observations.
    ```shell
    pylint slidepuzzle.py
    ```

# Rubric

This exercise is worth 5 points.

* Python virtual environment requirements file (3 points): contains the required packages to run the project and can be used to recreate the virtual environment
* slidepuzzle.py (2 points) The file was copied, added & committed, modified so that it can be executed in the virtual environment with the command `./slidepuzzle.py`.


# Remove the virtual env created by devbox (after running `devbox shell`) 
rm -rf .venv/

# Get the required python version in .python-version (already installed via pyenv)
PYTHON_VERSION=$(pyenv version-name)

# Configure poetry to use the installed python version and create a virtual env again
poetry env use $HOME/.pyenv/versions/$PYTHON_VERSION/bin/python
poetry config virtualenvs.in-project true
poetry check
poetry install
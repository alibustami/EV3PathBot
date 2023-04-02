cmake_minimum_required(VERSION 3.10)

project(EV3PathBot)

add_custom_target(virenv
    COMMAND conda env create -f environment.yaml
)

add_custom_target(install
    COMMAND python -m pip install --upgrade pip &&
            pip install --upgrade pip setuptools wheel &&
            python -m pip install -e . &&
            pre-commit install
)

add_custom_target(test
    COMMAND python -m unittest discover tests
)s

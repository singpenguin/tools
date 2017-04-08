# mix
mix is a project init tool for python


# Usage

    python mix project_name

    tree project_name

    > python mix test
    > tree test

    ├── README.md
    ├── backend
    │   └── __init__.py
    ├── common
    │   ├── __init__.py
    │   └── utils.py
    ├── config
    │   ├── __init__.py
    │   ├── settings.py
    │   └── url.py
    ├── controllers
    │   ├── __init__.py
    │   └── page.py
    ├── index.py
    ├── models
    │   └── __init__.py
    ├── requirements.txt
    ├── static
    ├── templates
    └── tests

    Tornado project
    > python mix test tornado
    > cd test
    > python index.py
    > wget http://localhost:8080

if git has been installed. It's already a git repository.

# Welcome to pycmd-todo

A [Textual](https://github.com/Textualize/textual) framework based todo application.

## Installation

You can install pycmd-todo via PyPI, with the following command:

```
pip install pycmd-todo
```

then you can run it by the follwoing command:
```
pytodo
```
### Default user

After running pytodo, pycmd-todo will initialize (if it is running for the first time)
and create a default user with username *aad* and password *admin*.
You will need these credentials to login for the first time. You can change it latter - of course.


### Database location
pycmd-todo will create a directory (*~/.pytodo*) in user home directory and will place
the database (*~/.pytodo/todo_db.sqlite*) file there. Removing the directory or the
database will result in data loss and reinitialization of the database.

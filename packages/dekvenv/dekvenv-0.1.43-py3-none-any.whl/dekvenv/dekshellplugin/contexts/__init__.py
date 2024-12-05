from ...active import activate_venv

context = {
    'avenv': lambda path_venv=None, ignore=True: activate_venv(path_venv, ignore),
}

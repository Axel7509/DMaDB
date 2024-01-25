GUEST_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign in': '--> sign in to to your account',
    'sign up': '--> create new account',
    'services': '--> list of all services',
    'reviews': '--> list of all reviews',
    'staff': '--> list of all teachers',
    'clinic info': '--> info about the Clinic',
    'exit': '--> quit the app'
}


PATIENT_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign out': '--> sign out of your account',
    'services': '--> list of all articles',
    'reviews': '--> list of all reviews',
    'staff': '--> list of all doctors',
    'clinic info': '--> info about the Clinic',
    'order': '--> order a ticket',
    'med card': '--> view personal medical card',
    'exit': '--> quit the app'
}

STAFF_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign out': '--> sign out of your account',
    'check med card': '--> check patient med card',
    'diagnose': '--> add diagnostic to patient',
    'reviews': '--> list of all reviews',
    'staff': '--> list of all teachers',
    'clinic info': '--> info about the Clinic',
    'audit': '--> check audit',
    'exit': '--> quit the app'
}

SUPERUSER_COMMANDS: dict[str, str] = {
    'list': '--> list all commands',
    'sign out': '--> sign out of your account',
    'audit': '--> view audit',
    'edit med card': "--> edit user's personal info",
    'bank': "--> view money bank",
    'exit': '--> quit the app'
}

COMMANDS_LIST_TITLE: str = '\n***** Commands (NOT case sensitive) *****\n\n'


def get_commands_list(list_type: str) -> str:
    global COMMANDS_LIST_TITLE
    commands_list = COMMANDS_LIST_TITLE
    commands: dict[str, str]

    if list_type == 'GUEST_COMMANDS':
        commands = GUEST_COMMANDS
    elif list_type == 'PATIENT_COMMANDS':
        commands = PATIENT_COMMANDS
    elif list_type == 'STAFF_COMMANDS':
        commands = STAFF_COMMANDS
    elif list_type == 'SUPERUSER_COMMANDS':
        commands = SUPERUSER_COMMANDS

    for comm in commands.keys():
        commands_list += f'{comm} {commands[comm]}\n'

    return commands_list


def get_commands(dict_type: str) -> dict:
    if dict_type == 'Guest':
        return GUEST_COMMANDS
    elif dict_type == 'Patient':
        return PATIENT_COMMANDS
    elif dict_type == 'Staff':
        return STAFF_COMMANDS
    elif dict_type == 'Superuser':
        return SUPERUSER_COMMANDS


ROLES: dict[int, str] = {
    1: 'Guest',
    2: 'Patient',
    3: 'Staff',
    4: 'Superuser'
}


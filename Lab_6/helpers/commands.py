from Lab_6.db_connection import db_sign_in, db_sign_in_staff


is_logged_in = False


def sign_in():
    if is_logged_in:
        return
    vvod = input("\nStaff or user: ").strip()

    if(vvod == "user"):
        username = input("\nUsername: ").strip()
        password = input("\nPassword: ").strip()
        db_sign_in(username, password)
    else:
        email = input("\nEmail: ").strip()
        password = input("\nPassword: ").strip()
        db_sign_in_staff(email, password)
   

def sign_up():
    print("SIGN UP")


def get_articles():
    print("ARTICLES")


def get_reviews():
    print("REVIEWS")


def get_school_info():
    print("SCHOOL INFO")


def print_commands():
    print("\n\nCommands list (NOT case sensitive):\n"
          "* 'List' --> list all commands\n"
          "* 'Sign in' --> sign in to to your account\n"
          "* 'Sign up' --> create new account\n"
          "* 'Articles' --> list of all articles\n"
          "* 'Reviews' --> list of all reviews\n"
          "* 'Clinic info' --> info about the clinic\n"
          "* 'Exit' --> quit the app\n\n")


def exit_program():
    exit()


commands = {
    'list': print_commands,
    'sign in': sign_in,
    'sign up': sign_up,
    'articles': get_articles,
    'reviews': get_reviews,
    'clinic info': get_school_info,
    'exit': exit
}

class User:
    username = ""
    editor = False

    @staticmethod
    def __init__(utilizador):
        User.username = utilizador[0]
        User.editor = utilizador[1]

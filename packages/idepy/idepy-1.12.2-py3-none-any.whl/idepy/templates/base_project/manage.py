# manage.py


from idepy.management.commandExecutor import CommandManager


def main():
    manager = CommandManager()
    manager.execute()


if __name__ == '__main__':
    main()

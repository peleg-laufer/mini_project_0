import argparse

class Todo:
    def parsers_setup(self):
        self.parser = argparse.ArgumentParser(prog="ToDo list",
                                         description="Add to a list and see all your Todo stuff",
                                         epilog="good luck and best regards"
                                         )
        self.parser.add_argument("-q", "--quiet", action="store_true",
                            help="write more shortly")
        self.subparsers = self.parser.add_subparsers(help='choose a command [add, list]', dest='command')
        self.parser_add = self.subparsers.add_parser('add',
                                           help='add an item to todo list')
        self.parser_add.add_argument("item", type=str,
                            help="add input to Todo List")
        self.parser_list = self.subparsers.add_parser('list',
                                            help='show todo list')
        args = self.parser.parse_args()

        command = args.command
        #print(args.subparser_name)
        if command == "list":
            print("printing todo list...")
        elif command == "add":
            print(f"adding new item to list: ")

    def __init__(self):
        self.parsers_setup()

if __name__ == '__main__':
    Todo()

import argparse
import os.path
import sqlite3

class Todo:
    def setup(self):
        """
        sets up: parsers, db_file
        :return:
        """
        self.parsers_setup()
        self.sqlite_setup()

    def parsers_setup(self):
        """"
        sets up parsers
        """
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


    def sqlite_setup(self):
        """
        checks if there is a db file self.db_file_path and if valid, creates one if not
        """
        self.db_file_path = r"listdb.db"
        if not os.path.exists(self.db_file_path):
            self.create_new_db_file()
        elif not self.is_db_file_valid():
            os.remove(self.db_file_path)
            self.create_new_db_file()

    def is_db_file_valid(self):
        """

       :return: True if the db file is good, false if not
        """
        # TODO: check if headers of file good
        pass
        return True

    def create_new_db_file(self):
        """
        creates db file and tables
        :return:
        """
        conn = sqlite3.connect(self.db_file_path)
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE list (
                            todo_item TEXT NOT NULL
                    );
                    """)

    def handle_req(self):
        """
        handles clients request
        """
        args = self.parser.parse_args()
        command = args.command
        if command == "list":
            print("printing todo list...")
            # TODO: add printing list func
            pass
        elif command == "add":
            print(f"adding new item to list: ")
            print(args.item)
            # TODO: add args.item to db file
            pass
        elif command == None:
            print("printing help")
            # TODO: print help stuff of parser
            pass

    def __init__(self):
        self.setup()
        self.handle_req()

if __name__ == '__main__':
    Todo()

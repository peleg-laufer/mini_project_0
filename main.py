import argparse
import os.path
import sqlite3
from xmlrpc.client import Boolean


class Todo:

    def parsers_setup(self):
        """"
        sets up parsers
        """
        print("setting up parsers")
        self.parser = argparse.ArgumentParser(prog="ToDo list",
                                         description="Add to a list and see all your Todo stuff",
                                         epilog="good luck and best regards"
                                         )


        self.subparsers = self.parser.add_subparsers(help='choose a command [add, list]', dest='command')

        self.parser_add = self.subparsers.add_parser('add',
                                           help='add an item to todo list')
        self.parser_add.add_argument("item", type=str,
                            help="add input to Todo List")

        self.parser_list = self.subparsers.add_parser('list',
                                            help='show todo list')
        group = self.parser_list.add_mutually_exclusive_group()
        group.add_argument("-q", "--quiet", action="store_true")

        print("     parsers set up successfully")

    def sqlite_setup(self):
        """
        checks if there is a db file self.db_file_path and if valid, creates one if not
        """
        self.db_file_path = r"listdb.db"
        print(f"setting up sqlite DB on {self.db_file_path}")
        if not os.path.exists(self.db_file_path):
            print(      f"db file {self.db_file_path} not exist")
            self.create_new_db_file()
        elif not self.is_db_file_valid():
            print(      f"db file {self.db_file_path} not valid")
            print(      "deleting existing file")
            os.remove(self.db_file_path) # TODO: check why not working
            self.create_new_db_file()
        else:
            print("db file exists and valid")


    def is_db_file_valid(self):
        """

       :return: True if the db file is good, False if not, assumes self.db_file exists
        """
        try:
            print(f"check validity of db file in {self.db_file_path}")
            conn = sqlite3.connect(self.db_file_path)
            print("     connected to db file")
            cur = conn.cursor()
            print("     got cursor on db file")
            cur.execute("""
            PRAGMA table_info(list);
            """)
            print("     executed PRAGMA")
            info = cur.fetchall()
            print("     got header of list table on db file: " + str(info))
        except Exception as e:
            print("error in checking db file: ")
            print(e)
            conn.close()
            return False
        db_is_valid = True
        if info == None or len(info) != 1 or len(info[0]) != 6:
            db_is_valid = False
        elif info[0] != self.DEFAULT_DB_HEADER:
            db_is_valid = False
        conn.close()
        return db_is_valid


    def create_new_db_file(self):
        """
        creates db file and tables on self.db_file
        assumse no self.db_file exists
        :return:
        """
        with sqlite3.connect(self.db_file_path) as conn:
            cur = conn.cursor()
            cur.execute(f"""
                        CREATE TABLE list (
                                {self.DEFAULT_DB_HEADER[1]} {self.DEFAULT_DB_HEADER[2]} NOT NULL
                        );
                        """)


    def print_list(self):
        """
        prints the list of todo_item from self.db_file
        assumes it exists and valid
        """
        with sqlite3.connect(self.db_file_path) as conn:
            cur = conn.cursor()
            cur.execute(f"""
                SELECT
                    {self.DEFAULT_DB_HEADER[1]}
                FROM
                    list;
            """)
            info = cur.fetchall()
            if self.args.quiet:
                print("TODO list:")
                if info != None:
                    for todo_item in info:
                        print(todo_item[0])
            else:
                print("TODO list is:")
                if info != None:
                    i = 1
                    for todo_item in info:
                        print(f"        item no {i}: {todo_item[0]}")
                        i += 1


    def add_to_db(self, todo_item):
        """
        adds an item to self.db_file
        assumes it exists and valid (todo_item table exists, consists on non-null string)
        :param todo_item: item to add to table (has to be non-null string)
        """
        if todo_item is not None:
            with sqlite3.connect(self.db_file_path) as conn:
                cur = conn.cursor()
                print(f"inserting '{todo_item}' to {self.DEFAULT_DB_HEADER[1]} column in list table")
                query = f"""
                    INSERT INTO list ({self.DEFAULT_DB_HEADER[1]})
                    VALUES(?);
                """
                cur.execute(query, (todo_item,))
        else:
            print("invalid todo_item inserted")

    def print_help(self):
        """
        prints this.parser help
        assumes exists, valid
        """
        # TODO
        pass


    def handle_req(self):
        """
        handles clients request
        """
        self.args = self.parser.parse_args()
        command = self.args.command
        if command == "list":
            print("printing todo list...")
            self.print_list()
        elif command == "add":
            print(f"adding new item to list: ")
            print(self.args.item)
            self.add_to_db(self.args.item)
        elif command == None:
            print("printing help")
            self.print_help()


    def __init__(self):
        self.DEFAULT_DB_HEADER = (0, 'todo_item', 'TEXT', 1, None,
                                  0)  # (column index, column name, type, is non-null, default, is pk primary key)
        print(f"DEFAULT_DB_HEADER: {self.DEFAULT_DB_HEADER}")
        print("setting up")
        self.parsers_setup()
        self.sqlite_setup()
        self.handle_req()

if __name__ == '__main__':
    Todo()

import argparse
import os.path
import sqlite3
import sys
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
        try:
            with sqlite3.connect(self.db_file_path) as conn:
                cur = conn.cursor()
                cur.execute(f"""
                            CREATE TABLE IF NOT EXISTS list (
                                    todo_item TEXT NOT NULL
                            );
                            """)
        except sqlite3.OperationalError as e:
            # unclosed connection causing problems usually
            print(f"cant access the file, probably open somewhere. error code: {e}")
        except sqlite3.DatabaseError as e:
            # self.db_file is corrupt, cant continue
            print(f"Critical Database Error: {e}. fix the file to use program")
            sys.exit(1)
        except Exception as e:
            print(f"unusual error. error code: {e}")
        else:
            pass



    def print_list(self):
        """
        prints the list of todo_item from self.db_file
        assumes it exists and valid
        """
        with sqlite3.connect(self.db_file_path) as conn:
            cur = conn.cursor()
            cur.execute(f"""
                SELECT
                    *
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
            try:
                with sqlite3.connect(self.db_file_path) as conn:
                    cur = conn.cursor()
                    query = f"""
                                        INSERT INTO list (todo_item)
                                        VALUES(?);
                                    """
                    cur.execute(query, (todo_item,))
            except sqlite3.OperationalError as e:
                # unclosed connection causing problems usually
                print(f"cant access the file, probably open somewhere. error code: {e}")
            except sqlite3.DatabaseError as e:
                # self.db_file is corrupt, cant continue
                print(f"Critical Database Error: {e}. fix the file to use program")
                sys.exit(1)
            except Exception as e:
                print(f"unusual error. error code: {e}")
            else:
                pass
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
        # default header: (0, 'todo_item', 'TEXT', 1, None, 0)  # (column index, column name, type, is non-null, default, is pk primary key)
        self.db_file_path = r"listdb.db"
        print("setting up")
        self.parsers_setup()
        self.sqlite_setup()


if __name__ == '__main__':
    todo_list = Todo()
    todo_list.handle_req()


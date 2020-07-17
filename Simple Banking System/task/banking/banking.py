# Write your code here
import random
import sqlite3


class CardSystem:

    def __init__(self):
        self.card_account_info = ()
        self.top_menu = None
        self.user_card = None
        self.user_pin = None
        self.login_input = None
        self.checksum = None
        self.card_num = None
        self.personal_id = None
        self.login_bool = None
        self.balance = None
        self.id = 1
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()

    def run_menu(self):  # Main menu
        self.create_table()
        print('1. Create an account\n2. Log into account\n0. Exit')
        self.top_menu = input()
        if self.top_menu in ['1', '2', '0']:
            if self.top_menu == '0':  # exits program
                print("Bye!")
                self.conn.close()
                exit()
            elif self.top_menu == '1':  # user creates a new account
                self._generate_card_num()
                self.run_menu()
            elif self.top_menu == '2':  # user goes to login menu
                self.login()
        else:
            self.run_menu()

    def _generate_card_num(self):
        # Generate a card number along with a PIN and create an entry into the 'card' Database
        account = str(random.randint(0, 999999999)).zfill(9)
        self.personal_id = str(random.randint(0, 9999)).zfill(4)
        self.card_num = "400000" + account
        self.check_sum(self.card_num)
        self.card_num += self.checksum
        self.card_account_info = (self.id, self.card_num, self.personal_id, 0)
        self.insert_info()
        print("\nYour card has been created")
        print(f"Your card number:\n{self.card_num}")
        print(f"Your card PIN:\n{self.personal_id}\n")

    def check_sum(self, number):
        # perform the Luhn algorithm to determine the final digit of a card number
        num_list = [int(number[i]) for i in range(len(number))]
        num_list = [num_list[i] * 2 if i % 2 == 0 else num_list[i] for i in range(len(num_list))]
        num_list = [num_list[i] - 9 if num_list[i] > 9 else num_list[i] for i in range(len(num_list))]
        num_list = sum(num_list)
        if num_list % 10 == 0:
            self.checksum = '0'
        else:
            total = num_list % 10
            self.checksum = str(10 - total)

    def login(self):
        # path to the login menu
        self.user_card = input("\nEnter your card number:\n")
        self.user_pin = input("Enter your PIN:\n")
        self.login_bool = self.check_login()
        if self.login_bool:
            print("\nYou have successfully logged in!")
            self.login_menu()
        else:
            print("\nWrong card number or PIN!\n")
            self.run_menu()

    def login_menu(self):
        print("1. Balance\n2. Log out\n0. Exit")
        self.login_input = input()
        if self.login_input == '1':
            print(f"\nBalance: {self.balance}\n\n")
            self.login_menu()
        elif self.login_input == "2":
            print("\n")
            self.run_menu()
        elif self.login_input == "0":
            print("\nBye!")
            self.conn.close()
            exit()

    def create_table(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card';")
        check_tbl = self.cur.fetchall()
        if check_tbl:  # check to see if the table 'card' exists, if it does, pick up the count of the id number
            self.cur.execute('SELECT id FROM card;')
            id_list = [v for v in self.cur.fetchall()]
            if id_list:
                self.id = max(id_list)  # get the last id number
                self.id = int(self.id[0]) + 1  # cast id number to 'int' and add 1 to it.
            else:
                self.id = self.id
        else:  # if table 'card' doesn't exist, create it
            self.cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER DEFAULT 0, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
            self.conn.commit()

    def insert_info(self):
        # add new account info and update id number
        self.cur.execute('INSERT INTO card VALUES (?,?,?,?);', self.card_account_info)
        self.conn.commit()
        self.id += 1

    def check_login(self):
        x = (self.user_card,)
        self.cur.execute('SELECT pin, balance FROM card WHERE number=?', x)
        table_info = self.cur.fetchone()
        if table_info:
            if self.user_pin == table_info[0]:
                self.balance = table_info[1]
                return True
            return False
        return False


random.seed()
if __name__ == '__main__':
    cs = CardSystem()
    cs.run_menu()

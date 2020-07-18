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
        self.balance = None
        self.transfer_account = None
        self.transfer_account_num = None
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
        login_bool = self.check_login()
        if login_bool:
            print("\nYou have successfully logged in!\n")
            self.login_menu()
        else:
            print("\nWrong card number or PIN!\n")
            self.run_menu()

    def login_menu(self):
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        self.login_input = input()
        if self.login_input == '1':
            print(f"\nBalance: {self.balance}\n")
            self.login_menu()
        elif self.login_input == "2":
            self.add_income()
            self.login_menu()
        elif self.login_input == '3':
            self.transfer()
            self.login_menu()
        elif self.login_input == '4':
            self.close_acct()
        elif self.login_input == '5':
            print('\n')
            self.run_menu()
        elif self.login_input == "0":
            print("\nBye!")
            self.conn.close()
            exit()

    def create_table(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card';")
        check_tbl = self.cur.fetchone()
        if check_tbl:  # check to see if the table 'card' exists, if it does, pick up the count of the id number
            self.cur.execute('SELECT id FROM card;')
            id_list = [v for v in self.cur.fetchall()]
            if id_list:
                self.id = max(id_list)  # get the last id number
                self.id = int(self.id[0]) + 1  # cast id number to 'int' and add 1 to it.
            else:
                self.id = self.id
        else:  # if table 'card' doesn't exist, create it
            self.cur.execute('''CREATE TABLE IF NOT EXISTS card (
                             id INTEGER DEFAULT 0, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);''')
            self.conn.commit()

    def insert_info(self):
        # add new account info and update id number
        self.cur.execute('INSERT INTO card VALUES (?,?,?,?);', self.card_account_info)
        self.conn.commit()
        self.id += 1

    def check_login(self):
        self.cur.execute('SELECT pin, balance FROM card WHERE number=?', (self.user_card,))
        table_info = self.cur.fetchone()
        if table_info:
            if self.user_pin == str(table_info[0]):
                self.balance = table_info[1]
                return True
            return False
        return False

    def add_income(self):
        print("Enter income:")
        add_income = int(input())
        print("Income was added!\n")
        self.balance += add_income
        self.update_balance()

    def update_balance(self):
        up_bal = (self.balance, self.user_card, self.user_pin)
        self.cur.execute('UPDATE card SET balance=? WHERE number=? AND pin=?', up_bal)
        self.conn.commit()

    def transfer(self):
        print("\nTransfer")
        self.transfer_account_num = input("Enter card number:\n")
        if self.user_card == self.transfer_account_num:
            print("You can't transfer money to the same account!\n")
            self.login_menu()
        luhn_bool = self.luhn_check(self.transfer_account_num)
        if luhn_bool:
            trans_bool = self.check_account()
            if trans_bool:
                self.trans_money()
                print('Success!\n')
                self.login_menu()
            else:
                print('Such a card does not exist.\n')
                self.login_menu()
        else:
            print("Probably you made mistake in the card number.\nPlease try again!\n")
            self.login_menu()

    def check_account(self):
        self.cur.execute('SELECT * FROM card WHERE number=?', (self.transfer_account_num,))
        check_acct = self.cur.fetchone()
        if check_acct:
            return True
        else:
            return False

    def trans_money(self):
        trans_amount = int(input("Enter how much money you want to transfer:\n"))
        if trans_amount > self.balance:
            print('Not enough money!\n')
            self.login_menu()
        else:
            self.balance -= trans_amount
            self.cur.execute('UPDATE card SET balance=? WHERE number=?;', (self.balance, self.user_card))
            self.cur.execute('SELECT balance FROM card WHERE number=?;', (self.transfer_account_num,))
            new_bal = self.cur.fetchone()
            new_bal = new_bal[0] + trans_amount
            self.cur.execute('UPDATE card SET balance=? WHERE number=?;', (new_bal, self.transfer_account_num))
            self.conn.commit()

    def close_acct(self):
        self.cur.execute('DELETE FROM card WHERE number=? AND pin=?', (self.user_card, self.user_pin))
        self.conn.commit()
        print('The account has been closed!\n')
        self.run_menu()

    @staticmethod
    def luhn_check(number):
        num_list = [int(number[i]) for i in range(len(number))]
        num_list = [num_list[i] * 2 if i % 2 == 0 else num_list[i] for i in range(len(num_list))]
        num_list = [num_list[i] - 9 if num_list[i] > 9 else num_list[i] for i in range(len(num_list))]
        num_list = sum(num_list)
        return num_list % 10 == 0


random.seed()
if __name__ == '__main__':
    cs = CardSystem()
    cs.run_menu()

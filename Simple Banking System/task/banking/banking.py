# Write your code here
import random


class CardSystem:

    def __init__(self):
        self.card_dict = {}
        self.top_menu = None
        self.user_card = None
        self.user_pin = None
        self.login_input = None
        self.checksum = None

    def run_menu(self):
        print('1. Create an account\n2. Log into account\n0. Exit')
        self.top_menu = input()
        if self.top_menu in ['1', '2', '0']:
            if self.top_menu == '0':
                print("Bye!")
                exit()
            elif self.top_menu == '1':
                self._generate_card_num()
                self.run_menu()
            elif self.top_menu == '2':
                self.login()
        else:
            self.run_menu()

    def _generate_card_num(self):
        # Generate a card number along with a PIN and create a dictionary entry to link the two
        account = str(random.randint(0, 999999999)).zfill(9)
        personal_id = str(random.randint(0, 9999)).zfill(4)
        card_num = "400000" + account
        self.check_sum(card_num)
        card_num += self.checksum
        self.card_dict[card_num] = personal_id
        print("\nYour card has been created")
        print(f"Your card number:\n{card_num}")
        print(f"Your card PIN:\n{personal_id}\n")

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
        if self.user_card in self.card_dict and self.card_dict[self.user_card] == self.user_pin:
            print("\nYou have successfully logged in!")
            self.login_menu()
        else:
            print("\nWrong card number or PIN!\n")
            self.run_menu()

    def login_menu(self):
        print("1. Balance\n2. Log out\n0. Exit")
        self.login_input = input()
        if self.login_input == '1':
            print("\nBalance: 0\n\n")
            self.login_menu()
        elif self.login_input == "2":
            print("\n")
            self.run_menu()
        elif self.login_input == "0":
            print("\nBye!")
            exit()


if __name__ == '__main__':
    cs = CardSystem()
    cs.run_menu()

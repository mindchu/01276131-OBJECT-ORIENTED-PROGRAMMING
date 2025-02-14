class Bank:
    def __init__(self):
        self.__user_list = []
        self.__account_list = []
        self.__ATMCard_list = []
        self.__ATMMachine_list = []

    def create_user(self, user):
        self.__user_list.append(user)

    def create_account(self, account):
        self.__account_list.append(account)

    def create_ATMCard(self, ATMcard):
        self.__ATMCard_list.append(ATMcard)

    def create_ATMMachine(self, ATMmachine):
        self.__ATMMachine_list.append(ATMmachine)

    def use_ATM(self, machine_id):
        for atm in self.__ATMMachine_list:
            if atm.machine_id == machine_id:
                return atm

    def find_account(self, account_number):
        for account in self.__account_list:
            if account.account_number == account_number:
                return account

    def find_ATMcard(self, card_number):
        for ATMcard in self.__ATMCard_list:
            if ATMcard.card_number == card_number:
                return ATMcard

class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name

class Account:
    def __init__(self, account_number: str, owner: User, balance: float = 0.0):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = balance
        self.__transaction_list = []

    @property
    def account_number(self) -> str:
        return self.__account_number

    @property
    def balance(self) -> float:
        return self.__balance
    @balance.setter
    def balance(self, balance: float):
        self.__balance = balance

    @property
    def transaction_list(self):
        return self.__transaction_list
    
    def add_transaction_list(self, transaction):
        self.__transaction_list.append(transaction)

class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin
        self.__annual_fee = 150
        self.__maximum_withdraw = 40000
        self.__total_withdraw_today = 0

    @property
    def card_number(self) -> str:
        return self.__card_number

    @property
    def account(self) -> Account:
        return self.__account

    @property
    def pin(self) -> str:
        return self.__pin
    
    @property
    def maximum_withdraw(self) -> float:
        return self.__maximum_withdraw

    @property
    def total_withdraw_today(self) -> float:
        return self.__total_withdraw_today
    @total_withdraw_today.setter
    def total_withdraw_today(self, total_withdraw_today: float):
        self.__total_withdraw_today = total_withdraw_today

class ATMMachine:
    def __init__(self, machine_id: str, initial_amount: float = 1000000):
        self.__machine_id = machine_id
        self.__initial_amount = initial_amount

    @property
    def machine_id(self) -> str:
        return self.__machine_id

    @property
    def initial_amount(self) -> float:
        return self.__initial_amount

    def insert_ATMCard(self, card_number, pin):
        ATMcard = bank.find_ATMcard(card_number)
        if ATMcard == None:
            return "ATM card not found"
        elif ATMcard.pin == pin:
            return ATMcard
        else:
            return "Invalid PIN"
        
    def deposit(self, ATMcard, amount):
        account = ATMcard.account
        if amount <= 0:
            return "Error: Invalid amount"
        
        account.balance += amount
        transaction = Transaction("D", self.__machine_id, amount, account.balance)
        account.add_transaction_list(transaction)
        self.__initial_amount += amount
        return f"Success: {transaction.record}"
    
    def withdraw(self, ATMcard, amount):
        account = ATMcard.account
        if amount <= 0:
            return "Invalid amount"
        if amount > self.__initial_amount:
            return "ATM has insufficient funds"
        if amount + ATMcard.total_withdraw_today > ATMcard.maximum_withdraw:
            return "Exceeds daily withdrawal limit of 40,000 Baht"
        if amount > account.balance:
            return "Insufficient balance"
        
        account.balance -= amount
        transaction = Transaction("W", self.__machine_id, amount, account.balance)
        account.add_transaction_list(transaction)
        ATMcard.total_withdraw_today += amount
        self.__initial_amount -= amount
        return f"Success: {transaction.record}"
    
    def transfer(self, ATMcard, transfer_account, amount):
        account = ATMcard.account
        if transfer_account == None:
            return "Error: Account not found"
        if amount <= 0:
            return "Error: Invalid amount"
        if amount > account.balance:
            return "Error: Insufficient balance"
        
        account.balance -= amount
        transaction = Transaction("TW", self.__machine_id, amount, account.balance, transfer_account.account_number)
        account.add_transaction_list(transaction)

        transfer_account.balance += amount
        transaction_receive = Transaction("TD", self.__machine_id, amount, transfer_account.balance)
        transfer_account.add_transaction_list(transaction_receive)
        return f"Success: {transaction.record}, {transaction_receive.record}"

class Transaction:
    def __init__(self, transaction_type: str, ATM_number: str, amount: float, balance: float, transfer_account_number: str = None):
        self.__transaction_type = transaction_type
        self.__ATM_number = ATM_number
        self.__amount = amount
        self.__balance = balance
        self.__transfer_account_number = transfer_account_number
        if transfer_account_number == None:
            self.__record = f"{self.__transaction_type}-ATM:{self.__ATM_number}-{self.__amount}-{self.__balance}"
        else:
            self.__record = f"{self.__transaction_type}-ATM:{self.__ATM_number}-{self.__amount}-{self.__balance}-{self.__transfer_account_number}"

    @property
    def record(self) -> str:
        return self.__record


##################################################################################


## Define the format of the user as follows:
## {Citizen ID: [Name, Account Number, ATM Card Number, Account Balance]}

bank = Bank()

user ={'1-1101-12345-12-0':['Harry Potter','1234567890','12345',20000],
       '1-1101-12345-13-0':['Hermione Jean Granger','0987654321','12346',1000]}

atm ={'1001':1000000,'1002':200000}

## TODO 1: From the user data, create instances with the following details:
## TODO: key:value, where the key is the Citizen ID, and the value contains
## TODO: [Name, Account Number, ATM Card Number, Account Balance].
## TODO: Return the instance of the bank and create two ATM instances.

for citizen_id, data in user.items():
    user = User(citizen_id, data[0])
    account = Account(data[1], user, data[3])
    ATMcard = ATMCard(data[2], account, '1234')
    bank.create_user(user)
    bank.create_account(account)
    bank.create_ATMCard(ATMcard)

for machine_id, initial_amount in atm.items():
    ATMmachine = ATMMachine(machine_id, initial_amount)
    bank.create_ATMMachine(ATMmachine)

## TODO 2: Write a method to insert an ATM card into the machine. It should accept two parameters:
## TODO: 1) Bank instance 2) ATM card number.
## TODO: If the card is valid, return the account instance; if not, return None.
## TODO: This should be a method of the ATM machine.

## TODO 3: Write a method to deposit money. It should accept three parameters:
## TODO: 1) ATM machine instance, 2) Account instance, 3) Deposit amount.
## TODO: The method should increase the account balance and log the transaction in the account.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0.

## TODO 4: Write a method to withdraw money. It should accept three parameters:
## TODO: 1) ATM machine instance, 2) Account instance, 3) Withdrawal amount.
## TODO: The method should decrease the account balance and log the transaction in the account.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0 and not exceed the account balance.

## TODO 5: Write a method to transfer money. It should accept four parameters:
## TODO: 1) ATM machine instance, 2) Sender account instance, 3) Recipient account instance, 4) Transfer amount.
## TODO: The method should decrease the sender's balance, increase the recipient's balance, and log the transaction.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0 and not exceed the sender's balance.

print("--------------------------")
print("     Start Test Cases     ")
print("--------------------------")

## Test case #1: Test inserting Harry's ATM card into ATM machine #1
## and call the corresponding method.
## Expected result: Print Harry's account number and ATM card number correctly.
## Ans: 12345, 1234567890, Success

print("Test case #1: Test inserting Harry's ATM card into ATM machine #1")
print("12345, 1234567890, Success")
print("--------------------------")
atm = bank.use_ATM("1001")
ATMcard = atm.insert_ATMCard("12345", "1234")
print(f"{ATMcard.card_number}, {ATMcard.account.account_number}, Success")
print("--------------------------")

## Test case #2: Test depositing 1000 Baht into Hermione's account using ATM machine #2.
## Call the deposit method.
## Expected result: Display Hermione's balance before and after the deposit, along with the transaction.
## Hermione's account before test: 1000
## Hermione's account after test: 2000
# print("-------------------------")

print("Test case #2: Test depositing 1000 Baht into Hermione's account using ATM machine #2")
print("Hermione's account before test: 1000\nHermione's account after test: 2000")
print("--------------------------")
atm = bank.use_ATM("1002")
ATMcard = atm.insert_ATMCard("12346", "1234")
print(f"Hermione's account before test: {ATMcard.account.balance}")
print(atm.deposit(ATMcard, 1000))
print(f"Hermione's account after test: {ATMcard.account.balance}")
print("--------------------------")

## Test case #3: Test depositing -1 Baht into Hermione's account using ATM machine #2.
## Expected result: Display "Error."
# print("-------------------------")

print("Test case #3: Test depositing -1 Baht into Hermione's account using ATM machine #2")
print("Error")
print("--------------------------")
atm = bank.use_ATM("1002")
ATMcard = atm.insert_ATMCard("12346", "1234")
print(atm.deposit(ATMcard, -1))
print("--------------------------")

## Test case #4: Test withdrawing 500 Baht from Hermione's account using ATM machine #2.
## Call the withdrawal method.
## Expected result: Display Hermione's balance before and after the withdrawal, along with the transaction.
## Hermione's account before test: 2000
## Hermione's account after test: 1500
# print("-------------------------")

print("Test case #4: Test withdrawing 500 Baht from Hermione's account using ATM machine #2")
print("Hermione's account before test: 2000\nHermione's account after test: 1500")
print("--------------------------")
atm = bank.use_ATM("1002")
ATMcard = atm.insert_ATMCard("12346", "1234")
print(f"Hermione's account before test: {ATMcard.account.balance}")
print(atm.withdraw(ATMcard, 500))
print(f"Hermione's account after test: {ATMcard.account.balance}")
print("--------------------------")

## Test case #5: Test withdrawing 2000 Baht from Hermione's account using ATM machine #2.
## Expected result: Display "Error."
# print("-------------------------")

print("Test case #5: Test withdrawing 2000 Baht from Hermione's account using ATM machine #2")
print("Error")
print("--------------------------")
atm = bank.use_ATM("1002")
ATMcard = atm.insert_ATMCard("12346", "1234")
print(atm.withdraw(ATMcard, 2000))
print("--------------------------")

## Test case #6: Test transferring 10,000 Baht from Harry's account to Hermione's account using ATM machine #2.
## Call the transfer method.
## Expected result: Display Harry's balance before and after the transfer, Hermione's balance before and after the transfer, and the transaction log.
## Harry's account before test: 20000
## Harry's account after test: 10000
## Hermione's account before test: 1500
## Hermione's account after test: 11500
# print("-------------------------")

print("Test case #6: Test transferring 10,000 Baht from Harry's account to Hermione's account using ATM machine #2")
print("Harry's account before test: 20000\nHarry's account after test: 10000")
print("Hermione's account before test: 1500\nHermione's account after test: 11500")
print("--------------------------")
atm = bank.use_ATM("1002")
ATMcard = atm.insert_ATMCard("12345", "1234")
transfer_account = bank.find_account("0987654321")
print(f"Harry's account before test: {ATMcard.account.balance}")
print(f"Hermione's account before test: {transfer_account.balance}")
print(atm.transfer(ATMcard, transfer_account, 10000))
print(f"Harry's account after test: {ATMcard.account.balance}")
print(f"Hermione's account before test: {transfer_account.balance}")
print("--------------------------")

## Test case #7: Display all of Hermione's transactions.
## Expected result:
## Hermione's transaction log:
## D-ATM:1002-1000-2000
## W-ATM:1002-500-1500
## TD-ATM:1002-10000-11500
# print("-------------------------")

print("Test case #7: Display all of Hermione's transactions")
print("Hermione's transaction log:\nD-ATM:1002-1000-2000\nW-ATM:1002-500-1500\nTD-ATM:1002-10000-11500")
print("--------------------------")
account = bank.find_account("0987654321")
print("Hermione's transaction log:")
for transaction in account.transaction_list:
    print(transaction.record)
print("--------------------------")

## Test case #8: Test inserting an incorrect PIN.
## Call the method to insert the card and check the PIN.
## atm_machine = bank.get_atm('1001')
## test_result = atm_machine.insert_card('12345', '9999')  # Incorrect PIN
## Expected result: Invalid PIN
# print("-------------------------")

print("Test case #8: Test inserting an incorrect PIN")
print("Invalid PIN")
print("--------------------------")
atm = bank.use_ATM("1001")
ATMcard = atm.insert_ATMCard("12345", "9999")
print(ATMcard)
print("--------------------------")

# Test case #9: Test withdrawing more than the daily limit (40,000 Baht).
print("Test case #9: Test withdrawing more than the daily limit (40,000 Baht)")
atm_machine = bank.use_ATM('1001')
ATMcard = atm_machine.insert_ATMCard('12345', '1234')  # Correct PIN
account = ATMcard.account
harry_balance_before = account.balance
print(f"Harry's account before test: {harry_balance_before}")
print("Attempting to withdraw 45,000 Baht...")
result = atm_machine.withdraw(ATMcard, 45000)
print(f"Expected result: Exceeds daily withdrawal limit of 40,000 Baht")
print(f"Actual result: {result}")
print(f"Harry's account after test: {account.balance}")
print("-------------------------")

# Test case #10: Test withdrawing money when the ATM has insufficient funds.
atm_machine = bank.use_ATM('1002')  # Assume machine #2 has 200,000 Baht left
ATMcard = atm_machine.insert_ATMCard('12345', '1234')
account = ATMcard.account
print("Test case #10: Test withdrawal when ATM has insufficient funds.")
print(f"ATM machine balance before: {atm_machine.initial_amount}")
print("Attempting to withdraw 250,000 Baht...")
result = atm_machine.withdraw(ATMcard, 250000)
print(f"Expected result: ATM has insufficient funds.")
print(f"Actual result: {result}")
print(f"ATM machine balance after: {atm_machine.initial_amount}")
print("-------------------------")


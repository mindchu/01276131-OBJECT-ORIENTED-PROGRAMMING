
class Bank:
    def __init__(self,name):
        self.__name = name
        self.__user_list = []
        self.__atm_list = []
        self.__seller_list = []

    def add_user(self, user):
        self.__user_list.append(user)

    def search_user_from_id(self, citizen_id):
        for user in self.__user_list:
            if user.citizen_id == citizen_id:
                return user
            
    def add_atm_machine(self, machine):
        self.__atm_list.append(machine)

    def search_atm_machine(self, atm_no):
        for machine in self.__atm_list:
            if machine.atm_no == atm_no:
                return machine
            
    def search_account_from_card(self, card_no):
        for user in self.__user_list:
            for account in user.account_list:
                if account.card.card_no == card_no:
                    return account

    def search_account_from_account_no(self, account_no):
        for user in self.__user_list:
            for account in user.account_list:
                if account.account_no == account_no:
                    return account

    def add_seller(self, seller):
        self.__seller_list.append(seller)

    def search_seller(self, name):
        for seller in self.__seller_list:
            if seller.name == name:
                return seller

class User:
    def __init__(self, citizen_id, name):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__account_list = []

    @property
    def citizen_id(self):
        return self.__citizen_id
    
    @property
    def account_list(self):
        return self.__account_list

    def add_account(self, account):
        self.__account_list.append(account)

    def search_account(self, account_no):
        for account in self.__account_list:
            if account.account_no == account_no:
                return account

class Account:
    def __init__(self, account_no, user, amount):
        self.__account_no = account_no
        self.__user = user
        self.__amount = amount
        self.__transaction = []

    def __add__(self, amount):
        if amount <= 0:
            return "Invalid amount"
        self.__amount += amount
        transaction = Transaction("D",  amount, self.__amount)
        self.add_transaction(transaction)

    def __sub__(self, amount):
        if amount <= 0:
            return "Invalid amount"
        if amount > self.amount:
            return "Insufficient balance"
        self.__amount -= amount
        transaction = Transaction("W",  amount, self.__amount)
        self.add_transaction(transaction)


    def add_transaction(self, transaction):
        self.__transaction.append(transaction)

    def transfer(self, account, amount, target_account):
        if account == "0000":
            account = self
        if amount <= 0:
            return "Invalid amount"
        if amount > account.amount:
            return "Insufficient balance"
        account.amount -= amount
        target_account.amount += amount
        transaction = Transaction("TW",  amount, account.amount, target_account.account_no)
        account.add_transaction(transaction)
        transaction = Transaction("TD",  amount, account.amount, account.account_no)
        target_account.add_transaction(transaction)

    @property
    def account_no(self):
        return self.__account_no
    
    @property
    def user(self):
        return self.__user
    
    @property
    def amount(self):
        return self.__amount
    @amount.setter
    def amount(self, amount):
        self.__amount = amount
    
    @property
    def transaction(self):
        return self.__transaction

class SavingAccount(Account):

    interest_rate = 0.5
    type = "Saving"

    def __init__(self, account_no, user, amount):
        Account.__init__(self, account_no, user, amount)
        self.__card = None

    @property
    def card(self):
        return self.__card
    @card.setter
    def card(self, card):
        self.__card = card

    def add_card(self, card):
        self.__card = card

class FixDepositAccount(Account):

    interest_rate = 2.5

class Transaction:
    def __init__(self, transaction_type, amount, total, target_account = None):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__total = total
        self.__target_account = target_account
        if target_account == None:
            self.__record = f"{self.__transaction_type}-{self.__amount}-{self.__total}"
        else:
            self.__record = f"{self.__transaction_type}-{self.__amount}-{self.__total}-{self.__target_account}"

    @property
    def record(self):
        return self.__record


class Card:
    def __init__(self,card_no, account, pin):
        self.__card_no = card_no
        self.__account = account
        self.__pin = pin

    @property
    def card_no(self):
        return self.__card_no
    
    @property
    def account(self):
        return self.__account
    
    @property
    def pin(self):
        return self.__pin

class ATM_Card(Card):

    fee = 150

class Debit_Card(Card):

    fee = 300

class ATM_machine:

    withdraw_limit = 20000

    def __init__(self, atm_no, money = 1000000):
        self.__atm_no = atm_no
        self.__money = money

    @property
    def atm_no(self):
        return self.__atm_no

    def insert_card(self, card, pin):
        if card.pin == pin:
            return "Success"
        return None

    def deposit(self, account, amount):
        account + amount
        
    def withdraw(self, account, amount):
        if amount > self.__money:
            return "ATM has insufficient funds"
        if amount > ATM_machine.withdraw_limit:
            return "Exceeds withdrawal limit of 20,000 Baht"
        account - amount
        
    def transfer(self, account, amount, target_account):
        account.transfer(account, amount, target_account)

class Seller:
    def __init__(self, seller_no, name):
        self.__seller_no = seller_no
        self.__name = name
        self.__edc_list = []

    @property
    def name(self):
        return self.__name

    def add_edc(self, edc):
        self.__edc_list.append(edc)

    def search_edc_from_no(self, edc_no):
        for edc in self.__edc_list:
            if edc.edc_no == edc_no:
                return edc
            
    def paid(self, account, amount, target_account):
        account.transfer(account, amount, target_account)

class EDC_machine:
    def __init__(self,edc_no,seller):
        self.__edc_no = edc_no
        self.__seller = seller

    @property
    def edc_no(self):
        return self.__edc_no
    
    def paid(self, card, amount, target_account):
        account = card.account
        account.transfer(account, amount, target_account)

##################################################################################

# Define the format of the user as follows: {Citizen ID: [Name, Account Type, Account Number, Account Balance, Card Type, Card Number]}

user ={'1-1101-12345-12-0':['Harry Potter','Savings','1234567890',20000,'ATM','12345'],
       '1-1101-12345-13-0':['Hermione Jean Granger','Saving','0987654321',1000,'Debit','12346'],
       '1-1101-12345-13-0':['Hermione Jean Granger','Fix Deposit','0987654322',1000,'',''],
       '9-0000-00000-01-0':['KFC','Savings','0000000321',0,'',''],
       '9-0000-00000-02-0':['Tops','Savings','0000000322',0,'','']}

atm ={'1001':1000000,'1002':200000}

seller_dic = {'210':"KFC", '220':"Tops"}

EDC = {'2101':"KFC", '2201':"Tops"}


# TODO 1: Create an instance of the Bank and create instances of User, Account, and Card
# TODO   : Use the data in the `user` dictionary freely in any format.
# TODO   : The Account class is divided into two subclasses: Savings and FixedDeposit.
# TODO   : The Card class is divided into two subclasses: ATM and Debit.


scb = Bank('SCB')
scb.add_user(User('1-1101-12345-12-0','Harry Potter'))
scb.add_user(User('1-1101-12345-13-0','Hermione Jean Granger'))
scb.add_user(User('9-0000-00000-01-0','KFC'))
scb.add_user(User('9-0000-00000-02-0','Tops'))
harry = scb.search_user_from_id('1-1101-12345-12-0')
harry.add_account(SavingAccount('1234567890', harry, 20000))
harry_account = harry.search_account('1234567890')
harry_account.add_card(ATM_Card('12345', harry, '1234'))
hermione = scb.search_user_from_id('1-1101-12345-12-0')
hermione.add_account(SavingAccount('0987654321',hermione,2000))
hermione_account1 = hermione.search_account('0987654321')
hermione_account1.add_card(Debit_Card('12346',hermione_account1,'1234'))
hermione.add_account(FixDepositAccount('0987654322',hermione,1000))
kfc = scb.search_user_from_id('9-0000-00000-01-0')
kfc.add_account(SavingAccount('0000000321', kfc, 0))
tops = scb.search_user_from_id('9-0000-00000-02-0')
tops.add_account(SavingAccount('0000000322', tops, 0))

# TODO 2: Create an instance of the ATM machine

scb.add_atm_machine(ATM_machine('1001',1000000))
scb.add_atm_machine(ATM_machine('1002',200000))

# TODO 3: Create an instance of Seller and add EDC machines to the Seller

temp = Seller('210','KFC')
temp.add_edc(EDC_machine('2101',temp))
scb.add_seller(temp)
temp = Seller('220',"Tops")
temp.add_edc(EDC_machine('2201',temp))
scb.add_seller(temp)

# TODO 4: Create a method for deposit using `__add__` and withdrawal using `__sub__`.
# TODO   : Test deposit, withdrawal, and transfer using `+` and `-` with each account type.

# TODO 5: Create methods `insert_card`, `deposit`, `withdraw`, and `transfer` in the ATM machine and call them through the account.
# TODO   : Test money transfers between each account type.

# TODO 6: Create a method paid on the EDC machine and call it through the account.

# TODO 7: Create the itermethod in the Account class to return transactions for use in afor loop.

# Test case #1: Test deposit from an ATM using Harry's ATM card.
# The card must be inserted first. Locate ATM machine 1 and Harry's ATM card.
# Then call the function or method `deposit` from the ATM machine and use `+` from the account.
# Expected outcome:
# Test Case #1
# Harry's ATM No :  12345
# Harry's Account No :  1234567890
# Success
# Harry account before deposit :  20000
# Deposit 1000
# Harry account after deposit :  21000

atm_machine = scb.search_atm_machine('1001')
harry_account = scb.search_account_from_card('12345')
atm_card = harry_account.card
print("Test Case #1")
print("Harry's ATM No : ",atm_card.card_no)
print("Harry's Account No : ",harry_account.account_no)
print(atm_machine.insert_card(atm_card, "1234"))
print("Harry account before deposit : ",harry_account.amount)
print("Deposit 1000")
atm_machine.deposit(harry_account,1000)
print("Harry account after deposit : ",harry_account.amount)
print("")

# Test case #2: Test withdrawal from an ATM using Hermione's ATM card.
# The card must be inserted first. Locate ATM machine 2 and Hermione's ATM card.
# Then call the function or method `withdraw` from the ATM machine and use `-` from the account.
# Expected outcome:
# Test Case #2
# Hermione's ATM No :  12346
# Hermione's Account No :  0987654321
# Success
# Hermione account before withdraw :  2000
# withdraw 1000
# Hermione account after withdraw :  1000

atm_machine = scb.search_atm_machine('1002')
hermione_account = scb.search_account_from_card('12346')
atm_card = hermione_account.card
print("Test Case #2")
print("Hermione's ATM No : ", atm_card.card_no)
print("Hermione's Account No : ", hermione_account.account_no)
print(atm_machine.insert_card(atm_card, "1234"))
print("Hermione account before withdraw : ",hermione_account.amount)
print("withdraw 1000")
atm_machine.withdraw(hermione_account,1000)
print("Hermione account after withdraw : ",hermione_account.amount)
print("")

# Test case #3: Test transferring 10,000 THB from Harry's account to Hermione's account at the counter.
# Call the method for performing the money transfer.
# Expected outcome:
# Test Case #3
# Harry's Account No :  1234567890
# Hermione's Account No :  0987654321
# Harry account before transfer :  21000
# Hermione account before transfer :  1000
# Harry account after transfer :  11000
# Hermione account after transfer :  11000

harry_account = scb.search_account_from_card('12345')
hermione_account = scb.search_account_from_card('12346')
print("Test Case #3")
print("Harry's Account No : ",harry_account.account_no)
print("Hermione's Account No : ", hermione_account.account_no)
print("Harry account before transfer : ",harry_account.amount)
print("Hermione account before transfer : ",hermione_account.amount)
harry_account.transfer("0000", 10000, hermione_account)
print("Harry account after transfer : ",harry_account.amount)
print("Hermione account after transfer : ",hermione_account.amount)
print("")

# Test case #4: Test payment using a card reader. Call the `paid` method from the card reader.
# Hermione makes a payment of 500 THB to KFC using her own card.
# Expected outcome:
# Hermione's Debit Card No :  12346
# Hermione's Account No :  0987654321
# Seller :  KFC
# KFC's Account No :  0000000321
# KFC account before paid :  0
# Hermione account before paid :  11000
# KFC account after paid :  500
# Hermione account after paid :  10500

hermione_account = scb.search_account_from_account_no('0987654321')
debit_card = hermione_account.card
kfc_account = scb.search_account_from_account_no('0000000321')
kfc = scb.search_seller('KFC')
edc = kfc.search_edc_from_no('2101')

print("Test Case #4")
print("Hermione's Debit Card No : ", debit_card.card_no)
print("Hermione's Account No : ",hermione_account.account_no)
print("Seller : ", kfc.name)
print("KFC's Account No : ", kfc_account.account_no)
print("KFC account before paid : ",kfc_account.amount)
print("Hermione account before paid : ",hermione_account.amount)
edc.paid(debit_card, 500, kfc_account)
print("KFC account after paid : ",kfc_account.amount)
print("Hermione account after paid : ",hermione_account.amount)
print("")

# Test case #5: Test electronic payment by calling the `paid` method from KFC.
# Hermione makes a payment of 500 THB to Tops.
# Expected outcome:
# Test Case #5
# Hermione's Account No :  0987654321
# Tops's Account No :  0000000322
# Tops account before paid :  0
# Hermione account before paid :  10500
# Tops account after paid :  500
# Hermione account after paid :  10000

hermione_account = scb.search_account_from_account_no('0987654321')
debit_card = hermione_account.card
tops_account = scb.search_account_from_account_no('0000000322')
tops = scb.search_seller('Tops')
print("Test Case #5")
print("Hermione's Account No : ",hermione_account.account_no)
print("Tops's Account No : ", tops_account.account_no)
print("Tops account before paid : ",tops_account.amount)
print("Hermione account before paid : ",hermione_account.amount)
tops.paid(hermione_account,500,tops_account)
print("Tops account after paid : ",tops_account.amount)
print("Hermione account after paid : ",hermione_account.amount)
print("")

# Test case #6: Display all transactions of Hermione using a `for` loop.
print("Test Case #6")
hermione_account = scb.search_account_from_account_no('0987654321')
print("Hermione's transaction log:")
for data in hermione_account.transaction:
    print(data.record)

import logging
import sys
import json
from collections import namedtuple
from print_scripts import *

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
formatter = logging.Formatter('[%(asctime)s]: %(message)s')
stream_handler.setFormatter(formatter)

title = print_title()
about = print_about()
exit_message = print_exit()
line_break = print_line_break()

print(title)
print(about)

class BankProduct:

    def __init__(self):
        self.message = input("Is this a 'loan' or 'savings'? ").strip().lower()
        self.product = self.create_product()
   
    def create_product(self):
        if self.message == "loan":
            return LoanProduct(str, int, float, int) 
        elif self.message == "savings":
            return DepositProduct().product     
        else:
            logger.error("\nNo valid product entered \n")
            return None
    # This allows for error logging inputs without excessive code
    def get_input(self, prompt, cast_type):
        while True:
            try:
                return cast_type(input(prompt))
            except ValueError:
                logger.error("\nInvalid input. Please enter a valid number. \n")

class LoanProduct(BankProduct):

    def __init__(self, name, principal, annual_interest_rate, loan_term_years):
        self.name = input("Enter name of product: ")
        self.principal = self.get_input("Enter total amount borrowed: ", int)
        self.annual_interest_rate = self.get_input("Enter interest rate: ", float)
        self.loan_term_years = self.get_input("Enter loan term in years: ", int)

    def __repr__(self):
        return f"\nLoan: {self.name} \nAmount: ${self.principal} \nAPR: {self.annual_interest_rate}% \nTerm: {self.loan_term_years} years\n"

    def calculate_monthly_payment(self):
        monthly_interest_rate = self.annual_interest_rate / 12 / 100
        self.total_payments = self.loan_term_years * 12
        self.monthly_payment = (self.principal * monthly_interest_rate * (1 + monthly_interest_rate) ** self.total_payments) / ((1 + monthly_interest_rate) ** self.total_payments - 1)
        return f"Monthly payment: ${round(self.monthly_payment, 2)}"

    def get_interest(self):
        total_amount_paid = self.monthly_payment * self.total_payments
        total_interest_paid = total_amount_paid - self.principal
        return f"Total interest paid: ${round(total_interest_paid, 2)} \nTotal amount paid: ${round(total_amount_paid, 2)} \n"

class DepositProduct(BankProduct):

    def __init__(self):
        self.message = input("Is this a 'certificate' or 'money market'? ").strip().lower()
        self.product = self.choose_product()
    # Because DP also has child classes, this does the same thing as create_product in BankProduct
    def choose_product(self):
        if self.message == "certificate":
            return Certificate(str, int, float, int)
        elif self.message == "money market":
            return MoneyMarket(str, int, float, int)
        else:
            logger.error("\nNo valid product entered \n")
            return None
    # This calculation reduces code by giving me a method to call for both compound calculations
    def calculate_compound_interest(self, balance, rate, term_months, compounding_periods=12):
        r = rate / 100
        t = term_months / 12
        A = balance * (1 + r / compounding_periods) ** (compounding_periods * t)
        dividends = A - balance
        return round(dividends, 2), round(A, 2)

class Certificate(DepositProduct):

    def __init__(self, name, balance, apr, deposit_term_months):
        self.name = "Certificate of Deposit"
        self.balance = self.get_input("Enter the deposit balance: ", int)
        self.apr = self.get_input("Enter the dividend rate: ", float)
        self.deposit_term_months = self.get_input("Enter the deposit term in months: ", int)

    def __repr__(self):
        return f"\n{self.name} \nDeposit: ${self.balance} \nDividend Rate: {self.apr}% \nDeposit Term: {self.deposit_term_months} months"

    def calculate_dividends_fixed(self):
        dividends_earned, new_balance = self.calculate_compound_interest(self.balance, self.apr, self.deposit_term_months)
        return f"\nDividends earned: ${dividends_earned} \nNew Balance: ${new_balance}"

class MoneyMarket(DepositProduct):

    def __init__(self, name, balance, tiered_interest, deposit_term_months):
        self.name = "Money Market"
        self.balance = self.get_input("Enter deposit balance in whole dollars: ", int)
        self.tiered_interest = self.get_tiered_value()  
        # Money Market dividends are variable and based on balance tiers
        self.deposit_term_months = self.get_input("Enter deposit term to calculate in months: ", int)

    def get_tiered_value(self):
        try:
            with open('dividend_rates.json') as json_file:
                data = json.load(json_file)
                Tier = namedtuple("Tier", ["balance_range", "rate"])
                tiers = map(lambda x: Tier(x["balance_range"], x["rate"]), data["tiers"])
            # This uses a JSON list to determine the appropriate dividend based on balance value
            for tier in tiers:
                balance_range = tier.balance_range.split('-')
                if len(balance_range) == 2:
                    lower_bound = int(balance_range[0])
                    upper_bound = int(balance_range[1])
                    if lower_bound <= self.balance <= upper_bound:
                        return tier.rate
                else:
                    if self.balance >= int(balance_range[0].replace('+', '')):
                        return tier.rate
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error reading dividend rates: {e}")
        return 0

    def __repr__(self):
        return f"\n{self.name} \nDeposit Balance: ${self.balance} \nCurrent Dividend: {self.tiered_interest}% \nDividend Term to Calculate: {self.deposit_term_months} months"

    def calculate_dividends_tiered(self):
        dividends_earned, new_balance = self.calculate_compound_interest(self.balance, self.tiered_interest, self.deposit_term_months)
        return f"\nDividends earned: ${dividends_earned} \nNew Balance: ${new_balance} \n"

# The while loop iterates the program repeatedly until the user confirms 'no' to the choice
while True:
    bank_product = BankProduct()
    if bank_product.product:
        if isinstance(bank_product.product, LoanProduct):
            loan_product = bank_product.product
            loan_payment = loan_product.calculate_monthly_payment()
            loan_interest = loan_product.get_interest()
            print(loan_product)
            print(loan_payment)
            print(loan_interest)
        elif isinstance(bank_product.product, Certificate):
            certificate = bank_product.product
            dividends = certificate.calculate_dividends_fixed()
            print(certificate)
            print(dividends)
        elif isinstance(bank_product.product, MoneyMarket):
            money_market = bank_product.product
            dividends = money_market.calculate_dividends_tiered()
            print(money_market)
            print(dividends)
    print(line_break)
    choice = input("Do you want to perform another calculation? (yes/no): ").strip().lower()
    if choice != 'yes':
        print(exit_message)
        break

# Text based slot machine
import random


MAX_LINES=3
MAX_BET=100
MIN_BET=1

ROWS = 3
COLS = 3

symbol_count={
    "A":2,
    "B":4,
    "C":6,
    "D":8
}

symbol_value={
    "A":5,
    "B":4,
    "C":3,
    "D":2
}

def check_winnings(columns,lines,bet,values):
    winnings=0
    winning_lines=[]
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check=column[line]
            if symbol != symbol_to_check:
                break
        
        else:
            winnings += values[symbol]*bet
            winning_lines.append(line+1)

    return winnings,winning_lines



def get_slot_spin(rows,cols,symbols):
    all_symbols=[]

    # It gives both keys, and values seprately by using .items() in a dictionary
    for symbol,symbol_count in symbols.items():
        for _ in range (symbol_count):
            all_symbols.append(symbol)
        
    columns=[]
    for _ in range(cols):
        column=[]
        curret_symbol=all_symbols.copy()
        #can also do: =all_symbols[:]

        for _ in range(rows):
            value=random.choice(all_symbols)
            curret_symbol.remove(value)
            column.append(value)
        
        columns.append(column)
    
    return columns


def print_slot(columns):

    #TRANSPOSING (MATRIX OPERATION)
    for row in range(len(columns[0])):
        for i,column in enumerate(columns):
            if i != len(columns)-1:
                print(column[row],end=" | ")
            else:
                print(column[row],end="")

        print()


def deposit():
    while True:
        amount=input("What would you lik to deposit? $")
        if amount.isdigit():
            amount=int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Enter a number")

    return amount


def get_number_of_lines():
    while True:
        lines=input("Enter the number of lines to be bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines=int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines")
        else:
            print("Enter a numebr")
        
    return lines


def get_bet():
    while True:
        amount=input("What would you like to bet on each line? $")
        if amount.isdigit():
            if MIN_BET <= int(amount) <= MAX_BET:
                amount=int(amount)
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}")
                # BY PUTTING A F (STRING), WE CAN PUT VARIABLES INSIDE A STRING
                # YOU PUT A F INSIDE A STRING, THE PUT CURLY BRACES AROUND A VARIABLE, THEN IT WILL
                # AUTOMATICALL CONVERT A VARIABLE INTO STRING, IF IT CAN BE CONVERTED
        else:
            print("Please enter a number")
    
    return amount


def spin(balance):
    lines=get_number_of_lines()
    while True:
        bet=get_bet()
        total_bet=lines*bet

        if total_bet > balance:
            print(f"Your total bet amount exceeds you balance, please retry, your balance is: ${balance}")
        else:
            break

    print(f"you are betting ${bet} on {lines} lines. Total bet is equal to : ${total_bet}")
    slots=get_slot_spin(ROWS,COLS,symbol_count)
    print_slot(slots)
    winnings, winning_lines =check_winnings(slots,lines,bet,symbol_value)
    print(f"you won ${winnings}")

    #ADVANCE syntax: SPLAT OPERATOR/ UNPACK OPERATOR
    print(f"you won on line:", *winning_lines)
    return winnings - total_bet


def main():
    balance=deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press Enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
    
    print(f"Your are left with ${balance}")
    

main()
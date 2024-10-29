import donkeydefs


def show_state(donkey_dict):
    print(f"""The donkey is {donkey_dict['AGE']} years old and has {donkey_dict['MONEY']} eur.
Satiation: {donkey_dict['SATIATION']}
Happiness: {donkey_dict['HAPPINESS']}
Energy: {donkey_dict['ENERGY']}""")
    if donkey_dict['RETIRED']:
        print("The donkey has retired.")


def get_user_input(acceptable_vals):
    while True:
        val = input("Input next choice: ")
        if val in acceptable_vals:
            return val
        else:
            print("Invalid input!")


def prompt_choice(donkey_dict):
    if donkey_dict['RETIRED']:
        print(f"Choices: {', '.join(donkeydefs.RETIREMENT_CHOICES)}")
        return get_user_input(donkeydefs.RETIREMENT_CHOICES)
    else:
        print(f"Choices: {', '.join(donkeydefs.CHOICES)}")
        return get_user_input(donkeydefs.CHOICES)

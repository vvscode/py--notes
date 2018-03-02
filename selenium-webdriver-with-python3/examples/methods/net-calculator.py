STATE_TEXES = {
    "Alabama": 5,
    "Florida": 15
}

FED_TAX = 10

def get_net(state = "Alabama", gross = 0):
    state_tax = STATE_TEXES.get(state, 0)
    return gross * (100 - FED_TAX - state_tax) / 100


print(get_net(gross = 100))
print(get_net(state = "Florida", gross = 200))
print(get_net(state = "Unknown state", gross =  200))
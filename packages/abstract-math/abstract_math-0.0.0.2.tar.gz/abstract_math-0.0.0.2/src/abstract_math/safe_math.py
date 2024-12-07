from abstract_utilities import *
#math functions ------------------------------------------------------------------------------------------------------
def exponential(value,exp=9,num=-1):
    return multiply_it(value,exp_it(10,exp,num))

def return_0(*args):
    for arg in args:
        if arg == None or not is_number(arg) or arg in [0,'0','','null',' ']:
            return float(0)
        
def exp_it(number,integer,mul):
    if return_0(number,integer,mul)==float(0):
        return float(0)
    return float(number)**float(float(integer)*int(mul))

def divide_it(number_1,number_2):
    if return_0(number_1,number_2)==float(0):
        return float(0)
    return float(number_1)/float(number_2)

def multiply_it(number_1,number_2):
    if return_0(number_1,number_2)==float(0):
        return float(0)
    return float(number_1)*float(number_2)

def add_it(number_1,number_2):
    if return_0(number_1,number_2)==float(0):
        return float(0)
    return float(number_1)+float(number_2)

def get_percentage(owner_balance,address_balance):
    retained_div = divide_it(owner_balance,address_balance)
    retained_mul = multiply_it(retained_div,100)
    return round(retained_mul,2)

def get_proper_args(strings,*args,**kwargs):
    properArgs = [] 
    for key in strings:
        kwarg = kwargs.get(key)
        if kwarg == None and args:
            kwarg = args[0]
            args = [] if len(args) == 1 else args[1:]
        properArgs.append(kwarg)
    return properArgs
def get_lamp_difference(*args,**kwargs):
    sol_lamports =int(exponential(1,exp=9,num=1))
    proper_args = get_proper_args(["virtualSolReserves"],*args,**kwargs)
    virtualLamports = len(str(proper_args[0]))
    virtual_sol_lamports =int(exponential(1,exp=virtualLamports,num=1))
    return int(exponential(1,exp=len(str(int(virtual_sol_lamports/sol_lamports))),num=1))
def get_price(*args,**kwargs):
    proper_args = get_proper_args(["virtualSolReserves","virtualTokenReserves"],*args,**kwargs)
    return divide_it(*proper_args)/get_lamp_difference(*args,**kwargs)
def get_amount_price(*args,**kwargs):
    proper_args = get_proper_args(["solAmount","tokenAmount"],*args,**kwargs)
    return divide_it(*proper_args) 
def getSolAmountUi(*args,**kwargs):
    proper_args = get_proper_args(["solAmount"],*args,**kwargs)
    return exponential(proper_args[0],9)
def getTokenAmountUi(*args,**kwargs):
    solAmountUi = getSolAmountUi(*args,**kwargs)
    price = get_price(*args,**kwargs)
    return solAmountUi/price
def derive_token_decimals(*args,**kwargs):
    proper_args = get_proper_args(["virtualTokenReserves","tokenAmount"],*args,**kwargs)
    price = get_price(*args,**kwargs)
    if not (proper_args[1] > 0 and proper_args[0] > 0 and price > 0):
        raise ValueError("All inputs must be positive.")
    derived_token_amount = proper_args[0] / price
    ratio = derived_token_amount / proper_args[1]
    decimals = -1
    while abs(ratio - round(ratio)) > 1e-9:
        ratio *= 10
        decimals += 1
    return decimals
def derive_token_decimals_from_token_variables(variables):
  variables["price"] = get_price(**variables)
  derived_token_amount = variables["virtualTokenReserves"] / variables["price"]
  ratio = derived_token_amount / variables["tokenAmount"]
  decimals = -1
  while abs(ratio - round(ratio)) > 1e-9:
      ratio *= 10
      decimals += 1
  variables["tokenDecimals"] = decimals
  return variables
def get_token_amount_ui(*args,**kwargs):
  proper_args = get_proper_args(["tokenAmount"],*args,**kwargs)
  return exponential(proper_args[0],exp=-derive_token_decimals(*args,**kwargs),num=1)
def update_token_variables(variables):
    variables['solAmountUi'] = getSolAmountUi(**variables)
    variables['solDecimals'] = 9
    variables = derive_token_decimals_from_token_variables(variables)
    variables['tokenAmountUi'] = exponential(variables['tokenAmount'],exp=-variables["tokenDecimals"],num=1)
    return variables
variables =   {"solAmount": 396000000,
  "tokenAmount": 1627047727651,
  "virtualSolReserves": 88711399815,
  "virtualTokenReserves":362862046933704}

input(update_token_variables(variables))

from decimal import Decimal, getcontext
from .safe_math import *
getcontext().prec = 50  # High precision for accuracy
SOL_DECIMAL_PLACE = 9
SOL_LAMPORTS = sol_lamports =int(exponential(1,exp=SOL_DECIMAL_PLACE,num=1))
def get_proper_args(strings,*args,**kwargs):
    properArgs = [] 
    for key in strings:
        kwarg = kwargs.get(key)
        if kwarg == None and args:
            kwarg = args[0]
            args = [] if len(args) == 1 else args[1:]
        properArgs.append(kwarg)
    return properArgs

#lamports
def get_lamports(integer):
    return exp_it(10,len(str(integer))+1,1)
def get_lamport_difference(lamports,virtual_lamports):
    integer = int(virtual_lamports/lamports)
    exponential = len(str(integer))
    return int(exponential(1,exp=exponential,num=1))
#virtual reserves
def get_vitual_reserves(*args,**kwargs):
    proper_args = get_proper_args(["virtualSolReserves","virtualTokenReserves"],*args,**kwargs)
    return proper_args
def get_virtual_reserve_ratio(*ars,**kwargs):
    proper_args = get_vitual_reserves(*args,**kwargs)
    return divide_it(*proper_args)
#sol reserves
def get_virtual_sol_reservs(*args,**kwargs):
    proper_args = get_proper_args(["virtualSolReserves"],*args,**kwargs)
    return proper_args[0] if proper_args else proper_args
def get_virtual_sol_lamports(*args,**kwargs):
    virtual_sol_reserves = get_virtual_sol_reservs(*args,**kwargs)
    virtual_sol_lamports = get_lamports(virtual_sol_reserves)
    return virtual_sol_lamports
def get_virtual_sol_lamp_difference(*args,**kwargs):
    virtual_sol_lamports = get_virtual_sol_lamports(*args,**kwargs)
    return get_lamport_difference(SOL_LAMPORTS,virtual_sol_lamports)
#sol Amount
def get_sol_amount(*args,**kwargs):
    proper_args = get_proper_args(["solAmount"],*args,**kwargs)
    return proper_args[0] if proper_args else proper_args
def getSolAmountUi(*args,**kwargs):
    sol_amount = get_sol_amount(*args,**kwargs)
    return exponential(sol_amount,SOL_DECIMAL_PLACE)
#token reserves
def get_virtual_token_reservs(*args,**kwargs):
    proper_args = get_proper_args(["virtualTokenReserves"],*args,**kwargs)
    return proper_args[0] if proper_args else proper_args
def get_virtual_token_lamports(*args,**kwargs):
    virtual_token_reserves = get_virtual_token_reservs(*args,**kwargs)
    virtual_token_lamports = get_lamports(virtual_token_reserves)
    return virtual_token_lamports
#token amount
def get_token_amount(*args,**kwargs):
    proper_args = get_proper_args(["tokenAmount"],*args,**kwargs)
    return proper_args[0] if proper_args else proper_args
def get_token_amount_ui(*args,**kwargs):
    token_amount = get_token_amount(*args,**kwargs)
    token_decimals = derive_token_decimals(*args,**kwargs)
    return exponential(token_amount,exp=token_decimals)
#token derivision
def derive_token_decimals_from_token_variables(variables):
    variables["price"] = get_price(**variables)
    variables["tokenDecimals"] = derive_decimals_from_vars(*args,**kwargs)
    return variables
def get_derived_token_ratio(*args,**kwarg):
    derived_token_amount = derive_token_amount(*args,**kwargs)
    token_amount = get_token_amount(*args,**kwargs)
    ratio = divide_it(derived_token_amount,token_amount)
    return ratio
def derive_token_amount(*args,**kwargs):
    virtual_token_reserves = get_virtual_token_reserves(*args,**kwargs)
    price = get_price(*args,**kwargs)
    derived_token_amount = divide_it(virtual_token_reserves,price)
    return derived_token_amount
#derive variables
def get_price(*args,**kwargs):
    reserve_ratios = get_virtual_reserve_ratio(*ars,**kwargs)
    virtual_sol_lamp_difference = get_virtual_sol_lamp_difference(*args,**kwargs)
    return reserve_ratios/virtual_sol_lamp_difference
def derive_decimals_from_vars(*args,**kwargs):
  ratio = get_derived_token_ratio(*args,**kwarg)
  decimals = -1
  while abs(ratio - round(ratio)) > 1e-9:
      ratio *= 10
      decimals += 1
  return decimals
def update_token_variables(variables):
    variables['solAmountUi'] = getSolAmountUi(**variables)
    variables['solDecimals'] = 9
    variables = derive_token_decimals_from_token_variables(variables)
    variables['tokenAmountUi'] = exponential(variables['tokenAmount'],variables["tokenDecimals"])
    return variables


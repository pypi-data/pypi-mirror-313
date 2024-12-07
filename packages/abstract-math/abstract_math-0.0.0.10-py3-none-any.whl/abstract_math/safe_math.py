#abstract_bots.py
import os
import re
import json
import shutil
import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from abstract_utilities import (safe_dump_to_file,
                                safe_read_from_json,
                                get_any_value,
                                make_list,
                                eatAll)
#json functions-----------------------------------------------------------------------------------------------------------------------------------------
def safe_json_loads(data):
    if not isinstance(data, (dict, str)):
        data = str(data)
    if not isinstance(data, dict):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            logger.error("Error parsing data with json, data might not be in correct format.")
            data = None
    return data

def load_json_data(file_path):
    try:
        with file_path.open('r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"Error reading JSON file: {e}")
        return None
    
def safe_list(obj,keys):
    keys = make_list(keys)
    for key in keys:
        if obj and isinstance(obj,list) and is_number(key) and len(obj)>key:
            obj = obj[int(key)]
        else:
            return obj
    return obj

def safe_get(obj,keys):
    keys = make_list(keys)
    new_obj = obj
    for i,key in enumerate(keys):
        if isinstance(new_obj,dict):
            new_obj = new_obj.get(key,None if len(keys)-1 == i else {})
        elif isinstance(new_obj,list):
            new_obj = safe_list(new_obj,key)
        else:
            return new_obj
    return new_obj

def get_all_keys(dict_data,keys=[]):
  if isinstance(dict_data,dict):
    for key,value in dict_data.items():
      keys.append(key)
      keys = get_all_keys(value,keys=keys)
  return keys
#address sanitation-----------------------------------------------------------------------------------------------
def get_data(file_path):
    if os.path.isfile(file_path):
        return safe_read_from_json(file_path)
    
#directory functions --------------------------------------------------------------------------------------------
def move_file(src_path,dst_file_path):
    shutil.move(str(src_path), str(dst_file_path))
    logger.info(f"Moved {src_path.name} to errored messages directory.")

def secure_delete(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File {file_path} has been deleted.")
        else:
            logger.warning(f"File {file_path} does not exist.")
    except OSError as e:
        logger.error(f"Error deleting file {file_path}: {e.strerror}")

def make_directory(file_path):
    os.makedirs(file_path, exist_ok=True)
    return file_path

def get_create_data(file_path,data={}):
    if not os.path.isfile(file_path):
        safe_dump_to_file(data=data,file_path=file_path)
    return safe_read_from_json(file_path)

#type functions --------------------------------------------------------------------------------------------------
def get_args_send_args(function, *args):
    if not args:
        return args
    input_type = type(args[0])
    flattened_args = []
    for arg in args:
        if isinstance(arg, (list, set, tuple)):
            flattened_args.extend(arg)
        else:
            flattened_args.append(arg)
    processed_items = [function(item) for item in flattened_args]
    if input_type is list:
        return processed_items
    elif input_type is set:
        return set(processed_items)
    elif input_type is tuple:
        return tuple(processed_items)
    else:
        # Assuming if_single_obj is a function that handles single objects
        return if_single_obj(processed_items)
    
def list_set(obj):
    obj = obj or []
    return list(set(obj))

def get_symetric_difference(obj_1,obj_2):
    set1 = set(obj_1)
    set2 = set(obj_2)
    # Find elements that are unique to each list
    unique_elements = set1.symmetric_difference(set2)
    # Convert the set back to a list, if needed
    return list(unique_elements)

def if_single_obj(list_obj):
    if list_obj and isinstance(list_obj,list) and len(list_obj)==1:
        list_obj = list_obj[0]
    return list_obj

def list_set(obj):
    try:
        obj = list(set(obj))
    except Exception as e:
        print(f"{e}")
    return obj

def str_lower(obj):
    try:
        obj=str(obj).lower()
    except Exception as e:
        print(f"{e}")
    return obj

def is_number(obj):
    try:
        float(obj)
        return True
    except (ValueError, TypeError):
        return False
#address functions-------------------------------------------------------------------------------------------------
def normalize_address(address):
    address =str(address).lower()
    if address.startswith('0x'):
        address = address[2:]
    return address

def normalize_all_addresses(*args):
    return get_args_send_args(normalize_address,*args)

def serialize_all_addresses(*args):
    return get_args_send_args(check_and_reserialize_solana_address, *args)

def make_directory(data_path):
    os.makedirs(data_path, exist_ok=True)
    return data_path

def get_amount_dict(amount,decimals=9):
    if amount!= None:
        if isinstance(amount,dict):
            amount_dict = get_any_value(amount,'uiTokenAmount')
            amount = get_any_value(amount_dict,'amount')
            decimals = get_any_value(amount_dict,'decimals')
        return exponential(amount,decimals,-1)
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

 


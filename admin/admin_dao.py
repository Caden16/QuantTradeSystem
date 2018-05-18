from dataSort.QAUtil import DATABASE

def check_user(user_name, password):
    user_collection = DATABASE.user_list
    find_condition = {"user_name": user_name, "password": password}
    user_result = user_collection.find(find_condition)
    if user_result.count() > 0:
        return True
    else:
        return False

def get_admin_name():
    user_collection = DATABASE.user_list
    user_result = user_collection.find()
    user_name = ""
    if user_result.count() > 0:
        user_name = user_result[0]["user_name"]
    return user_name

def add_terminal(mac_addr):
    terminal_collection = DATABASE.terminals
    documents = {"mac": mac_addr}
    exist_mac = terminal_collection.find(documents)
    if exist_mac.count() > 0:
        return True
    terminal_collection.insert_one(documents)
    return True

def get_terminals():
    terminal_collection = DATABASE.terminals
    terminals = terminal_collection.find({})
    all_terminal = []
    for item in terminals:
        all_terminal.append({"mac": item["mac"]})
    return all_terminal

def delete_terminal(mac_addr):
    terminal_collection = DATABASE.terminals
    terminal_collection.remove({"mac": mac_addr})

def check_terminal(mac_addr):
    terminal_collection = DATABASE.terminals
    result = terminal_collection.find({"mac": mac_addr})
    if result.count() > 0:
        return True
    return False

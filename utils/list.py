
def find(list: list, callback):
    
    if not callback:
        return None

    for item in list:
        is_item = callback(item)

        if is_item:
            return item
        
    return None
from typing import Any

def is_empty(param: Any) -> bool:
    '''
    Возвращает булеву переменную которая сообщает является ли параметр или атрибут "пустым" или нулевым
    '''
    if param is None:
        return True
    
    if isinstance(param, list):
        if param == []:
            return True
        
    if isinstance(param, str):
        if param == "":
            return True
        
    return False
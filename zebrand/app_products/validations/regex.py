import re

def validateParams(*args):
    for word in args:
        pattern = re.compile('[\[\]{}$\',.":;<>\-&\/^*+??@#$%()=]')
        
        if pattern.search(word):
            return True
        
    
    return False


    
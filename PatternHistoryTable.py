from State import State

class PatternHistoryTable:
    '''State History Table is a basic dictonary with extended functionality. 
    
    Args:
        :param ``state_size``: When creating, size of the new State
    '''

    def __init__(self, state_size=2) -> None:
        self.values = {}                                # A dictonary containing the addresses and their 'actual' values
        self.state_size = state_size


    def get_val(self, key):
        '''retreive state with key and return its decimal value'''

        state = self.__getitem__(key)
        return state.get_val()


    def __getitem__(self, key):
        '''acess item with []'''

        if not key in self.values:                      # I Key not in values: creates a State of the default key size
            self.values[key] = State(self.state_size)
        return self.values[key]                         


    def __setitem__(self, key, value):
        '''set item with []'''
        
        self.values[key] = value


    def __len__(self):
        '''get length of values'''
        return len(self.values)
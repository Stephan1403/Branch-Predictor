#TODO: implement for diffrent bit (use bin instead of hex)
#TODO: e.g. change increment method

class State:
    '''State is used to predict the next branch (jump or no jump)

    Args:
        :param ``bit``: the size of bit each state has
        :param ``value``: set a start value from 0 to the hightest possible with n bits


    Functions:
        ????


    ---------TODO: redo------
    > State meaining:
        - ``0 or 1:`` No jump is expected for this branch the next time
        - ``2 or 3:``A jump is expected for this branch the next time

    > State changing:
        - ``no jump:`` subtracting one but the lowest is 0
        - ``Jump:``  adding one but the highest is 3
    '''

    def __init__(self, bit, value = 0) -> None:
        self.bit = bit                          # Size of history table
        if value >= 0 and value <=2**bit-1:     # value has to be between 0 and the highest representative number with n bits
            self.value = value
        else:
            self.value = 0

    def no_jump(self):
        if(self.value in [1, 2, 3]):
            self.value-=1

    def jump(self):
        if(self.value in [0, 1, 2]):
            self.value+=1

    def left_shift(self, x):
        r'''Shift the value to the left using x
        
            :param ``x``: A bit that is shifted from the right side (0 or 1)
        '''

        
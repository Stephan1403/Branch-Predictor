#TODO: implement for diffrent bit
#TODO: e.g. change increment method

class State:
    '''State is used to determine wether to jump from a branch.

        :param ``bit``: the bit each state has
        :param ``value``: set a start value from 0 to 3

    > State meaining:
        - ``0 or 1:`` No jump is expected for this branch the next time
        - ``2 or 3:``A jump is expected for this branch the next time

    > State changing:
        - ``no jump:`` subtracting one but the lowest is 0
        - ``Jump:``  adding one but the highest is 3
    '''

    def __init__(self, bit, value = 0) -> None:
        if value >= 0 and value <=3:
            self.value = value
        else:
            self.value = 0

    def no_jump(self):
        if(self.value in [1, 2, 3]):
            self.value-=1

    def jump(self):
        if(self.value in [0, 1, 2]):
            self.value+=1
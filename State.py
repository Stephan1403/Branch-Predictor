#TODO: store precicion rate, when was it right

class State:
    '''State is used to determine wether to jump from a branch.

        Depending on the correct result the state is changing:

        - ``no jump:`` subtracting one but the lowest is 0
        - ``Jump:``  adding one but the highest is 11 (Binary)
    '''

    def __init__(self, value = "00") -> None:
        self.value = value
        self.count = 0              # Number of times a branch is called
        self.correct = 0            # Number of times a branch prediction was correct

    def __add__(self, val):
        if self.value == "00":      # 00
            self.value = "01"
        elif self.value == "01":    # 01
            self.value = "10"
        elif self.value == "10":    # 10
            self.value = "11"

    def __sub__(self, val):
        if self.value == "01":      # 01
            self.value = "00"
        elif self.value == "10":    # 10
            self.value = "01"
        elif self.value == "11":    # 11
            self.value = "10"



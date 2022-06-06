#TODO: store precicion rate, when was it right

class State:
    '''State is used to determine wether to jump from a branch.


        << State meaining: >>
        
        - ``0 or 1:`` No jump is expected for this branch the next time
        - ``2 or 3:``A jump is expected for this branch the next time



        << State changing: >>

        - ``no jump:`` subtracting one but the lowest is 0
        - ``Jump:``  adding one but the highest is 3

        
    '''

    def __init__(self, value = 0) -> None:
        self.value = value
        self.count = 0              # Number of times a branch is called
        self.correct = 0            # Number of times a branch prediction was correct

    def no_jump(self):
        self.count+=1

        if(self.value in [0, 1]):   # Correct prediction
            self.value+=1
            self.correct+=1
        elif(self.value == 2):      # Wrong prediction
            self.value+=1
        elif(self.value == 3):
            pass

    def jump(self):
        self.count+=1

        if(self.value == 0):        # Wrong prediction
            pass
        elif(self.value == 1):
            self.value-=1
        elif(self.value in [2, 3]): # Correct Prediction
            self.value-=1
            self.correct+=1

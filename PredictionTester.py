from State import State

class PredictionTester:
    r'''Prediction Tester is used to test different branch prediction methods
    
            > Parameter: 
                - ``file_path`` =  path to file containing the branches and their results
            
            > Predictors:
                - ``local_2_bit_predictor``
                - ``lorem ipsum``
                - ``lorem ipsum``
    '''

    def __init__(self, file_path) -> None:
        self.pht = {}                                           # Pattern history table containing states
        self.branches = {}                                      # Address is the key and the state is the value

        with open(file_path, 'r') as f:
            for b in f.read().splitlines():
                address, state = b.split(' ')
                self.branches[address] = state


# Predictors        
    async def local_2_bit_predictor(self):                      # TODO: Using async to await the result and show a loading bar in the meantime
        r'''Test precicion of the local 2 Bit predictor'''   

        for key, state in self.branches.items():
            if not self.pht[key]:                               # Init branch if not done
                self.pht[key] = State()

            if state == '0':                                    # No jump
                self.pht[key]-=1
                break
            self.pht[key]+=1                                    # Jump
            

    async def two_level_global_predictor():
        r'''Test percicion of the two level global predictor'''


    async def __private_function():
        pass


        
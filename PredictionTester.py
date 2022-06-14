from State import State

# TODO: change jump (name) to acutal

# TODO: introduce variable that represents the used predictor (to show what correct_rate is for)

class PredictionTester:
    r'''Prediction Tester is used to test different branch prediction methods
    
            :param ``file_path``: path to file containing branches and their actual results
            

        > Predictors:
            - ``local_2_bit_predictor``
            - ``lorem ipsum``
            - ``lorem ipsum``

        > Usage:
         # TODO: ...    
    '''

    def __init__(self, file_path) -> None:
        self.pht = {}                                           # Pattern history table containing states
        self.ghr = State(4)                                     # Global history register, has 4 Bit by default
        self.branches = self.__branch_file_to_list(file_path)   # List of tuples with addresses and actuals

        self.count = 0                                          # All branches of last predictor             
        self.correct = 0                                        # Count of branches which have been right predicted
        self.precision_rate = 0                                 # Rate of correct predicted branches


# Predictors        
    def local_2_bit_predictor(self, address_size=32):                            # TODO: Using async to await the result and show a loading bar in the meantime
        r'''Test precision of the local 2 Bit predictor.
        
            :param ``address_size``: set Size of Pattern history table keys in bits (default: 32 bit)
        ''' 
        
        for key, actual in self.branches:
            address = bin(int(key, 16))[-address_size:]         # address: binary value of old hexadecimal branch address
            if address not in self.pht:                         # Create new dictonary entry, if key doesn't exist
                self.pht[address] = State(2)  

            self.__update_precision(address, actual)            # Update Precision first
            self.__set_state(address, actual)
                                
        print(f"Local 2-Bit Predictor\n-{address_size} bit address size\n-------- Precision rate: {self.precision_rate*100}% --------\n")
        
        
        
    def two_level_global_predictor(self, ghr_size=4):
        r'''Test percicion of the two level global predictor

            :param ``ghr_size``: size of gloabl history table in bits (default: 4 Bit)
        
        Each address in the ghr (global history register) address one cell from the pht (pattern history table)
        '''

        self.ghr = State(ghr_size)                              # default = 4 Bit long global history register

        for data in self.branches:
            actual = data[1]                                    # Actual is always the 2nd value of the tuple
            self.ghr.left_shift(actual)                         # Push Actual value (0 or 1) from the right to change ghr value
            
            address = self.ghr
            if address not in self.pht:
                self.pht[address] = State(2)

            self.__update_precision(address, actual)
            self.__set_state(address, actual)
            
        print(f"2-Lvl-Global-Predictor\n-{ghr_size} global history table size\n-------- Precision rate: {self.precision_rate*100}% --------\n")
        


# Functions
    def __branch_file_to_list(self, file_path):
        r'''Converts branches inside of file into a list of tuples
               
                :param ``file_path``: path to a file with the following format (``branch address`` ``actual``)
            
            Output in the following format: Tuple(``branch address``, ``actual``)
        '''

        tem_list = []                               # Temporary list           
        with open(file_path, 'r') as f:
            for b in f.read().splitlines():
                address, actual = b.split(' ')
                tem_list.append( (address, actual) )
        return tem_list



    def __set_state(self, address, actual):
        r'''Set state of pattern history table depending on current actual value

            :param ``address``: pht key to the regarding state
            :param ``actual``: actual jump(1) or no jump(0)
        '''

        state = self.pht[address]

        if actual == "0":                 # no Jump
            state.no_jump()
        if actual == "1":                 # Jump
            state.jump()    
     


    def __update_precision(self, address, actual):
        r'''Calculates the precision rate depending on expected outcome and actual outcome
            
            :param ``address``: Key for pht to current state
            :param ``actual``: Eventual outcome (jump o. no jump) 
        '''

        state = self.pht[address].get_val()                           # State converted to int value from binary

        #TODO: split jump and no jump depending on size_bit
        if(state in [0, 1] and actual == "0"):                          # Expected prediction: no jump
            self.correct+=1
        elif(state in [2, 3] and actual == "1"):                        # Expected prediction: jump
            self.correct+=1

        self.count+=1
        self.precision_rate = self.correct / self.count
        
        
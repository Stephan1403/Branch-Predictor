from State import State
from tqdm import tqdm                                       # For progress bar

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
        self.correct_predictions = 0                            # Count of branches which have been right predicted
        self.precision_rate = 0                                 # Rate of correct predicted branches


# Predictors        
    def local_2_bit_predictor(self, address_size=32):
        r'''Test precision of the local 2 Bit predictor.
        
            :param ``address_size``: set Size of Pattern history table keys in bits (default: 32 bit)
        ''' 

        for key, actual in tqdm(iterable=self.branches, unit="branches" ,colour='green'):       # Iterate through branches, Tqdm is used to show the progress bar
            address = bin(int(key, 16))[-address_size:]                                         # Address: binary value of hexadecimal branch address
            if address not in self.pht:                                                         
                self.pht[address] = State(2)

            state = self.pht[address]                                                           # state is State at the address 'address' in the pattern history table
            self.__update_precision(state, actual)                                              # First update precision the set state
            self.__set_state(state, actual)                                   
             

        print(f"Local 2-Bit Predictor\n-{address_size} bit address size\n-------- Precision rate: {self.precision_rate*100}% --------\n")
        
        
        
    def two_level_global_predictor(self, ghr_size=4):                   #TODO write cleaner
        r'''Test percicion of the two level global predictor

            :param ``ghr_size``: size of gloabl history table in bits (default: 4 Bit)
        
        Each address in the ghr (global history register) address one cell from the pht (pattern history table)
        '''

        self.ghr = State(ghr_size)                                                  # Default = 4 Bit long global history register

        actuals_list = [data[1] for data in self.branches]
        for actual in tqdm(iterable=actuals_list, unit="branches" ,colour='green'): # Iterate throug all 'actual' values
            
            address = self.ghr.get_val(bin=True)
            if address not in self.pht:
                self.pht[address] = State(2)

            state_before_shift = self.pht[address]
            self.__update_precision(state_before_shift, actual)

            self.ghr.left_shift(actual)                                             # Push Actual value (0 or 1) from the right to change ghr value
            state_after_shift = self.pht[address]                                              
            self.__set_state(state_after_shift, actual)
            

        print(f"2-Lvl-Global-Predictor\n-{ghr_size} global history table size\n-------- Precision rate: {self.precision_rate*100}% --------\n")
        


    def gshar_predictor(self, ghr_size=4):
        r'''

        '''

        self.ghr = State(ghr_size)

        for key, actual in tqdm(iterable=self.branches, unit="branches", colour='green'):
            

            self.ghr.left_shift(actual)
 
            address = self.__address_xor_ghr(key)
            if address not in self.pht:
                self.pht[address] = State(2)

            self.__update_precision(address, actual)
            self.__set_state(address, actual)


        print(f"G-share-Predictor\n-{ghr_size} global history table size\n-------- Precision rate: {self.precision_rate*100}% --------\n")


# Functions
    def __set_state(self, state, actual):
        r'''Set state of pattern history table depending on current actual value

            :param ``state``: The state that will be updated
            :param ``actual``: Actual jump(1) or no jump(0)
        '''

        if actual == "0":                 # no Jump
            state.no_jump()
        if actual == "1":                 # Jump
            state.jump()    
     


    def __update_precision(self, state, actual):
        r'''Increase the 
            
            :param ``state``: last State before update (what was expected - jump o. no jump)
            :param ``actual``: Eventual outcome (jump o. no jump) 
        '''

        state_val = state.get_val()

        #TODO: split jump and no jump depending on size_bit
        if(state_val in [0, 1] and actual == "0"):                          # Expected prediction: no jump
            self.correct_predictions+=1
        elif(state_val in [2, 3] and actual == "1"):                        # Expected prediction: jump
            self.correct_predictions+=1

        self.count+=1
        self.precision_rate = self.correct_predictions / self.count



    def __address_xor_ghr(self, address):
        r'''XOR a given address with ghr (The length will be the size of ghr)

            :param ``address``: Hexadecimal address
            :param ``ghr``: binary value of global history table
        
        '''

        address_str = str( int(address, 16) )[:-self.ghr.size_bit]                      # Convert and cut address to the correct length
        return int(address_str) ^ self.ghr.get_val()                                    # Return XOR of address and ghr 



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

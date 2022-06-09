from State import State

# TODO: introduce variable that represents the used predictor (to show what corret_rate is for)

class PredictionTester:
    r'''Prediction Tester is used to test different branch prediction methods
    
            :param ``file_path``: path to file containing branches and their jump results
            

        > Predictors:
            - ``local_2_bit_predictor``
            - ``lorem ipsum``
            - ``lorem ipsum``
    '''

    def __init__(self, file_path) -> None:
        self.pht = {}                                           # Pattern history table containing states
        self.branches = self.__branch_file_to_list(file_path)   # List of tuples with addresses and jumps

        self.count = 0                                          # All branches of last predictor             
        self.correct = 0                                        # Count of branches which have been right predicted
        self.precision_rate = 0                                 # Rate of correct predicted branches


# Predictors        
    def local_2_bit_predictor(self, address_size=32):                            # TODO: Using async to await the result and show a loading bar in the meantime
        r'''Test precision of the local 2 Bit predictor
        
            :param ``address_size``: set Size of Pattern history table keys in bits (default: 32 bit)
        ''' 
        
        for key, jump in self.branches:
            address = bin(int(key, 16))[-address_size:]         # address: binary value of old hexadecimal branch address
            if address not in self.pht:
                self.pht[address] = State(2)                    # Create new dictonary entry, if key doesn't exist


            self.__set_state(address, jump)
            self.__update_precision(address, jump)  

                                                
        print(f"Precision rate: {self.precision_rate*100}%")
        
        
    async def two_level_global_predictor():
        r'''Test percicion of the two level global predictor'''


# Functions
    def __branch_file_to_list(self, file_path):
        r'''Converts branches inside of file into a list of tuples
               
                :param ``file_path``: path to a file with the following format (``branch address`` ``jump``)
            
            Output in the following format: Tuple(``branch address``, ``jump``)
        '''

        tem_list = []                               # Temporary list           
        with open(file_path, 'r') as f:
            for b in f.read().splitlines():
                address, jump = b.split(' ')
                tem_list.append( (address, jump) )
        return tem_list

    def __set_state(self, address, jump):
        r'''Set state depending on jump value

            :param ``address``: Key for pht to current state
            :param ``jump``: a integer value of either 0 or 1
        '''
        
        state = self.pht[address]

        if jump == "0":                 # no Jump
            state.no_jump()
        if jump == "1":                 # Jump
            state.jump()    
     

    def __update_precision(self, address, jump):
        r'''Calculates the precision rate depending on expected outcome and actual outcome
            
            :param ``address``: Key for pht to current state
            :param ``jump``: Eventaul outcome (jump o. no jump) 
        '''

        state = self.pht[address]

        if(state.value in [0, 1] and jump == "0"):                                    # Expected prediction: no jump
            self.correct+=1
        elif(state.value in [2, 3] and jump == "1"):                                  # Expected prediction: jump
            self.correct+=1 

        self.count+=1
        self.precision_rate = self.correct / self.count
        
        
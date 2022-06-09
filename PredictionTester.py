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
        self.branches = self.__branch_file_to_dic(file_path)

        self.count = 0                                          # All branches of last predictor             
        self.correct = 0                                        # Count of branches which have been right predicted
        self.precision_rate = 0                                 # Rate of correct predicted branches


# Predictors        
    def local_2_bit_predictor(self):                            # TODO: Using async to await the result and show a loading bar in the meantime
        r'''Test precision of the local 2 Bit predictor
        
            :param ``address_size``: set Size of Pattern history table keys in bits (e.g. 10 bit)
        '''   

        for key, jump in self.branches.items():
            if key not in self.pht:                             # Init branch if not done
                self.pht[key] = State()

            self.__update_precision(self.pht[key], jump)   

            state = self.pht[key]                               # Set state
            if jump == '0':                                     # No jump
                self.pht[key].no_jump()
            else:                                               # Jump
                self.pht[key].jump()
                               


    async def two_level_global_predictor():
        r'''Test percicion of the two level global predictor'''


# Functions
    def __branch_file_to_dic(self, file_path):
        r'''Converts branches inside of file into a dictonary

            - Epected format inside file:
                ``b77b5c36`` ``0`` (branch address, jump)
            - Use: ``Key:`` branch address, ``Value:`` jump
        '''

        dic = {}                   
        with open(file_path, 'r') as f:
            for b in f.read().splitlines():
                address, state = b.split(' ')
                dic[address] = state

        return dic


    def __hex_to_bin():
        r'''Convert a hexadecimal number to binary
        
            :param ``num``: a hexadecimal number that should be converted
            :param ``len``: bit length of the binary number (10: takes the 10 least significant bit)
        
        '''

    def __update_precision(self, state, jump):
        r'''Calculates the precision rate
            
            :param ``state:``: Expected prediction for branch
            :param ``jump:`` Eventaul outcome (jump o. no jump) 
        '''

        self.count+=1
        
        if(state in [0, 1]):                                    # Expected prediction: no jump
            if jump == 0: self.correct+=1
        elif(state in [2, 3]):                                  # Expected prediction: jump
            if jump == 1: self.correct+=1        

        self.precision_rate = self.correct / self.count
        
        print(f"Precision rate: {self.precision_rate}%")
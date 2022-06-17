from State import State
from PatternHistoryTable import PatternHistoryTable
from tqdm import tqdm                                       # For progress bar

# TODO: change jump (name) to acutal

# TODO: introduce variable that represents the used predictor (to show what correct_rate is for)

class PredictionTester:
    r'''Prediction Tester is used to test different branch prediction methods
    
    Args:
        :param ``file_path``: path to file containing branches and their actual results
            

    Predictors:
        - ``local_2_bit_predictor``
        - ``lorem ipsum``
        - ``lorem ipsum``

    Usage:
        # TODO: ...    
    '''

    def __init__(self, file_path) -> None:
        self.branches = self.__branch_file_to_list(file_path)   # List of tuples with addresses and actuals

        self.count = 0                                          # All branches of last predictor             
        self.correct_predictions = 0                            # Count of branches which have been right predicted
        self.precision_rate = 0                                 # Rate of correct predicted branches


# Predictors        
    def local_2_bit_predictor(self, address_size=32, state_size=2):
        r'''Test precision of the local 2 Bit predictor.
        
        Args
            :param ``address_size``: Size of address in Pattern history table in Bits
            :param ``state_size``: Size of state in Pattern history table in Bits
        ''' 

        pht = PatternHistoryTable(state_size)

        for key, actual in tqdm(iterable=self.branches, unit="branches" ,colour='green'):       # Iterate through branches, Tqdm is used to show the progress bar
            address = bin(int(key, 16))[-address_size:]                                         # Address: binary value of hexadecimal branch address

            self.__update_precision( pht[address].get_jump_val(), actual )                             # Check if last prediction was correct
            self.__set_state( pht[address], actual )                                          


        print(f"Local 2-Bit Predictor\n-{address_size} bit address size\n-------- Precision rate: {self.precision_rate*100}% --------\n")
        
        
        
    def two_level_global_predictor(self, ghr_size=4, state_size=2):                   #TODO write cleaner
        r'''Test percicion of the two level global predictor

        Args
            :param ``ghr_size``: Bit size of the global history register
            :param ``state_size``: Bit size of states inside pattern history table
        '''

        ghr = State(ghr_size)                        
        pht = PatternHistoryTable(state_size)

        actuals_list = [data[1] for data in self.branches]
        for actual in tqdm(iterable=actuals_list, unit="branches" ,colour='green'): # Iterate throug all 'actual' values


            # Check for correct prediction
            address = ghr.get_val( bin=True )                                                
            self.__update_precision( pht[address].get_jump_val(), actual )                 # Compare state at ghr value with 'acutal' value


            # Update state for the next ghr value
            self.__set_state( pht[address], actual )
            ghr.left_shift( actual )

        print(f"2-Lvl-Global-Predictor\n-{ghr_size} global history table size\n-------- Precision rate: {self.precision_rate*100.0}% --------\n")
        


    def gshare_predictor(self, ghr_size=4, state_size=2):
        r'''Test prediction of share predictor

        Args:
            :param: ``ghr_size``: Bit size of the global history register
            :param ``state_size``: Bit size of states inside pattern history table
        '''

        ghr = State(ghr_size)
        pht = PatternHistoryTable(state_size)

        for key, actual in tqdm(iterable=self.branches, unit="branches", colour='green'):

            address = ghr.xor_address(key)   
                                          
            self.__update_precision( pht[address].get_jump_val(), actual )                  # Compare state at ghr value with 'acutal' value
            self.__set_state( pht[address], actual )

            ghr.left_shift( actual )                                                        # Update global history register


        print(f"G-share-Predictor\n-{ghr_size} global history table size\n-------- Precision rate: {self.precision_rate*100}% --------\n")



    def tournament_predictor(self):
        r''''''


# Functions
    def __set_state(self, state, actual):
        r'''Set state depending on current actual value

        Args:
            :param ``state``: The state that will be updated
            :param ``actual``: Actual jump(1) or no jump(0)
        '''

        if actual == "0":                 # no Jump
            state.no_jump()
        if actual == "1":                 # Jump
            state.jump()    
     


    def __update_precision(self, jump_val, actual):
        r'''Increase the correct_predictions value depending on expected outcome and actual outcome
            
        Args:
            :param ``jump_val``: jump value of state ("no jump" or "jump") - expected outcome
            :param ``actual``: Eventual outcome (0 or 1)                   - acutal outcome
        '''


        #TODO: split jump and no jump depending on size_bit/ handle in State
        if(jump_val == "no jump" and actual == "0"):                          # Expected prediction: no jump
            self.correct_predictions+=1
            #print(f"correct at: {self.count+1}, state_val:{state_val}, actual:{actual} -- correct:{self.correct_predictions}")
        elif(jump_val == "jump" and actual == "1"):                        # Expected prediction: jump
            self.correct_predictions+=1
            #print(f"correct at: {self.count+1}, state_val:{state_val}, actual:{actual} -- correct:{self.correct_predictions}")
        #else:
            #print(f"wrong   at: {self.count+1}, state_val:{state_val}, actual:{actual} ")

        self.count+=1
        self.precision_rate = self.correct_predictions / self.count



    def __branch_file_to_list(self, file_path):
        r'''Converts branches inside of file into a list of tuples

        Args:  
            :param ``file_path``: path to a file with the following format (``branch address`` ``actual``)
            
        Output in the following format: Tuple(``branch address``, ``actual``)
        '''

        tem_list = []                               # Temporary list           
        with open(file_path, 'r') as f:
            for b in f.read().splitlines():
                address, actual = b.split(' ')
                tem_list.append( (address, actual) )
        return tem_list

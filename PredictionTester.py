from Classes.PrecisionStorage import PrecisionStorage
from Classes.PredictionSelecter import PredictionSelecter
from Classes.State import State
from Classes.PatternHistoryTable import PatternHistoryTable
from tqdm import tqdm                                       # For progress bar


# TODO: introduce variable that represents the used predictor (to show what correct_rate is for)

class PredictionTester:
    r'''Prediction Tester is used to test different branch prediction methods
    
    Args:
        :param ``file_path``: path to file containing branches and their actual results
            

    Predictors:
        - ``local_2_bit_predictor``
        - ``two_level_gloabl_predictor``
        - ``gshare_predictor``
        - ``tournament_predictor``

    Usage:
        # TODO: ...    
    '''

    def __init__(self, file_path) -> None:
        self.branches = self.__branch_file_to_list(file_path)   # List of tuples with addresses and actuals
        self.percision_storage_dic = {}                         # Dic with key (used predictor) and a PercisionStorage object


# Predictors        
    def local_2_bit_predictor(self, address_size=32, state_size=2):
        r'''Test precision of the local 2 Bit predictor.
        
        Args
            :param ``address_size``: Size of address in Pattern history table in Bits
            :param ``state_size``: Size of state in Pattern history table in Bits
        ''' 

        pht = PatternHistoryTable(state_size)
        p_storage = self.percision_storage_dic['local'] = PrecisionStorage()                           # Store all correct predictions

        for key, actual in tqdm(iterable=self.branches, unit="branches" ,colour='green'):       # Iterate through branches, Tqdm is used to show the progress bar
            address = bin(int(key, 16))[-address_size:]                                         # Address: binary value of hexadecimal branch address

            p_storage.set_precision( pht[address].get_jump_val(), actual )
            pht[address].set_state(actual)

        p_storage.evaluate()
        
        

    def two_level_global_predictor(self, ghr_size=4, state_size=2):                   #TODO write cleaner
        r'''Test percicion of the two level global predictor

        Args
            :param ``ghr_size``: Bit size of the global history register
            :param ``state_size``: Bit size of states inside pattern history table
        '''

        ghr = State(ghr_size)                        
        pht = PatternHistoryTable(state_size)
        p_storage = self.percision_storage_dic['global'] = PrecisionStorage()

        actuals_list = [data[1] for data in self.branches]
        for actual in tqdm(iterable=actuals_list, unit="branches" ,colour='green'):    # Iterate throug all 'actual' values

            # Check for correct prediction
            address = ghr.get_val( bin=True )   
            p_storage.set_precision( pht[address].get_jump_val(), actual)                                             

            # Update state for the next ghr value
            pht[address].set_state(actual)
            ghr.left_shift(actual)

        p_storage.evaluate()
        


    def gshare_predictor(self, ghr_size=4, state_size=2):
        r'''Test prediction of share predictor

        Args:
            :param: ``ghr_size``: Bit size of the global history register
            :param ``state_size``: Bit size of states inside pattern history table
        '''

        ghr = State(ghr_size)
        pht = PatternHistoryTable(state_size)
        p_storage = self.percision_storage_dic['gshare'] = PrecisionStorage()               # Create a new 

        for key, actual in tqdm(iterable=self.branches, unit="branches", colour='green'):

            # Check for correct prediction
            address = ghr.xor_address(key)   
            p_storage.set_precision( pht[address].get_jump_val(), actual )                

            # Set state
            pht[address].set_state(actual)
            ghr.left_shift(actual)                                                          # Update global history register

        p_storage.evaluate()



    #TODO: allow to use gshare instead of just global ???
    # - alway update ghr, global_pht and local_pht (whatever selected_predictor is)
    # - but only choosen predictor gives value
    def tournament_predictor(self, ghr_size=4, state_size=2):
        r''''''

        ghr = State(ghr_size)                        
        pht = PatternHistoryTable(state_size)
        p_storage = self.percision_storage_dic['global'] = PrecisionStorage()

        actuals_list = [data[1] for data in self.branches]
        for actual in tqdm(iterable=actuals_list, unit="branches" ,colour='green'):    # Iterate throug all 'actual' values

            # Check for correct prediction
            address = ghr.get_val( bin=True )   
            p_storage.set_precision( pht[address].get_jump_val(), actual)                                             

            # Update state for the next ghr value
            pht[address].set_state(actual)
            ghr.left_shift(actual)

        p_storage.evaluate()



        '''
        selected_predictor = PredictionSelecter()
        p_storage = self.percision_storage_dic['tournament'] = PrecisionStorage()

        # Global
        ghr = State(4)
        global_pht = PatternHistoryTable(2)

        # Local
        local_pht = PatternHistoryTable(2)

        for key, actual in tqdm(iterable=self.branches, unit="branches", colour='green'):
            
            # Global
            address_global = ghr.get_val( bin=True )
            global_jump = global_pht[address_global].get_jump_val()

            # Local
            address_local = bin( int(key, 16) )
            local_jump = local_pht[address_local].get_jump_val()

            # Set order of jump values depending on selected_predictor
            selected_jump, other_jump =  self.__set_jumps(selected_predictor[address_local], global_jump, local_jump)

            # Set precision for selected jump and store if the prediction was correct in jump_was_correct
            jump_was_correct = p_storage.set_precision( selected_jump, actual)

            if not jump_was_correct:
                if other_jump == actual:                                     # Check if other predictor would have been correct
                    #self.__switch_local_global( selected_predictor[address_local] )               # Switch from gloabl to lcoal and vice versa
                    pass

            # Set global state + left shift
            global_pht[address_global ].set_state(actual)
            global_pht[address_global].left_shift(actual)

            # Set local state
            local_pht[address_local].set_state(actual)

        '''
        #print(p_storage.count, " ", p_storage.correct_predictions)
        #p_storage.evaluate()


# Functions
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


    def __set_jumps(self, selected_pred, global_jump, local_jump):
        r'''Return global and local jump in the correct order
        
        Args:
            :param ``selected_pred``: Currently selected predictor (global or local)
            :param ``global_jump``: Jump value of the global predictor
            :param ``local_jump`: Jump value of the local predictor
        '''

        if selected_pred == "global":
            return global_jump, local_jump
        else:
            return local_jump, global_jump

        

    def __switch_local_global(self, selected_pred):
        r'''Switch a predictor from local to global and vice versa

        Args:
            :param ``selecteed_pred``: Predictor which contains the value that will be changed
        '''

        if selected_pred == "global":
            selected_pred = "local"
        else:
            selected_pred = "global"
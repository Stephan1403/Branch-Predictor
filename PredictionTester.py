from Classes.PatternHistoryTable import PatternHistoryTable
from Classes.PrecisionStorage import PrecisionStorage
from Classes.PredictionSelecter import PredictionSelecter
from Classes.State import State
from tqdm import tqdm                                       # For progress bar


class PredictionTester:
    '''
    Prediction Tester
    ~~~~~~~~~~~~~~~~~
    
    used to test different branch prediction methods
    
    Args:
        :param ``file_path``: path to file containing branches and their actual results
            

    Predictors:
        - ``local_2_bit_predictor``
        - ``two_level_gloabl_predictor``
        - ``gshare_predictor``
        - ``tournament_predictor``

    Usage:
        >>> pt = PredictionTester('file.txt')  
        >>> pt.local_2_bit_predictor(state_size=4)
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

        print(f"Local-2-bit-predictor: {address_size} Bit address size; {state_size} Bit state size")

        pht = PatternHistoryTable(state_size)
        p_storage = self.percision_storage_dic['local'] = PrecisionStorage()                           # Store all correct predictions

        for key, actual in tqdm(iterable=self.branches, unit="branches" ,colour='green'):       # Iterate through branches, Tqdm is used to show the progress bar
            address = bin( int(key, 16) )[-address_size:]                                         # Address: binary value of hexadecimal branch address

            p_storage.set_precision( pht[address].get_jump_val(), actual )                      # Check for correct prediction
            pht[address].set_state(actual)                                                      # Update State

        p_storage.evaluate()
        
        

    def two_level_global_predictor(self, ghr_size=4, state_size=2):                   #TODO write cleaner
        r'''Test precicion of the two level global predictor

        Args
            :param ``ghr_size``: Bit size of the global history register
            :param ``state_size``: Bit size of states inside pattern history table
        '''

        print(f"Two Level Global Predictor:     {ghr_size} Bit global history register size;    {state_size} Bit state size")

        ghr = State(ghr_size)                        
        pht = PatternHistoryTable(state_size)
        p_storage = self.percision_storage_dic['global'] = PrecisionStorage()

        actuals_list = [data[1] for data in self.branches]
        for actual in tqdm(iterable=actuals_list, unit="branches" ,colour='green'):    # Iterate throug all 'actual' values

            address = ghr.get_val( bin=True ) 

            # Check for correct prediction  
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

        print(f"Gshare Predictor:   {ghr_size} Bit global history register size;    {state_size} Bit state size")

        ghr = State(ghr_size)
        pht = PatternHistoryTable(state_size)
        p_storage = self.percision_storage_dic['gshare'] = PrecisionStorage()               # Create a new 

        for key, actual in tqdm(iterable=self.branches, unit="branches", colour='green'):

            address = ghr.xor_address(key)   

            # Check for correct prediction
            p_storage.set_precision( pht[address].get_jump_val(), actual )                

            # Set state
            pht[address].set_state(actual)
            ghr.left_shift(actual)                                                          # Update global history register

        p_storage.evaluate()



    def tournament_predictor(self, ghr_size=4, state_size=2, address_size=32):
        r'''Test prediction of tournament predictor

        Args:
            :param ``ghr_size``: Bit size of global history register and theirfore the global pht
            :param ``state_size``: Bit size of all states in the pattern history tables
            :param ``address_size``: Bit size of the addresses in the local pattern history table
        '''

        print(f"Tournament Predictor:   {address_size} Bit address size;   {ghr_size} Bit global history register size;     {state_size} Bit state size")

        p_storage = self.percision_storage_dic['tournament'] = PrecisionStorage()
        pred_selecter = PredictionSelecter()

        # Global Declaration
        ghr = State(ghr_size)
        glo_pht = PatternHistoryTable(state_size)                                   # Global Pattern History Table

        # Local Declaration
        loc_pht = PatternHistoryTable(state_size)                                   # Local Pattern History Table


        for key, actual in tqdm(iterable=self.branches, unit="branches" ,colour='green'):
            
            address = bin( int(key, 16) )[-address_size:]
            ghr_val = ghr.get_val( bin=True )

            # Set jump_val_selected pred and second_jump_val depending on the PredictionSelecter
            if pred_selecter[key] == "global":                                      # Global Predictor selected
                jump_val_selected_pred = glo_pht[ghr_val].get_jump_val()
                second_jump_val = loc_pht[address].get_jump_val()
            else:                                                                   # Local Predictor selected
                jump_val_selected_pred = loc_pht[address].get_jump_val()
                second_jump_val = glo_pht[ghr_val].get_jump_val()


            # Update precision and store if the prediction was correct in pred_was_correct
            pred_was_correct = p_storage.set_precision( jump_val_selected_pred, actual)

            # Switch predictors if only the second prediction would have been correct
            if (not pred_was_correct) and second_jump_val == actual:
                pred_selecter.switch_predictor_at(key)


            # Set global state
            glo_pht[ghr_val].set_state(actual)
            ghr.left_shift(actual)

            # Set local state
            loc_pht[address].set_state(actual)


        p_storage.evaluate()


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

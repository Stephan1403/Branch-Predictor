

class PrecisionStorage:
    r'''Stores important information about a Predictor. 
    
    '''

    def __init__(self) -> None:
        self.count = 0                      # Count all branches
        self.correct_predictions = 0        # Count all predictions which were the same as their outcome

        # Lists for graph
        self.precision_rate_history = [0]

    def set_precision(self, jump_val, actual):
        r'''Increase the correct_predictions value depending on expected outcome and actual outcome.
            
        Args:
            :param ``jump_val``: jump value of state ("no jump" or "jump") - expected outcome
            :param ``actual``: Eventual outcome (0 or 1)                   - acutal outcome

        Return True if prediction was correct otherwise false
        '''
        self.count+=1
        

        if(jump_val == actual):                        # Expected prediction is same as outcome
            self.correct_predictions+=1
            self.precision_rate_history.append(self.correct_predictions/self.count*100) # For graph
            return True

        self.precision_rate_history.append(self.correct_predictions/self.count*100)     # For graph
        return False


    def evaluate(self, predictor_type):
        '''Calculate the precision rate for the given predictor
        
        Return history of the precision rate
        '''
        print(f"Precisionrate = {self.correct_predictions/self.count*100}%")

        return self.precision_rate_history



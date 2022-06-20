
class PrecisionStorage:           # TODO: activate analysis - to store further information
    r'''Store important information about one Predictor. 
    
    '''

    def __init__(self) -> None:
        self.count = 0                      # Count all branches
        self.correct_predictions = 0        # Count all predictions who has been as their outcome


    def set_precision(self, jump_val, actual):
        r'''Increase the correct_predictions value depending on expected outcome and actual outcome
            
        Args:
            :param ``jump_val``: jump value of state ("no jump" or "jump") - expected outcome
            :param ``actual``: Eventual outcome (0 or 1)                   - acutal outcome
        '''
        self.count+=1

        if(jump_val == actual):                            # Expected prediction is same as outcome
            self.correct_predictions+=1
            return True

        return False


    def evaluate(self):
        r'''Process all'''
        print(f"-------- Precision rate: {self.correct_predictions/self.count}% --------\n")
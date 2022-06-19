class CorrectPredictionEvaluater:
    def __init__(self) -> None:
        self.count = 0                      # Count all branches
        self.correct_predictions = 0        # Count all predictions who has been as their outcome

    def set_prediction(self, jump_val, actual):
        r'''Increase the correct_predictions value depending on expected outcome and actual outcome
            
        Args:
            :param ``jump_val``: jump value of state ("no jump" or "jump") - expected outcome
            :param ``actual``: Eventual outcome (0 or 1)                   - acutal outcome
        '''
        self.count+=1

        if(jump_val == "no jump" and actual == "0"):                            # Expected prediction: no jump
            self.correct_predictions+=1
            return True
        elif(jump_val == "jump" and actual == "1"):                             # Expected prediction: jump
            self.correct_predictions+=1
            return True

        return False
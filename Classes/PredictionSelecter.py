class PredictionSelecter:
    r'''Dictonary containing the selected predictor for a branch.

    Possible values: 
        - ``"global"`` 
        - ``"local"``

    Args:
        :param ``default_predictor``: The value that will be set when creating a new entry
    '''

    def __init__(self, default_predictor='global') -> None:
        self.predictors = {}
        self.def_predictor = default_predictor


    def switch_predictor_at(self, address):
        '''Switch predictor from global to local and vice versa
        
        Args:
            :param ``address``: address of dic where predictor will be changed
        '''
        pred = self.predictors[address]

        if pred == "global":
            self.predictors[address] = "local"
        else:
            self.predictors[address] = "global"


    def __getitem__(self, key):
        if not key in self.predictors:
            self.predictors[key] = self.def_predictor
        return self.predictors[key]


        

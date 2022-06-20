class PredictionSelecter:
    r'''Choose one of two predictors'''

    def __init__(self, default_predictor='global') -> None:
        self.predictors = {}
        self.def_predictor = default_predictor


    def __getitem__(self, key):
        if not key in self.predictors:
            self.predictors[key] = self.def_predictor
        return self.predictors[key]
        

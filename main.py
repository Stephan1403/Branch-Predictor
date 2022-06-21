from PredictionTester import PredictionTester

if __name__ == "__main__":

    a = PredictionTester('trace_files/trace.txt')
    
    a.tournament_predictor(address_size=10)



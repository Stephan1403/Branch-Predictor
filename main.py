from PredictionTester import PredictionTester

if __name__ == "__main__":


    pr = PredictionTester('trace_files/trace.txt')
    
    pr.local_predictor()
    pr.two_level_global_predictor()
    pr.gshare_predictor()
    pr.tournament_predictor()

    pr.compare_predictors()                             # Compare all predictors that have been tested


    '''
    print("\n")
    pr = PredictionTester('trace_files/trace_gcc.txt')
    pr.local_predictor()
    pr.local_predictor(address_size=10)

    print("\n")
    pr2 = PredictionTester('trace_files/trace.txt')
    pr2.two_level_global_predictor()
    pr.two_level_global_predictor(ghr_size=2)
s
    print("\n")
    pr3 = PredictionTester('trace_files/trace_gcc.txt')
    pr3.gshare_predictor()
    '''
    

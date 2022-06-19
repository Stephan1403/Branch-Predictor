from PredictionTester import PredictionTester

if __name__ == "__main__":

    a = PredictionTester('trace_files/trace_gcc.txt')
    
    a.gshare_predictor(4)

from PredictionTester import PredictionTester
from PatternHistoryTable import PatternHistoryTable

if __name__ == "__main__":

    a = PredictionTester('trace_files/trace_gcc.txt')
    
    a.two_level_global_predictor()

  
  

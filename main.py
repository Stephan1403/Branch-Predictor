from PredictionTester import PredictionTester
from State import State

if __name__ == "__main__":

    a = PredictionTester('trace_files/trace_gcc.txt')
    
    a.gshar_predictor()

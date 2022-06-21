from PredictionTester import PredictionTester
import requests

if __name__ == "__main__":

    a = PredictionTester('trace_files/trace.txt')
    
    a.tournament_predictor(address_size=10)

    a = requests.get

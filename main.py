from PredictionTester import PredictionTester
import requests

if __name__ == "__main__":

    a = PredictionTester('trace_files/trace.txt')

    a.local_2_bit_predictor()
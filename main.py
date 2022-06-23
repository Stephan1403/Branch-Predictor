from PredictionTester import PredictionTester

import matplotlib.pyplot as plt


if __name__ == "__main__":

    print("\n")
    a = PredictionTester('trace_files/trace_gcc.txt')
    a.local_2_bit_predictor()

  
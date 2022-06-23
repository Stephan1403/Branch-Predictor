from PredictionTester import PredictionTester

if __name__ == "__main__":

    print("\n")
    a = PredictionTester('trace_files/trace_gcc.txt')
    a.tournament_predictor(address_size=10)



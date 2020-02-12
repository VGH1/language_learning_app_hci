
"""
A class that saves the prediction received from Matlab PC
"""

class Prediction:
    time = 0 # system's time in milliseconds
    pred = "" # h (hard) or e (easy)
    predClassOne = 0.0 #high cog workload
    predClassTwo = 0.0 #low cog workload
    trueClass = "" # represents the current trial

    """ Constructor """
    def __init__(self, pred, classOne, classTwo):
        self.pred = pred
        self.predClassOne = classOne
        self.predClassTwo = classTwo

def parseString(string):
    '''Parses string and uses Dr. Beste\'s alogrithm to see which prediction is sent'''
    try:
        preds = string.split(";")
        if len(preds) == 3:
            predClassOne = float(preds[1])
            predClassTwo = float(preds[2])
            if (preds[0] == "h" and predClassOne > 50) or (preds[0] == "e" and predClassTwo > 50):
                return Prediction(preds[0], predClassOne, predClassTwo)
            else:
                return Prediction(preds[0], predClassTwo, predClassOne)
    except Exception as e:
        print(e)
        return None

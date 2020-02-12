import time

""" A class that holds all of the predictions that are collected from the Matlab PC """

predictionsList = []
startTime = -1;
currentTrial = "";

"""
 A function that adds a new prediction
"""
def addPred (pred):
    pred.time = int(round(time.time() * 1000))  # Get current time in milliseconds and assign it to pred.time

    if currentTrial == "":
        pred.trueClass = currentTrial;

    predictionsList.append(pred);


"""
A function that returns prediction list
"""
def getPredList():
    return predictionsList

def printPredList():
    if len(predictionsList) > 0:
        print('[')
        for pred in predictionsList:
            print('{} {} {}, '.format(pred.pred, pred.predClassOne, pred.predClassTwo))
        print(']\n')

"""
A function that returns average prediciton for low cognitive workload for a specific window size (By Points).
It starts from the last index till the first one and counts 20 elements from last index
if the list doesn't containt 20 elements then the function returns -1
"""
def getAvgPredLowByPoints(windowSize):
    global predictionsList
    avgPred = 0.0

    if windowSize > len(predictionsList): # if predictionlist size less than window size return -1
        return -1.0

    # Otherwise, return the average of the moving range size
    else:
        stopIndex = len(predictionsList) - windowSize # start from last index and subtract window size to get stop index
        sum = 0
        index = len(predictionsList) -1 # get last index in the list
        while index > stopIndex: # the loop starts from last to first index
            pred = predictionsList[index]
            sum += pred.predClassTwo
            index -= 1

        avgPred = sum/windowSize
    return avgPred

"""
A function that returns average prediciton for high cognitive workload for a specific window size (By Points).
It starts from the last index till the first one and counts 20 elements from last index
if the list doesn't containt 20 elements then the function returns -1
"""
def getAvgPredHighByPoints(windowSize):
    global predictionsList
    avgPred = 0.0

    if windowSize > len(predictionsList):  # if predictionlist size less than window size return -1
        return -1.0

    # Otherwise, return the average of the moving range size
    else:
        stopIndex = len(predictionsList) - windowSize # start from last index and subtract window size to get stop index
        sum = 0
        index = len(predictionsList) -1 # get last index in the list
        while index > stopIndex: # the loop starts from last to first index
            pred = predictionsList[index]
            sum += pred.predClassOne
            index -= 1

        avgPred = sum/windowSize
    return avgPred

"""
A function that returns average prediciton for low cognitive workload for a specific time in seconds.

It first gets the current time in milliseconds then it starts from the last index to the first.
It gets the prediction from the list at each index and gets its time, then it calculates the time difference between
the current time and the precition time (when it was added). If the time diff is less than time window, then the prediction was added between time window.
Continue checking till a time difference greater than time window is found so the loop breaks because it means that this element is older than
time window and all previous elements will also be older.
Example: if element was at index "X" then from 0 to X, all the elements are older because predictions are appended so as index increases,
new elements are added.
"""
def getAvgPredLowByTime(timeWindow):
    global predictionsList
    avgPred = 0.0
    currentTime = int(round(time.time() * 1000))  # Get current time in milliseconds
    count = 1 # counts number of pred calculated in loop because we don't know how many pred would be used in the loop

    stopIndex = 0
    sum = 0
    index = len(predictionsList) -1
    while index > stopIndex:
        pred = predictionsList[index]
        time_diff = (currentTime - pred.time)/1000 # get the difference then convert it to seconds
        if time_diff > timeWindow: # if the difference between the prediction's added time and current time is greater than timeWindow
            break
        sum += pred.predClassTwo
        index -= 1
        count += 1

    avgPred = sum/count
    return avgPred

"""
A function that returns average prediciton for high cognitive workload for a specific time in seconds.

It first gets the current time in milliseconds then it starts from the last index to the first.
It gets the prediction from the list at each index and gets its time, then it calculates the time difference between
the current time and the precition time (when it was added). If the time diff is less than time window, then the prediction was added between time window.
Continue checking till a time difference greater than time window is found so the loop breaks because it means that this element is older than
time window and all previous elements will also be older.
Example: if element was at index "X" then from 0 to X, all the elements are older because predictions are appended so as index increases,
new elements are added.
"""
def getAvgPredHighByTime(timeWindow):
    global predictionsList
    avgPred = 0.0
    currentTime = int(round(time.time() * 1000))  # Get current time in milliseconds
    count = 1 # counts number of pred calculated in loop because we don't know how many pred would be used in the loop

    stopIndex = 0
    sum = 0
    index = len(predictionsList) -1
    while index > stopIndex:
        pred = predictionsList[index]
        time_diff = (currentTime - pred.time)/1000 # get the difference then convert it to seconds
        if time_diff > timeWindow: # if the difference between the prediction's added time and current time is greater than timeWindow
            break
        sum += pred.predClassOne
        index -= 1
        count += 1

    avgPred = sum/count
    return avgPred

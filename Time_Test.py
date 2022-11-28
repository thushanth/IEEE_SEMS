import datetime

start = datetime.time(8, 0, 0)
end = datetime.time(14, 56, 0)
currentTime = datetime.datetime.now().time()

def time_in_range(start, end, current):
    return start <= current <= end

def mainControl():
    while True:
        currentTime = datetime.datetime.now().time()

        if time_in_range(start, end, currentTime) == True:
            print(currentTime)
        else:
            print("false")

mainControl()
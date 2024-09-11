import time
from pandas import isna
from multiprocessing import Process, Manager, Pipe
from category import Category as cat

'''
Class to test a set of codes with the given inputs and expected outputs
funcName is the name of the function to be executed.
'''


class TestQuestion:
    def __init__(self, codes, funcName, inputs, answers):
        self.codes = codes
        self.funcName = funcName
        self.inputs = inputs
        self.answers = answers

        self.resultStatus = None
        self.blankTemplate = ''
        self.extraFunctions = dict()
        self.parentConn, self.childConn = Pipe()

    def start(self):
        self.resultStatus = Manager().list([cat.INIT for i in range(len(self.codes) + 1)])

        for (i, code) in self.codes.items():
            self.testCode(i+1, code)

        return self.writeResults()


    def testCode(self, idx, code):
        print(f'starting: {idx}')

        # check blank
        if self.isBlank(code):
            self.resultStatus[idx] = cat.BLANK

        # check compile
        elif not self.canCompile(code):
            self.resultStatus[idx] = cat.COMPILE_ERROR

        # check function exist
        elif self.isMissingFunction(code):
            self.resultStatus[idx] = cat.MISSING_FUNCTION

        # run function with input
        else:
            result = self.runCode(code)
            self.resultStatus[idx] = result


    def isBlank(self, code):
        return isna(code) or (code == self.blankTemplate)

    def canCompile(self, code):
        try:
            exec(code, globals())
            return True
        except Exception as e:
            return False

    def isMissingFunction(self, code):
        namespace = {}
        exec(code, globals(), namespace)
        return self.funcName not in namespace

    def runCode(self, code):
        for (inp, ans) in zip(self.inputs, self.answers):
            childProcess = Process(
                target = self.runOnce,
                args   = (code, inp, ans))
            childProcess.start()

            startTime = time.time()
            while childProcess.is_alive():
                if (time.time() - startTime) > 40: # 40 seconds limit
                    childProcess.kill()
                    return cat.TLE
                time.sleep(0.4)

            result = self.parentConn.recv()
            if result != cat.PASS:
                return result

        return cat.PASS
        
    def runOnce(self, code, inp, ans):
        self.addFunctions()
        exec(code, globals())

        try:
            out = globals()[self.funcName](*inp)
        except Exception as e:
            self.childConn.send(cat.RUN_ERROR)
            return

        self.childConn.send((cat.PASS, cat.WRONG)[out != ans])


    def writeResults(self):
        fileName = self.funcName + ".csv" 
        outfile = open(fileName, "w")
        outfile.write('index,Correct,Blank,Wrong,CompileErr,RunErr,MissingFunc,TLE,Others\n')

        for i in range(1, len(self.codes) + 1):
            result = self.resultStatus[i]
            line = self.formatLine(i, result)
            outfile.write(line)
        
        outfile.close()
        return fileName

    def formatLine(self, idx, result):
        isCorrect = int(result == cat.PASS)
        isBlank = int(result == cat.BLANK)
        isWrong = int(result == cat.WRONG)
        isCompileErr = int(result == cat.COMPILE_ERROR)
        isRunErr = int(result == cat.RUN_ERROR)
        isMissingFunc = int(result == cat.MISSING_FUNCTION)
        isTLE = int(result == cat.TLE)
        isOthers = int(result == cat.INIT)
        return (f"{idx},{isCorrect},{isBlank},{isWrong},"
              + f"{isCompileErr},{isRunErr},{isMissingFunc},"
              + f"{isTLE},{isOthers}\n")

    def addFunctions(self):
        for (name, func) in self.extraFunctions.items():
            globals()[name] = func

    def setFunctions(self, funcMap): # add helper functions to the environment
        for (name, func) in funcMap.items():
            self.extraFunctions[name] = func

    def setBlankTemplate(self, blankTemplate):
        self.blankTemplate = blankTemplate



        

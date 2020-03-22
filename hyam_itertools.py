#  Suspended and restartable iterator

from datetime import datetime   
import pickle
import os
import sys 
import random

class HyamIterator:
    def __init__(self, options):      
        
        self.options = options  # lists of "test options list"
        self.EOF = 'false'
        
        self.testPos = []   # test parameter position
        self.serializeFile = './_serialize_conditions.pkl' 
        
        self.teststarttime = datetime.now()
        self.testendtime = datetime.now()
        self.testCount = 0 
        
        for list1 in options:
            self.testPos.append(0)  # initialize
    
    #------------------------------------------        
    #  iterator (product iterator)
    #
    def __iter__(self):
        return self
        
    def __next__(self):
        
        if self.EOF == 'true':
            self.testendtime = datetime.now()
            raise StopIteration()  
            
        cnt = 0
        for pos in self.testPos:
            if pos == (len(self.options[cnt]) - 1):
                if cnt == (len(self.options) - 1):
                    self.EOF = 'true'  #  last iterator
                else:
                    cnt += 1
                    continue
            else:
                break
        
        #  make return value
        returnOpt = []
        cnt = 0
        upped = 0
        for pos in self.testPos:
            list = self.options[cnt]
            returnOpt.append( list[pos]  )
            
            if pos == (len(self.options[cnt]) - 1) :
                if upped == 0:
                    self.testPos[cnt] = 0
            else:
                if upped == 0:
                    self.testPos[cnt] +=  1
                    upped = 1
            cnt += 1

        self.testCount += 1
        return returnOpt

    #------------------------------------------        
    #  random (other test)
    def GetRandom(self):
        returnParam = []
        for opt in self.options:
            rand_pos = random.randrange(len(opt))
            returnParam.append( opt[rand_pos] )
            
        self.testCount += 1
        return returnParam

    #------------------------------------------
    def serialize(self):
        with open(self.serializeFile, 'wb') as f:
            f.write(pickle.dumps(self))
    
    def loads(self):
        with open(self.serializeFile, 'rb') as f:
            desirial_object = pickle.loads(f.read())
        return desirial_object

    def resume(self):
        if not os.path.exists(self.serializeFile):
            print('resume file is not found. cannot resume')
            sys.exit()
            
        obj = self.loads()
        self.testPos = obj.testPos
        self.testCount = obj.testCount
        self.options = obj.options
        self.teststarttime = obj.teststarttime
        self.testendtime = obj.testendtime
    #------------------------------------------
    def TestCount(self):
        return self.testCount 
               
    #------------------------------------------
    # infotmation
    def saveExecutingTime(self):
        self.testendtime = datetime.now()
        
    def printTestInfo(self):
        print('# test information')
        print('start=' + str(self.teststarttime) )
        print('end=' + str(self.testendtime) )
        
        print('test count=' + str(self.testCount) )
        
        #  elapsed time
        elapsed = self.testendtime - self.teststarttime
        print('elapsed=' + str(elapsed) )
        
        #  
        total= 1
        for opt in self.options:
            total = total * len(opt)
        print('total=' + str(total))
        
        # estimate total time
        estimate = elapsed * ( total / self.testCount) 
        print('estimated test time=' + str(estimate) )

#---------------------------------------------------
#  test code
if __name__ == "__main__":
    
    o1 = ('a', 'b', 'c')
    o2 = ('1', '2')
    o3 = ('x', 'y')
    
    options = (o1, o2, o3)
    testIter = HyamIterator(options)
    
    for testParam in testIter:
        print( str(testIter.testCount) + " : " + str(testParam) )
        if testIter.testCount > 5:
            break   #  Interrupt
    
    testIter.serialize()
    
    # testIter.printTestInfo()

    print('-- resume --')
    testIter.resume
    
    for testParam in testIter:
         print( str(testIter.testCount) + " : " + str(testParam) )

'''
 Bjoern Annighoefer 2022
 
'''

from ..error import EOQ_ERROR_DOES_NOT_EXIST

class History:
    ''' A class to store the history of a compound command
    
    '''
    
    def __init__(self):
        self.values = []
        self.valueNames = {}
        self.n = 0
        self.nMute = 0
        
#     def Reset(self):
#         self.values = []
#         self.valueNames = {}
#         self.n = 0
        
    def AddValue(self,v,mute:bool,name:str=None):
        self.values.append(v)
        if(name):
            self.valueNames[name] = (self.n,mute,self.nMute)
        self.n += 1
        if(not mute): self.nMute += 1 #build a second index only including muted values
        
    def GetValueByIndex(self,i:int):
        try: 
            return self.values[i]
        except KeyError:
            raise EOQ_ERROR_DOES_NOT_EXIST('History index %d is out of range'%(i))
    
    def GetValueByName(self,n:str):
        try: 
            return self.values[self.valueNames[n][0]]
        except KeyError:
            raise EOQ_ERROR_DOES_NOT_EXIST('History name %s is unknown '%(n))
    
    def GetValueNamesAndIndicies(self):
        valueNames = []
        valueIndicies = []
        for (k,v) in self.valueNames.items():
            if(not v[1]): #is not muted? 
                valueNames.append(k)
                valueIndicies.append(v[2]) #only append the muted index, which is correct for the reduced history
        return (valueNames,valueIndicies)
            
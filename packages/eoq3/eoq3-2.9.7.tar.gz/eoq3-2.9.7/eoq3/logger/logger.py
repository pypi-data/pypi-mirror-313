'''
2019 Bjoern Annighoefer
'''

from typing import List,Callable

class LOG_LEVEL:
    DEBUG =  "debug"
    INFO =   "info"
    WARN =   "warning"
    ERROR =  "error"
    
class DEFAULT_LOGGER_LEVELS:
    L0_SILENT  = []
    L1_ERROR   = [LOG_LEVEL.ERROR]
    L2_WARNING = [LOG_LEVEL.WARN, LOG_LEVEL.ERROR]
    L3_INFO    = [LOG_LEVEL.INFO, LOG_LEVEL.WARN, LOG_LEVEL.ERROR]
    L4_DEBUG   = [LOG_LEVEL.INFO, LOG_LEVEL.WARN, LOG_LEVEL.ERROR, LOG_LEVEL.DEBUG]

class Logger:
    def __init__(self, activeLevels:List[str]=DEFAULT_LOGGER_LEVELS.L2_WARNING):
        self.activeLevels = activeLevels
        
    def ShallLog(self):
        return True
    
    def Log(self, level:str, msg:str):
        if(level in self.activeLevels and self.ShallLog()):
            self._Log(level,msg)
    
    #simple log functions
    
    def Debug(self, msg:str):
        self.Log(LOG_LEVEL.DEBUG, msg)
    
    def Info(self, msg:str):
        self.Log(LOG_LEVEL.INFO, msg)
        
    def Warn(self, msg:str):
        self.Log(LOG_LEVEL.WARN, msg)
        
    def Error(self, msg:str):
        self.Log(LOG_LEVEL.ERROR, msg)
        
    #passive log functions
    
    def PLog(self, level:str, msgFactory:Callable[[],str]):
        '''Passivatable log. Is supposed to have higher waste less
        performance if not used, because msgFactory is only evaluated if
        log level is active'''
        if(level in self.activeLevels and self.ShallLog()):
            try:
                self._Log(level,msgFactory())
            except Exception as e:
                self._Log(level,'ERROR while logging: %s'%str(e))
                
    def PDebug(self,msgFactory:Callable[[],str]):
        self.PLog(LOG_LEVEL.DEBUG, msgFactory)
        
    def PInfo(self,msgFactory:Callable[[],str]):
        self.PLog(LOG_LEVEL.INFO, msgFactory)
        
    def PWarn(self,msgFactory:Callable[[],str]):
        self.PLog(LOG_LEVEL.WARN, msgFactory)
    
    def PError(self,msgFactory:Callable[[],str]):
        self.PLog(LOG_LEVEL.ERROR, msgFactory)
    

    #the following must be overwritten to produce the output
    def _Log(self, level:str, msg:str):
        pass 

        
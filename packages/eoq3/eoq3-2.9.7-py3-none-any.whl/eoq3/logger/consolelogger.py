'''
2019 Bjoern Annighoefer
'''



from .logger import Logger,DEFAULT_LOGGER_LEVELS

class ConsoleLogger(Logger):
    '''A logger printing to the console
    '''
    def __init__(self,activeLevels=DEFAULT_LOGGER_LEVELS.L2_WARNING):
        super().__init__(activeLevels)

        
    #@Override         
    def _Log(self,level,msg):
        print("%s: %s"%(level,msg))
'''
2019 Bjoern Annighoefer
'''

from .logger import Logger

class NoLogger(Logger):
    '''A logger which does nothing
    '''
    def __init__(self):
        super().__init__()
        
    #@Override
    def ShallLog(self):
        return False
    
    
'''
2019 Bjoern Annighoefer
'''

from .logger import Logger,DEFAULT_LOGGER_LEVELS

import os
import logging

class ConsoleAndFileLogger(Logger):
    '''A logger that outputs every thing to the console and dedicated files for each active log level
    '''
    def __init__(self,toConsole=True,toFile=True,logDir='./log',activeLevels=DEFAULT_LOGGER_LEVELS.L2_WARNING):
        super().__init__(activeLevels)
        self.toConsole = toConsole
        self.toFile = toFile
        self.logDir = logDir
        
        self.loggers = {}
        
        if(self.toFile):
            #make sure the
            if(not os.path.isdir(self.logDir)):
                os.makedirs(self.logDir)
            #create native python loggers for each level
            for level in self.activeLevels:
                #init error logger
                logger = logging.getLogger(level)
                logFile = os.path.join(self.logDir,"%s.log"%(level))
                fh = logging.FileHandler(logFile,'w')
                fh.setLevel(logging.INFO)
                formatter = logging.Formatter('%(asctime)s - %(message)s')
                fh.setFormatter(formatter)
                logger.addHandler(fh)
                logger.setLevel(logging.INFO)
                self.loggers[level] = logger
                
    #@Override
    def ShallLog(self):
        return (self.toConsole or self.toFile)
                
    #@Override         
    def _Log(self,level,msg):
        if(self.toConsole):
            print("%s: %s"%(level,msg))
        if(self.toFile):
            self.loggers[level].info(msg)
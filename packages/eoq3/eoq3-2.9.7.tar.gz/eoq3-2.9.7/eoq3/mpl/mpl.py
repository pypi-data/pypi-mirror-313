'''
 Model Persistence Layer (MPL) Interface

 Bjoern Annighoefer 2021
'''
from ..query import Qry, Obj
from ..domain import Domain


class Mpl:
    ''' Definition of a basic MPL interfaces
    
        Any EOQ Model Persistence Layer (MPL) should implement this interfaces
    '''
    
    def Load(self)->None:
        ''' Initializes the persistence locally
        
            Loads stored models and elements from the persistence store, e.g.
            the file system.
        '''
        
        pass
    
    def Connect(self,domain:Domain, target:Qry, featureName:str, sessionId:str, trackDomainChanges:bool=False)->Obj:
        ''' Connects and synchronizes with an domain
        
            Elements from the persistence are transfered into the domain or 
            vice versa. 
            The MPL will listens for model in the domain changes and persist those. 
            
            Args:
                domain: The domain which is the target for the domain
                target: The the element which will become the parent of the MPLs root
                featureName: The feature of the parent where the MPL root is added.
                sessionId: All commands will be executed with this session ID. If track 
                    changes is enabled, make sure that the user related with the session
                    has sufficient rights to observe all events.
                trackDomainChanges: If true the MPL monitors changes in the domain continously
                    and updates the local model accordingly
                    
            Returns:
                The workspace root element
        '''
        pass
    
    def Store(self)->None:
        ''' Persists the actual model state to the permanent store
        
            Forces the MPL to persist the current model to the permanent store, e.g. 
            the in memory content is written to the file system.          
            Store might also be carried out automatically by the MPL while changes occur. 
        '''
        pass
    
    def Close(self)->None:
        '''Gracefully shutting down and cleaning up the persistency
        '''
        pass
    
    
    
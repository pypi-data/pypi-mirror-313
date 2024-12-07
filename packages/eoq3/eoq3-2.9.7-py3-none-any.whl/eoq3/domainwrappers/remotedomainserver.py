'''
 2022 Bjoern Annighoefer
'''
from .serialdomain import SerialDomain

from ..domain import Domain
from ..frame import Frm, FRM_TYPE
from ..serializer import DesCmd, SerCmd, CreateSerializer
from ..command import Cmp, Err
from ..config import Config
from ..error import EOQ_ERROR, EOQ_ERROR_CODES
from ..error import EOQ_ERROR_INVALID_TYPE

class RemoteDomainServer():
    def __init__(self, domain:Domain, shallForwardSerializedCmds:bool, config:Config):
        self.domain = domain
        if(shallForwardSerializedCmds and not isinstance(domain,SerialDomain)):
            raise EOQ_ERROR_INVALID_TYPE('Can only forward serial commands to SerialDomains.')
        self.shallForwardSerializedCmds = shallForwardSerializedCmds
        self.config = config
        self.remoteFrmSerializer = CreateSerializer(config.remoteFrmSerializer)
        self.remoteCmdSerializer = CreateSerializer(config.remoteCmdSerializer)
        self.CmdFrameHandler = self.__ProcesscmdFrameNormal
        #prepare processor of commands
        if(shallForwardSerializedCmds):
            self.CmdFrameHandler = self.__ProcesscmdFrameSerial
    
    def OnSerFrmReceived(self, frmStr:str):
        frm = self.remoteFrmSerializer.DesFrm(frmStr)
        self.OnFrmReceived(frm)
    
    def OnFrmReceived(self, frm:Frm):
        sessionId = frm.sid
        if(FRM_TYPE.CMD == frm.typ):
            resFrm = self.CmdFrameHandler(frm)
            resFrmStr = self.remoteFrmSerializer.SerFrm(resFrm)
            self.SendSerFrm(resFrmStr,sessionId)
        elif(FRM_TYPE.OBS == frm.typ):
            self.domain.Observe(self.__OnDomainEvent, sessionId, sessionId)
        elif(FRM_TYPE.UBS == frm.typ):
            self.domain.Unobserve(self.__OnDomainEvent, sessionId, sessionId)
        else:
            self.logger.Warn("Skipped unexpected frm type: %s"%(frm.typ))

    def __OnDomainEvent(self, evts, context, source)->None:
        #print('Forwarding %d events from the domain for context %s and source %s.'%(len(evts),context,source))
        evtCmd = Cmp(evts) #pack commands in compound
        evtCmdStr = self.remoteCmdSerializer.SerCmd(evtCmd)
        frm = Frm(FRM_TYPE.EVT, 0, self.remoteCmdSerializer.Name(), evtCmdStr, context) #context equals the session id of the receiver. Source can is the session id of the event source4
        frmStr = self.remoteFrmSerializer.SerFrm(frm)
        self.SendSerFrm(frmStr,context)
        
    ### INTERCACE ###
    
    def SendSerFrm(self, frmStr:str, sessionId:str)->None:
        '''Needs to be overwritten by the implementation
        '''
        raise NotImplemented()
    
    
    def __ProcesscmdFrameNormal(self, frm:Frm)->Frm:
        '''returns the result frame, by invoking a normal domain
        '''
        commandId = frm.uid
        serType = frm.ser
        try:
            cmd = DesCmd(serType,frm.dat)
            res = self.domain.RawDo(cmd,frm.sid,frm.roc)
        except EOQ_ERROR as e:
            res = Err(e.code,e.msg)
        except Exception as e:
            res = Err(EOQ_ERROR_CODES.UNKNOWN,str(e))
        resStr = SerCmd(serType,res) #reply with the same serialization
        resFrm = Frm(FRM_TYPE.RES, commandId, serType, resStr, frm.sid)
        return resFrm
    
    def __ProcesscmdFrameSerial(self, frm:Frm)->Frm:
        '''returns the result frame by invoking a serial domain
        '''
        resStr = None
        resSer = None
        try:
            (resStr,resSer) = self.domain.SerRawDo(frm.dat,frm.sid,frm.ser,frm.roc)
        except EOQ_ERROR as e:
            res = Err(e.code,e.msg)
            resStr = self.remoteCmdSerializer.SerCmd(res)
            resSer = self.remoteCmdSerializer.Name()
        except Exception as e:
            res = Err(EOQ_ERROR_CODES.UNKNOWN,str(e))
            resStr = self.remoteCmdSerializer.SerCmd(res)
            resSer = self.remoteCmdSerializer.Name()
        resFrm = Frm(FRM_TYPE.RES, frm.uid, resSer, resStr, frm.sid)
        return resFrm
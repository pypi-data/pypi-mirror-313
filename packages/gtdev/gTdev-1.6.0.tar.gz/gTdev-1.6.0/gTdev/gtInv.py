
from . import gtcurve
from .gtdevCommon import physicalQuantity

class inverter():
    def __init__(self,vin,vout,vdd = 2):
        '''
        vin: list input voltage
        vout: list output voltage
        vdd: work voltage, 2V for default
        '''
        self.vin = vin
        self.vout = vout
        self.vdd = vdd
        
    def __getattribute__(self, __name: str):
        def checkSet(keys,unit,anaFunc):
            if __name in keys:
                if not __name in object.__getattribute__(self,'__dict__'):
                    anaFunc()
                return physicalQuantity(object.__getattribute__(self,__name),unit)
            else:
                return None
        answers = []
        answers.append(checkSet(['Vm'],'V',
                object.__getattribute__(self,"_getVm")))
        answers.append(checkSet(['NMH','NML'],'V',
                object.__getattribute__(self,"_getNoiseMargin")))
        answers.append(checkSet(['hys'],'V',
                object.__getattribute__(self,"_gethys")))
        answers.append(checkSet(['gain'],'',
                object.__getattribute__(self,"_getgain")))
        for ans in answers:
            if ans:
                return ans
        return object.__getattribute__(self,__name)

    def _getCross(self,x,y):
        for i in range(len(x)-1):
            a = x[i]-y[i]
            b = x[i+1] - y[i+1]
            if a*b < 0:
                return x[i] + (x[i+1]-x[i])*a/(a-b)
            elif a == b:
                return (x[i]+x[i+1])/2

    def _getVm(self):
        x,y = gtcurve.noBack(self.vin,self.vout)
        y = gtcurve.smooth(y)
        self.Vm = self._getCross(x,y)
        return self.Vm
    
    def _gethys(self,type=1):
        x = self.vin
        y = self.vout
        x1,x2 = x[:len(x)//2], x[len(x)//2:]
        y1,y2 = list(y[:len(y)//2]), list(y[len(y)//2:])
        x2.reverse()
        y2.reverse()
        if x1==x2 and type:
            self.hyscross1 = self._getCross(x1,y1)
            self.hyscross2 = self._getCross(x2,y2)
            self.hys = abs(self.hyscross2-self.hyscross1)
        else:
            self.hys = gtcurve.findhys(self.vin,self.vout)
        return self.hys
    
    def _getNoiseMargin(self):
        x,y = gtcurve.noBack(self.vin,self.vout)
        y = gtcurve.smooth(y)
        nms = []
        for i in range(len(x)-2):
            d1 = (y[i+1] - y[i])/(x[i+1] - x[i])
            d2 = (y[i+2] - y[i+1])/(x[i+2] - x[i+1])
            if (d1+1) * (d2+1) <= 0:
                nms.append((x[i+1],y[i+1]))
        if len(nms) >= 2:
            hx,hy = nms[0]
            lx,ly = nms[-1]
            self.NMH = abs(hx-ly)
            self.NML = abs(lx-hy)
        else:
            self.NMH = 0
            self.NML = 0
    
    def _getgain(self):
        diff = []
        x, y = gtcurve.noBack(self.vin,self.vout)
        for i in range(len(x)-1):
            diff.append(abs((y[i]-y[i+1])/(x[i]-x[i+1])))
        self.gain = max(diff)
        return self.gain
    
    def listPara(self):
        return [self.Vm.num, self.gain.num, self.hys.num, self.NMH.num, self.NML.num]

    def listParaName(self):
        return ['Vm(V)','gain','hys(V)','NMH(V)','NML(V)']
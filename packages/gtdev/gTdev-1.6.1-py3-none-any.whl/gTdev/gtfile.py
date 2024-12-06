
import os
import numpy as np
import pandas

class curve():
    def __init__(self,x,y,name='',info = {}):
        self.name = name
        self.x = x
        self.y = y
        self.info = info
        self.curve = (self.x,self.y)
    def __str__(self):
        return str(self.curve)
    def cut(self,start,end):
        data = list(zip(self.x,self.y))
        self.x = [d[0] for d in data if d[0]>=start and d[0]<=end]
        self.y = [d[1] for d in data if d[0]>=start and d[0]<=end]

class gtfile():
    def __init__(self,key='.xls',location='./',X_Axis='GateV',Y_Axis="DrainI",Z_Axis='',absY=True,sheetNames=['Data','Append',"Run","Sheet"]):
        self.key=key
        self.location = location
        
        self.X_Axis = X_Axis
        self.Y_Axis = Y_Axis
        self.Z_Axis = Z_Axis

        self.files = set()
        self.sheetNames = sheetNames
        self.curves = []
        
        self.filterFile()
        self.getcurves(absY)

    def filterFile(self):
        for f  in os.listdir(self.location):
            if self.key in f:
                if f.endswith('xlsx') or f.endswith('xls') or f.endswith('csv'):
                    self.files.add(f)
    def cutcurve(self,start,end):
        for curve in self.curves:
            curve.cut(start,end)
    def axis2d(self, df, absY=True):
        try:
            x=list(df[self.X_Axis])
            if absY:
                y=np.abs(list(df[self.Y_Axis]))
            else:
                y=list(df[self.Y_Axis])
            return x,y
        except Exception as e:
            print(e)
            return (None,None)

    def getcurves(self, absY=True):
        for file in self.files:
            dataforms = pandas.read_excel(
                os.path.join(self.location,file),
                sheet_name=None)

            sheets = list(dataforms.keys())
            for sht in sheets:
                if any(n in sht for n in self.sheetNames):
                    x, y = self.axis2d(dataforms[sht],absY)
                    info = {}
                    if self.Z_Axis in dataforms[sht].columns:
                        info['Z'] = list(dataforms[sht][self.Z_Axis])
                    self.curves.append(curve(x,y,sht+'@'+file,info))

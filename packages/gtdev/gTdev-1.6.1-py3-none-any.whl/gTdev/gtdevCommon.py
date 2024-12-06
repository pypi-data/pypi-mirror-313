class physicalQuantity():
    def __init__(self,num,unit):
        self.num = num
        self.unit = unit
    def __str__(self):
        return "{:.4g}{}".format(self.num,self.unit)
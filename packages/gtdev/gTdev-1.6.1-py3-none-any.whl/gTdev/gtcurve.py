
import numpy as np

def smooth(args:list):
    '''
    smooth an input array
    from http://cn.voidcc.com/question/p-siqqkcck-tc.html
    because numpy does not have direct implementation
    '''
    try:
        a=args

        WSZ=5
        # a: NumPy 1-D array containing the data to be smoothed 
        # WSZ: smoothing window size needs, which must be odd number, 
        # as in the original MATLAB implementation 
        out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ  
        r = np.arange(1,WSZ-1,2) 
        start = np.cumsum(a[:WSZ-1])[::2]/r 
        stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1] 
        ans = np.concatenate(( start , out0, stop )) 
        return ans  
    except:
        return args 

def spectral_analysis_get_search(arr,i,step,Cond):
    '''
    # search along a 1d array
    # return an index
    # for region detection etc.
    '''
    try:
        while not Cond(arr[i]):
            i+=step
    except Exception as e:
        i-=step # roll back to return a valid i
    finally:
        ans=i    
    return None if 'ans' not in locals() else ans

def linearOfCurve(x,y,thres=0.8):
    # search the quasi-linear region within a data curve
    # to determine threshold voltage, swing etc...
    # return a range of continuous linear region

    # threshold for linearity detection
    sy=smooth(y)
    yy=np.ediff1d(sy,to_begin=0)/np.ediff1d(x,to_begin=1)
    ayy=abs(yy)
    start=np.argmax(ayy) # find peak first
    Search=spectral_analysis_get_search
    opt={"arr":ayy,"step":1,"i":start,
         "Cond":lambda v,c=ayy[start]*thres: v<=c}

    h=Search(**opt)
    opt['step']=-1
    l=Search(**opt)
    region=list(range(l,h))
    return region


def linearFit(xdata,ydata):
    '''
    input(xdata:list,ydata:list)
    try to fit the input fit object using linear model
    fit function y = bx - a
    return: (a:float,b:float)
    '''
    import numpy as np
    from scipy.optimize import curve_fit

    def fitFunc(x, a, b):
        #import numpy as np
        return b*x-a
    p0 = [1,0.1]
    fitParams, fitCovariances = curve_fit(fitFunc, xdata, ydata, p0)
    return fitParams

def noBack(x,y):
    '''
    input(x,y)
    output(x,y)
    Delete Backline。
    '''
    if len(x)<2:
        return x,y
    tag = x[0] > x[1]
    t = len(x)
    for i in range(len(x)-1):
        if (x[i] > x[i+1])!=tag:
            t=i
            break
    return x[0:t],y[0:t]

def findhys(x,y,type = 0):
    '''
    type 0: 算数平均值
    type 1: 几何平均值
    '''
            
    cross = []
    for i in range(len(x)-1):
        ref = (np.max(y) + np.min(y))/2 if type == 0 else np.sqrt(np.max(y) * np.min(y))
        if (y[i]>=ref and y[i+1]<ref) or (y[i]<=ref and y[i+1]>ref):
            cross.append(x[i]+(x[i+1]-x[i])*np.abs(y[i]-ref)/np.abs(y[i+1]-y[i]))
    if len(cross)>1:
        return np.max(cross)-np.min(cross)
    else: 
        return 0
    
def nfSmooth(args):
    # 试分析噪声
    # 平滑数据, n=9,o=2
    y=args
    import scipy as sp
    try:
        ans=sp.signal.savgol_filter(y,9,2)
    except AttributeError:
        #有时没包括signal
        import scipy.signal as ss
        ans=ss.savgol_filter(y,9,2)
    return ans

def nfRmseData(nfSeq,nfFit,iPts=4):
    # 获取rmse序列
    import numpy as np

    iLen=len(nfSeq)

    nfRem=nfSeq-nfFit

    #临近取点，边上的点不取
    res=nfRem.copy()
    for i,v in enumerate(nfRem):
        if i<iPts:
            nfRes=nfRem[0:i+iPts]
        elif i+iPts>=iLen:
            nfRes=nfRem[i-iPts:-1]
        else:
            nfRes=nfRem[i-iPts:i+iPts]
        #计算均方值
        res[i]=np.sqrt(np.mean(nfRes**2))
    ans=res
    return ans

def linth(args):
    #算出symlogy所适合的阈值
    # https://matplotlib.org/stable/tutorials/pyplot.html
    import numpy as np
    data=args #输入为enumerable一些数

    faData=abs(np.array(data))

    faDataSorted=sorted(faData) #从小到大排的序
    #print(faDataSorted)

    if faDataSorted[0]==0:
        fMin=faDataSorted[1]
    else:
        fMin=faDataSorted[0]
        
    #取个整
    import numpy as np
    fLogLevel=int(np.log10(fMin))+1

    linthresh=10**fLogLevel
    #print(f'自动将Symlog阈值设为{linthresh}')
    ans=linthresh
    return ans

def wicNoise(data,fComplianceA=0.99e-2,dataOnly = False):

    nfSmoothed=nfSmooth(data)
    nfRmse=nfRmseData(nfSeq=data,nfFit=nfSmoothed)

    lValid=(abs(np.array(data))<fComplianceA)
    fNoiseFloor=min(nfRmse[lValid])

    #画一下
    if not dataOnly:
        mesg=f'得到噪底：{"{:.4e}".format(fNoiseFloor)}'
        print(mesg)
        import matplotlib.pyplot as plt

        plt.subplot(211)
        plt.title('Calculated Floor: '+"{:.4e}".format(fNoiseFloor))
        plt.plot(data,'+',label='Data')
        plt.plot(nfSmoothed,label='Smoothed')

        linthresh=linth(data)

        plt.yscale('symlog',linthresh=linthresh)
        plt.legend()
        plt.grid(True)

        plt.subplot(212)
        plt.semilogy(nfRmse)
        plt.ylabel('RMSE9',fontsize=20)
        plt.grid(True)

        plt.show()

    return fNoiseFloor
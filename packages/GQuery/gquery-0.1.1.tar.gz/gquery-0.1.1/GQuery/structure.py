import numpy as np
import torch.utils.data as data_utils
from .rfmini import rfmini
import random
from dispCal.disp import calDisp,toQa
from scipy import interpolate
from scipy.signal import resample,convolve
import os 
import sys
from matplotlib import pyplot as plt
#from obspy.taup import TauPyModel
from glob import glob
from h5py import File

from scipy.interpolate import griddata
from scipy.spatial import cKDTree
from scipy.interpolate import RBFInterpolator

def interpolate_with_nan_cleaned(points, values, xi, method='linear', max_distance=np.inf):
    # 移除 points 中含有 NaN 的行以及对应的 values 中的值
    mask = ~np.isnan(values)
    clean_points = points[mask]
    clean_values = values[mask]
    
    # 如果清理后的点为空，则无法进行插值，直接返回 NaN 数组
    if len(clean_points) == 0:
        return np.full_like(xi[:, 0], np.nan)

    # 使用 griddata 进行插值
    #interpolated_values = griddata(clean_points, clean_values, xi, method=method)
    interpolated_values = RBFInterpolator(clean_points, clean_values,smoothing=2,kernel='cubic',neighbors=9)(xi)

    # 构建 KDTree 以便快速计算距离
    tree = cKDTree(clean_points)

    # 对于每个插值点，找到最近的数据点，并计算距离
    distances, _ = tree.query(xi, k=1)
    #return distances*(interpolated_values*0+1)
    # 如果距离超过阈值，设置插值结果为 NaN
    #print(distances,max_distance,np.isnan(interpolated_values).sum())
    #exit()
    interpolated_values[distances > max_distance] = np.nan

    return interpolated_values

def vs2vp(vs,*argv):
    vp=0.9409 + 2.0947*vs - 0.8206*vs**2+ 0.2683*vs**3 - 0.0251*vs**4
    vp[vs<0.01]=1.45
    #vp[vs<2.5] = vs[vs<2.5]*2.0
    #vp[vs<2.8] = vs[vs<2.8]*2.0
    return vp
def vs2vp_mantle1(vs,z):
    vsRemove = removePressure(vs,z)
    vp = vs*1.845
    vp[vsRemove>4.47] = vs[vsRemove>4.47]*1.815
    vp[vsRemove>4.53] = vs[vsRemove>4.53]*1.794
    return vp
def vs2rho_mantle1(vs,z):
    vsRemove = removePressure(vs,z)
    #rho = vs*0.73
    #ratio = vs*0 + 0.73
    ratio = np.where(vsRemove<4.45,-0.4*(vsRemove-4.45)+0.72,0.74+0.24*(vsRemove-4.45))
    return vs*ratio
def decompose(vs,z):
    vsRemove = removePressure(vs,z)
    vp = vs*0
    rho = vs*0
    Q_kappa = vs*0
    Q_mu = vs*0
    vp = np.where(vs<0.25,1.45,vp)
    rho = np.where(vs<0.25,1.02,rho)
    Q_kappa = np.where(vs<0.25,57822.00,Q_kappa)
    Q_kappa = np.where(vs<0.25,57822.00,Q_kappa)
def vp2rho(vp,*argv):
    return 1.6612*vp - 0.4721*vp**2 + 0.0671*vp**3 - 0.0043*vp**4 + 0.000106*vp**5
def vs2rho(vs,*argv):
    vp = vs2vp(vs)
    rho = 1.6612*vp - 0.4721*vp**2 + 0.0671*vp**3 - 0.0043*vp**4 + 0.000106*vp**5
    rho[vs<0.01]=1
    return rho
def removePressure(V,z):
    V = V+0
    bv=3.84e-4
    z0=50
    ZZ=150
    tmp = (1+bv*(z-z0))/(1+bv*(ZZ-z0))
    V0 = V+0
    V/=tmp
    return V
def vs_z2Q_mantle1(vs,z):
    vsRemove = removePressure(vs,z)
    Q_kappa = vs*0+185
    Q_mu = vs*0+76
    Q_kappa[vsRemove>4.61] = 975
    Q_mu[vsRemove>4.61] = 400
    Q_kappa[z>250]=350
    Q_mu[z>250]=135
    return Q_kappa,Q_mu
def deconvtime(source,response,maxIT=200,minErro = 1e-6,dIndex=0):
    sourceSTD = (source**2).sum()**0.5
    source = source/sourceSTD
    response = response/sourceSTD
    N = len(response)
    response = np.concatenate([source*0,response,source*0])
    de = response*0
    for i in range(maxIT):
        cor = np.correlate(response,source,'valid')
        maxIndex = np.argmax(np.abs(cor))
        A = cor[maxIndex]
        de[maxIndex]+=A
        response[maxIndex:maxIndex+len(source)]-=A*source
        if np.abs(A)<minErro:
            break
        #print(A,maxIndex,i)
    return de[dIndex+len(source):dIndex+len(source)+N]#,response
def thickness2depth(*thicknessL):
    z0 = 0
    zL =[]
    for thickness in thicknessL:
        if thickness<-10:
            z0 = -thickness
        elif thickness<0:
            z0 = z0
        else:
            z0 = z0+max(thickness,0)
        zL.append(z0)
    return zL
interp = 'cubic'

paraL0=[
            ['linear',2,1.0,1.5,-0.2,2.0,2.5,2.0,0,2,0],
            [interp ,4,3.2*0.8, 3.3*0.8, 3.6*0.8, 3.7*0.8,25,3.2*1.2,3.3*1.2,3.6*1.2,3.7*1.2,80,0,4,0.],
            [interp ,9,4.3*0.85,4.2*0.85, 4.3*0.85, 4.4*0.85, 4.55*0.85, 4.65*0.85,4.73*0.85,4.8*0.85,4.87*0.85,-425,4.3*1.15,4.2*1.15, 4.3*1.15, 4.4*1.15, 4.55*1.15, 4.65*1.15,4.73*1.15,4.8*1.15,4.87*1.15,-395,0,9,0.2],
            ['linear',2,5.07*0.85, 5.6000*0.85,-690,5.07*1.15, 5.6000*1.15,-640,0,2,0.],
            ['linear',2,5.9500*0.85, 6.3833*0.85,-1000*1.001,5.9500*1.15, 6.3833*1.15,-1000*1.000,0,2,0.]]
paraL0=[
    {'name':'sediment','interp':'linear','velocity_count':2,'velocity_lb':[1.0,1.5],'velocity_ub':[2.0,2.5],'thickness_lb':-1,'thickness_ub':5.0,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':2.5,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':60,'Q_mu_ub':80,'Q_kappa_mu':2.5},
    {'name':'crust','interp':interp,'velocity_count':4,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.6*1.2,3.7*1.2],'thickness_lb':25,'thickness_ub':80,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':400,'Q_mu_ub':700,'Q_kappa_mu':2.5},
     {'name':'mantle1','interp':interp,'velocity_count':9,'velocity_lb':[4.3*0.85,4.2*0.85, 4.3*0.85, 4.4*0.85, 4.55*0.85, 4.65*0.85,4.73*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.3*1.15, 4.4*1.15, 4.55*1.15, 4.65*1.15,4.73*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':9,'maxDecrease':0.2,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':80,'Q_mu_ub':200,'Q_kappa_mu':2.5},
     {'name':'mantle2','interp':'linear','velocity_count':2,'velocity_lb':[5.07*0.85, 5.6000*0.85],'velocity_ub':[5.07*1.15, 5.6000*1.15],'thickness_lb':-690,'thickness_ub':-640,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':150,'Q_mu_ub':160,'Q_kappa_mu':2.5},
     {'name':'mantle3','interp':'linear','velocity_count':2,'velocity_lb':[5.9500*0.85, 6.3833*0.85],'velocity_ub':[5.9500*1.15, 6.3833*1.15],'thickness_lb':-1001,'thickness_ub':-1000,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':450,'Q_mu_ub':550,'Q_kappa_mu':2.5},
]

paraLWide=[
    {'name':'sediment','interp':'linear','velocity_count':2,'velocity_lb':[1.0,1.5],'velocity_ub':[2,2.5],'thickness_lb':-2.5,'thickness_ub':5.0,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':2.0,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':60,'Q_mu_ub':80,'Q_kappa_mu':2.5},
    {'name':'crust','interp':interp,'velocity_count':4,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.6*1.2,3.7*1.2],'thickness_lb':25,'thickness_ub':70,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':700,'Q_kappa_mu':2.5},
     {'name':'mantle1','interp':interp,'velocity_count':9,'velocity_lb':[4.3*0.85,4.2*0.85, 4.3*0.85, 4.4*0.85, 4.55*0.85, 4.65*0.85,4.73*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.3*1.15, 4.4*1.15, 4.55*1.15, 4.65*1.15,4.73*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':9,'maxDecrease':0.2,'PS_ratio_lb':1.7,'PS_ratio_ub':1.85,'RhoS_ratio_lb':0.7,'RhoS_ratio_ub':0.8,'Q_mu_lb':80,'Q_mu_ub':200,'Q_kappa_mu':2.5},
     {'name':'mantle2','interp':'linear','velocity_count':2,'velocity_lb':[5.07*0.85, 5.6000*0.85],'velocity_ub':[5.07*1.15, 5.6000*1.15],'thickness_lb':-690,'thickness_ub':-640,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.70,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.7,'RhoS_ratio_ub':0.85,'Q_mu_lb':150,'Q_mu_ub':160,'Q_kappa_mu':2.5},
     {'name':'mantle3','interp':'linear','velocity_count':2,'velocity_lb':[5.9500*0.85, 6.3833*0.85],'velocity_ub':[5.9500*1.15, 6.3833*1.15],'thickness_lb':-1001,'thickness_ub':-1000,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.7,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':450,'Q_mu_ub':550,'Q_kappa_mu':2.5},
]

paraLShallow=[
    {'name':'sediment0','interp':'linear','velocity_count':4,'velocity_lb':[0.5,0.6,0.7,.8,0.9,1.0,1.1,1.2],'velocity_ub':[1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5],'thickness_lb':-2.5,'thickness_ub':-1,'noDecrease_i0':0,'noDecrease_i1':8,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'sediment1','interp':'linear','velocity_count':4,'velocity_lb':[0.5,0.6,0.7,.8,0.9,1.0,1.1,1.2],'velocity_ub':[1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5],'thickness_lb':-2.5,'thickness_ub':4.0,'noDecrease_i0':0,'noDecrease_i1':8,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':4,'velocity_lb':[3.2*0.8, 3.25*0.8, 3.3*0.8, 3.4*0.8],'velocity_ub':[3.2*1.2,3.25*1.2,3.3*1.2,3.4*1.2],'thickness_lb':10,'thickness_ub':20,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
]
paraLShallow_=[
    {'name':'sediment0','interp':'linear','velocity_count':4,'velocity_lb':[0.5,0.6,0.7,0.8],'velocity_ub':[1.2,1.4,1.6,1.8,],'thickness_lb':-2.5,'thickness_ub':4.0,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'sediment1','interp':'linear','velocity_count':4,'velocity_lb':[0.9,1.0,1.1,1.2],'velocity_ub':[2.0,2.2,2.4,2.6],'thickness_lb':-2.5,'thickness_ub':6.0,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':4,'velocity_lb':[3.2*0.8, 3.25*0.8, 3.3*0.8, 3.4*0.8],'velocity_ub':[3.2*1.2,3.25*1.2,3.3*1.2,3.4*1.2],'thickness_lb':10,'thickness_ub':20,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
]

paraLShallow=[
    {'name':'sediment0','interp':'linear','velocity_count':2,'velocity_lb':[0.1,0.2],'velocity_ub':[0.2,0.3],'thickness_lb':-2.5,'thickness_ub':-1,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'sediment1','interp':interp,'velocity_count':8,'velocity_lb':[0.5,0.6,0.7,.8,0.9,1.0,1.1,1.2],'velocity_ub':[1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4],'thickness_lb':-2.5,'thickness_ub':10.0,'noDecrease_i0':0,'noDecrease_i1':8,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':4,'velocity_lb':[3.2*0.8, 3.25*0.8, 3.3*0.8, 3.4*0.8],'velocity_ub':[3.2*1.2,3.25*1.2,3.3*1.2,3.4*1.2],'thickness_lb':10,'thickness_ub':20,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},]
paraLFunc=[
    {'name':'sediment','interp':'linear','velocity_count':3,'velocity_lb':[0.5,0.75,1.0],'velocity_ub':[2.0,2.25,2.5],'thickness_lb':-6.0,'thickness_ub':6.0,'noDecrease_i0':0,'noDecrease_i1':3,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':6,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.4*0.8,3.5*0.8,3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.4*1.2,3.5*1.2,3.6*1.2,3.7*1.2],'thickness_lb':-70,'thickness_ub':-20,'noDecrease_i0':0,'noDecrease_i1':6,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
     {'name':'mantle1','interp':interp,'velocity_count':12,'velocity_lb':[4.3*0.85,4.2*0.85,4.25*0.85, 4.3*0.85, 4.4*0.85, 4.5*0.85, 4.55*0.85, 4.65*0.85,4.7*0.85,4.75*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.2*1.15,4.25*1.15, 4.4*1.15,4.5*1.15,4.55*1.15,4.65*1.15,4.7*1.15,4.75*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':12,'maxDecrease':0.2,'PS_ratio_lb':1.82,'PS_ratio_ub':1.83,'RhoS_ratio_lb':0.73,'RhoS_ratio_ub':0.75,'Q_mu_lb':80,'Q_mu_ub':200,'Q_kappa_mu':2.5,'vs2Q':vs_z2Q_mantle1,'vs2rho':vs2rho_mantle1,'vs2vp':vs2vp_mantle1},
]

paraLFunc_=[
    {'name':'sediment','interp':'linear','velocity_count':2,'velocity_lb':[0.5,2.0],'velocity_ub':[1.5,2.5],'thickness_lb':-2.5,'thickness_ub':6.0,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':6,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.4*0.8,3.5*0.8,3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.4*1.2,3.5*1.2,3.6*1.2,3.7*1.2],'thickness_lb':-75,'thickness_ub':-20,'noDecrease_i0':0,'noDecrease_i1':6,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
     {'name':'mantle1','interp':interp,'velocity_count':12,'velocity_lb':[4.3*0.85,4.2*0.85,4.25*0.85, 4.3*0.85, 4.4*0.85, 4.5*0.85, 4.55*0.85, 4.65*0.85,4.7*0.85,4.75*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.2*1.15,4.25*1.15, 4.4*1.15,4.5*1.15,4.55*1.15,4.65*1.15,4.7*1.15,4.75*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':12,'maxDecrease':0.2,'PS_ratio_lb':1.82,'PS_ratio_ub':1.83,'RhoS_ratio_lb':0.73,'RhoS_ratio_ub':0.75,'Q_mu_lb':80,'Q_mu_ub':200,'Q_kappa_mu':2.5,'vs2Q':vs_z2Q_mantle1,'vs2rho':vs2rho_mantle1,'vs2vp':vs2vp_mantle1},
]

paraLFunc_=[
    {'name':'water','interp':'linear','velocity_count':2,'velocity_lb':[0.0,0.000001],'velocity_ub':[0.0000001,0.000002],'thickness_lb':-9.9999,'thickness_ub':-0.5,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':2.0,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':lambda x,z:x*0+1.45,'vs2rho':lambda x,z:x*0+1.02,'vs2Q':lambda x,z: [x*0+57822.00,x*0]},
    {'name':'sediment','interp':'linear','velocity_count':2,'velocity_lb':[0.5,2.0],'velocity_ub':[1.5,2.5],'thickness_lb':-2.5,'thickness_ub':6.0,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':1.9,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':6,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.4*0.8,3.5*0.8,3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.4*1.2,3.5*1.2,3.6*1.2,3.7*1.2],'thickness_lb':-75,'thickness_ub':-20,'noDecrease_i0':0,'noDecrease_i1':6,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
     {'name':'mantle1','interp':interp,'velocity_count':12,'velocity_lb':[4.3*0.85,4.2*0.85,4.25*0.85, 4.3*0.85, 4.4*0.85, 4.5*0.85, 4.55*0.85, 4.65*0.85,4.7*0.85,4.75*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.2*1.15,4.25*1.15, 4.4*1.15,4.5*1.15,4.55*1.15,4.65*1.15,4.7*1.15,4.75*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':12,'maxDecrease':0.2,'PS_ratio_lb':1.82,'PS_ratio_ub':1.83,'RhoS_ratio_lb':0.73,'RhoS_ratio_ub':0.75,'Q_mu_lb':80,'Q_mu_ub':200,'Q_kappa_mu':2.5,'vs2Q':vs_z2Q_mantle1,'vs2rho':vs2rho_mantle1,'vs2vp':vs2vp_mantle1},
     {'name':'mantle2','interp':'linear','velocity_count':2,'velocity_lb':[5.07*0.85, 5.6000*0.85],'velocity_ub':[5.07*1.15, 5.6000*1.15],'thickness_lb':-690,'thickness_ub':-640,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.70,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.7,'RhoS_ratio_ub':0.85,'Q_mu_lb':150,'Q_mu_ub':160,'Q_kappa_mu':2.5},
     {'name':'mantle3','interp':'linear','velocity_count':2,'velocity_lb':[5.9500*0.85, 6.3833*0.85],'velocity_ub':[5.9500*1.15, 6.3833*1.15],'thickness_lb':-1001,'thickness_ub':-1000,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.7,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':450,'Q_mu_ub':550,'Q_kappa_mu':2.5},
]

paraLFunc__=[
    {'name':'water','interp':'linear','velocity_count':2,'velocity_lb':[0.0,0.000001],'velocity_ub':[0.0000001,0.000002],'thickness_lb':-9.9999,'thickness_ub':2.5,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':2.0,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':lambda x,z:x*0+1.45,'vs2rho':lambda x,z:x*0+1.02,'vs2Q':lambda x,z: [x*0+57822.00,x*0]},
    {'name':'sediment','interp':'linear','velocity_count':2,'velocity_lb':[0.5,2.0],'velocity_ub':[1.5,2.5],'thickness_lb':-2.5,'thickness_ub':6.0,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':2.0,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':6,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.4*0.8,3.5*0.8,3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.4*1.2,3.5*1.2,3.6*1.2,3.7*1.2],'thickness_lb':25,'thickness_ub':70,'noDecrease_i0':0,'noDecrease_i1':6,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
     {'name':'mantle1','interp':interp,'velocity_count':12,'velocity_lb':[4.3*0.85,4.2*0.85,4.25*0.85, 4.3*0.85, 4.4*0.85, 4.5*0.85, 4.55*0.85, 4.65*0.85,4.7*0.85,4.75*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.2*1.15,4.25*1.15, 4.4*1.15,4.5*1.15,4.55*1.15,4.65*1.15,4.7*1.15,4.75*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':12,'maxDecrease':0.2,'PS_ratio_lb':1.82,'PS_ratio_ub':1.83,'RhoS_ratio_lb':0.73,'RhoS_ratio_ub':0.75,'Q_mu_lb':80,'Q_mu_ub':200,'Q_kappa_mu':2.5,'vs2Q':vs_z2Q_mantle1,'vs2rho':vs2rho_mantle1,'vs2vp':vs2vp_mantle1},
     {'name':'mantle2','interp':'linear','velocity_count':2,'velocity_lb':[5.07*0.85, 5.6000*0.85],'velocity_ub':[5.07*1.15, 5.6000*1.15],'thickness_lb':-690,'thickness_ub':-640,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.70,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.7,'RhoS_ratio_ub':0.85,'Q_mu_lb':150,'Q_mu_ub':160,'Q_kappa_mu':2.5},
     {'name':'mantle3','interp':'linear','velocity_count':2,'velocity_lb':[5.9500*0.85, 6.3833*0.85],'velocity_ub':[5.9500*1.15, 6.3833*1.15],'thickness_lb':-1001,'thickness_ub':-1000,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.7,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':450,'Q_mu_ub':550,'Q_kappa_mu':2.5},
]

paraLFunc_=[
    {'name':'water','interp':'linear','velocity_count':2,'velocity_lb':[0.0,0.000001],'velocity_ub':[0.0000001,0.000002],'thickness_lb':-9.9999,'thickness_ub':2.5,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':2.0,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':lambda x,z:x*0+1.45,'vs2rho':lambda x,z:x*0+1.02,'vs2Q':lambda x,z: [x*0+57822.00,x*0]},
    {'name':'sediment','interp':'linear','velocity_count':2,'velocity_lb':[1.0,1.5],'velocity_ub':[2,2.5],'thickness_lb':-2.5,'thickness_ub':5.0,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':2.0,'PS_ratio_ub':2.1,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.9,'Q_mu_lb':70,'Q_mu_ub':80,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
    {'name':'crust','interp':interp,'velocity_count':4,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.6*1.2,3.7*1.2],'thickness_lb':25,'thickness_ub':70,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.6,'PS_ratio_ub':1.9,'RhoS_ratio_lb':0.65,'RhoS_ratio_ub':0.8,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5,'vs2vp':vs2vp,'vs2rho':vs2rho},
     {'name':'mantle1','interp':interp,'velocity_count':9,'velocity_lb':[4.3*0.85,4.2*0.85, 4.3*0.85, 4.4*0.85, 4.55*0.85, 4.65*0.85,4.73*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.3*1.15, 4.4*1.15, 4.55*1.15, 4.65*1.15,4.73*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':9,'maxDecrease':0.2,'PS_ratio_lb':1.82,'PS_ratio_ub':1.83,'RhoS_ratio_lb':0.73,'RhoS_ratio_ub':0.75,'Q_mu_lb':80,'Q_mu_ub':200,'Q_kappa_mu':2.5,'vs2Q':vs_z2Q_mantle1,'vs2rho':vs2rho_mantle1,'vs2vp':vs2vp_mantle1},
     {'name':'mantle2','interp':'linear','velocity_count':2,'velocity_lb':[5.07*0.85, 5.6000*0.85],'velocity_ub':[5.07*1.15, 5.6000*1.15],'thickness_lb':-690,'thickness_ub':-640,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.70,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.7,'RhoS_ratio_ub':0.85,'Q_mu_lb':150,'Q_mu_ub':160,'Q_kappa_mu':2.5},
     {'name':'mantle3','interp':'linear','velocity_count':2,'velocity_lb':[5.9500*0.85, 6.3833*0.85],'velocity_ub':[5.9500*1.15, 6.3833*1.15],'thickness_lb':-1001,'thickness_ub':-1000,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.7,'PS_ratio_ub':1.8,'RhoS_ratio_lb':0.6,'RhoS_ratio_ub':0.9,'Q_mu_lb':450,'Q_mu_ub':550,'Q_kappa_mu':2.5},
]



paraLSmall=[
    {'name':'sediment','interp':'linear','velocity_count':2,'velocity_lb':[1.0,1.5],'velocity_ub':[2.0,2.5],'thickness_lb':-1.0,'thickness_ub':2.0,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0,'PS_ratio_lb':2.0,'PS_ratio_ub':2.01,'RhoS_ratio_lb':0.79,'RhoS_ratio_ub':0.8,'Q_mu_lb':65,'Q_mu_ub':70,'Q_kappa_mu':2.5},
    {'name':'crust','interp':interp,'velocity_count':4,'velocity_lb':[3.2*0.8, 3.3*0.8, 3.6*0.8, 3.7*0.8],'velocity_ub':[3.2*1.2,3.3*1.2,3.6*1.2,3.7*1.2],'thickness_lb':30,'thickness_ub':60,'noDecrease_i0':0,'noDecrease_i1':4,'maxDecrease':0,'PS_ratio_lb':1.72,'PS_ratio_ub':1.73,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.81,'Q_mu_lb':400,'Q_mu_ub':500,'Q_kappa_mu':2.5},
     {'name':'mantle1','interp':interp,'velocity_count':9,'velocity_lb':[4.3*0.85,4.2*0.85, 4.3*0.85, 4.4*0.85, 4.55*0.85, 4.65*0.85,4.73*0.85,4.8*0.85,4.87*0.85,],'velocity_ub':[4.3*1.15,4.2*1.15, 4.3*1.15, 4.4*1.15, 4.55*1.15, 4.65*1.15,4.73*1.15,4.8*1.15,4.87*1.15],'thickness_lb':-425,'thickness_ub':-395,'noDecrease_i0':0,'noDecrease_i1':9,'maxDecrease':0.125,'PS_ratio_lb':1.70,'PS_ratio_ub':1.75,'RhoS_ratio_lb':0.7,'RhoS_ratio_ub':0.71,'Q_mu_lb':150,'Q_mu_ub':160,'Q_kappa_mu':2.5},
     {'name':'mantle2','interp':'linear','velocity_count':2,'velocity_lb':[5.07*0.85, 5.6000*0.85],'velocity_ub':[5.07*1.15, 5.6000*1.15],'thickness_lb':-690,'thickness_ub':-640,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.75,'PS_ratio_ub':1.76,'RhoS_ratio_lb':0.70,'RhoS_ratio_ub':0.71,'Q_mu_lb':150,'Q_mu_ub':155,'Q_kappa_mu':2.5},
     {'name':'mantle3','interp':'linear','velocity_count':2,'velocity_lb':[5.9500*0.85, 6.3833*0.85],'velocity_ub':[5.9500*1.15, 6.3833*1.15],'thickness_lb':-1001,'thickness_ub':-1000,'noDecrease_i0':0,'noDecrease_i1':2,'maxDecrease':0.,'PS_ratio_lb':1.7,'PS_ratio_ub':1.71,'RhoS_ratio_lb':0.8,'RhoS_ratio_ub':0.81,'Q_mu_lb':450,'Q_mu_ub':500,'Q_kappa_mu':2.5},
]

paraD = {'small':paraLSmall,'wide':paraLWide,'func':paraLFunc,'shallow':paraLShallow}
def rfmini_obs_(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type,G=[],gauss=[]):
    #vs0 = vs0*(1+0.05*2*(np.random.rand()-0.5))
    fp, fsv, qrf = rfmini.synrf(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type)
    slow_P = 1/vp[0]
    slow_S = 1/vs[0]
    ar = 6371
    deg2rad = np.pi/180.0
    p = p/(ar*deg2rad)
    if len(G)>1:
        qrf *= G
    if len(gauss)>1:
        #source= convolve(source, gauss, mode='same')
        qrf= convolve(qrf, gauss, mode='same')
    return fp, fsv,qrf
def rfmini_obs_(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type,G=[],gauss=[]):
    fp, fsv, qrf = rfmini.synrf(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type)
    slow_P = 1/vp[0]
    slow_S = 1/vs[0]
    ar = 6371
    deg2rad = np.pi/180.0
    p = p/(ar*deg2rad)
    thetaP = np.arcsin(p/slow_P)
    thetaS = np.arcsin(p/slow_S)
    if Type == 'P':
        dIndex = int(fp.argmax()-t0*f)
        iL = (np.arange(fp.shape[0])+dIndex)%fp.shape[0]
        
        source = fp
        
        response = fp*np.sin(thetaP-thetaS) + fsv
        #response = fp*np.sin(thetaP) + fsv*np.cos(thetaS)
    else:
        dIndex = int(fsv.argmax()-t0*f)
        iL = (np.arange(fp.shape[0])+dIndex)%fp.shape[0]
        source = fsv
        response = fp+fsv*np.sin(thetaP-thetaS) 
        #response = -fp*np.cos(thetaP) + fsv*np.sin(thetaS)
    if len(G)>1:
        source *= G
        response *= G
    if len(gauss)>1:
        source= convolve(source, gauss, mode='same')
        response= convolve(response, gauss, mode='same')
    rf =response[iL]
    if True:
        dIndex = -int(t0*f)
        #print((source**2).sum()**0.5)
        #exit()
        source = source/(source**2).sum()**0.5/f
        iL = (np.arange(fp.shape[0])+dIndex)%fp.shape[0]
        specSource = np.fft.fft(source)
        A = np.abs(specSource).max()
        wL = 1e-3
        #specSource = 
        specTarget = np.fft.fft(response)
        specDe = np.where(np.abs(specSource)>A*wL,specTarget/specSource,0)
        rf=np.fft.ifft(specDe).real[iL]
    if len(gauss)>1:
        rf= convolve(rf, gauss, mode='same')
    return fp, fsv,rf

def rfmini_obs(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type,G=[],gauss=[],maxIT=50,minErro=1e-4):
    fp, fsv, qrf = rfmini.synrf(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type)
    slow_P = 1/vp[0]
    slow_S = 1/vs[0]
    ar = 6371
    deg2rad = np.pi/180.0
    p = p/(ar*deg2rad)
    thetaP = np.arcsin(p/slow_P)
    thetaS = np.arcsin(p/slow_S)
    if Type == 'P':
        dIndex = int(fp.argmax()-t0*f)
        iL = (np.arange(fp.shape[0])+dIndex)%fp.shape[0]
        
        source = fp*np.cos(thetaP)-fsv*np.sin(thetaS)
        response = fp*np.sin(thetaP)+fsv*np.cos(thetaS)
        #response = fp*np.sin(thetaP) + fsv*np.cos(thetaS)
    else:
        dIndex = int(fsv.argmax()-t0*f)
        iL = (np.arange(fp.shape[0])+dIndex)%fp.shape[0]
        source = fsv*np.cos(thetaS)+fp*np.sin(thetaP)
        response = -fsv*np.sin(thetaS)+fp*np.cos(thetaP)
    if len(G)>1:
        source *= G
        response *= G
    if len(gauss)>1:
        source= convolve(source, gauss, mode='same')
        response= convolve(response, gauss, mode='same')
    rf =response[iL]
    if True:
        dIndex = -int(t0*f)
        #print((source**2).sum()**0.5)
        #exit()
        source = source#/(source**2).sum()**0.5/f
        iL = (np.arange(fp.shape[0])+dIndex)%fp.shape[0]
        #specSource = np.fft.fft(source)
        #A = np.abs(specSource).max()
        #wL = 1e-3
        #specSource = 
        #specTarget = np.fft.fft(response)
        #specDe = np.where(np.abs(specSource)>A*wL,specTarget/specSource,0)
        #rf=np.fft.ifft(specDe).real[iL]
        #print(source)
        rf = deconvtime(source, response,maxIT=maxIT,minErro=minErro,dIndex=dIndex)
    if len(gauss)>1:
        #pass
        rf= convolve(rf, gauss, mode='same')
    return fp, fsv,rf
def rfmini_obs_only(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type,G=[],gauss=[],maxIT=50,minErro=1e-4):
    fp, fsv, qrf = rfmini.synrf(Z, vp, vs, rho, qp, qs,p, lamdata,N, f,t0, vs0, po, Type)
    if len(G)>1:
        qrf *= G
        #qrf *= G
    if len(gauss)>1:
        qrf= convolve(qrf, gauss, mode='same')
        #response= convolve(response, gauss, mode='same')
    rf =qrf
    return fp, fsv,rf



def sphere(A,B,Rho,D,ar,isR=True):
    r0=ar
    log = np.log
    r1 = r0
    LN = len(D)
    D0 = D[LN-1]
    D[LN-1]=0.0
    d = D*0
    a = A*0
    b = B*0
    rho = Rho*0
    for i in range(LN):
        r1 = r0-D[i]
        d[i] = ar*log(ar/r1)-ar*log(ar/r0)
        tmp=(ar+ar)/(r1+r0)
        a[i]=A[i]*tmp
        b[i]=B[i]*tmp
        if isR:
            rho[i]=Rho[i]*tmp**(-2.275)
        else:
            rho[i]=Rho[i]*tmp**(-5)
        r0 =r1
    D[LN-1]=D0

    return r0,a,b,rho,d


class Generator(data_utils.Dataset):
    def __init__ (self,isTest=False,mN=200,paraL=paraLSmall,TN=80,TNG=50,TNE=50,G=[],gauss=[],timeLP=0.1,timeLS=0.1,timeLVDSS=0.1,timeLPDec=0.1,timeLSDec=0.1,timeLVDSSDec=0.1,RF_vp0=-1,RF_kappa=1.73,isZ=True):
        self.TL =(4*40**np.arange(0,1,0.00001)).tolist()
        self.TL =(5*32**np.arange(0,1,0.00001)).tolist()
        self.TL =(8*20**np.arange(0,1,0.00001)).tolist()
        self.TL =(2*80**np.arange(0,1,0.00001)).tolist()
        self.Z = np.arange(0.01,100,0.01).tolist()#(5*20**np.arange(0,1,0.0001)).tolist()#
       
        self.RF_vp0=RF_vp0
        self.RF_kappa=RF_kappa
        self.isZ = isZ
        
        self.thickness = np.array([0.5]*5+[1]*5+[2.5]*10+[5]*10+[10]*10)
        self.thickness = np.array([1]*5+[2]*5+[5]*18+[10]*12+[50]*2+[100]*3)
        self.thickness = np.array([1]*5+[2]*5+[5]*18+[10]*12)
        self.thickness = np.array([0.5]*3+[1]*2+[2]*5+[5]*18+[10]*12+[20]*2+[40]*4)
        self.ZNL = [10,10,10,10,10,10,10,10,10,10,10,10]
        self.ZNL = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]+[5,5,5,5,5,5,5,5,5,5,5,5]
        self.ZL = [
            np.arange(0.000,0.25,0.0001).tolist(),#1
            np.arange(0.25,0.5,0.0001).tolist(),#2
            np.arange(0.5,1.5,0.0001).tolist(),#3
            np.arange(1.5,3.0,0.0001).tolist(),#4
            np.arange(3.0,4.5,0.0001).tolist(),#5
            np.arange(4.5,6.0,0.0001).tolist(),#5
            np.arange(6.0,10.0,0.0001).tolist(),#6
            np.arange(10.0,15,0.0001).tolist(),#6
            np.arange(15,20,0.001).tolist(),#7
            np.arange(20,25,0.001).tolist(),#7
            np.arange(25,30,0.001).tolist(),#8
            np.arange(30,35,0.001).tolist(),#8
            np.arange(35,40,0.001).tolist(),#9
            np.arange(40,45,0.001).tolist(),#9
            np.arange(45,50,0.001).tolist(),#10
            np.arange(50,55,0.001).tolist(),#10
            np.arange(55,60,0.001).tolist(),#11
            np.arange(60,65,0.001).tolist(),#11
            np.arange(65,70,0.001).tolist(),#12
            np.arange(70,75,0.001).tolist(),#12
            np.arange(75,100,0.001).tolist(),#13
            np.arange(100,125,0.001).tolist(),#14
            np.arange(125,150,0.001).tolist(),#15
            np.arange(150,175,0.001).tolist(),#16
            np.arange(175,200,0.001).tolist(),#17
            np.arange(200,225,0.001).tolist(),#18
            np.arange(225,250,0.001).tolist(),#19
            np.arange(250,275,0.001).tolist(),#20
            np.arange(275,300,0.001).tolist(),#21
            np.arange(300,325,0.001).tolist(),#22
            np.arange(325,350,0.001).tolist(),#23
            np.arange(350,375,0.001).tolist()]#24
        #self.thickness = np.array([4]*5+[8]*5+[10]*5)
        self.TN = TN
        self.TNG = TNG
        self.TNE = TNE
        self.N = 2048*160*10
        
        
        self.gauss =gauss #np.exp(-np.arange(-8,8,self.delta)**2/2/self.rfT**2)
        #self.gauss /= np.sum(self.gauss)
        #self.decNRf = 1
        #self.RFN = RFNO//self.decNRf
        
        #G = np.ones(RFNO)
        #G[:RFNO//8] = RFNO//8-np.arange(RFNO//8)
        #G[-RFNO//8:] = np.arange(RFNO//8)
        #G = np.exp(-G**2/(2*(RFNO//32)**2))
        self.G = G
        #self.i0 = self.RFN//12+self.RFN//4
        #self.i1 = -self.RFN//12-self.RFN//4
        #self.i0 =int((0-self.timeLP[0])/self.delta)
        #self.i1 = int((10.1-self.timeLP[0])/self.delta)
        self.timeLP = timeLP
        self.timeLS = timeLS
        self.timeLVDSS = timeLVDSS
        self.timeLPDec = timeLPDec
        self.timeLSDec = timeLSDec 
        self.timeLVDSSDec = timeLVDSSDec 
        self.model = Model(paraL=paraL)
        self.mN = mN
        self.m =[]
        for i in range(self.mN):
            if i%10==0:
                print(i)
            self.m.append(self.model.Generate(walkN=2000))
        self.mIL = np.arange(self.mN).tolist()
        self.isTest = isTest
        #self.taup = TauPyModel(model="prem")
    def __len__(self):
        return self.N
    def diff_(self, index,m,Z0=[],T=[],TE=[],TG=[],pRef=-1,fixP = False,isZ=None):
        inter = 1e-5
        isZ0 = self.isZ
        self.isZ = isZ
        #Z0 = np.array(Z0)
        #Z = Z0+0
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = self.model(m,Z0,self.isZ)
        Z = np.cumsum(thickness)
        Z[1:]=Z[:-1]
        Z[0]=0
        Q_s = Q_mu
        Q_p = toQa(vp,vs,Q_kappa,Q_mu)
        c0 =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='phase', flat_earth=True,ar=6370,dc0=0.005)
        g0 =  calDisp(thickness, vp, vs, rho, TG,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='group', flat_earth=True,ar=6370,dc0=0.005)
        vs0 = vs
        dc = []
        dg = []
        drf = []
        ar =6371
        vpvs = vp[0] / vs[0]
        
        
        poisson = (2 - vpvs**2)/(2 - 2 * vpvs**2)
        slownessP = (ar-Z)*np.pi/180/vp
        SlownessP = slownessP+0
        minSlowP = 1000000
        for i in range(len(slownessP)):
            if slownessP[i]<minSlowP:
                minSlowP = slownessP[i]
            SlownessP[i] = minSlowP
        slownessS = (ar-Z)*np.pi/180/vs
        p = pRef 
        
        fp, fsv, qrf0 = rfmini_obs_only(Z[SlownessP>(p*1.1)], vp[SlownessP>(p*1.1)], vs[SlownessP>(p*1.1)], rho[SlownessP>(p*1.1)], Q_p[SlownessP>(p*1.1)],Q_s[SlownessP>(p*1.1)],p, 4, len(self.timeLP), 1/(self.timeLP[1]-self.timeLP[0]),-self.timeLP[0], vs.astype('float64')[0], poisson, 'P',G=self.G,gauss=self.gauss,maxIT=1000,minErro=1e-9)
        qrfO = qrf0
        
        water_depth, sediment_depth, crust_depth = thickness2depth(water_thickness,sediment_thickness,crust_thickness)
        
        if self.RF_vp0>0:
            slownessP = (ar-Z)*np.pi/180/self.RF_vp0
            slownessS = (ar-Z)*np.pi/180/self.RF_vp0*self.RF_kappa
        else:
            pRef = min(pRef,slownessP[Z<crust_depth].min()-0.05)
        
        thicknessDeg = thickness/(ar*np.pi/180)
        qP = (slownessP**2-p**2)**0.5
        qS = (slownessS**2-p**2)**0.5
        dt = np.sum((thicknessDeg*(qS-qP))[Z<crust_depth])
        
        qPRef = (slownessP**2-pRef**2)**0.5
        qSRef = (slownessS**2-pRef**2)**0.5
        dtRef = np.sum((thicknessDeg*(qSRef-qPRef))[Z<crust_depth])
        
        timeLDec_ref = self.timeLPDec/dtRef*dt
        qrf0 = np.interp( timeLDec_ref,self.timeLP, qrf0, left=0, right=0)
        
        dc =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='kernel', flat_earth=True,ar=6370,dc0=0.005,parameter='vs')
        dg =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='kernelGroup', flat_earth=True,ar=6370,dc0=0.005,parameter='vs')

        for i in range(len(vs)):
            vs = vs0+0
            jN=5
            for j in range(-jN,jN):
                if i+j>=0 and i+j<len(vs):
                    vs[i+j] += inter*np.abs(j)/jN
            #vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = self.model(m,Z0,isZ=self.isZ)
            #c =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='phase', flat_earth=True,ar=6370,dc0=0.005)
            #g =  calDisp(thickness, vp, vs, rho, TG,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='group', flat_earth=True,ar=6370,dc0=0.005)
            fp, fsv, qrf = rfmini_obs_only(Z[SlownessP>(p*1.1)], vp[SlownessP>(p*1.1)], vs[SlownessP>(p*1.1)], rho[SlownessP>(p*1.1)], Q_p[SlownessP>(p*1.1)],Q_s[SlownessP>(p*1.1)],p, 4, len(self.timeLP), 1/(self.timeLP[1]-self.timeLP[0]),-self.timeLP[0], vs.astype('float64')[0], poisson, 'P',G=self.G,gauss=self.gauss,maxIT=1000,minErro=1e-9)
            
            #qrf = qrf-qrfO
            
            timeLDec_ref = self.timeLPDec/dtRef*dt
            qrf = np.interp( timeLDec_ref,self.timeLP, qrf, left=0, right=0)
            
            
            #dc.append((c-c0)/inter)
            #dg.append((g-g0)/inter)
            dqrf = (qrf-qrf0)/inter
            #dqrf = (qrf)/inter
            #dqrf = convolve(qrf, self.gauss, mode='same')
            drf.append(dqrf)
        #dc/=thickness.reshape(-1,1)
        #dg/=thickness.reshape(-1,1)
        #drf/=thickness.reshape(-1,1)
        self.isZ = isZ0
        return np.array(dc)[:,:],np.array(dg)[:,:],np.array(drf)[:,:]
    
    def diff(self, index,m,Z0=[],T=[],TE=[],TG=[],pRef=-1,fixP = False,isZ=None,maxIT=500,minErro=1e-9):
        inter = 1e-8
        isZ0 = self.isZ
        self.isZ = isZ
        #Z0 = np.array(Z0)
        #Z = Z0+0
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = self.model(m,Z0,self.isZ)
        Z = np.cumsum(thickness)
        Z[1:]=Z[:-1]
        Z[0]=0
        Q_s = Q_mu
        Q_p = toQa(vp,vs,Q_kappa,Q_mu)
        c0 =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='phase', flat_earth=True,ar=6370,dc0=0.005)
        g0 =  calDisp(thickness, vp, vs, rho, TG,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='group', flat_earth=True,ar=6370,dc0=0.005)
        vs0 = vs
        dc = []
        dg = []
        drf = []
        ar =6371
        vpvs = vp[0] / vs[0]
        
        
        poisson = (2 - vpvs**2)/(2 - 2 * vpvs**2)
        slownessP = (ar-Z)*np.pi/180/vp
        SlownessP = slownessP+0
        minSlowP = 1000000
        for i in range(len(slownessP)):
            if slownessP[i]<minSlowP:
                minSlowP = slownessP[i]
            SlownessP[i] = minSlowP
        slownessS = (ar-Z)*np.pi/180/vs
        p = pRef 
        
        fp, fsv, qrf0 = rfmini_obs(Z[SlownessP>(p*1.1)], vp[SlownessP>(p*1.1)], vs[SlownessP>(p*1.1)], rho[SlownessP>(p*1.1)], Q_p[SlownessP>(p*1.1)],Q_s[SlownessP>(p*1.1)],p, 4, len(self.timeLP), 1/(self.timeLP[1]-self.timeLP[0]),-self.timeLP[0], vs.astype('float64')[0], poisson, 'P',G=self.G,gauss=self.gauss,maxIT=maxIT,minErro=minErro)
        qrfO = qrf0
        
        water_depth, sediment_depth, crust_depth = thickness2depth(water_thickness,sediment_thickness,crust_thickness)
        
        if self.RF_vp0>0:
            slownessP = (ar-Z)*np.pi/180/self.RF_vp0
            slownessS = (ar-Z)*np.pi/180/self.RF_vp0*self.RF_kappa
        else:
            pRef = min(pRef,slownessP[Z<crust_depth].min()-0.05)
        
        thicknessDeg = thickness/(ar*np.pi/180)
        qP = (slownessP**2-p**2)**0.5
        qS = (slownessS**2-p**2)**0.5
        dt = np.sum((thicknessDeg*(qS-qP))[Z<crust_depth])
        
        qPRef = (slownessP**2-pRef**2)**0.5
        qSRef = (slownessS**2-pRef**2)**0.5
        dtRef = np.sum((thicknessDeg*(qSRef-qPRef))[Z<crust_depth])
        
        timeLDec_ref = self.timeLPDec/dtRef*dt
        qrf0 = np.interp( timeLDec_ref,self.timeLP, qrf0, left=0, right=0)
        
        dc =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='kernel', flat_earth=True,ar=6370,dc0=0.005,parameter='vs')
        dg =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='kernelGroup', flat_earth=True,ar=6370,dc0=0.005,parameter='vs')

        vs0 = vs
        m0 = m
        dvs = []
        for i in range(len(m)):
            m = m0+0
            m[i] += inter
            
            vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = self.model(m,Z0,self.isZ)
            Q_s = Q_mu
            Q_p = toQa(vp,vs,Q_kappa,Q_mu)
            fp, fsv, qrf = rfmini_obs(Z[SlownessP>(p*1.1)], vp[SlownessP>(p*1.1)], vs[SlownessP>(p*1.1)], rho[SlownessP>(p*1.1)], Q_p[SlownessP>(p*1.1)],Q_s[SlownessP>(p*1.1)],p, 4, len(self.timeLP), 1/(self.timeLP[1]-self.timeLP[0]),-self.timeLP[0], vs.astype('float64')[0], poisson, 'P',G=self.G,gauss=self.gauss,maxIT=maxIT,minErro=minErro)
            
            #qrf = qrf-qrfO
            dvsTmp =(vs-vs0)/inter
            if np.abs(dvsTmp).max()==0:
                continue
            timeLDec_ref = self.timeLPDec/dtRef*dt
            qrf = np.interp( timeLDec_ref,self.timeLP, qrf, left=0, right=0)
            
            
            #dc.append((c-c0)/inter)
            #dg.append((g-g0)/inter)
            dqrf = (qrf-qrf0)/inter
            #dqrf = (qrf)/inter
            #dqrf = convolve(qrf, self.gauss, mode='same')
            drf.append(dqrf)
            dvs.append((vs-vs0)/inter)
        #dc=np.array(dc)[:,:,0]
        #dg=np.array(dg)[:,:,0]
        drf=np.array(drf)[:,:]
        dvs = np.array(dvs).T
        ##print(dvs.shape)
        MTM=dvs.T@dvs
        print(MTM.shape)
        M=np.linalg.inv(dvs.T@dvs)@dvs.T
        #dc = (dc.T@M).T
        #dg = (dg.T@M).T
        drf = (drf.T@M).T
        self.isZ = isZ0
        return np.array(dc)[:,:],np.array(dg)[:,:],np.array(drf)[:,:]
    def diff_(self, index,m,Z0=[],isZ=False,**kwags):
        inter = 1e-6
        m0 = np.array(m)
        T,c,TG,g,TE,e,Z,vs,qrf,timeL,qrfS,timeLS,qrfVDSS,timeLVDSS,water_thickness,para_water_thickness,sediment_thickness,para_sediment_thickness,crust_thickness,para_crust_thickness,weight,kappa=self.__getitem__(index,m=m,Z0=Z0,**kwags)
        #dc = []
        #dg = []
        drf = []
        dvs = []
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness = self.model(m ,Z0,isZ=isZ)
        Q_s = Q_mu
        Q_p = toQa(vp,vs,Q_kappa,Q_mu)
        dc =  calDisp(thickness, vp, vs, rho, T[:,0],Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='kernel', flat_earth=True,ar=6370,dc0=0.005,parameter='vs')
        dg =  calDisp(thickness, vp, vs, rho, T[:,0],Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='kernelGroup', flat_earth=True,ar=6370,dc0=0.005,parameter='vs')
        vs0 = vs
        for i in range(len(m)):
            m = m0+0
            m[i] += inter
            T,c1,TG,g1,TE,e1,Z,vs,qrf1,timeL,qrfS,timeLS,qrfVDSS,timeLVDSS,water_thickness,para_water_thickness,sediment_thickness,para_sediment_thickness,crust_thickness,para_crust_thickness,weight,kappa=self.__getitem__(index,m=m,Z0=Z0,**kwags)
            vp0,vs,rho0,thickness0,Q_mu0,Q_kappa0,water_thickness,sediment_thickness,crust_thickness = self.model(m ,Z0,isZ=isZ)
            dvsTmp =(vs-vs0)/inter
            if np.abs(dvsTmp).max()==0:
                continue
            #dc.append((c1-c)/inter)
            #dg.append((g1-g)/inter)
            drf.append((qrf1-qrf)/inter)
            dvs.append((vs-vs0)/inter)
        #dc=np.array(dc)[:,:,0]
        #dg=np.array(dg)[:,:,0]
        drf=np.array(drf)[:,:,0]
        dvs = np.array(dvs).T
        ##print(dvs.shape)
        MTM=dvs.T@dvs
        print(MTM.shape)
        M=np.linalg.inv(dvs.T@dvs)@dvs.T
        #dc = (dc.T@M).T
        #dg = (dg.T@M).T
        drf = (drf.T@M).T
        return dc,dg,drf
    def __getitem__(self, index,m=[],Z0=[],T=[],TE=[],TG=[],pRef=-1,fixP = False,maxIT=50,minErro=1e-4):
        isZ = self.isZ
        if len(T)==0:
            T = random.sample(self.TL,self.TN)
            T.sort()
            T = np.array(T)
        if len(TG)==0:
            TG = random.sample(self.TL,self.TNG)
            TG.sort()
            TG = np.array(TG)
        if len(TE)==0:
            TE = random.sample(self.TL,self.TNE)
            TE.sort()
            TE = np.array(TE)
        
        #Z  = np.cumsum(self.thickness*(0.85+np.random.rand(len(self.thickness))*0.3))
        if len(Z0)==0:
            Z0L =[0]
            for i in range(len(self.ZNL)):
                Z0 = random.sample(self.ZL[i],self.ZNL[i])
                #Z0.sort()
                Z0L = Z0L+Z0 
            Z0L.sort()
            #Z0L = [0]+Z0
            Z0 = np.array(Z0L)
        #thickness = Z*0
        #thickness[:-1] = Z[1:]-Z[:-1]
        ar = 6371
        degRad = np.pi/180
        if len(m)==0:
            mI = random.choice(self.mIL)
            for i in range(100):
                self. m[mI] = self.model.walk(self.m[mI])
            m = self.m[mI]
        
        vp0,vs0,rho0,thickness0,Q_mu0,Q_kappa0,water_thickness,sediment_thickness,crust_thickness = self.model(m ,Z0)
        if not isZ:
            vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = self.model(m,Z0,isZ=False)
        else:
            vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = vp0,vs0,rho0,thickness0,Q_mu0,Q_kappa0,water_thickness,sediment_thickness,crust_thickness
        
        water_Z,sediment_Z,crust_Z = thickness2depth(water_thickness,sediment_thickness,crust_thickness)
        
        #Z0 = Z
        Z = np.cumsum(thickness)
        Z[1:]=Z[:-1]
        Z[0]=0
        
        weightZ = vs0*0
        weightZ[np.abs(Z0-water_Z)<0.1] = 1
        weightZ[np.abs(Z0-sediment_Z)<0.5] = 1
        weightZ[np.abs(Z0-crust_Z)<2.5] = 1
        
        Q_p = toQa(vp,vs,Q_kappa,Q_mu)
        Q_s = Q_mu
        crustZ = self.model.getZ(m,'mantle1')
        R = ar-Z
        p_max_vsTmp = R*degRad/vs
        p_max_vs_Now =  10000
        p_max_vs = []
        for p_max in p_max_vsTmp:
            if p_max<p_max_vs_Now:
                p_max_vs_Now = p_max
            p_max_vs.append(p_max_vs_Now+0)
        p_max_vs = np.array(p_max_vs)
        
        p_max_vpTmp = R*degRad/vp
        p_max_vp_Now =  10000
        p_max_vp = []
        for p_max in p_max_vpTmp:
            if p_max<p_max_vp_Now:
                p_max_vp_Now = p_max
            p_max_vp.append(p_max_vp_Now+0)
        p_max_vp = np.array(p_max_vp)
        
        p_max_vp_c = p_max_vp[Z<crustZ-1]
        p_max_vp_m = p_max_vp[Z>crustZ+1]
        
        p_max_vs_c = p_max_vs[Z<crustZ-1]
        p_max_vs_m = p_max_vs[Z>crustZ+1]
        minVs=0.001
        flat_earth = True
        if self.isTest:
            Q_p[:]=1e9
            Q_s[:]=1e9
            flat_earth=False
            minVs = -10
        
        c =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='phase', flat_earth=flat_earth,ar=6370,dc0=0.005)
        g =  calDisp(thickness, vp, vs, rho, TG,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='group', flat_earth=flat_earth,ar=6370,dc0=0.005)
        if vs[0]<minVs:
            e = TE*np.nan
            qrf = self.timeLPDec*np.nan
            qrfS = self.timeLSDec*np.nan
            qrfVDSS = self.timeLVDSSDec*np.nan
            p=0
            s=0
            vdss=0
            
        else:
            e =  calDisp(thickness, vp, vs, rho, TE,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='ellipticity', flat_earth=flat_earth,ar=6370,dc0=0.005)
            vpvs = vp[0] / vs[0]
            poisson = (2 - vpvs**2)/(2 - 2 * vpvs**2)
        
            ar = 6371
            deg2rad = np.pi/180.
            
            
            
            alpha = np.random.rand()
            p=  5.4*alpha+(1-alpha)*8.3
            if pRef<0:
                pRef = 0.06*111.32*(1+0.1*(np.random.rand()-0.5))
            
            slownessP = (ar-Z)*np.pi/180/vp
            SlownessP = slownessP+0
            minSlowP = 1000000
            for i in range(len(slownessP)):
                if slownessP[i]<minSlowP:
                    minSlowP = slownessP[i]
                SlownessP[i] = minSlowP
            slownessS = (ar-Z)*np.pi/180/vs
            water_depth, sediment_depth, crust_depth = thickness2depth(water_thickness,sediment_thickness,crust_thickness)
            p = min(p,SlownessP[Z<crust_depth+50].min()*0.9)
            if fixP:
                p = pRef
                
            fp, fsv, qrf = rfmini_obs(Z[SlownessP>(p*1.1)], vp[SlownessP>(p*1.1)], vs[SlownessP>(p*1.1)], rho[SlownessP>(p*1.1)], Q_p[SlownessP>(p*1.1)],Q_s[SlownessP>(p*1.1)],p, 4, len(self.timeLP), 1/(self.timeLP[1]-self.timeLP[0]),-self.timeLP[0], vs.astype('float64')[0], poisson, 'P',G=self.G,gauss=self.gauss,maxIT=maxIT,minErro=minErro)
            if np.isnan(qrf).sum()>0:
                print(p,slownessP[Z<crust_depth+50].min())
                exit()
            
            
            thicknessDeg = thickness/(ar*np.pi/180)
            
            
            
            pRef = min(pRef,slownessP[Z<crust_depth].min()-0.05)
            
            pTravel_time = (thicknessDeg*slownessP)[Z<=crust_depth+1e-6].sum()
            sTravel_time = (thicknessDeg*slownessS)[Z<=crust_depth+1e-6].sum()
            kappa = sTravel_time/pTravel_time
            
            if self.RF_vp0>0:
                slownessP = (ar-Z)*np.pi/180/self.RF_vp0
                slownessS = (ar-Z)*np.pi/180/self.RF_vp0*self.RF_kappa
            else:
                pRef = min(pRef,slownessP[Z<crust_depth].min()-0.05)
            qP = (slownessP**2-p**2)**0.5
            qS = (slownessS**2-p**2)**0.5
            dt = np.sum((thicknessDeg*(qS-qP))[Z<crust_depth])
            
            qPRef = (slownessP**2-pRef**2)**0.5
            qSRef = (slownessS**2-pRef**2)**0.5
            dtRef = np.sum((thicknessDeg*(qSRef-qPRef))[Z<crust_depth])
            
            timeLDec_ref = self.timeLPDec/dtRef*dt
            qrf = np.interp( timeLDec_ref,self.timeLP, qrf, left=0, right=0)
            
            p=pRef
            
            
            if False:
                p= 5.4*alpha+(1-alpha)*8.3
                #print(a.get_travel_times(source_depth_in_km=10.0, distance_in_degree=80,receiver_depth_in_km=0.0, phase_list=["P"])[0].ray_param/180*3.1415927)
                #fp, fsv, qrf = rfmini_obs(Z[p<p_max_vp*0.9], vp[p<p_max_vp*0.9], vs[p<p_max_vp*0.9], rho[p<p_max_vp*0.9], Q_p[p<p_max_vp],Q_s[p<p_max_vp*0.9],p, 4, len(self.timeLP), 1/(self.timeLP[1]-self.timeLP[0]),-self.timeLP[0], vs.astype('float64')[0], poisson, 'P')
                fp, fsv, qrf = rfmini_obs(Z[Z<200], vp[Z<200], vs[Z<200], rho[Z<200], Q_p[Z<200],Q_s[Z<200],p, 4, len(self.timeLP), 1/(self.timeLP[1]-self.timeLP[0]),-self.timeLP[0], vs.astype('float64')[0], poisson, 'P',G=self.G,gauss=self.gauss)
                #qrf = qrf*self.G
                #qrf= convolve(qrf, self.gauss, mode='same')
                qrf  = resample(qrf, self.RFN)[self.i0:self.i1]
            
            
                alpha = np.random.rand()
                s= 10.5*alpha+(1-alpha)*12.8
                #vTop=ar*deg2rad/s*0.99/vpvs
                #fp, fsv, qrfS = rfmini_obs(Z[s<p_max_vs*0.9], vp[s<p_max_vs*0.9], vs[s<p_max_vs*0.9], rho[s<p_max_vs*0.9], Q_p[s<p_max_vs*0.9],Q_s[s<p_max_vs*0.9],s, 4, len(self.timeLS), 1/(self.timeLS[1]-self.timeLS[0]),-self.timeLS[0], vs.astype('float64')[0], poisson, 'SV')
                fp, fsv, qrfS = rfmini_obs(Z[Z<200], vp[Z<200], vs[Z<200], rho[Z<200], Q_p[Z<200],Q_s[Z<200],s, 4, len(self.timeLS), 1/(self.timeLS[1]-self.timeLS[0]),-self.timeLS[0], vs.astype('float64')[0], poisson, 'SV',G=self.G,gauss=self.gauss)
                #qrfS = qrfS*self.G
                #qrfS= convolve(qrfS, self.gauss, mode='same')
                qrfS  = resample(qrfS, self.RFN)[self.i0:self.i1]
                
                
                vdssMax = p_max_vp_c.min()
                
                vdssMin = p_max_vp_m.max()
                alpha = (np.random.rand()-0.5)*0.2+0.6
                vdss = vdssMin*alpha+vdssMax*(1-alpha)
                
                vdssTop=ar*deg2rad/vdss*0.99/vpvs
                #fp, fsv, qrfVDSS = rfmini_obs(Z[vdss<p_max_vs*0.9], vp[vdss<p_max_vs*0.9], vs[vdss<p_max_vs*0.9], rho[vdss<p_max_vs*0.9], Q_p[vdss<p_max_vs*0.9],Q_s[vdss<p_max_vs*0.9],vdss, 10, len(self.timeLS), 1/(self.timeLVDSS[1]-self.timeLVDSS[0]),-self.timeLVDSS[0], vs.astype('float64')[0], poisson, 'SV')
                fp, fsv, qrfVDSS = rfmini_obs(Z[Z<200], vp[Z<200], vs[Z<200], rho[Z<200], Q_p[Z<200],Q_s[Z<200],vdss, 10, len(self.timeLS), 1/(self.timeLVDSS[1]-self.timeLVDSS[0]),-self.timeLVDSS[0], vs.astype('float64')[0], poisson, 'SV',G=self.G,gauss=self.gauss)
                #qrfVDSS = qrfVDSS*self.G
                #qrfVDSS= convolve(qrfVDSS, self.gauss, mode='same')
                qrfVDSS  = resample(qrfVDSS, self.RFN)[self.i0:self.i1]
            else:
                s=0
                #p=0
                #qrf = self.timeLPDec*np.nan
                qrfS = self.timeLSDec*np.nan
                qrfVDSS = self.timeLVDSSDec*np.nan
                vdss=0
        if self.isTest:
            c1 =  calDisp(thickness, vp, vs, rho**2, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='phase', flat_earth=flat_earth,ar=6370,dc0=0.005)
            g1 =  calDisp(thickness, vp, vs, rho**2, TG,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='group', flat_earth=flat_earth,ar=6370,dc0=0.005)
            #print((c1-c)/c*100)
            #print((g1-g)/g*100)
            print(vs[0])
            #exit()
            pd = PhaseDispersion(thickness,vp,vs,rho,dc=0.001)
            pdg = GroupDispersion(thickness,vp,vs,rho,dc=0.001)
            pde = Ellipticity(thickness,vp,vs,rho)
            cT = pd(T, mode=0, wave="rayleigh").velocity
            gT = pdg(TG, mode=0, wave="rayleigh").velocity
            eT = pde(TE, mode=0).ellipticity
            print(np.abs(c-cT).mean(),np.abs(g-gT).mean(),np.abs(e-eT).mean())
            print(np.abs(c-cT).max(),np.abs(g-gT).max(),np.abs(e-eT).max())
        
        
        
        T = T.reshape([-1,1])
        c = c.reshape([-1,1])
        TG = TG.reshape([-1,1])
        g = g.reshape([-1,1])
        TE = TE.reshape([-1,1])
        e = e.reshape([-1,1])
        Z0 = Z0.reshape([-1,1])
        vs0 = vs0.reshape([-1,1])
        weightZ = weightZ.reshape([-1,1])
        
        qrf = qrf.astype(float).reshape([-1,1])
        timeLPDec = self.timeLPDec.reshape([-1,1])
        paraQrf = np.concatenate([timeLPDec,timeLPDec*0+p],axis=1)
        
        qrfS = qrfS.astype(float).reshape([-1,1])
        timeLSDec = self.timeLSDec.reshape([-1,1])
        paraQrfS = np.concatenate([timeLSDec,timeLSDec*0+p],axis=1)
        
        qrfVDSS = qrfVDSS.astype(float).reshape([-1,1])
        timeLVDSSDec = self.timeLVDSSDec.reshape([-1,1])
        paraQrfVDSS = np.concatenate([timeLVDSSDec,timeLVDSSDec*0+vdss],axis=1)
        
        water_thickness = np.array([water_thickness]).reshape([-1,1])
        para_water_thickness = water_thickness*0
        
        sediment_thickness = np.array([sediment_thickness]).reshape([-1,1])
        para_sediment_thickness = sediment_thickness*0
        
        crust_thickness = np.array([crust_thickness]).reshape([-1,1])
        para_crust_thickness = crust_thickness*0
        return T,c,TG,g,TE,e,Z0,vs0,qrf,paraQrf,qrfS,paraQrfS,qrfVDSS,paraQrfVDSS,water_thickness,para_water_thickness,sediment_thickness,para_sediment_thickness,crust_thickness,para_crust_thickness,weightZ,kappa.reshape([-1,1])
        #return T.reshape([-1,1]),c.reshape([-1,1]),TG.reshape([-1,1]),g.reshape([-1,1]),TE.reshape([-1,1]),e.reshape([-1,1]),Z[:self.ZN].reshape([-1,1]),vs0[:self.ZN].reshape([-1,1]),qrf.astype(float).reshape([-1,1]),np.concatenate([self.timeLPDec.reshape([-1,1]),np.concatenate([qrfS.astype(float).reshape([-1,1]),qrfS.reshape([-1,1])*0+s],axis=1),self.timeLSDec.reshape([-1,1]),np.concatenate([qrfVDSS.astype(float).reshape([-1,1]),qrfVDSS.reshape([-1,1])*0+vdss],axis=1),self.timeLVDSSDec.reshape([-1,1])#[:self.decNRf*self.RFN:self.decNRf]
#Christensen & Mooney (1995) in the crust and by Karato (1993)
class Model:
    def __init__(self,paraL=paraLSmall,dense=4.0,layerNameL=[],smooth=0,walkType = 'one',walkSpaceRatio=0.1,minThickness=0.0,minDecrease=-0.12):
        self.paraL = paraL
        self.constraintFuncL=[]
        self.thicknessL = []
        self.dense = dense+0.0
        self.smooth=smooth
        self.layerlNameL = layerNameL
        self.paraNameL = []
        self.minThickness = minThickness
        mCount=0
        IL = []
        for i in range(len(self.paraL)):
            N= paraL[i]['velocity_count']
            i0,i1,maxDecrease=paraL[i]['noDecrease_i0'],paraL[i]['noDecrease_i1'],paraL[i]['maxDecrease']
            layerName = paraL[i]['name']
            if i0>=0:
                iL = np.arange(i0+mCount,i1+mCount).astype('int')
                self.constraintFuncL.append(limitDecreaseIL(maxDecrease,iL))
            for I in range(N):
                self.paraNameL.append('%s_vs_%d'%(layerName,I+1))
            self.paraNameL.append('%s_thickness'%(layerName))
            self.paraNameL.append('%s_kappa'%(layerName))
            self.paraNameL.append('%s_rhovs'%(layerName))
            self.paraNameL.append('%s_Q_mu'%(layerName))
            self.paraL[i]['index']=mCount+0
            if self.paraL[i]['velocity_lb'][0]>0.01:
                self.thicknessL.append(mCount+N)
                IL.append(mCount+0)
                IL.append(mCount+N-1)
            mCount+=N+4
        self.constraintFuncL.append(limitDecreaseIL(minDecrease,IL[:-1]))
        self.constraint_ueq = self.constraintFuncL
        self.lb,self.ub = self.gaveLU()
        self.walkType = walkType
        self.walkerSpace = walkSpaceRatio*(self.ub-self.lb)
        self.n_dim = len(self.lb)
        self.iL = np.arange(self.n_dim).tolist()
    def generate(self):
        a = np.random.rand()
        b = 1-(1-a)*np.random.rand()
        r = np.arange(self.n_dim)/(self.n_dim-1)
        m = a*(1-r)+b*r+0.1*(b-a)*(np.random.rand((self.n_dim))-0.5)
        return self.lb*m+(1-m)*self.ub
    def generate_(self):
        m = np.random.rand((self.n_dim))
        return self.lb*m+(1-m)*self.ub
    def check(self,m):
        if (m>self.ub).sum()+(m<self.lb).sum()>0:
            return False
        for eq in self.constraint_ueq:
            if eq(m)>0:
                return False
        return True
    def Generate(self,walkN=0):
       while True:
           m = self.generate()
           if self.check(m):
               for i in range(walkN):
                   m=self.walk(m)
               return m
    def walk(self,m):
        if self.walkType =='all':
            count = 0
            mul = 1
            N=1
        elif self.walkType =='one':
            count = 0
            mul = 1
            N= 1
        while True:
            indexL = random.sample(self.iL,N)
            mNew = m+0
            mNew[indexL]+=np.random.randn(N)*self.walkerSpace[indexL]*mul
            if self.check(mNew):
                return mNew
            count+=1
    def __call__(self,m,z,isZ=True,ar=-1):
        if len(m.shape)==2:
            Vp  = []
            Vs  = []
            Rho = []
            Thickness   = []
            for i in range(len(m)):
                vp,vs,rho,thickness=self(m[i],z,isZ)
                Vp.append(vp)
                Vs.append(vs)
                Rho.append(rho)
                Thickness.append(thickness)
            return np.array(Vp).transpose(),np.array(Vs).transpose(),np.array(Rho).transpose(),np.array(Thickness).transpose()
        smooth=self.smooth
        paraL = self.paraL
        water_thickness = -1
        sediment_thickness = -1
        crust_thickness = -1 
        if not isZ:
            vsL =[]
            vpL = []
            rhoL = []
            Q_muL = []
            Q_kappaL=[]
            thicknessL=[]
            Z0=0
            for i in range(len(paraL)):
                para = paraL[i]
                method,N,mCount,Q_kappa_mu= paraL[i]['interp'],paraL[i]['velocity_count'],paraL[i]['index'],paraL[i]['Q_kappa_mu']
                Vs = m[mCount:mCount+N]
                Thickness = m[mCount+N]
                PS_ratio = m[mCount+N+1]
                rhoS_ratio = m[mCount+N+2]
                Q_mu = m[mCount+N+3]
                
                if Thickness<=self.minThickness and Thickness>-10:
                    continue
                else:
                    if para['name'] == 'water' :
                        water_thickness = Thickness
                    if para['name'] == 'sediment' :
                        sediment_thickness = Thickness
                    if para['name'] == 'crust' :
                        crust_thickness = Thickness
                if Thickness<-10:
                    Thickness = -Thickness-Z0
                Z = np.arange(N+0.0)/(N-1+0.0)*Thickness
                z = np.arange((N-1+0.0)*self.dense)/(N+0.0-1)/self.dense*Thickness
                thickness = Thickness/(N-1+0.0)/self.dense+z*0
                if method =='linear':
                    vs=interpolate.interp1d(Z,Vs,method)(z+0.0+thickness/2)
                elif method =='cubic':
                    k=3
                    x_renorm=(z+0.0+thickness/2)/Thickness
                    t = np.arange(-k,N+1.0)/(N-k+0.0)
                    t[t<0]=0
                    t[t>1]=1
                    vs=interpolate.splev(x_renorm,(t,Vs,k))
                thicknessL.append(thickness)
                vsL.append(vs)
                if 'vs2vp' in para:
                    vpL.append(para['vs2vp'](vs,Z0+z))
                else:
                    vpL.append(vs*PS_ratio)
                if 'vs2rho' in para:
                    rhoL.append(para['vs2rho'](vs,Z0+z))
                else:
                    rhoL.append(rhoS_ratio*vs)
                if 'vs2Q' in para:
                    Q_kappa,Q_mu =para['vs2Q'](vs,Z0+z)
                else:
                    Q_kappa = Q_kappa_mu*Q_mu
                Q_muL.append(Q_mu+vs*0)
                Q_kappaL.append(Q_kappa+vs*0)
                Z0 =Z0+Thickness
            vs = np.concatenate(vsL)
            Thickness = np.concatenate(thicknessL)
            vp = np.concatenate(vpL)
            rho = np.concatenate(rhoL)
            Q_mu = np.concatenate(Q_muL)
            Q_kappa = np.concatenate(Q_kappaL)
        else:
            Z0 =0
            vs = z*0
            Thickness=z*0
            Thickness[:-1] = z[1:]-z[:-1]
            rho = z*0
            vp = z*0
            Q_mu = z*0
            Q_kappa = z*0
            #z = z+Thickness/2
            for i in range(len(self.paraL)):
                para = self.paraL[i]
                method,N,mCount,Q_kappa_mu= paraL[i]['interp'],paraL[i]['velocity_count'],paraL[i]['index'],paraL[i]['Q_kappa_mu']
                Vs = m[mCount:mCount+N]
                thickness = m[mCount+N]
                PS_ratio = m[mCount+N+1]
                rhoS_ratio = m[mCount+N+2]
                q_mu = m[mCount+N+3]
                #mCount += N+1
                
                
                
                if thickness<=self.minThickness and thickness>-10:
                    continue
                else:
                    if para['name'] == 'water' :
                        water_thickness = thickness
                    if para['name'] == 'sediment' :
                        sediment_thickness = thickness
                    if para['name'] == 'crust' :
                        crust_thickness = thickness
                if thickness<-10:
                    thickness = -thickness-Z0
                
                Z = np.arange(0,1.00000001,1/(N-1))*thickness+Z0
                if method =='linear':
                   vs[(z>=Z[0])*(z<=Z[-1])]=interpolate.interp1d(Z,Vs,method)(z[(z>=Z[0])*(z<=Z[-1])])
                elif method =='cubic':
                    k=3
                    x_renorm=(z[(z>=Z[0])*(z<=Z[-1])]-Z0)/thickness
                    t = np.arange(-k,N+1.0)/(N-k+0.0)
                    t[t<0]=0
                    t[t>1]=1
                    vs[(z>=Z[0])*(z<=Z[-1])]=interpolate.splev(x_renorm,(t,Vs,k))
                
                Vs_tmp = vs[(z>=Z[0])*(z<=Z[-1])]
                if 'vs2vp' in para:
                    vp[(z>=Z[0])*(z<=Z[-1])] =para['vs2vp'](Vs_tmp,z[(z>=Z[0])*(z<=Z[-1])])
                else:
                    vp[(z>=Z[0])*(z<=Z[-1])] = Vs_tmp*PS_ratio
                if 'vs2rho' in para:
                    rho[(z>=Z[0])*(z<=Z[-1])] =para['vs2rho'](Vs_tmp,z[(z>=Z[0])*(z<=Z[-1])])
                else:
                    rho[(z>=Z[0])*(z<=Z[-1])] = Vs_tmp*rhoS_ratio
                if 'vs2Q' in para:
                    Q_kappa[(z>=Z[0])*(z<=Z[-1])],Q_mu[(z>=Z[0])*(z<=Z[-1])]=para['vs2Q'](Vs_tmp,z[(z>=Z[0])*(z<=Z[-1])])
                else:
                    Q_mu[(z>=Z[0])*(z<=Z[-1])] = q_mu
                    Q_kappa[(z>=Z[0])*(z<=Z[-1])] = q_mu*Q_kappa_mu
                Z0=Z[-1]
            vs[z>Z0]=vs[z<=Z0][-1]
        if ar>0:
            return *sphere(vp,vs,rho,Thickness,ar=ar)[1:],Q_mu,Q_kappa
        return vp,vs,rho,Thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness
    def calPQ(self,vs,z,*thicknessL,isL=False):
        Z0 =0
        Thickness=z*0
        Thickness[:-1] = z[1:]-z[:-1]
        rho = z*0
        vp = z*0
        Q_mu = z*0
        Q_kappa = z*0
        #z = z+Thickness/2
        paraL = self.paraL
        if not isL:
            water_thickness,sediment_thickness,crust_thickness = thicknessL
        else:
            water_thickness = -1
            sediment_thickness = -1
            crust_thickness = -1
        if vs[0]<0.25 and vs.max()>0.25 and False:
            water_thickness = z[vs>0.25][0]*0.999
            print(water_thickness)
            #exit()
        if vs[0]<2.75 and vs.max()>2.75 and False:
            sediment_thickness = z[vs>2.75][0]*0.999
            if water_thickness>0:
                sediment_thickness = sediment_thickness-water_thickness
        for i in range(len(self.paraL)):
            para = self.paraL[i]
            method,N,mCount,Q_kappa_mu= paraL[i]['interp'],paraL[i]['velocity_count'],paraL[i]['index'],paraL[i]['Q_kappa_mu']
            PS_ratio = paraL[i]['PS_ratio_lb']/2+paraL[i]['PS_ratio_ub']/2
            rhoS_ratio = paraL[i]['RhoS_ratio_lb']/2+paraL[i]['RhoS_ratio_ub']/2
            q_mu = paraL[i]['Q_mu_lb']/2+paraL[i]['Q_mu_ub']/2
            thickness = paraL[i]['thickness_lb']/2+paraL[i]['thickness_ub']/2
            #mCount += N+1
            
            if isL:
                thickness = thicknessL[i]
            else:
                if para['name'] == 'water' :
                    thickness=water_thickness 
                if para['name'] == 'sediment' :
                    thickness=sediment_thickness  
                if para['name'] == 'crust' :
                    thickness=crust_thickness 
                
            if thickness<=self.minThickness and thickness>-10:
                continue
            elif thickness<-10:
                thickness = -thickness-Z0
            
            Z = np.arange(0,1.00000001,1/(N-1))*thickness+Z0
            Vs_tmp = vs[(z>=Z[0])*(z<=Z[-1])]
            if len(Vs_tmp)==0:
                break
            if 'vs2vp' in para:
                vp[(z>=Z[0])*(z<=Z[-1])] =para['vs2vp'](Vs_tmp,z[(z>=Z[0])*(z<=Z[-1])])
            else:
                vp[(z>=Z[0])*(z<=Z[-1])] = Vs_tmp*PS_ratio
            if 'vs2rho' in para:
                rho[(z>=Z[0])*(z<=Z[-1])] =para['vs2rho'](Vs_tmp,z[(z>=Z[0])*(z<=Z[-1])])
            else:
                rho[(z>=Z[0])*(z<=Z[-1])] = Vs_tmp*rhoS_ratio
            if 'vs2Q' in para:
                Q_kappa[(z>=Z[0])*(z<=Z[-1])],Q_mu[(z>=Z[0])*(z<=Z[-1])]=para['vs2Q'](Vs_tmp,z[(z>=Z[0])*(z<=Z[-1])])
            else:
                Q_mu[(z>=Z[0])*(z<=Z[-1])] = q_mu
                Q_kappa[(z>=Z[0])*(z<=Z[-1])] = q_mu*Q_kappa_mu
            Z0=Z[-1]
        #vs[z>Z0]=vs[z<=Z0][-1]
        return vp,vs,rho,Thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness
    def cal(self,*args,res = 'c',T=[],pRef=[],phase='P',timeL=[],gauss=[],G=[],timeLDec=[],RF_vp0=-1,RF_kappa=1.73,**kwargs):
        vp,vs,rho,Thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness = self.calPQ(*args,**kwargs)
        Q_p = toQa(vp,vs,Q_kappa,Q_mu)
        Q_s = Q_mu
        ar = 6371
        flat_earth = True 
        #if res == 'c':
        if res in ['c','g','e']:
            return calDisp(Thickness, vp, vs, rho, T,Qp=Q_p.astype(np.float64),Qs=Q_s.astype(np.float64),wave='rayleigh', mode=1, velocity={'c':'phase','g':'group','e':'ellipticity'}[res], flat_earth=flat_earth,ar=6370,dc0=0.005)
        elif res == 'rf':
            Z = np.cumsum(Thickness)
            thickness = Thickness
            Z[1:]=Z[:-1]
            Z[0]=0
            vpvs = vp[0] / vs[0]
            poisson = (2 - vpvs**2)/(2 - 2 * vpvs**2)
            alpha = np.random.rand()
            p =  5.4*alpha+(1-alpha)*8.3
            slownessP = (ar-Z)*np.pi/180/vp
            SlownessP = slownessP+0
            minSlowP = 1000000
            for i in range(len(slownessP)):
                if slownessP[i]<minSlowP:
                    minSlowP = slownessP[i]
                SlownessP[i] = minSlowP
            slownessS = (ar-Z)*np.pi/180/vs
            water_depth, sediment_depth, crust_depth = thickness2depth(water_thickness,sediment_thickness,crust_thickness)
            #print(crust_depth,'***')
            crust_depth = max(crust_depth,20)
            #p = min(p,slownessP[Z<crust_depth+50].min()-0.05)
            p = min(p,SlownessP[Z<crust_depth+50].min()*0.9)
            #pRef = min(pRef,slownessP[Z<crust_depth].min()-0.05)
            #print(pRef)
            #exit()
            
            #fp, fsv, qrf = rfmini_obs(Z[Z<crust_depth+50], vp[Z<crust_depth+50], vs[Z<crust_depth+50], rho[Z<crust_depth+50], Q_p[Z<crust_depth+50],Q_s[Z<crust_depth+50],p, 4, len(timeL), 1/(timeL[1]-timeL[0]),-timeL[0], vs.astype('float64')[0], poisson, 'P',G=G,gauss=gauss)
            fp, fsv, qrf = rfmini_obs(Z[SlownessP>(p*1.1)], vp[SlownessP>(p*1.1)], vs[SlownessP>(p*1.1)], rho[SlownessP>(p*1.1)], Q_p[SlownessP>(p*1.1)],Q_s[SlownessP>(p*1.1)],p, 4, len(timeL), 1/(timeL[1]-timeL[0]),-timeL[0], vs.astype('float64')[0], poisson, 'P',G=G,gauss=gauss)
            #slownessP>(p*1.1)
            #qrf  = qrf[i0:i1]
            #timeLPDec = timeL[i0:i1]
            #print(qrf.max(),qrf.min(),timeL.shape)
            thicknessDeg = thickness/(ar*np.pi/180)
        
            #pRef = min(pRef,slownessP[Z<crust_depth].min()-0.05)
            if RF_vp0>0:
                slownessP = (ar-Z)*np.pi/180/RF_vp0
                slownessS = slownessP*RF_kappa
                
            qP = (slownessP**2-p**2)**0.5
            qS = (slownessS**2-p**2)**0.5
            dt = np.sum((thicknessDeg*(qS-qP))[Z<crust_depth])
            
            qPRef = (slownessP**2-pRef**2)**0.5
            qSRef = (slownessS**2-pRef**2)**0.5
            dtRef = np.nansum((thicknessDeg*(qSRef-qPRef))[Z<crust_depth])
            
            timeLDec_ref = timeLDec/dtRef*dt
            #timeLDec_ref = timeLDec*dtRef/dt
            qrf = np.interp( timeLDec_ref,timeL, qrf, left=0, right=0)
            #print(crust_depth,qrf.max(),qrf.min(),timeLDec_ref.max(),timeLDec_ref.min(),timeL.max(),timeL.min(),p,pRef,1/dtRef*dt,'*********')  
            p=pRef
            return qrf
    def getV0(self,m,name = 'crust'):
        mCount=0
        for i in range(len(self.paraL)):
            if self.paraL[i]['name']==name:
                mCount=self.paraL[i]['index']
                return m[mCount:mCount+self.paraL[i]['velocity_count']]
    def getThickness(self,m,name = 'crust'):
        mCount=0
        for i in range(len(self.paraL)):
            if self.paraL[i]['name']==name:
                mCount=self.paraL[i]['index']
                return m[mCount+self.paraL[i]['velocity_count']]
    def diff(self,m,z):
        vp_ori,vs_ori,rho_ori = self(m,z)
        dm = (m*0.001).reshape([-1,1])
        M = m.reshape([1,-1])+dm
        vp,vs,rho = self(M,z)
        return (vp.transpose()-vp_ori.reshape([1,-1]))/dm,(vs.transpose()-vs_ori.reshape([1,-1]))/dm,(rho.transpose()-rho_ori.reshape([1,-1]))/dm,
    def compare(self,m,m0):
        mCount=0
        res = 0
        for i in range(len(self.paraL)):
            method,N= self.paraL[i][:2]
            Vs = m[mCount:mCount+N]
            thickness = m[mCount+N]
            Vs0 = m0[mCount:mCount+N]
            thickness0 = m0[mCount+N]
            mCount += N+1
            if thickness<=0 or thickness0<=0 or Vs[0]<0.01 or Vs0[0]<0.01 :
                continue
            res += (((Vs-Vs0)/(Vs+Vs0)*2)**2).sum()
            res += ((thickness-thickness0)/(thickness+thickness0)*2)**2
        return res
    def gaveLU(self,):
        lb=[]
        ub=[]
        for i in range(len(self.paraL)):
            N= self.paraL[i]['velocity_count']
            lb = lb+ self.paraL[i]['velocity_lb']+[self.paraL[i]['thickness_lb']]+[self.paraL[i]['PS_ratio_lb']]+[self.paraL[i]['RhoS_ratio_lb']]+[self.paraL[i]['Q_mu_lb']]
            ub = ub+ self.paraL[i]['velocity_ub']+[self.paraL[i]['thickness_ub']]+[self.paraL[i]['PS_ratio_ub']]+[self.paraL[i]['RhoS_ratio_ub']]+[self.paraL[i]['Q_mu_ub']]
        return np.array(lb),np.array(ub)  
    def getThicknessL(self,m):
        if len(m.shape)==2:
            return m[:,self.thicknessL].transpose()
        else:
            return  m[self.thicknessL]
    def getZ(self,m,name):
        Z = 0
        for i in range(len(self.paraL)):
            if self.paraL[i]['name']==name:
                return Z
            else:
                N = self.paraL[i]['velocity_count']
                index = self.paraL[i]['index']
                thickness = m[N+index]
                if thickness<=0 and thickness>-10:
                    continue
                elif thickness<-10:
                    Z = thickness
                else:
                    Z += thickness
class limitDecrease:
    def __init__(self,maxDecrease):
        self.maxDecrease = maxDecrease
    def __call__(self,m):
        minM = m+0
        for i in range(len(m)-2,-1,-1):
            minM[i] = min(minM[i+1],m[i])
        return (m-minM-self.maxDecrease>0).sum()
class limitDecreaseIL:
    def __init__(self,maxDecrease,iL):
        self.maxDecrease = maxDecrease
        self.iL=iL
    def __call__(self,m):
        m = m[self.iL]
        #print(self.iL,m)
        minM = m*0+100000000000
        for i in range(len(m)-2,-1,-1):
            minM[i] = min(minM[i+1],m[i+1])
        return (m-minM-self.maxDecrease>0).sum()
class limitContinureIL:
    def __init__(self,maxDecrease,iL):
        self.maxDecrease = maxDecrease
        self.iL=iL
    def __call__(self,m):
        m = m[self.iL]
        minM = m*0+100000000000
        for i in range(len(m)-2,-1,-1):
            minM[i] = min(minM[i+1],m[i+1])
        return (m-minM-self.maxDecrease>0).sum()

def getTL(resDir,pattern = '*.?????',minT=0,maxT=10000):
    periodDirs = glob(resDir+pattern)
    T = [ float(os.path.basename(periodDir)) for periodDir in periodDirs]
    T.sort()
    T = np.array(T)
    T = T[(T>=minT)*(T<=maxT)]
    return T

class DispModel:
    def __init__(self,resDir,minSample=10,withR=False,iso=False,mode='mine',maxT=10000,minT=0) -> None:
        if mode in ['mine','Ordos','OrdosW']:
            vL=[]
            stdL =[]
            samplingL=[]
            RL = []
            SDL = []
            SDL_r  =[]
            vTrueL =[]
            if not iso:
                CL=[]
                SL=[]
                CTrueL=[]
                STrueL=[]
                CstdL =[]
                SstdL =[]
            self.T = getTL(resDir,minT=minT,maxT=maxT)
            for T in self.T:
                periodDir = f'{resDir}/{T:.5f}/'
                if os.path.exists(periodDir+'output_c.txt'):
                    self.la = np.loadtxt(periodDir+'la.txt')
                    self.lo = np.loadtxt(periodDir+'lo.txt')
                    vL.append(np.loadtxt(periodDir+'output_c.txt')) 
                    samplingL.append(np.loadtxt(periodDir+'output_Map0.txt'))
                    indexL = np.array([2,4,6,8,11])
                    resData = np.loadtxt(periodDir+'output_res.txt','str')[:,indexL].astype('float')
                    SDL.append(resData[0,2])
                    SDL_r.append(resData[1,2])
                    if os.path.exists(periodDir+'output_c_std.txt'):
                        stdL.append(np.loadtxt(periodDir+'output_c_std.txt'))
                        if not iso:
                            CstdL.append(np.loadtxt(periodDir+'output_C_std.txt'))
                            SstdL.append(np.loadtxt(periodDir+'output_S_std.txt'))
                        if withR:
                            R = np.loadtxt(periodDir+'output_c_R.txt')
                            RL.append(R+0)
                    else:
                        stdL.append(vL[-1]*0)
                        if not iso:
                            CstdL.append(vL[-1]*0)
                            SstdL.append(vL[-1]*0)
                    if not iso:
                        CL.append(np.loadtxt(periodDir+'output_C.txt')) 
                        SL.append(np.loadtxt(periodDir+'output_S.txt')) 
                    if os.path.exists(periodDir+'true.txt'):
                        vTrueL.append(np.loadtxt(periodDir+'true.txt'))
                        if not iso:
                            CTrueL.append(np.loadtxt(periodDir+'trueC.txt')) 
                            STrueL.append(np.loadtxt(periodDir+'trueS.txt')) 
                else:
                    vL.append(vL[-1]*0)
                    stdL.append(vL[-1]*0)
                    CL.append(CL[-1]*0)
                    SL.append(SL[-1]*0)
                    samplingL.append(samplingL[-1]*0)
            self.vL = np.array(vL).transpose([1,2,0])
            self.stdL = np.array(stdL).transpose([1,2,0])
            self.samplingL=np.array(samplingL).transpose([1,2,0])
            self.SDL = np.array(SDL)
            self.SDL_r = np.array(SDL_r)
            if len(RL)>0:
                self.RL=np.array(RL).transpose([1,2,0])
            print(self.samplingL.max())
            self.vL[self.samplingL<minSample]=np.nan
            #self.T=np.array(TL)
            if len(vTrueL)>0:
                self.vTrueL=np.array(vTrueL).transpose([1,2,0])
                self.vTrueModel = self.vTrueL
                #self.vTrueModel.mode = 'DSP'
                if not self.iso:
                    self.CTrueL=np.array(CTrueL).transpose([1,2,0])
                    self.STrueL=np.array(STrueL).transpose([1,2,0])
                    angle,amp= self.transferCS(self.CTrueL,self.STrueL)
                    amp /= self.vTrueModel
                    self.fastPTrue = amp*np.cos(angle)+1j*amp*np.sin(angle)
                    #self.fastPTrue.mode = 'fastP'
            self.stdL[self.samplingL<minSample]=np.nan
            self.vModel = self.vL
            self.vModel_std = self.stdL/self.vL
            if len(RL)>0:
                self.vModel_R = self.RL
                #self.vModel_R.mode = 'DSP'
            self.vModel_sampling = v=self.samplingL
            #self.vModel.mode = 'DSP'
            #self.vModel_std.mode = 'DSP'
            #self.vModel_sampling.mode = 'DSP'
            if not iso:
                self.CL = np.array(CL).transpose([1,2,0])
                self.SL = np.array(SL).transpose([1,2,0])
                self.CstdL = np.array(CstdL).transpose([1,2,0])
                self.SstdL = np.array(SstdL).transpose([1,2,0])
                self.CL[self.samplingL<minSample]=np.nan
                self.SL[self.samplingL<minSample]=np.nan
                angle,amp= self.transferCS(self.CL,self.SL)
                amp /= self.vModel
                self.fastP = amp*np.cos(angle)+1j*amp*np.sin(angle)
                #self.fastP.mode = 'fastP'
        if mode == 'lmk':
            TL = []
            vL = []
            self.la  = np.arange(16.0,56.1,0.5)[::-1]
            self.lo  = np.arange(70.0,150.1,0.5) 
            for filename in glob(resDir+'Tomo_*_*s.dat'):
                basename = os.path.basename(filename)
                T = float(basename.split('_')[2][:-5])
                TL.append(T)
                vL .append(np.loadtxt(filename))
                #print(vL])
            vL = np.array(vL).transpose([1,2,0])
            T = np.array(TL)
            vL = vL[:,:,T.argsort()]
            T = T[T.argsort()]  
            self.vL = vL
            self.T = T
            print('**************',self.vL.shape)
        if mode == 'USA':
            TL = []
            vL = []
            sprL = []
            self.la  = np.loadtxt(resDir+'la.txt')
            self.lo  = np.loadtxt(resDir+'lo.txt')
            #self.lo  = -121+np.arange(264)*0.25
            for filename in glob(resDir+'*.*.txt'):
                basename = os.path.basename(filename)
                T = float(basename[:-4])
                TL.append(T)
                vL .append(np.loadtxt(filename))
                sprL.append(np.loadtxt(filename+'.spr'))
                #print(vL])
            vL = np.array(vL).transpose([1,2,0])
            sprL= np.array(sprL).transpose([1,2,0])
            T = np.array(TL)
            vL = vL[:,:,T.argsort()]
            sprL = sprL[:,:,T.argsort()]
            self.sprL = sprL
            T = T[T.argsort()]  
            self.vL = vL
            self.T = T
            self.stdL = vL*0-1
            #self.vL[self.sprL<10]=np.nan
            print('**************',self.vL.shape)
        if mode == 'HV':
            TL = []
            vL = []
            with File(resDir) as h5:
                self.vL = h5['HV'][:]
                self.stdL = h5['STD'][:]
                self.T = h5['T'][:]
                self.la = h5['la'][:]
                self.lo = h5['lo'][:]
    def transferCS(self,CL,SL):
        M = CL+SL*1j
        angle = np.angle(M)/2
        amp = np.abs(M)
        return angle,amp 

if __name__ == '__main__':
    
    if 'period' in sys.argv:
        path = '/HOME/jiangyr/resDir/China/SurfNet/20230304V2_140_adamW_0.05_V25_randSeed_newSyn_smallV3/ori/NC_new_0.50_5_minSta-1_2.0STDABS_-1_16_PWTrue_WCTrue_WSFalse_GVFalse_AUTrue_isoFalse_finiteTrue_threshold0.015_newV3/'
        dispM = DispModel(path)
        plt.pcolor(dispM.lo,dispM.la,dispM.vL[:,:,0],cmap='jet')
        plt.savefig('period.png')
        exit()
    if 'findQVs' in sys.argv:
        depth,rho,vp,vs,Q_kappa,Q_mu = np.loadtxt('ak135F.txt')[8:21].transpose()
        vsRemove = removePressure(vs,depth)
        Q_kappa1,Q_mu1 = vs_z2Q_mantle1(vs,depth)
        plt.figure(figsize=(5,5))
        plt.plot(vsRemove,Q_kappa,'.b')
        plt.plot(vsRemove,Q_mu,'.r')
        plt.plot(vsRemove,Q_kappa1,'ob',mfc='None')
        plt.plot(vsRemove,Q_mu1,'or',mfc='None')
        plt.tight_layout()
        plt.savefig('Q-vs.jpg')
        
        ratio = vp/vs
        plt.figure(figsize=(5,5))
        plt.plot(vsRemove,ratio,'.b')
        plt.plot(vsRemove,vs2vp_mantle1(vs,depth)/vs,'.r')
        #plt.plot(vsRemove,Q_mu,'.r')
        plt.tight_layout()
        plt.savefig('Q-ratio.jpg')
        
        ratio = rho/vs
        plt.figure(figsize=(5,5))
        plt.plot(vsRemove,ratio,'.b')
        plt.plot(vsRemove,vs2rho_mantle1(vs,depth)/vs,'.r')
        #plt.plot(vsRemove,Q_mu,'.r')
        plt.tight_layout()
        plt.savefig('Q-ratio-rho.jpg')
        
        plt.figure(figsize=(5,5))
        plt.plot(depth,Q_kappa,'.b')
        #plt.plot(vsRemove,Q_mu,'.r')
        plt.tight_layout()
        plt.savefig('Q-depth.jpg')
        
        plt.figure(figsize=(5,5))
        
        plt.plot(depth,vs,'.b')
        plt.plot(depth,vsRemove,'.r')
        #plt.plot(vsRemove,Q_mu,'.r')
        plt.tight_layout()
        plt.savefig('vs-depth.jpg')
        exit()
    
    if 'rf' in sys.argv:
        Z = np.array([0,1,50.0])
        p= 7.2
        s =12.
        #s = 10.5
        r = 3**0.5
        vdss = 111/4.25/1.73
        plt.figure(figsize=[6,4])
        timeL = np.arange(1024)/10-51.2
        vs = np.array([2.5,4.,5.])
        vp = vs*r
        rho = vs*0+2
        r = 3**0.5
        ar = 6371
        deg2rad = np.pi/180.
        vTop=ar*deg2rad/s*0.99/r
        vdssTop=ar*deg2rad/vdss*0.99/r
        
        #vTop=0.01
        #vdssTop=1
        #syn_z,      // << vertical responses
        #syn_r,      // << radial responses
        #syn_rf
        fp0, fsv0, qrf = rfmini_obs(Z, vp, vs, rho, 1000000+vp, 100000+vs,p, 4,1024, 10,51.2, vs.astype('float64')[0], 0.25, 'P')
        fp1, fsv1, qrfS = rfmini_obs(Z, vp, vs, rho, 1000000+vp, 100000+vs,s, 4,1024, 10,51.2,vs.astype('float64')[0] , 0.25, 'SV')
        fp, fsv, qrfVdss = rfmini_obs(Z, vp, vs, rho, 1000000+vp, 100000+vs,vdss, 4,1024, 10,51.2, vs.astype('float64')[0], 0.25, 'SV')
        #plt.figure(figsize=[6,4])
        plt.subplot(3,1,1)
        #gauss = np.exp(-np.arange(-8,8,0.1)**2/2/0.5**2)
        #gauss /= gauss.sum()
        #qrfC= convolve(qrf, gauss, mode='same')
        #qrfSC= convolve(qrfS, gauss, mode='same')
        #qrfVdssC= convolve(qrfVdss, gauss, mode='same')
        plt.plot(timeL,qrfC,'k',lw=0.5)
        #plt.plot(timeL,fp1,'m',lw=0.5)
        #plt.plot(timeL,fsv1,'--m',lw=0.5)
        plt.plot(timeL,qrfSC,'--r',lw=0.5)
        plt.plot(timeL,qrfVdssC,'--b',lw=0.5)
        plt.title('vsvp change')
        
        vs = np.array([4.,4.])
        vp = vs*1.73
        vp[1]*=1.2
        rho = vs*0+2
        fp, fsv, qrf = rfmini.synrf(Z, vp, vs, rho, 1000000+vp, 100000+vs,p, 4,1024, 10,-51.2, vs.astype('float64')[0], 0.25, 'P')
        fp, fsv, qrfS = rfmini.synrf(Z, vp, vs, rho, 1000000+vp, 100000+vs,s, 4,1024, 10,-51.2, vs.astype('float64')[0], 0.25, 'SV')
        fp, fsv, qrfVdss = rfmini.synrf(Z, vp, vs, rho, 1000000+vp, 100000+vs,vdss, 4,1024, 10,-51.2, vs.astype('float64')[0], 0.25, 'SV')
        #plt.figure(figsize=[6,4])
        plt.xlim([-25,25])
        #plt.ylim([-0.5,0.5])
        plt.subplot(3,1,2)
        plt.plot(timeL,qrf,'k',lw=0.5)
        plt.plot(timeL,qrfS,'--r',lw=0.5)
        plt.plot(timeL,qrfVdss,'--b',lw=0.5)
        plt.title('vp change')
        
        
        vs = np.array([4.,5.])
        vp = vs*1.73
        vp[1]=vp[0]
        rho = vp*0+2
        fp, fsv, qrf = rfmini.synrf(Z, vp, vs, rho, 1000000+vp, 100000+vs,p, 4,1024, 10,-51.2, vs.astype('float64')[0], 0.25, 'P')
        fp, fsv, qrfS = rfmini.synrf(Z, vp, vs, rho, 1000000+vp, 100000+vs,s, 4,1024, 10,-51.2, vs.astype('float64')[0], 0.25, 'SV')
        fp, fsv, qrfVdss = rfmini.synrf(Z, vp, vs, rho, 1000000+vp, 100000+vs,vdss, 4,1024, 10,-51.2, vs.astype('float64')[0], 0.25, 'SV')
        #plt.figure(figsize=[6,4])
        plt.xlim([-25,25])
        plt.subplot(3,1,3)
        plt.plot(timeL,qrf,'k',lw=0.5)
        plt.plot(timeL,qrfS,'--r',lw=0.5)
        plt.plot(timeL,qrfVdss,'--b',lw=0.5)
        plt.title('vs change')
        plt.xlim([-25,25])
        plt.tight_layout()
        plt.savefig('rf.png',dpi=300)
        exit()
    
    
    
    g = Generator(isTest=True,mN=10,paraL=paraLFunc)
    
    for i in range(10):
        g[i]
    #exit()
    z = np.concatenate([np.arange(0,5.0,0.1),np.arange(5,50,1),np.arange(50.0,210.0,10)])
    model =Model(paraL=paraLFunc,walkSpaceRatio=0.05)
    m = model.Generate(walkN=10000)
    
    plt.figure(figsize=(10,10))
    TE = np.arange(10,160,2)
    for i in range(1000):
        for _ in range(50):
            m = model.walk(m)
        print(i)
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = model(m,z,isZ=True)
        if water_thickness>0:
            continue
        Q_p = toQa(vp,vs,Q_kappa,Q_mu)
        Q_s = Q_mu
        e =  calDisp(thickness, vp, vs, rho, TE,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity='ellipticity', flat_earth=False,ar=6370,dc0=0.005)
        #pde = Ellipticity(thickness,vp,vs,rho)
        #eT = pde(TE, mode=0).ellipticity
        if e.min()<0:
            print(vp[::4])
            print(vs[::4])
            print(rho[::4])
            print(vp[::4]/vs[::4])
            print(rho[::4]/vs[::4])
            #print(e[::4]-eT[::4])
            exit()
        plt.plot(e,TE,'-k',lw=0.5)
        #plt.plot(eT,TE,'-r',lw=0.5)
    plt.gca().set_yscale('log')
    plt.savefig('ss_e.jpg',dpi=400)
    plt.close()
    
    
    plt.figure(figsize=(10,10))
    for i in range(1):
        for _ in range(20):
            m = model.walk(m)
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = model(m,z,isZ=True)
        plt.plot(vs,z,'-k',lw=0.5,drawstyle='steps-pre')
        plt.plot(vp,z,'-g',lw=0.5,drawstyle='steps-pre')
        plt.plot(rho,z,'-m',lw=0.5,drawstyle='steps-pre')
        plt.plot(Q_mu/200,z,'-r',lw=0.5,drawstyle='steps-pre')
        plt.plot(Q_kappa/1000,z,'-b',lw=0.5,drawstyle='steps-pre')
        plt.ylim([210,0])
        
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = model.calPQ(vs,z,water_thickness,sediment_thickness,crust_thickness)
        plt.plot(vs,z,'ok',lw=0.5,drawstyle='steps-pre')
        plt.plot(vp,z,'og',lw=0.5,drawstyle='steps-pre')
        plt.plot(rho,z,'o-m',lw=0.5,drawstyle='steps-pre')
        
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = model(m,z,isZ=False)
        z = np.cumsum(thickness)
        z[:-1] =z[:-1]-thickness[:-1]
        plt.plot(vs,z,'--k',lw=0.5,drawstyle='steps-pre')
        plt.plot(vp,z,'--g',lw=0.5,drawstyle='steps-pre')
        plt.plot(rho,z,'--m',lw=0.5,drawstyle='steps-pre')
    plt.savefig('ss_recover.jpg',dpi=400)
    plt.close()
    
    plt.figure(figsize=(10,10))
    for i in range(1000):
        print(i)
        for _ in range(20):
            m = model.walk(m)
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = model(m,z,isZ=True)
        plt.plot(vs,z,'-k',lw=0.5)
        plt.plot(vp,z,'-g',lw=0.5)
        plt.plot(rho,z,'-m',lw=0.5)
        plt.plot(Q_mu/200,z,'-r',lw=0.5)
        plt.plot(Q_kappa/1000,z,'-b',lw=0.5)
        plt.ylim([210,0])
    plt.savefig('ss.jpg',dpi=400)
    
    plt.figure(figsize=(10,10))
    for i in range(100):
        print(i)
        m = model.Generate(walkN=500)
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness  = model(m,z,isZ=True)
        plt.plot(vs,z,'-k',lw=0.5)
        plt.plot(vp,z,'-g',lw=0.5)
        plt.plot(rho,z,'-m',lw=0.5)
        plt.plot(Q_mu/200,z,'-r',lw=0.5)
        plt.plot(Q_kappa/1000,z,'-b',lw=0.5)
        plt.ylim([210,0])
    plt.savefig('s.jpg',dpi=400)
from netCDF4 import Dataset        
class Litho:
    def __init__(self,litho='data/LITHO1.0.nc'):
        self.litho=Dataset(litho)
        litho=self.litho
        self.laL = litho.variables['latitude'][:]%180
        self.loL = litho.variables['longitude'][:]%360
    def getWater(self,la,lo):
        litho=self.litho
        la = la%180
        lo = lo%360
        i = np.abs(self.laL-la).argmin()
        j = np.abs(self.loL-lo).argmin()
        waterD= litho['water_bottom'+'_depth'][i,j]-litho['water_top'+'_depth'][i,j]
        if waterD>0:
            return waterD
        else:
            return -1      

class Func:
    def __init__(self,s_model,data={},dataStd={},Z=[],G=[],timeLP=[],timeLPDec=[],gauss=[],ar=6371):
        self.s_model=s_model
        self.data=data
        self.dataStd=dataStd
        self.Z = Z
        self.G = G
        self.gauss = gauss
        self.timeLP = timeLP
        self.timeLPDec = timeLPDec
        self.ar =ar
    def __call__(self,m,isData= False ,isFromVs = False,sediment_thickness=0,crust_thickness=0,water_thickness=0,Z=0):
        if isFromVs:
            vp0,vs0,rho0,thickness0,Q_mu0,Q_kappa0,water_thickness,sediment_thickness,crust_thickness= self.s_model.calPQ(m,Z,water_thickness,sediment_thickness,crust_thickness)
        else:
            vp0,vs0,rho0,thickness0,Q_mu0,Q_kappa0,water_thickness,sediment_thickness,crust_thickness = self.s_model(m ,self.Z,isZ= not len(self.Z)==0)
        vp,vs,rho,thickness,Q_mu,Q_kappa,water_thickness,sediment_thickness,crust_thickness  = vp0,vs0,rho0,thickness0,Q_mu0,Q_kappa0,water_thickness,sediment_thickness,crust_thickness
        Q_p = toQa(vp,vs,Q_kappa,Q_mu)
        Q_s = Q_mu
        S =0 
        #print(m.shape)
        #print(vp.shape)
        #exit()
        if isData:
            dataL = {}
        for key in self.data:
            data0 = self.data[key][0]
            dataStd = self.dataStd[key][0]
            if key in ['c','g','e']:
                T = self.data[key][1]
                data =  calDisp(thickness, vp, vs, rho, T,Qp=Q_p,Qs=Q_s,wave='rayleigh', mode=1, velocity={'c':'phase','g':'group','e':'ellipticity'}[key], flat_earth=True,ar=6370,dc0=0.005)
                if key == 'e' and water_thickness<0:
                    data*= np.nan
                #print(vs)
                #print(vp)
                ##print(rho)
                #exit()
            elif key in ['water_thickness','sediment_thickness','crust_thickness']:
                data = self.s_model.getThickness(m,key.split('_')[0])
            elif key in ['qrf']:
                ar = self.ar
                p = self.data[key][1]
                Thickness = thickness0
                Z = np.cumsum(Thickness)
                thickness = Thickness
                Z[1:]=Z[:-1]
                Z[0]=0
                vpvs = vp[0] / vs[0]
                poisson = (2 - vpvs**2)/(2 - 2 * vpvs**2)
                
                slownessP = (ar-Z)*np.pi/180/vp
                SlownessP = slownessP+0
                minSlowP = 1000000
                timeL = self.timeLP
                for i in range(len(slownessP)):
                    if slownessP[i]<minSlowP:
                        minSlowP = slownessP[i]
                    SlownessP[i] = minSlowP
                
                water_depth, sediment_depth, crust_depth = thickness2depth(water_thickness,sediment_thickness,crust_thickness)
                crust_depth = max(crust_depth,20)
                #print(p,SlownessP[Z<crust_depth+50].min())
                p = min(p,SlownessP[Z<crust_depth+50].min()*0.9)
                #print(crust_depth,p)
                fp, fsv, qrf = rfmini_obs(Z[SlownessP>(p*1.1)], vp[SlownessP>(p*1.1)], vs[SlownessP>(p*1.1)], rho[SlownessP>(p*1.1)], Q_p[SlownessP>(p*1.1)],Q_s[SlownessP>(p*1.1)],p, 4, len(timeL), 1/(timeL[1]-timeL[0]),-timeL[0], vs.astype('float64')[0], poisson, 'P',G=self.G,gauss=self.gauss)
                
                qrf = np.interp( self.timeLPDec,timeL, qrf, left=0, right=0)
                data = qrf
                #print(np.nansum(((data-data0)/dataStd)**2))
                #,data,data0,dataStd)
            if isData:
                tmp = self.data[key].copy()
                tmp[0]=data
                dataL[key] = tmp
            #print(key,data,data0,dataStd)
            S += np.nansum(((data-data0)/dataStd)**2)
        if isData:
            return S,dataL
        return S
            
class MCMC:
    def __init__(self,func,n_dim=None,lb=[],ub=[],steps=100,nwalkers=100,walkSpaceRatio=0.05,constraint_ueq=[],walkType='all',thresholdMul=1.5,count=5,**kwargs):
        self.func=func
        self.n_dim=n_dim
        self.lb=lb
        self.ub=ub
        self.nwalkers=nwalkers
        self.steps =steps
        self.walkerSpace = walkSpaceRatio*(ub-lb)
        self.constraint_ueq=constraint_ueq
        self.walkType=walkType
        self.iL = np.arange(self.n_dim).tolist()
        self.thresholdMul = thresholdMul
        self.count = count
        self.step = 0
        self.minValue = 10000000
    def generate(self):
        a = np.random.rand()
        b = 1-(1-a)*np.random.rand()
        r = np.arange(self.n_dim)/(self.n_dim-1)
        m = a*(1-r)+b*r+0.1*(b-a)*(np.random.rand((self.n_dim))-0.5)
        return self.lb*m+(1-m)*self.ub
    def walk(self,m):
        if self.walkType =='all':
            count = 0
            mul = 1
            N=1
        elif self.walkType =='one':
            count = 0
            mul = 1
            N= 1
        while True:
            indexL = random.sample(self.iL,N)
            mNew = m+0
            mNew[indexL]+=np.random.randn(N)*self.walkerSpace[indexL]*mul
            if self.check(mNew):
                return mNew
            count+=1
    def check(self,m):
        if (m>self.ub).sum()+(m<self.lb).sum()>0:
            return False
        for eq in self.constraint_ueq:
            if eq(m)>0:
                return False
        return True
    def init(self,nwalkers=-1):
        self.walkers=[]
        self.walkersValue=[]
        if nwalkers<0:
            nwalkers=self.nwalkers
        for i in range(nwalkers):
            while True:
                m = self.generate()
                if self.check(m):
                    self.walkers.append([m])
                    self.walkersValue.append([self.func(m)])
                    break
    def Step(self,output=False,steps=10):
        for i in range(self.nwalkers):
            walker=self.walkers[i]
            walkerValue=self.walkersValue[i]
            m =walker[-1]
            value= walkerValue[-1]
            while True:
                mNew = self.walk(m)
                valueNew = self.func(mNew)
                self.minValue = min(self.minValue,valueNew)
                if np.random.rand()<np.exp((value-valueNew)/2):
                    walker.append(mNew)
                    walkerValue.append(valueNew)
                    break
        self.step+=1
        print(self.step,'in',self.steps,self.minValue)
        if  self.step==self.steps//16 or self.step==self.steps//8 or self.step==self.steps//4:#loop==self.steps//10
            #pass#self.step==self.steps//16 or
            self.walkerSpace /= 2
            self.walkType='one'
        if output:
            return self.output(steps,isAll=False,isMean=True)
        else:   
            return 
    def run(self):
        self.init()
        for loop in range(self.steps):
            self.Step()
        return self.output(isAll=True)
    def output(self,steps=-1,isMean=False,isAll=True):
        if steps<0:
            steps = int(self.steps//2)
        else:
            steps = min(steps,self.step)
        self.X = np.array([walker[-steps:] for walker in self.walkers])#.reshape([-1,self.n_dim])
        self.Y = np.array([walker[-steps:] for walker in self.walkersValue])
        if isAll:
            self.Y_o = np.array(self.walkersValue)
        self.Y_mean = self.Y[:,-steps:].mean(axis=1)
        threshold = self.Y_mean.min()*self.thresholdMul
        self.threshold = threshold
        self.allow_X=self.X[self.Y_mean<threshold,-steps:,].reshape([-1,self.n_dim])
        self.allow_Y=self.Y[self.Y_mean<threshold,-steps:,].reshape([-1])
        self.Y = self.Y.reshape([-1])
        self.X = self.X.reshape([-1,self.n_dim])
        if isMean:
            self.best_x=self.allow_X.mean(axis=0)
            self.best_y=self.allow_Y.mean(axis=0)
        else:
            tmpIndex=self.Y.argmin()
            self.best_x=self.X[tmpIndex]
            self.best_y=self.Y[tmpIndex]
        return self.best_x,self.best_y


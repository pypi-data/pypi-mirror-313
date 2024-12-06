
import numpy as np

FORMAT ='jpg'
thicknessA=100
RFNO = 512
RF_delta = 0.1 
rfT = 1/2.5/2**0.5

RF_G = np.zeros(RFNO)
RF_G[:RFNO//8] = RFNO//8-np.arange(RFNO//8)
RF_G[-RFNO//8:] = np.arange(RFNO//8)
RF_G = np.exp(-RF_G**2/(2*(RFNO//32)**2))

RF_timeLP = (np.arange(RFNO)*RF_delta-12.8).astype('float64')
RF_timeLS = (np.arange(RFNO)*RF_delta-12.8).astype('float64')
RF_timeLVDSS = (np.arange(RFNO)*RF_delta-12.8).astype('float64')

RF_timeLPDec = np.arange(0,12.1,RF_delta).astype('float64')
RF_timeLSDec = np.arange(0,12.1,RF_delta).astype('float64')
RF_timeLVDSSDec =np.arange(0,12.1,RF_delta).astype('float64')
RF_gauss = np.exp(-np.arange(-8,8,RF_delta)**2/2/rfT**2)
RF_gauss /= RF_gauss.sum()*RF_delta

RF_gauss_short = np.exp(-np.arange(-3,3,RF_delta)**2/2/rfT**2)
RF_gauss_short /= RF_gauss_short.sum()*RF_delta
#print(RF_gauss.max())
#self.gauss /= np.sum(self.gauss)


emb_typeList=['zero','one','c','g','rf','rfs','vs','e','vdss','time','depth','p','velocity','water_thickness','sediment_thickness','crust_thickness','ratio','kappa']
emb_paraD = {'c':['time','velocity'],'g':['time','velocity'],'e':['time','ratio'],'vdss':['time','p'],'rf':['time','p','ratio'],'rfs':['time','p'],'vs':['depth','velocity'],'water_thickness':['depth'],'sediment_thickness':['depth'],'crust_thickness':['depth'],'kappa':['ratio','ratio']}
emb_typeD ={'c':'velocity','g':'velocity','e':'ratio','vs':'velocity','rf':'ratio','rfs':'ratio','vdss':'ratio','water_thickness':'depth','sediment_thickness':'depth','crust_thickness':'depth','kappa':'ratio'}
emb_mulA =  {'velocity':1,'time':40,'depth':thicknessA,'p':10,'ratio':1}

z_base = np.concatenate([
            np.arange(0.000,0.25,0.05).tolist(),#1
            np.arange(0.25,0.5,0.05).tolist(),#2
            np.arange(0.5,1.5,0.2).tolist(),#3
            np.arange(1.5,3.0,0.3).tolist(),#4
            np.arange(3.0,4.5,0.3).tolist(),#5
            np.arange(4.5,6.0,0.3).tolist(),#5
            np.arange(6.0,10.0,0.8).tolist(),#6
            np.arange(10.0,15,1).tolist(),#6
            np.arange(15,20,1).tolist(),#7
            np.arange(20,25,1).tolist(),#7
            np.arange(25,30,1).tolist(),#8
            np.arange(30,35,1).tolist(),#8
            np.arange(35,40,1).tolist(),#9
            np.arange(40,45,1).tolist(),#9
            np.arange(45,50,1).tolist(),#10
            np.arange(50,55,1).tolist(),#10
            np.arange(55,60,1).tolist(),#11
            np.arange(60,65,1).tolist(),#11
            np.arange(65,70,1).tolist(),#12
            np.arange(70,75,1).tolist(),#12
            np.arange(75,100,5).tolist(),#13
            np.arange(100,125,5).tolist(),#14
            np.arange(125,150,5).tolist(),#15
            np.arange(150,175,5).tolist(),#16
            np.arange(175,200,5).tolist(),#17
            np.arange(200,225,5).tolist(),#18
            np.arange(225,250,5).tolist(),#19
            np.arange(250,275,5).tolist(),#20
            np.arange(275,300,5).tolist(),#21
            np.arange(300,325,5).tolist(),#22
            np.arange(325,350,5).tolist(),#23
            np.arange(350,375,5).tolist()])#24])

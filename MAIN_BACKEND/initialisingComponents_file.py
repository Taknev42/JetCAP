from turbofan_mixed_alp_calculation import turbofan_mixed_alp_calculation
from atmosphere import atmosphere
from fuel import fuel
from aircraft import aircraft
from nozzle import nozzle
from compressor import compressor
from combuster import combustor
from turbine import turbine
from mixer import mixer
from turbofan import turbofan
from turbojet import turbojet
from ramjet import ramjet

class initialisingComponents:
    def __init__(self,engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType):
        self.engineType= engineType
        self.AB= AB
        #we dont add alt as a parameter because it is not used in the PCA component wise analysis code. It is only used as an input during parameter initialization part to get T0,P0 from altitude
        self.T0=T0
        self.P0=P0
        self.M0=M0
        self.M6=M6
        self.alp=alp
        self.gam_c=gam_c
        self.gam_t=gam_t
        self.gam_ab=gam_ab
        self.Rc=Rc
        self.Rt=Rt
        self.Rab=Rab
        self.Cpc=Cpc
        self.Cpt=Cpt
        self.Cpab=Cpab
        self.Tt4=Tt4
        self.Tt7=Tt7
        self.Hpr=Hpr
        self.eta_b=eta_b
        self.eta_m=eta_m
        self.eta_ab=eta_ab
        self.pi_d_max=pi_d_max
        self.pi_f=pi_f
        self.pi_c=pi_c
        self.pi_cL=pi_cL
        self.pi_cH=pi_cH
        self.pi_b=pi_b
        self.pi_m_max=pi_m_max
        self.pi_ab=pi_ab
        self.pi_n=pi_n
        self.pi_fn=pi_fn
        self.peta_f=peta_f
        self.peta_c=peta_c
        self.peta_t=peta_t
        self.P0_P9= P0_P9
        self.P0_P19= P0_P19
        self.sep_mixed_flow= sep_mixed_flow
        self.nozzleType= nozzleType
        
    def get_engine(self):
        engineType= self.engineType
        AB= self.AB
        T0=self.T0
        P0=self.P0
        M0=self.M0
        M6= self.M6
        alp=self.alp
        gam_c=self.gam_c
        gam_t=self.gam_t
        gam_ab=self.gam_ab
        Rc=self.Rc
        Rt=self.Rt
        Rab=self.Rab
        Cpc=self.Cpc
        Cpt=self.Cpt
        Cpab=self.Cpab
        Tt4=self.Tt4
        Tt7=self.Tt7
        Hpr=self.Hpr
        eta_b=self.eta_b
        eta_m=self.eta_m
        eta_ab=self.eta_ab
        pi_d_max=self.pi_d_max
        pi_f=self.pi_f
        pi_c=self.pi_c
        pi_cL=self.pi_cL
        pi_cH=self.pi_cH
        pi_b=self.pi_b
        pi_m_max=self.pi_m_max
        pi_ab=self.pi_ab
        pi_n=self.pi_n
        pi_fn=self.pi_fn
        peta_f=self.peta_f
        peta_c=self.peta_c
        peta_t=self.peta_t
        P0_P9= self.P0_P9
        P0_P19= self.P0_P19
        sep_mixed_flow= self.sep_mixed_flow
        nozzleType= self.nozzleType

        #pi_d calculation
        if M0<1 or pi_d_max==1:
            eta_r= 1
        else:
            eta_r= 1-0.075*pow((M0-1),1.35)
        pi_d= pi_d_max*eta_r

        if engineType=="turbofan" and sep_mixed_flow=="M":
            alp= turbofan_mixed_alp_calculation(T0,P0,M0,gam_c,gam_t,Cpc,Cpt,Hpr,Tt4,eta_b,eta_m,pi_f,pi_c,pi_cL,pi_cH,pi_b,peta_f,peta_c,peta_t)

        #making parameters dictionary which stores all the input parameters
        dict1= dict(locals().items())
        values= [engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType]
        keys_lst= list(dict1.keys())
        val_lst= list(dict1.values())
        keys=[]
        for i in values:
            ind=val_lst.index(i)
            keys.append(keys_lst[ind])
            val_lst[ind]=None
        parameters= dict(zip(keys,values))

        atmosphere1= atmosphere(T0,P0)
        fuel1= fuel(gam_c,gam_t,gam_ab,Rc,Rt,Cpc,Cpt,Cpab,Hpr)
        aircraft1= aircraft(M0,alp,atmosphere1,fuel1)

        fan1= compressor(pi_f,peta_f,aircraft1)
        diffuser1= nozzle(pi_d)
        LowCompressor1= compressor(pi_cL,peta_c,aircraft1)
        HighCompressor1= compressor(pi_cH,peta_c,aircraft1)
        combuster1= combustor(pi_b,eta_b,Tt4,aircraft1)
        HighTurbine1= turbine(eta_m,peta_t,aircraft1,fan1,LowCompressor1,HighCompressor1,combuster1)
        LowTurbine1= turbine(eta_m,peta_t,aircraft1,fan1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1)
        nozzle1= nozzle(pi_n)
        fanNozzle1= nozzle(pi_fn)

        #if sep_mixed_flow is M then we have to make a mixer
        if sep_mixed_flow=="M":
            mixer1= mixer(parameters,aircraft1,fan1,diffuser1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1,LowTurbine1) 
        else:
            mixer1= None

        # AfterBurner is optional
        if AB=="Y":
            afterBurner1= combustor(eta_ab,pi_ab,Tt7,aircraft1,combuster1,"AB")
        else:
            afterBurner1= None

        if engineType=="turbofan":
            turbofan1= turbofan(parameters,aircraft1,fan1,diffuser1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1,LowTurbine1,nozzle1,fanNozzle1,mixer1,afterBurner1)
            return turbofan1

        elif engineType =="turbojet":
            turbojet1= turbojet(parameters,aircraft1,fan1,diffuser1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1,LowTurbine1,nozzle1,fanNozzle1,afterBurner1)
            return turbojet1
    
        elif engineType =="ramjet":
            ramjet1= ramjet(parameters,aircraft1,fan1,diffuser1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1,LowTurbine1,nozzle1,fanNozzle1,afterBurner1)
            return ramjet1
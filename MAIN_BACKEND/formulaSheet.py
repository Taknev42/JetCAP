"""This file contains all the Engine performance formula's"""
from math import sqrt,pow


class formulaSheet:
    def __init__(self,engine):
        self.engine= engine

    def get_PnT_from_PtTtM(self,Pt,Tt,M,gam):
        tau= 1+0.5*(gam-1)*pow(M,2)
        gam_term= gam/(gam-1)
        pi= pow(tau,gam_term)

        P= Pt/pi
        T= Tt/tau

        return (P,T)
    
    def get_v(self,gam,R,T,M):
        v= M*self.get_a(gam,R,T)
        return v

    def get_a(self,gam,R,T):
        a= sqrt(gam*R*T)
        return a
    
    def get_Tc_Mc(self):
        if hasattr(self,"Tc_Mc"):
            return self.Tc_Mc
        
        gam_c= self.engine.parameters["gam_c"]
        gam_t= self.engine.parameters["gam_t"]
        Rc= self.engine.parameters["Rc"]
        Rt= self.engine.parameters["Rt"]
        M0= self.engine.parameters["M0"]
        P0= self.engine.parameters["P0"]
        T0= self.engine.parameters["T0"]
        M9= self.engine.M9
        alp = self.engine.parameters["alp"]
        f= self.engine.f

        a0= self.get_a(gam_c,Rc,T0)

        if self.engine.afterBurner:
            gam_t= self.engine.aircraft.fuel.gam_ab

        (P9,T9)= self.get_PnT_from_PtTtM(self.engine.Pt9,self.engine.Tt9,M9,gam_t)

        a9_a0 = sqrt((gam_t*Rt*T9)/(gam_c*Rc*T0))   
        t1= M9*a9_a0*(1+f*(1+alp)) -M0                                  #accurate formula
        # t1= M9*temp -M0                                               #PARA assumption           
        t2= (1+f*(1+alp))*a9_a0*(1-P0/P9)/(gam_t*M9)
        self.Tc_Mc= a0*(t1+t2)

        return self.Tc_Mc
    
    def get_Tb_Mb(self):
        if hasattr(self,"Tb_Mb"):
            return self.Tb_Mb
        
        gam_c= self.engine.parameters["gam_c"]
        Rc= self.engine.parameters["Rc"]
        M0= self.engine.parameters["M0"]
        P0= self.engine.parameters["P0"]
        T0= self.engine.parameters["T0"]
        M19= self.engine.M19

        (P19,T19)= self.get_PnT_from_PtTtM(self.engine.Pt19,self.engine.Tt19,M19,gam_c)
        a0= self.get_a(gam_c,Rc,T0)
        a19= self.get_a(gam_c,Rc,T19)   
        
        temp1= a0*(M19*sqrt(T19/T0) -M0)
        temp2= a19*(1- P0/P19)/(gam_c*M19)

        self.Tb_Mb= temp1+temp2

        return self.Tb_Mb
    
    def get_ST(self):
        if hasattr(self,"ST"):
            return self.ST
        
        alp= self.engine.parameters["alp"]

        self.ST= (alp/(1+alp))*self.get_Tb_Mb() + (1/(1+alp))*self.get_Tc_Mc()
        return self.ST
    
    def get_TSFC(self):
        if hasattr(self,"TSFC"):
            return self.TSFC
        
        f= self.engine.f
        ST= self.engine.ST
        
        self.TSFC= f/ST
        return self.TSFC
    
    def get_M_from_Pt_P(self,Pt_P,gam):
        t1= 2/(gam-1)
        t2= pow(Pt_P,(gam-1)/gam) -1
        M= sqrt(t1*t2)

        return M
    
    def get_eta_t(self):             #only for single inlet- single single and double inlet- double exhaust engines
        if hasattr(self,"eta_t"):
            return self.eta_t
        
        a0= self.engine.a0
        alp= self.engine.parameters["alp"]
        f= self.engine.f
        Hpr= self.engine.parameters["Hpr"]
        v9_a0= self.engine.v9_a0
        v19_a0= self.engine.v19_a0
        M0= self.engine.parameters["M0"]

        t1= (1/(1+alp)+f)*pow(v9_a0,2) + (alp/(1+alp))*pow(v19_a0,2) -pow(M0,2)
        num= pow(a0,2)*t1
        den= 2*f*Hpr

        self.eta_t= num/den

        return self.eta_t
    
    def get_eta_p(self):        #only for single inlet- single single and double inlet- double exhaust engines
        if hasattr(self,"eta_p"):
            return self.eta_p
        
        a0= self.engine.a0
        alp= self.engine.parameters["alp"]
        f= self.engine.f
        v9_a0= self.engine.v9_a0
        v19_a0= self.engine.v19_a0
        M0= self.engine.parameters["M0"]
        ST= self.engine.ST

        num= 2*ST*M0
        t1= (1/(1+alp)+f)*pow(v9_a0,2) + (alp/(1+alp))*pow(v19_a0,2)-pow(M0,2)
        den= a0*t1

        self.eta_p= num/den

        return self.eta_p
    
    def get_eta_o(self):
        if hasattr(self,"eta_o"):
            return self.eta_o
        
        eta_t= self.get_eta_t()
        eta_p= self.get_eta_p()

        self.eta_o= eta_t*eta_p
        return self.eta_o
    
    def get_ST_single_exhaust(self):          #only used for turbofan with two-inlets and one exhaust
        if hasattr(self,"ST"):
            return self.ST
        
        a0= self.engine.a0
        f= self.engine.f
        v9_a0= self.engine.v9_a0
        M0= self.engine.parameters["M0"]
        if self.engine.afterBurner:
            R9= self.engine.parameters["Rab"]
        else:
            R9= self.engine.parameters["Rt"]
        T9_T0= self.engine.T9_T0
        P0_P9= self.engine.P0_P9
        gam_c= self.engine.parameters["gam_c"]
        gam_t= self.engine.parameters["gam_t"]
        Rc= self.engine.parameters["Rc"]
        

        self.ST= a0*((1+f)*v9_a0-M0+(1+f)*R9*T9_T0*(1-P0_P9)/(Rc*v9_a0*gam_c))

        return self.ST


    




    

    





    



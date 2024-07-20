"""Here we take the thurst profile and give out the optimized turbojet which satisfies all the thrust requirements"""
from EPAtesting import EPAtesting_class
from initialisingComponents_file import initialisingComponents
import numpy as np
import matplotlib.pyplot as plt

class engineOptmization:
    def __init__(self,dict1,cEngine):
        self.dict1= dict1
        self.cEngine= cEngine #currentEngine

    def get_OptEngine(self):
        self.Tt4_min= 1400
        self.Tt4_max=2000
        dict1= self.dict1
        cEngine= self.cEngine
        engineType= self.cEngine.parameters["engineType"]
        AB=self.cEngine.parameters["AB"]
        T0=self.cEngine.parameters["T0"]
        P0=self.cEngine.parameters["P0"]
        M0=self.cEngine.parameters["M0"]
        alp=self.cEngine.parameters["alp"]
        gam_c=self.cEngine.parameters["gam_c"]
        gam_t=self.cEngine.parameters["gam_t"]
        gam_ab=self.cEngine.parameters["gam_ab"]
        Rc=self.cEngine.parameters["Rc"]
        Rt=self.cEngine.parameters["Rt"]
        Cpc=self.cEngine.parameters["Cpc"]
        Cpt=self.cEngine.parameters["Cpt"]
        Cpab=self.cEngine.parameters["Cpab"]
        Tt4=self.cEngine.parameters["Tt4"]
        Tt7=self.cEngine.parameters["Tt7"]
        Hpr=self.cEngine.parameters["Hpr"]
        eta_b=self.cEngine.parameters["eta_b"]
        eta_m=self.cEngine.parameters["eta_m"]
        eta_ab=self.cEngine.parameters["eta_ab"]
        pi_d=self.cEngine.parameters["pi_d"]
        pi_f=self.cEngine.parameters["pi_f"]
        pi_c=self.cEngine.parameters["pi_c"]
        pi_lpc=self.cEngine.parameters["pi_lpc"]
        pi_hpc=self.cEngine.parameters["pi_hpc"]
        pi_b=self.cEngine.parameters["pi_b"]
        pi_ab=self.cEngine.parameters["pi_ab"]
        pi_n=self.cEngine.parameters["pi_n"]
        pi_fn=self.cEngine.parameters["pi_fn"]
        peta_f=self.cEngine.parameters["peta_f"]
        peta_c=self.cEngine.parameters["peta_c"]
        peta_t=self.cEngine.parameters["peta_t"]

        #We size the engine firstly
        [mass,po,to,mo]= [float(i) for i in input(("To size the engine pls enter [m_dot, P0, T0, M0]: ")).strip("[]").split(",")]
        Refengine= initialisingComponents(engineType,AB,to,po,mo,alp,gam_c,gam_t,gam_ab,Rc,Rt,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d,pi_f,pi_c,pi_lpc,pi_hpc,pi_b,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t).get_engine()
        [f,ST,TSFC]= Refengine.get_engineDetails()
        ObjEPAtesting= EPAtesting_class(dict1,cEngine)  #object of EPAtesting class. Otherwise you cant call func defined inside it
        A_star= ObjEPAtesting.A_star(mass,Refengine.P_throat,Refengine.T_throat,gam_t,Rt)

        #get corresponding ST_reqd for all the given phases in dict1 using this refEngine.
        #But you need to iterate again to get the ST reqd for the optEngine 
        for i in dict1:
            [P0,T0,M0,T_reqd]= dict1[i]

            #make a engine out of those P0, T0, M0 atmosphere
            engine1= initialisingComponents(engineType,AB,T0,P0,M0,alp,gam_c,gam_t,gam_ab,Rc,Rt,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d,pi_f,pi_c,pi_lpc,pi_hpc,pi_b,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t).get_engine()
            [f,ST,TSFC]= engine1.get_engineDetails()

            m_flowRate= ObjEPAtesting.m_dot(A_star,engine1.P_throat,engine1.T_throat,gam_t, Rt)

            ST_reqd= T_reqd/ST

            dict1[i].append(ST_reqd)
        
        #Now dict1[i] has 5 element array where the last ele contains the ST reqd
        #We take the max ST reqd as our design point and put Tt4= Tt4_max and find the opt_Engine
        STreqd_arr=[dict1[i][4] for i in dict1]
        ind= STreqd_arr.index(max(STreqd_arr))
        designPoint= list(dict1.keys())[ind]  #usually it would be "takeoff"

        #finding most optEngine 
        [P0,T0,M0,T_reqd,ST_reqd]= dict1[designPoint]
        min_TSFC= np.Inf
        Tt4= self.Tt4_max
        pi_c_min,pi_c_max= (15,40)

        for pi_c in np.linspace(pi_c_min,pi_c_max,100):
            possible_engine1= initialisingComponents(engineType,AB,T0,P0,M0,alp,gam_c,gam_t,gam_ab,Rc,Rt,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d,pi_f,pi_c,pi_lpc,pi_hpc,pi_b,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t).get_engine()
            [f,ST,TSFC]= engine1.get_engineDetails()

            if TSFC<min_TSFC:
                opt_engine= possible_engine1
        
        #we test this opt_Engine for thrust requirements and find the throttle variable Tt4 requirement
        for i in dict1:
            opt_engine.parameters["P0"]= dict1[i][0] 
            opt_engine.parameters["T0"]= dict1[i][1]
            opt_engine.parameters["M0"]= dict1[i][2]

            ST_reqd= dict1[i][4]

            Tt4_reqd= self.get_Tt4_from_ST(ST_reqd,opt_engine)
            if Tt4_reqd> self.Tt4_min and Tt4_reqd < self.Tt4_max:
                print(f"optEngine meets requirements Tt4 reqd: {Tt4_reqd} against Tt4 max: {self.Tt4_max}")
            else:
                print("optEngine doesnot meets reqd")

        #return the opt_engine with P0, T0, M0 of the cruise phase
        opt_engine.parameters["P0"]= dict1["cruise"][0]
        opt_engine.parameters["T0"]= dict1["cruise"][1]
        opt_engine.parameters["M0"]= dict1["cruise"][2]
        return opt_engine
            
    def get_Tt4_from_ST(self,ST_reqd,engine):
        #For the engine to have ST just equal to STreqd, what Tt4 does it need. All other things remain constant for the engine
        guess1= self.Tt4_min -200
        guess2= self.Tt4_max*2
        
        print(f"\n\n\n\n\n\nBisection convergence for ST_reqd {ST_reqd}")
        es=1e-2
        
        plt.figure()
        x= np.linspace(self.Tt4_min,self.Tt4_max,100)
        y= [self.fx(ST_reqd,engine,xvar) for xvar in x]
        plt.plot(x,y)
        plt.show()

        assert(self.fx(ST_reqd,engine,guess1)*self.fx(ST_reqd,engine,guess2) <= 0) #only then there is a root between guess1 and guess2 
        while abs(self.fx(ST_reqd,engine,guess1)) >es:
            guess_new= (guess1+guess2)/2

            if self.fx(ST_reqd,engine,guess1)<0:
                if self.fx(ST_reqd,engine,guess_new)>0:
                    guess2= guess_new
                else:
                    guess1= guess_new
            else:
                if self.fx(ST_reqd,engine,guess_new)>0:
                    guess1= guess_new
                else:
                    guess2= guess_new
            print(f"guess1        {guess1}   guess2        {guess2}    guess_new           {guess_new}       self.fx()       {self.fx(ST_reqd,engine,guess_new)}")
        return guess1

    def fx(self,ST_reqd,engine,Tt4):
        engine.parameters["Tt4"] = Tt4
        engine.combuster.Tt4= Tt4

        [f,ST,TSFC]= engine.get_engineDetails()
        return ST_reqd- ST



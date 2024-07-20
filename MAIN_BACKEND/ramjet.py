from math import sqrt, pow
from formulaSheet import formulaSheet

class ramjet:
    def __init__(self,parameters1,aircraft1,fan1,diffuser1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1,LowTurbine1,nozzle1,fanNozzle1,afterBurner1=None):
        self.parameters= parameters1
        self.aircraft= aircraft1
        self.fan= fan1
        self.diffuser= diffuser1
        self.LowCompressor= LowCompressor1
        self.HighCompressor= HighCompressor1
        self.combuster= combuster1
        self.HighTurbine= HighTurbine1
        self.LowTurbine= LowTurbine1
        self.nozzle= nozzle1
        self.fanNozzle= fanNozzle1
        self.afterBurner= afterBurner1

    def get_engineDetails(self):
        formulaSheet1= formulaSheet(self)

        (self.P0,self.T0)= (self.parameters["P0"],self.parameters["T0"])

        self.Pt0= self.P0*self.aircraft.get_pi_r()
        self.Tt0= self.T0*self.aircraft.get_tau_r()

        self.Pt1,self.Tt1= self.diffuser.get_PnT(self.Pt0,self.Tt0)

        (self.Pt2,self.Tt2)= (self.Pt1,self.Tt1)
        (self.Pt25,self.Tt25)= self.LowCompressor.get_PnT(self.Pt2,self.Tt2)            #Point 2.5
        (self.Pt3,self.Tt3)= self.HighCompressor.get_PnT(self.Pt25,self.Tt25)
        (self.Pt4,self.Tt4)= self.combuster.get_PnT(self.Pt3,self.Tt3)
        (self.Pt45,self.Tt45)= self.HighTurbine.get_PnT(self.Pt4,self.Tt4)              #Point 4.5
        (self.Pt5,self.Tt5)= self.LowTurbine.get_PnT(self.Pt45,self.Tt45) 

        (self.Pt7,self.Tt7)= (self.Pt5,self.Tt5)                                        #There is no afterburner in ramjet
        (self.Pt8,self.Tt8)= (self.Pt7,self.Tt7)                                        #There is no afterburner in ramjet
        (self.Pt9,self.Tt9)= self.nozzle.get_PnT(self.Pt5,self.Tt5)                     #There is no afterburner in ramjet
        
        (self.Pt13,self.Tt13)= self.fan.get_PnT(self.Pt1,self.Tt1)                      #states 13 and 19 are same as ambient conditions
        (self.Pt19,self.Tt19)= self.fanNozzle.get_PnT(self.Pt13,self.Tt13)              #Pt19 is called in formulaSheet

        self.P9= self.P0 

        gam_c= self.parameters["gam_c"]
        gam_t= self.parameters["gam_t"]
        Rc= self.parameters["Rc"]
        Rt= self.parameters["Rt"]

        #Throat properties at station 8
        M_throat =1
        (self.P_throat,self.T_throat)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9, self.Tt9, M_throat, gam_t)
        
        self.M9= formulaSheet1.get_M_from_Pt_P(self.Pt9/self.P9,gam_t)
        self.M19=self.parameters["M0"]                                                  #M19 is called in formulaSheet 

        #Station properties at engine exit
        (self.P19,self.T19)= formulaSheet1.get_PnT_from_PtTtM(self.Pt19,self.Tt19,self.M19,gam_c)     #Pt19 is called in formulaSheet and is same as ambient conditions
        (self.P9,self.T9)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9,self.Tt9,self.M9,gam_t)
        
        #velocities and velocity ratios
        self.M0= self.parameters["M0"]
        self.a0= formulaSheet1.get_a(gam_c,Rc,self.T0)
        self.v9= formulaSheet1.get_v(gam_t,Rt,self.T9,self.M9)
        self.v0= formulaSheet1.get_v(gam_c,Rc,self.T0,self.M0)
        self.v9_v0= self.v9/self.v0
        self.v9_a0= self.v9/self.a0 
        self.v19= formulaSheet1.get_v(gam_c,Rc,self.T19,self.M19)
        self.v19_a0= self.v19/self.a0

        #general properties
        self.pi_d= self.diffuser.pi_n
        self.tau_r= self.aircraft.get_tau_r()
        self.pi_r= self.aircraft.get_pi_r()
        self.tau_L= self.combuster.get_tau_L()

        #compressor and turbine properties
        self.pi_cL= self.parameters["pi_cL"]
        self.pi_cH= self.parameters["pi_cH"]
        self.pi_c= self.pi_cL*self.pi_cH
        
        self.tau_cL= self.LowCompressor.get_tau_c()
        self.tau_cH= self.HighCompressor.get_tau_c()
        self.tau_c= self.tau_cL*self.tau_cH
        
        self.tau_tL= self.LowTurbine.get_tau_t()
        self.tau_tH= self.HighTurbine.get_tau_t()                                       #equal to 1
        self.tau_t= self.tau_tL*self.tau_tH

        self.pi_tL= self.LowTurbine.get_pi_t()
        self.pi_tH= self.HighTurbine.get_pi_t()                                         #equal to 1
        self.pi_t= self.pi_tL*self.pi_tH

        #pressure and temperature ratios
        self.P0_P9= self.P0/self.P9
        self.Pt9_P9= self.Pt9/self.P9
        self.T9_T0= self.T9/self.T0

        self.M9_M0= self.M9/self.M0

        self.f_CC= self.combuster.get_f()
        self.f= self.f_CC

        self.ST= formulaSheet1.get_ST()
        
        self.TSFC= formulaSheet1.get_TSFC()

        self.eta_t= formulaSheet1.get_eta_t()
        self.eta_p= formulaSheet1.get_eta_p()
        self.eta_o= formulaSheet1.get_eta_o()
        
        return [self.f,self.ST,self.TSFC*1e+6]
    
    def print_get_details(self):
        lst,lst0= [],[]
        lst.append(["a0",self.a0])
        lst.append(["ST",self.ST])
        lst.append(["f_CC",self.f_CC])
        lst.append(["f",self.f])
        lst.append(["TSFC",self.TSFC*1e+6])
        lst.append(["-"*20,"-"*20])
        lst.append(["v9",self.v9])
        lst.append(["v9/a0",self.v9_a0])
        lst.append(["v9/v0",self.v9_v0])
        lst.append(["-"*20,"-"*20])
        lst.append(["tau_L",self.tau_L])
        lst.append(["tau_r",self.tau_r])
        lst.append(["pi_r",self.pi_r])
        lst.append(["M0",self.M0])
        lst.append(["M9",self.M9])
        lst.append(["M9/M0",self.M9_M0])
        lst.append(["-"*20,"-"*20])
        lst.append(["eta_t",self.eta_t])
        lst.append(["eta_p",self.eta_p])
        lst.append(["eta_o",self.eta_o])


        lst0.append(["Static 0",self.P0/1e+3,self.T0])
        lst0.append(["Total 0",self.Pt0/1e+3,self.Tt0])
        lst0.append(["Total 1",self.Pt1/1e+3,self.Tt1])
        lst0.append(["Total 2",self.Pt2/1e+3,self.Tt2])
        lst0.append(["Total 3",self.Pt3/1e+3,self.Tt3])
        lst0.append(["Total 4",self.Pt4/1e+3,self.Tt4])
        lst0.append(["Total 5",self.Pt5/1e+3,self.Tt5])
        lst0.append(["Total 7",self.Pt7/1e+3,self.Tt7])
        lst0.append(["Total 8",self.Pt8/1e+3,self.Tt8])
        lst0.append(["Total 9",self.Pt9/1e+3,self.Tt9])
        lst0.append(["Static 9",self.P9/1e+3,self.T9])

        return lst,lst0
        


    
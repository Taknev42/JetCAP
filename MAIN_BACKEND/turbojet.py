from math import sqrt
from math import pow
from formulaSheet import formulaSheet
# from prettytable import PrettyTable # type: ignore

class turbojet:
    def __init__(self,parameters,aircraft1,fan1,diffuser1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1,LowTurbine1,nozzle1,fanNozzle1,afterBurner1=None):
        self.parameters= parameters
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
 
        (self.Pt2,self.Tt2)= (self.Pt1,self.Tt1)                                        #T0->T1 (diffuser) -> T2 (nothing happens)
        (self.Pt25,self.Tt25)= self.LowCompressor.get_PnT(self.Pt2,self.Tt2)            #Point 2.5
        (self.Pt3,self.Tt3)= self.HighCompressor.get_PnT(self.Pt25,self.Tt25)
        (self.Pt4,self.Tt4)= self.combuster.get_PnT(self.Pt3,self.Tt3)
        (self.Pt45,self.Tt45)= self.HighTurbine.get_PnT(self.Pt4,self.Tt4)              #Point 4.5
        (self.Pt5,self.Tt5)= self.LowTurbine.get_PnT(self.Pt45,self.Tt45) 

        if self.afterBurner:
            (self.Pt7,self.Tt7)= self.afterBurner.get_PnT(self.Pt5,self.Tt5)
            (self.Pt9,self.Tt9)= self.nozzle.get_PnT(self.Pt7,self.Tt7)
        else:
            (self.Pt9,self.Tt9)= self.nozzle.get_PnT(self.Pt5,self.Tt5)

        #Station 13 and 19 are used in the ST calculations and they are same as ambient conditions
        (self.Pt13,self.Tt13)= self.fan.get_PnT(self.Pt1,self.Tt1)                      #T0->T1 (diffuser) -> T13 (fan)
        (self.Pt19,self.Tt19)= self.fanNozzle.get_PnT(self.Pt13,self.Tt13)              #Pt19 is called in formulaSheet

        self.P0_P9= self.parameters["P0_P9"]
        self.P9= self.P0/self.P0_P9

        gam_c= self.parameters["gam_c"]
        gam_t= self.parameters["gam_t"]
        Rc= self.parameters["Rc"]
        Rt= self.parameters["Rt"]
        if self.afterBurner:
            gam_9= self.parameters["gam_ab"]
            R9= self.parameters["Rab"]
            Cp9= self.parameters["Cpab"]
        else:
            gam_9= gam_t
            R9= self.parameters["Rt"]
            Cp9= self.parameters["Cpt"]

        #Throat properties calculation at station 8
        M_throat =1
        (self.P_throat,self.T_throat)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9, self.Tt9, M_throat, gam_9)
        
        self.M9= formulaSheet1.get_M_from_Pt_P(self.Pt9/self.P9,gam_9)
        
        #properties at the engine exit
        self.M19=self.parameters["M0"]                                                                  #M19 is called in formulaSheet 
        (self.P19,self.T19)= formulaSheet1.get_PnT_from_PtTtM(self.Pt19,self.Tt19,self.M19,gam_c)       #station 19 is same as ambient conditions
        (self.P9,self.T9)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9,self.Tt9,self.M9,gam_t)


        #velocity ratio calculations
        self.M0= self.parameters["M0"]
        self.v9= formulaSheet1.get_v(gam_t,R9,self.T9,self.M9)
        self.v0= formulaSheet1.get_v(gam_c,Rc,self.T0,self.M0)
        v19= formulaSheet1.get_v(gam_c,Rc,self.T19,self.M19)                                #v19 is called in formulaSheet
        self.a0= formulaSheet1.get_a(gam_c,Rc,self.T0)
        self.v9_a0= self.v9/self.a0
        self.v9_v0= self.v9/self.v0
        self.v19_a0= v19/self.a0                                                            #v19_a0 is called in get_eta_p() in formulaSheet

        #general properties
        self.pi_d= self.diffuser.pi_n
        self.tau_r= self.aircraft.get_tau_r()
        self.pi_r= self.aircraft.get_pi_r()

        #temperature ratios
        self.tau_L_CC= self.combuster.get_tau_L()
        if self.afterBurner:
            self.tau_L_AB= self.afterBurner.get_tau_L() 
        self.Tt4_T0= self.Tt4/self.T0
        self.Pt9_P9= self.Pt9/self.P9
        self.T9_T0= self.T9/self.T0
        self.Tt4_Tt2= self.Tt4/self.Tt2
        self.M9_M0= self.M9/self.M0
        
        #compressor and turbine properties
        self.pi_cL= self.parameters["pi_cL"]
        self.pi_cH= self.parameters["pi_cH"]
        self.pi_c= self.pi_cL*self.pi_cH
        
        self.tau_cL= self.LowCompressor.get_tau_c()
        self.tau_cH= self.HighCompressor.get_tau_c()
        self.tau_c= self.tau_cL*self.tau_cH
        
        self.tau_tL= self.LowTurbine.get_tau_t()
        self.tau_tH= self.HighTurbine.get_tau_t()
        self.tau_t= self.tau_tL*self.tau_tH

        self.pi_tL= self.LowTurbine.get_pi_t()
        self.pi_tH= self.HighTurbine.get_pi_t()
        self.pi_t= self.pi_tL*self.pi_tH

        self.f_CC= self.combuster.get_f()
        self.f= self.f_CC
        if self.afterBurner:
            self.f_AB=  self.afterBurner.get_f()
            self.f+= self.f_AB
        
        self.ST= formulaSheet1.get_ST()

        self.TSFC= formulaSheet1.get_TSFC()

        self.eta_t= formulaSheet1.get_eta_t()
        self.eta_p= formulaSheet1.get_eta_p()
        self.eta_o= formulaSheet1.get_eta_o()
        
        return [self.f,self.ST,self.TSFC*1e+6]

    def print_get_details(self):
        lst= []
        lst.append(["a0",self.a0])
        lst.append(["ST",self.ST])
        lst.append(["f_CC",self.f_CC])
        if self.afterBurner:
            lst.append(["f_AB",self.f_AB])
        lst.append(["f",self.f])
        lst.append(["TSFC",self.TSFC*1e+6])
        lst.append(["M9",self.M9])
        lst.append(["-"*20,"-"*20])
        lst.append(["pi_d",self.pi_d])
        lst.append(["tau_r",self.tau_r])
        lst.append(["pi_r",self.pi_r])
        lst.append(["tau_L_CC",self.tau_L_CC])
        if self.afterBurner:
            lst.append(["tau_L_AB",self.tau_L_AB])
        lst.append(["-"*20,"-"*20])    
        lst.append(["pi_cL",self.pi_cL])
        lst.append(["pi_cH",self.pi_cH])
        lst.append(["pi_c",self.pi_c])
        lst.append(["tau_cL",self.tau_cL])
        lst.append(["tau_cH",self.tau_cH])
        lst.append(["tau_c",self.tau_c])
        lst.append(["-"*20,"-"*20])
        lst.append(["tau_tL",self.tau_tL])
        lst.append(["tau_tH",self.tau_tH])
        lst.append(["tau_t",self.tau_t])
        lst.append(["pi_tL",self.pi_tL])
        lst.append(["pi_tH",self.pi_tH])
        lst.append(["pi_t",self.pi_t])
        lst.append(["-"*20,"-"*20])
        lst.append(["eta_t",self.eta_t])
        lst.append(["eta_p",self.eta_p])
        lst.append(["eta_o",self.eta_o])
        lst.append(["-"*20,"-"*20])
        lst.append(["v9",self.v9])
        lst.append(["v9_v0",self.v9_v0])
        lst.append(["v0",self.v0])

        lst0=[]
        lst0.append(["Static 0",self.P0/1e+3,self.T0])
        lst0.append(["Total 0",self.Pt0/1e+3,self.Tt0])
        lst0.append(["Total 1",self.Pt1/1e+3,self.Tt1])
        lst0.append(["Total 2",self.Pt2/1e+3,self.Tt2])
        lst0.append(["Total 2.5",self.Pt25/1e+3,self.Tt25])
        lst0.append(["Total 3",self.Pt3/1e+3,self.Tt3])
        lst0.append(["Total 4",self.Pt4/1e+3,self.Tt4])
        lst0.append(["Total 4.5",self.Pt45/1e+3,self.Tt45])
        lst0.append(["Total 5",self.Pt5/1e+3,self.Tt5])
        if self.afterBurner:
            lst0.append(["Total 7",self.Pt7/1e+3,self.Tt7])
        lst0.append(["Total 9",self.Pt9/1e+3,self.Tt9])
        lst0.append(["Static 9",self.P9/1e+3,self.T9])

        return lst,lst0


    



    # def print_get_details(self):
    #     table1= PrettyTable(["PCA result","value"])
    #     table1.add_row(["a0",f"{self.a0:.3f}"])
    #     table1.add_row(["ST",f"{self.ST:.3f}"])
    #     table1.add_row(["f_cc",f"{self.f_CC:.5f}"])
    #     if self.afterBurner:
    #         table1.add_row(["f_ab",f"{self.f_AB:.5f}"])
    #     table1.add_row(["f (m_f/m_0)",f"{self.f:.5f}"])
    #     table1.add_row(["TSFC",f"{self.TSFC*1e+6:.3f}"])
    #     table1.add_row(["M9",f"{self.M9:.3f}"])
    #     table1.add_row(["pi_d",f"{self.pi_d:.3f}"])
    #     table1.add_row(["tau_r",f"{self.tau_r:.3f}"])
    #     table1.add_row(["pi_r",f"{self.pi_r:.3f}"])
    #     table1.add_row(["tau_L_CC",f"{self.tau_L_CC:.3f}"])
    #     if self.afterBurner:
    #         table1.add_row(["tau_L_AB",f"{self.tau_L_AB:.3f}"])
    #     table1.add_row(["tau_cL",f"{self.tau_cL:.3f}"])
    #     table1.add_row(["tau_cH",f"{self.tau_cH:.3f}"])
    #     table1.add_row(["tau_c",f"{self.tau_c:.3f}"])
    #     table1.add_row(["tau_tL",f"{self.tau_tL:.3f}"])
    #     table1.add_row(["tau_tH",f"{self.tau_tH:.3f}"])
    #     table1.add_row(["tau_t",f"{self.tau_t:.3f}"])
    #     table1.add_row(["pi_tL",f"{self.pi_tL:.3f}"])
    #     table1.add_row(["pi_tH",f"{self.pi_tH:.3f}"])
    #     table1.add_row(["pi_t",f"{self.pi_t:.3f}"])
    #     table1.add_row(["v0",f"{self.v0:.3f}"])
    #     table1.add_row(["v9",f"{self.v9:.3f}"])
    #     table1.add_row(["v9/v0",f"{self.v9_v0:.3f}"])
    #     table1.add_row(["eta_t",f"{self.eta_t:.3f}"])
    #     table1.add_row(["eta_p",f"{self.eta_p:.3f}"])
    #     table1.add_row(["eta_o",f"{self.eta_o:.3f}"])


    #     table2= PrettyTable(["Station","Pressure","Temperature"])
    #     table2.add_row(["0",f"{self.P0:.3f}",f"{self.T0:.3f}"])
    #     table2.add_row(["T0",f"{self.Pt0:.3f}",f"{self.Tt0:.3f}"])
    #     table2.add_row(["T1",f"{self.Pt1:.3f}",f"{self.Tt1:.3f}"])
    #     table2.add_row(["T2",f"{self.Pt2:.3f}",f"{self.Tt2:.3f}"])
    #     table2.add_row(["T2.5",f"{self.Pt25:.3f}",f"{self.Tt25:.3f}"])
    #     table2.add_row(["T3",f"{self.Pt3:.3f}",f"{self.Tt3:.3f}"])
    #     table2.add_row(["T4",f"{self.Pt4:.3f}",f"{self.Tt4:.3f}"])
    #     table2.add_row(["T4.5",f"{self.Pt45:.3f}",f"{self.Tt45:.3f}"])
    #     table2.add_row(["T5",f"{self.Pt5:.3f}",f"{self.Tt5:.3f}"])
    #     if self.afterBurner:
    #         table2.add_row(["T7",f"{self.Pt7:.3f}",f"{self.Tt7:.3f}"])
    #     table2.add_row(["T9",f"{self.Pt9:.3f}",f"{self.Tt9:.3f}"])
    #     table2.add_row(["9",f"{self.P9:.3f}",f"{self.T9:.3f}"])
    #     # table2.add_row(["","",""])
    #     # table2.add_row(["T13",f"{self.Pt13:.3f}",f"{self.Tt13:.3f}"])
    #     # table2.add_row(["T19",f"{self.Pt19:.3f}",f"{self.Tt19:.3f}"])
        
    #     print()
    #     print(table1)
    #     print()
    #     print(table2)

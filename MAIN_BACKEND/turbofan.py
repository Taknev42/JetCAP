from math import sqrt
from math import pow
from formulaSheet import formulaSheet

class turbofan:
    def __init__(self,parameters,aircraft1,fan1,diffuser1,LowCompressor1,HighCompressor1,combuster1,HighTurbine1,LowTurbine1,nozzle1,fanNozzle1,mixer1=None,afterBurner1=None):
        self.parameters= parameters
        self.aircraft= aircraft1
        self.fan= fan1
        self.diffuser= diffuser1
        self.LowCompressor= LowCompressor1
        self.HighCompressor= HighCompressor1
        self.combuster= combuster1
        self.HighTurbine= HighTurbine1
        self.LowTurbine= LowTurbine1
        self.mixer= mixer1
        self.nozzle= nozzle1
        self.fanNozzle= fanNozzle1
        self.afterBurner= afterBurner1

    def get_engineDetails(self):        
        formulaSheet1= formulaSheet(self)

        if self.mixer:                      #case for mixed exhaust turbofan
            self.P0= self.parameters["P0"]
            self.T0= self.parameters["T0"]

            self.Pt0= self.P0*self.aircraft.get_pi_r()
            self.Tt0= self.T0*self.aircraft.get_tau_r()
            self.Pt1,self.Tt1= self.diffuser.get_PnT(self.Pt0,self.Tt0)

            (self.Pt2,self.Tt2)= (self.Pt1,self.Tt1)                                        #T0->T1 (diffuser) -> T2 (nothing happens)
            (self.Pt25,self.Tt25)= self.LowCompressor.get_PnT(self.Pt2,self.Tt2)            #Point 2.5
            (self.Pt3,self.Tt3)= self.HighCompressor.get_PnT(self.Pt25,self.Tt25)
            (self.Pt4,self.Tt4)= self.combuster.get_PnT(self.Pt3,self.Tt3)
            (self.Pt45,self.Tt45)= self.HighTurbine.get_PnT(self.Pt4,self.Tt4)              #Point 4.5
            (self.Pt5,self.Tt5)= self.LowTurbine.get_PnT(self.Pt45,self.Tt45) 
            (self.Pt6,self.Tt6)= (self.Pt5,self.Tt5)                                        #T5->T6 (no change in state)
            (self.Pt6A,self.Tt6A)= self.mixer.get_PnT(self.Pt6,self.Tt6)                    #T6->T6A (mixer)

            if self.afterBurner:
                (self.Pt7,self.Tt7)= self.afterBurner.get_PnT(self.Pt6A,self.Tt6A)
            else:
                (self.Pt7,self.Tt7)= (self.Pt6A,self.Tt6A)
            (self.Pt9,self.Tt9)= self.nozzle.get_PnT(self.Pt7,self.Tt7)                     #equal to state T19
            

            (self.Pt13,self.Tt13)= self.fan.get_PnT(self.Pt1,self.Tt1)                      #T0->T1 (diffuser) -> T13 (fan)
            (self.Pt16,self.Tt16)= (self.Pt13,self.Tt13)                                    #T13->T16 (no change in state)
            #After State 16 we have common flow, so we don't need to calculate the properties of the flow after this point


            if self.afterBurner:
                gam_9= self.parameters["gam_ab"]
                Cp9= self.parameters["Cpab"]
                R9= self.parameters["Rab"]
            else:
                gam_9= self.parameters["gam_t"]
                Cp9= self.parameters["Cpt"]
                R9= self.parameters["Rt"]
            gam_c= self.parameters["gam_c"]
            gam_t= self.parameters["gam_t"]
            Rc= self.parameters["Rc"]
            Rt= self.parameters["Rt"]

            self.tau_r= self.aircraft.get_tau_r()
            self.pi_r= self.aircraft.get_pi_r()
            self.pi_d= self.diffuser.pi_n

            self.alp= self.parameters["alp"] 

            #fan and compressor properties
            self.pi_f= self.parameters["pi_f"]
            self.pi_cL= self.parameters["pi_cL"]
            self.pi_cH= self.parameters["pi_cH"]
            self.pi_c= self.pi_cL*self.pi_cH

            self.tau_f= self.fan.get_tau_c()
            self.tau_cL= self.LowCompressor.get_tau_c()
            self.tau_cH= self.HighCompressor.get_tau_c()
            self.tau_c= self.tau_cL*self.tau_cH

            #Turbine properties
            self.tau_tL= self.LowTurbine.get_tau_t()
            self.tau_tH= self.HighTurbine.get_tau_t()
            self.tau_t= self.tau_tL*self.tau_tH

            self.pi_tL= self.LowTurbine.get_pi_t()
            self.pi_tH= self.HighTurbine.get_pi_t()
            self.pi_t= self.pi_tL*self.pi_tH

            #mixer properties
            self.tau_m= self.mixer.get_tau_m()
            self.pi_m= self.mixer.get_pi_m()
            
            #M9 calculation
            pi_ab= self.parameters["pi_ab"]
            pi_n= self.parameters["pi_n"]
            pi_b= self.parameters["pi_b"]
            pi_fn= self.parameters["pi_fn"]

            if self.parameters["AB"]=="Y":     
                self.Pt9_P0= pi_n*pi_ab*self.pi_m*self.pi_tL*self.pi_tH*pi_b*self.pi_cL*self.pi_cH*self.pi_d*self.pi_r
            else: 
                self.Pt9_P0= pi_n*self.pi_m*self.pi_tL*self.pi_tH*pi_b*self.pi_cL*self.pi_cH*self.pi_d*self.pi_r
   
            if self.parameters["nozzleType"]=="CD":
                self.P0_P9= self.parameters["P0_P9"]
                self.Pt9_P9= self.Pt9_P0*self.P0_P9

                self.M9= formulaSheet1.get_M_from_Pt_P(self.Pt9_P9,gam_9)
            
            elif self.parameters["nozzleType"]=="C":                                #It is a converging nozzle. M9= M8= 1 at choking
                if self.Pt9_P0 >= pow((gam_9+1)/2, gam_9/(gam_9-1)):                #choked flow condition
                    self.P0_P9= pow((gam_9+1)/2, gam_9/(gam_9-1))/self.Pt9_P0       #<1 P9 is underexpanded                                       
                else:                                                               #unchoked flow condition
                    self.P0_P9= 1                                                   #=1 P9 is fully expanded
                
                self.Pt9_P9= self.Pt9_P0*self.P0_P9                                            
                self.M9= formulaSheet1.get_M_from_Pt_P(self.Pt9_P9,gam_9)

            
            #Static Properties at the nozzle exit
            (self.P9,self.T9)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9,self.Tt9,self.M9,gam_9)

            #Throat properties at station 8
            M8 =1
            (self.P8,self.T8)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9, self.Tt9, M8, gam_9)

            #velocities and velocity ratios
            self.M0= self.parameters["M0"]
            self.a0= formulaSheet1.get_a(gam_c,Rc,self.T0)
            self.v0= formulaSheet1.get_v(gam_c,Rc,self.T0,self.M0)
            self.v9= formulaSheet1.get_v(gam_9,R9,self.T9,self.M9)
            self.v9_a0= self.v9/self.a0
            self.v9_v0= self.v9/self.v0
            self.v19_a0= self.v9_a0                                         #called in the get_eta_p() and get_eta_t() in formula sheet

            #temperature and pressure ratios
            self.tau_L= self.combuster.get_tau_L()
            self.tau_L_CC= self.combuster.get_tau_L()
            if self.afterBurner:
                self.tau_L_AB= self.afterBurner.get_tau_L()
            self.Tt4_T0= self.Tt4/self.T0
            self.P0_P9= self.P0/self.P9
            self.Pt9_P9= self.Pt9/self.P9
            self.T9_T0= self.T9/self.T0

            M9_M0= self.M9/self.M0

            self.f_CC= self.combuster.get_f()
            self.f= self.f_CC
            if self.afterBurner:
                self.f_AB=  self.afterBurner.get_f()
                self.f+= self.f_AB

            self.ST= formulaSheet1.get_ST_single_exhaust()

            self.TSFC= formulaSheet1.get_TSFC()

            self.eta_t= formulaSheet1.get_eta_t()
            self.eta_p= formulaSheet1.get_eta_p()
            self.eta_o= formulaSheet1.get_eta_o()

            return [self.f,self.ST,self.TSFC*1e+6]

        else: #case for seperate exhaust turbofan
            self.P0= self.parameters["P0"]
            self.T0= self.parameters["T0"]

            self.Pt0= self.P0*self.aircraft.get_pi_r()
            self.Tt0= self.T0*self.aircraft.get_tau_r()

            self.Pt1,self.Tt1= self.diffuser.get_PnT(self.Pt0,self.Tt0)

            (self.Pt2,self.Tt2)= (self.Pt1,self.Tt1)                                        #state T1 -> T2 (no change in state)
            (self.Pt25,self.Tt25)= self.LowCompressor.get_PnT(self.Pt2,self.Tt2)            #Point 2.5
            (self.Pt3,self.Tt3)= self.HighCompressor.get_PnT(self.Pt25,self.Tt25)
            (self.Pt4,self.Tt4)= self.combuster.get_PnT(self.Pt3,self.Tt3)
            (self.Pt45,self.Tt45)= self.HighTurbine.get_PnT(self.Pt4,self.Tt4)              #Point 4.5
            (self.Pt5,self.Tt5)= self.LowTurbine.get_PnT(self.Pt45,self.Tt45) 
            (self.Pt6,self.Tt6)= (self.Pt5,self.Tt5)                                        #State T5 -> T6 (no change in state)

            (self.Pt7,self.Tt7)= (self.Pt5,self.Tt5)                                        #for seperate flow turbofan dont have AB
            (self.Pt9,self.Tt9)= self.nozzle.get_PnT(self.Pt7,self.Tt7)
            
            (self.Pt13,self.Tt13)= self.fan.get_PnT(self.Pt0,self.Tt0)
            (self.Pt16,self.Tt16)= (self.Pt13,self.Tt13)                                    #T13->T16 (no change in state)
            (self.Pt19,self.Tt19)= self.fanNozzle.get_PnT(self.Pt13,self.Tt13)


            #general properties
            self.tau_r= self.aircraft.get_tau_r()
            self.pi_r= self.aircraft.get_pi_r()
            self.pi_d= self.diffuser.pi_n

            self.alp= self.parameters["alp"]
            
            #fan and compressor properties
            self.pi_f= self.parameters["pi_f"]
            self.pi_cL= self.parameters["pi_cL"]
            self.pi_cH= self.parameters["pi_cH"]
            self.pi_c= self.pi_cL*self.pi_cH

            self.tau_f= self.fan.get_tau_c()
            self.tau_cL= self.LowCompressor.get_tau_c()
            self.tau_cH= self.HighCompressor.get_tau_c()
            self.tau_c= self.tau_cL*self.tau_cH
            
            #turbine properties
            self.tau_tL= self.LowTurbine.get_tau_t()
            self.tau_tH= self.HighTurbine.get_tau_t()
            self.tau_t= self.tau_tL*self.tau_tH

            self.pi_tL= self.LowTurbine.get_pi_t()
            self.pi_tH= self.HighTurbine.get_pi_t()
            self.pi_t= self.pi_tL*self.pi_tH
            
            #M9 calculation
            pi_n= self.parameters["pi_n"]
            pi_b= self.parameters["pi_b"]
            pi_fn= self.parameters["pi_fn"]
            gam_c= self.parameters["gam_c"]
            gam_t= self.parameters["gam_t"]
            Rc= self.parameters["Rc"]
            Rt= self.parameters["Rt"]
                                                                    
            self.Pt9_P0= pi_n*self.pi_tL*self.pi_tH*pi_b*self.pi_cL*self.pi_cH*self.pi_d*self.pi_r    

            if self.parameters["nozzleType"]=="CD":
                self.P0_P9= self.parameters["P0_P9"]
                self.Pt9_P9= self.Pt9_P0*self.P0_P9

                self.M9= formulaSheet1.get_M_from_Pt_P(self.Pt9_P9,gam_t)
            
            elif self.parameters["nozzleType"]=="C":                                #It is a converging nozzle. M9= M8= 1 at choking
                if self.Pt9_P0 >= pow((gam_t+1)/2, gam_t/(gam_t-1)):                #choked flow condition
                    self.P0_P9= pow((gam_t+1)/2, gam_t/(gam_t-1))/self.Pt9_P0       #<1 P9 is underexpanded                                       
                else:                                                               #unchoked flow condition
                    self.P0_P9= 1                                                   #=1 P9 is fully expanded
                
                self.Pt9_P9= self.Pt9_P0*self.P0_P9                                            
                self.M9= formulaSheet1.get_M_from_Pt_P(self.Pt9_P9,gam_t)

            #M19 calculation
            self.pi_f= self.parameters["pi_f"]

            self.Pt19_P0= self.pi_r*self.pi_d*self.pi_f*pi_fn
            
            if self.parameters["nozzleType"]=="CD":
                self.P0_P19= self.parameters["P0_P19"]
                self.Pt19_P19= self.Pt19_P0*self.P0_P19

                self.M19= formulaSheet1.get_M_from_Pt_P(self.Pt19_P19,gam_c) 

            elif self.parameters["nozzleType"]=="C":
                if self.Pt19_P0 >= pow((gam_c+1)/2, gam_c/(gam_c-1)):                #choked flow condition
                    self.P0_P19= pow((gam_c+1)/2, gam_c/(gam_c-1))/self.Pt19_P0      #<1 P19 is underexpanded
                else:                                                                #unchoked flow condition
                    self.P0_P19= 1                                                   #=1 P19 is fully expanded  
                self.Pt19_P19= self.Pt19_P0*self.P0_P19

                self.M19= formulaSheet1.get_M_from_Pt_P(self.Pt19_P19,gam_c)
            
            #station properties at the engine exit
            (self.P9,self.T9)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9,self.Tt9,self.M9,gam_t)
            (self.P19,self.T19)= formulaSheet1.get_PnT_from_PtTtM(self.Pt19,self.Tt19,self.M19,gam_c)


            #Throat properties at station 8
            M8 =1
            (self.P8,self.T8)= formulaSheet1.get_PnT_from_PtTtM(self.Pt9, self.Tt9, M8, gam_t)

            #velocities and velocity ratios
            self.M0= self.parameters["M0"]
            self.a0= formulaSheet1.get_a(gam_c,Rc,self.T0)
            self.v0= formulaSheet1.get_v(gam_c,Rc,self.T0,self.M0)
            self.v9= formulaSheet1.get_v(gam_t,Rt,self.T9,self.M9)
            self.v9_a0= self.v9/self.a0
            self.v9_v0= self.v9/self.v0
            self.v19= formulaSheet1.get_v(gam_c,Rc,self.T19,self.M19)
            self.v19_a0= self.v19/self.a0
            self.v19_v0= self.v19/self.v0

            #temperature and pressure ratios
            self.tau_L= self.combuster.get_tau_L()
            self.tau_L_CC= self.combuster.get_tau_L()
            self.Tt4_T0= self.Tt4/self.T0
            self.Pt19_P19= self.Pt19/self.P19
            self.P0_P9= self.P0/self.P9
            self.Pt9_P9= self.Pt9/self.P9
            self.T9_T0= self.T9/self.T0
            self.M9_M0= self.M9/self.M0
            self.Pt19_P0= self.Pt19/self.P0
            self.Tt19_T0= self.Tt19/self.T0
            self.P0_P19= self.P0/self.P19


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
        if self.afterBurner:
            lst.append(["f_AB",self.f_AB])
        lst.append(["f",self.f])
        lst.append(["TSFC",self.TSFC*1e+6])
        lst.append(["-"*20,"-"*20])
        lst.append(["alp",self.alp])
        lst.append(["Opt. Alpha",self.opt_alp()])
        lst.append(["Opt. pi_f",self.opt_pi_f()])
        lst.append(["M9",self.M9])
        if self.mixer ==None:
            lst.append(["M19",self.M19])
        lst.append(["P0_P9",self.P0_P9])
        if self.mixer == None:
            lst.append(["P0_P19",self.P0_P19])
        lst.append(["pi_d",self.pi_d])
        lst.append(["tau_r",self.tau_r])
        lst.append(["pi_r",self.pi_r])
        lst.append(["tau_L",self.tau_L])
        lst.append(["-"*20,"-"*20])
        lst.append(["pi_f",self.pi_f])
        lst.append(["pi_cL",self.pi_cL]) 
        lst.append(["pi_cH",self.pi_cH])     
        lst.append(["tau_f",self.tau_f])
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



        lst0.append(["Static 0",self.P0/1e+3,self.T0])
        lst0.append(["Total 0",self.Pt0/1e+3,self.Tt0])
        lst0.append(["Total 1",self.Pt1/1e+3,self.Tt1])
        lst0.append(["Total 2",self.Pt2/1e+3,self.Tt2])
        lst0.append(["Total 2.5",self.Pt25/1e+3,self.Tt25])
        lst0.append(["Total 3",self.Pt3/1e+3,self.Tt3])
        lst0.append(["Total 4",self.Pt4/1e+3,self.Tt4])
        lst0.append(["Total 4.5",self.Pt45/1e+3,self.Tt45])
        lst0.append(["Total 5",self.Pt5/1e+3,self.Tt5])
        lst0.append(["Total 6",self.Pt6/1e+3,self.Tt6])
        if self.mixer !=None:
            lst0.append(["Total 6A",self.Pt6A/1e+3,self.Tt6A])
        lst0.append(["Total 7",self.Pt7/1e+3,self.Tt7])
        lst0.append(["Total 9",self.Pt9/1e+3,self.Tt9])
        lst0.append(["Static 9",self.P9/1e+3,self.T9])
        lst0.append([" "," "," "])
        lst0.append(["Total 1",self.Pt1/1e+3,self.Tt1])
        lst0.append(["Total 13",self.Pt13/1e+3,self.Tt13])
        if self.mixer ==None:
            lst0.append(["Total 16",self.Pt16/1e+3,self.Tt16])
            lst0.append(["Total 19",self.Pt19/1e+3,self.Tt19])
            lst0.append(["Static 19",self.P19/1e+3,self.T19])
        
        return lst,lst0
        
    
    def opt_alp(self):
        if hasattr(self,"alp_opt"):
            return self.alp_opt
        
        tau_r= self.tau_r
        tau_f= self.tau_f
        tau_L= self.tau_L
        tau_c= self.tau_c
        term1 = 1/(tau_r*(tau_f-1))
        term2 = tau_L - tau_r*(tau_c-1) - tau_L/(tau_r*tau_c) - 0.25*((sqrt(tau_r*tau_f-1) + sqrt(tau_r-1))**2)

        self.alp_opt = term1*term2
        return self.alp_opt
    
    def opt_pi_f(self):
        if hasattr(self,"pi_f_opt"):
            return self.pi_f_opt
        
        tau_r= self.tau_r
        tau_f= self.tau_f
        tau_L= self.tau_L
        tau_c= self.tau_c
        alp = self.parameters["alp"]
        term1 = tau_L - tau_r*(tau_c-1) - tau_L/(tau_r*tau_c) + alp*tau_r + 1
        term2 = tau_r*(1+alp)
        tau_f_opt = term1/term2

        self.pi_f_opt = self.fan.get_pi_c(tau_f_opt)

        return self.pi_f_opt









    





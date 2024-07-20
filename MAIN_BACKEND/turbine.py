from math import pow

class turbine:
    def __init__(self,eta_m,peta_t,aircraft,fan,LowCompressor,HighCompressor,combustor,HighTurbine=None):
        self.eta_m= eta_m
        self.peta_t= peta_t
        self.aircraft= aircraft
        self.fan= fan
        self.LowCompressor= LowCompressor
        self.HighCompressor= HighCompressor
        self.combustor= combustor
        self.HighTurbine= HighTurbine

    def get_tau_t(self):
        if hasattr(self,"tau_t"):
            return self.tau_t

        tau_r= self.aircraft.get_tau_r()
        tau_L= self.combustor.get_tau_L()
        tau_lpc= self.LowCompressor.get_tau_c()
        tau_hpc= self.HighCompressor.get_tau_c()
        alp= self.aircraft.alp
        tau_f= self.fan.get_tau_c()
        eta_m= self.eta_m
        f_cc= self.combustor.get_f()


        if self.HighTurbine== None:  #if HPT is not been made that means this is a HPT bcz HPT is made before LPT
            #here tau_t powers only the HPC 
            #High pressure Turbine
            t1= tau_lpc*tau_r*(tau_hpc-1)
            t2= eta_m*tau_L*(1+f_cc*(1+alp))
            self.tau_t= 1- t1/t2
        
            return self.tau_t
        
        elif self.HighTurbine !=None:  #if HPT has been provided that means this is a LPT bcz LPT is made after HPT
            # here tau_t powers both fan and LPC 
            #Low pressure Turbine
            tau_hpt= self.HighTurbine.get_tau_t()

            t1= tau_r/tau_L
            t2= eta_m*tau_hpt*(1+f_cc*(1+alp))                     #accurate formula
            # t2= eta_m*tau_hpt                         #PARA assumption             
            t3= tau_lpc-1 +alp*(tau_f-1)
            self.tau_t= 1- t1*t3/t2

            return self.tau_t


    def get_pi_t(self):
        if hasattr(self,"pi_t"):
            return self.pi_t
        
        gam_t= self.aircraft.fuel.gam_t
        peta_t= self.peta_t
        tau_t= self.get_tau_t()

        gam_term= gam_t/((gam_t-1)*peta_t)
        self.pi_t= pow(tau_t,gam_term)

        return self.pi_t
    
    def get_PnT(self,Pt_in,Tt_in):
        Pt_out= self.get_pi_t()*Pt_in
        Tt_out= self.get_tau_t()*Tt_in

        return (Pt_out,Tt_out)
    

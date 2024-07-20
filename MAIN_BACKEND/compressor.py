class compressor:
    def __init__(self,pi_c,peta_c,aircraft):
        self.pi_c= pi_c
        self.peta_c=peta_c
        self.aircraft= aircraft

    def get_tau_c(self):    
        if hasattr(self,"tau_c"):
            return self.tau_c
        
        gam_c= self.aircraft.fuel.gam_c
        peta_c= self.peta_c
        pi_c= self.pi_c

        gam_term= (gam_c-1)/(gam_c*peta_c) 
        self.tau_c= pow(pi_c,gam_term)
        return self.tau_c
    
    def get_pi_c(self,tau_c):
        if hasattr(self,"pi_c"):
            return self.pi_c
        
        gam_c= self.aircraft.fuel.gam_c
        peta_c= self.peta_c

        gam_term = gam_c*peta_c/(gam_c -1)
        self.pi_c= pow(tau_c,gam_term)

        return self.pi_c

    
    def get_PnT(self,Pt_in,Tt_in):
        Pt_out= self.pi_c*Pt_in
        Tt_out= self.get_tau_c()*Tt_in

        return (Pt_out, Tt_out)
    
    
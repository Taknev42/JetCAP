"""class to store all the aircraft and fuel/air properties"""

from math import sqrt
class aircraft:
    def __init__(self,M0,alp,atm,fuel):
        self.M0= M0
        self.alp=alp
        self.atm= atm
        self.fuel= fuel

    def get_tau_r(self):
        if hasattr(self,"tau_r"):
            return self.tau_r
        gam_c= self.fuel.gam_c
        M0= self.M0

        self.tau_r= 1+0.5*(gam_c-1)*pow(M0,2)
        return self.tau_r
    
    def get_pi_r(self):
        if hasattr(self,"pi_r"):
            return self.pi_r
        
        gam_c= self.fuel.gam_c
        gam_term= gam_c/(gam_c-1)
        self.pi_r= pow(self.get_tau_r(),gam_term)
        return self.pi_r
    





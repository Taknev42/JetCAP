#mixer class is used only in mixed exhausts turbofan engines
#pi_m is the mixer pressure ratio and is constant
#tau_m is calculated based on the bypass ratio and pi_m

from turbofan_mixed_alp_calculation import get_mf_CC_mc
from math import pow,sqrt

class mixer:
    def __init__(self,parameters,aircraft,fan,diffuser,LowCompressor,HighCompressor,combuster,HighTurbine,LowTurbine):
        self.parameters= parameters
        self.aircraft= aircraft
        self.fan= fan
        self.diffuser= diffuser
        self.LowCompressor= LowCompressor
        self.HighCompressor= HighCompressor
        self.combuster= combuster
        self.HighTurbine= HighTurbine
        self.LowTurbine= LowTurbine

    def get_tau_m(self):
        if hasattr(self,"tau_m"):
            return self.tau_m
        
        T0 = self.parameters["T0"]
        M0 = self.parameters["M0"]
        alp= self.parameters["alp"]
        gam_c = self.parameters["gam_c"]
        Cpc = self.parameters["Cpc"]
        Cpt = self.parameters["Cpt"]
        Rc= self.parameters["Rc"]
        Rt= self.parameters["Rt"]
        Hpr = self.parameters["Hpr"]
        Tt4 = self.parameters["Tt4"]
        eta_b = self.parameters["eta_b"]
        pi_c= self.parameters["pi_c"]
        peta_c= self.parameters["peta_c"]
        pi_f= self.parameters["pi_f"]
        pi_cL= self.parameters["pi_cL"]
        pi_b= self.parameters["pi_b"]

        
        pi_t= self.LowTurbine.get_pi_t()*self.HighTurbine.get_pi_t()

        mf_CC_mc= get_mf_CC_mc(T0,M0,gam_c,Cpc,Cpt,Hpr,Tt4,pi_c,eta_b,peta_c)   

        self.alp_dash= alp/(1+mf_CC_mc)
        alp_dash= self.alp_dash

        Cp6A= (Cpt+alp_dash*Cpc)/(1+alp_dash)

        self.R6A= (Rt+alp_dash*Rc)/(1+alp_dash)

        self.gam_6A= Cp6A/(Cp6A-self.R6A)

        tau_r= self.aircraft.get_tau_r()
        tau_f= self.fan.get_tau_c()
        tau_t= self.LowTurbine.get_tau_t()*self.HighTurbine.get_tau_t()
        self.Tt16_Tt6= T0*tau_r*tau_f/(Tt4*tau_t)

        num= Cpt*(1+alp_dash*(Cpc/Cpt)*(self.Tt16_Tt6))
        den= Cp6A*(1+alp_dash)
        self.tau_m= num/den

        return self.tau_m
    
    def phi(self,gam,M):
        num= M**2*(1+0.5*(gam-1)*M**2)
        den= pow(1+gam*M**2,2)
        phi= num/den

        return phi
    
    def MFP(self,gam,R,M):
        MFP= M*sqrt(gam/R)*pow(1+0.5*(gam-1)*M**2,-(gam+1)/(2*(gam-1)))

        return MFP
    
    def get_pi_m(self):
        if hasattr(self,"pi_m"):
            return self.pi_m
        
        gam_c= self.parameters["gam_c"]
        gam_t= self.parameters["gam_t"]
        Rc= self.parameters["Rc"]
        Rt= self.parameters["Rt"]
        pi_f= self.parameters["pi_f"]
        pi_c= self.parameters["pi_c"]
        pi_b= self.parameters["pi_b"]
        pi_m_max= self.parameters["pi_m_max"]
        pi_t= self.LowTurbine.get_pi_t()*self.HighTurbine.get_pi_t()
        M6= self.parameters["M6"]

        if pi_m_max !="NA":
            Pt16_Pt6= pi_f/(pi_c*pi_b*pi_t)
            
            in_term= Pt16_Pt6*pow((1+0.5*(gam_t-1)*M6**2),gam_t/(gam_t-1))
            M16= pow((2/(gam_c-1))*(pow(in_term,(gam_c-1)/gam_c)-1),0.5)

            phi_6= self.phi(gam_t,M6)

            phi_16= self.phi(gam_c,M16)

            tau_m= self.get_tau_m()
            num= 1+self.alp_dash
            den1= 1/sqrt(phi_6)
            den2= self.alp_dash*sqrt(Rc*gam_t*self.Tt16_Tt6/(Rt*gam_c*phi_16))
            cap_phi= pow(num/(den1+den2),2)*(self.R6A*gam_t*tau_m/(Rt*self.gam_6A))

            M6A= sqrt(2*cap_phi/(1-2*self.gam_6A*cap_phi+sqrt(1-2*(self.gam_6A+1)*cap_phi)))

            num= self.alp_dash*sqrt(self.Tt16_Tt6)
            den= M16*sqrt((gam_c*Rt*(1+0.5*(gam_c-1)*M16**2))/(gam_t*Rc*(1+0.5*(gam_t-1)*M6**2)))/M6
            A16_A6= num/den

            pi_m_ideal= (1+self.alp_dash)*sqrt(tau_m)*self.MFP(gam_t,Rt,M6)/((1+A16_A6)*self.MFP(self.gam_6A,self.R6A,M6A))

            self.pi_m= pi_m_max*pi_m_ideal

        else:                                     #bcz for real mixed_exhaust turbofan, pi_m is 1 
            self.pi_m= 1

        return self.pi_m
    
    def get_PnT(self,Pt_in,Tt_in):
        Pt_out= self.get_pi_m()*Pt_in
        Tt_out= self.get_tau_m()*Tt_in

        return (Pt_out,Tt_out)


    



    
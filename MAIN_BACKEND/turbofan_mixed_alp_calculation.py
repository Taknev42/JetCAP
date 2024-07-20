"""This file is used to calculate alp for a mixed_exhaust turbofan engine, which can be used to initialise the engine in initialisingComponents.py"""
from math import sqrt,pow

def turbofan_mixed_alp_calculation(T0,P0,M0,gam_c,gam_t,Cpc,Cpt,Hpr,Tt4,eta_b,eta_m,pi_f,pi_c,pi_cL,pi_cH,pi_b,peta_f,peta_c,peta_t):

    mf_CC_mc= get_mf_CC_mc(T0,M0,gam_c,Cpc,Cpt,Hpr,Tt4,pi_c,eta_b,peta_c)

    tau_r= get_tau_r(gam_c,M0)
    tau_cL= get_tau_c(gam_c,pi_cL,peta_c)
    tau_cH= get_tau_c(gam_c,pi_cH,peta_c)
    tau_L= get_tau_lambda(Cpc,Cpt,T0,Tt4)
    tau_tH= 1- tau_r*tau_cL*(tau_cH-1)/(tau_L*eta_m*(1+mf_CC_mc))

    tau_t= pow(pi_f/(pi_b*pi_c),peta_t*(gam_t-1)/gam_t)

    tau_tL= tau_t/tau_tH

    tau_f= get_tau_c(gam_c,pi_f,peta_f)

    term1= (1-tau_tL)*tau_tH*tau_L*eta_m*(1+mf_CC_mc)/(tau_r*(tau_f-1))
    term2= (1-tau_cL)/(tau_f-1)
    alp= term1+ term2

    return alp

def get_mf_CC_mc(T0,M0,gam_c,Cpc,Cpt,Hpr,Tt4,pi_c,eta_b,peta_c):
    
    Tt3= T0*get_tau_r(gam_c,M0)*get_tau_c(gam_c,pi_c,peta_c)
    ht4= Cpt*Tt4
    ht3= Cpc*Tt3
    mf_CC_m_c= (ht4-ht3)/(eta_b*Hpr- ht4)

    return mf_CC_m_c

def get_tau_c(gam_c,pi_c,peta_c):
    tau_c= pow(pi_c,(gam_c-1)/(gam_c*peta_c))

    return tau_c

def get_tau_r(gam_c,M0):
    tau_r= 1+ 0.5*(gam_c-1)*pow(M0,2)

    return tau_r

def get_tau_lambda(Cpc,Cpt,T0,Tt4):
    tau_L= Cpt*Tt4/(Cpc*T0)

    return tau_L
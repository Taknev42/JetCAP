"""This file is used for Engine Performance Analysis(EPA) testing. You input the reference engine(at design point) and get out the off-design point"""

from initialisingParameters import initialisingParameters
from initialisingComponents_file import initialisingComponents
from math import sqrt,pow
import numpy as np
# import sympy as sym
# from scipy.optimize import fsolve   # type: ignore

class EPAtesting_class:                                       #class for testing the engine except for mixed flow turbofans
    def __init__(self,refEngine,m_dot_R,lst):
        self.refEngine= refEngine
        self.m_dot_R= m_dot_R                           #reference engine mass flow rate is inputted
        [self.T0,self.P0,self.M0,self.Tt4]= lst


    def MFP(self,gam,R,M):
        MFP1 = sqrt(gam/R)*M*((1+((gam-1)/2)*(M**2))**(-(gam+1)/(2*(gam-1))))

        return MFP1
    
    def get_testEngine_m_dot_T(self):
        
        refEngine= self.refEngine
        [f_R,ST_R,TSFC_R]= refEngine.get_engineDetails()

        #Thrust of refEngine
        Thrust_ref= ST_R*self.m_dot_R

        engineType= refEngine.parameters["engineType"]
        AB= refEngine.parameters["AB"]
        T0_R=refEngine.parameters["T0"]
        P0_R=refEngine.parameters["P0"]
        M0_R=refEngine.parameters["M0"]
        M6=refEngine.parameters["M6"]
        alp_R=refEngine.parameters["alp"]
        gam_c=refEngine.parameters["gam_c"]
        gam_t=refEngine.parameters["gam_t"]
        gam_ab=refEngine.parameters["gam_ab"]
        Rc=refEngine.parameters["Rc"]
        Rt=refEngine.parameters["Rt"]
        Rab=refEngine.parameters["Rab"]
        Cpc=refEngine.parameters["Cpc"]
        Cpt=refEngine.parameters["Cpt"]
        Cpab=refEngine.parameters["Cpab"]
        Hpr=refEngine.parameters["Hpr"]
        Tt4_R=refEngine.parameters["Tt4"]
        Tt7=refEngine.parameters["Tt7"]
        eta_b=refEngine.parameters["eta_b"]
        eta_m=refEngine.parameters["eta_m"]
        eta_ab=refEngine.parameters["eta_ab"]
        pi_d_R= refEngine.pi_d
        pi_d_max=refEngine.parameters["pi_d_max"]
        pi_f_R=refEngine.parameters["pi_f"]
        pi_c_R=refEngine.parameters["pi_c"]
        tau_cL_R= refEngine.tau_cL
        pi_cL_R=refEngine.parameters["pi_cL"]
        pi_cH_R=refEngine.parameters["pi_cH"]
        pi_b=refEngine.parameters["pi_b"]
        pi_m_max=refEngine.parameters["pi_m_max"]
        pi_ab=refEngine.parameters["pi_ab"]
        pi_n=refEngine.parameters["pi_n"]
        pi_fn=refEngine.parameters["pi_fn"]
        peta_f=refEngine.parameters["peta_f"]
        peta_c=refEngine.parameters["peta_c"]
        peta_t=refEngine.parameters["peta_t"]
        P0_P9_R= refEngine.parameters["P0_P9"]
        P0_P19_R= refEngine.parameters["P0_P19"]
        sep_mixed_flow= refEngine.parameters["sep_mixed_flow"]
        nozzleType= refEngine.parameters["nozzleType"]

        tau_tL_R = refEngine.tau_tL
        pi_tL_R = refEngine.pi_tL
        tau_cH_R = refEngine.tau_cH
        pi_tH_R = refEngine.pi_tH

        tau_r_R= refEngine.tau_r
        pi_r_R= refEngine.pi_r
        Tt4_T0_R = refEngine.Tt4/refEngine.T0
        M19_R = refEngine.M19
        M9_R = refEngine.M9

        #making the off-design point
        [T0,P0,M0,Tt4]= [self.T0,self.P0,self.M0,self.Tt4]

        #calculating the values of tau_tL, M9, M19, tau_f, tau_hpc, alp using Mattingly's iteration scheme
        Tt4_T0 = Tt4/T0

        eta_r = 1 if M0<1 or pi_d_max==1 else 1- 0.075*((M0-1)**1.35)
        pi_d= pi_d_max*eta_r

        tau_r = 1 + ((gam_c-1)/2)*(M0**2)
        pi_r = tau_r**(gam_c/(gam_c-1))

        if engineType=="turbofan":
            tau_f_R= refEngine.tau_f

            # initializing tau_f, pi_tL, and tau_tL using the reference parameters
            tau_f = tau_f_R
            # tau_cL= tau_cL_R       #bcz we sometime back we tried taking pi_cL as our main iterting parameter
            tau_tL = tau_tL_R
            pi_tL = pi_tL_R
            pi_tH = pi_tH_R

            tau_tL_1= np.Inf

            # print("\n\n\nStarting the iteration for the test engine\n\n\n")

            num_iter=0
            er=0.00001                              #tolerance
            while abs(tau_tL_1 - tau_tL) > er :
                
                tau_cH = 1 + (Tt4_T0/Tt4_T0_R)*(tau_r_R*tau_f_R/(tau_r*tau_f))*(tau_cH_R-1)
                # tau_cH = 1 + (Tt4_T0/Tt4_T0_R)*(tau_r_R*tau_cL_R/(tau_r*tau_cL))*(tau_cH_R-1)

                pi_cH = tau_cH**(gam_c*peta_c/(gam_c-1))

                pi_f = tau_f**(gam_c*peta_f/(gam_c-1))
                # pi_cL= tau_cL**(gam_c*peta_c/(gam_c-1))

                Pt19_P0 = pi_r*pi_d*pi_f*pi_fn
                # Pt19_P0 = pi_r*pi_d*pi_cL*pi_fn
                
                if Pt19_P0 < ((gam_c+1)/2)**(gam_c/(gam_c-1)) and Pt19_P0>1:
                    Pt19_P19 = Pt19_P0
                elif  Pt19_P0 > ((gam_c+1)/2)**(gam_c/(gam_c-1)):
                    Pt19_P19 = ((gam_c+1)/2)**(gam_c/(gam_c-1))
                else:
                    # print("Pt19_P0 is less than 1. Engine not feasible")
                    # return
                    if "Pt19_P19" not in locals(): #otherwise use its old value
                        Pt19_P19= 1.00001  


                M19 = sqrt((2/(gam_c-1))*(Pt19_P19**((gam_c-1)/gam_c)-1))

                P0_P19= Pt19_P19/Pt19_P0

                Pt9_P0 = pi_r*pi_d*pi_f*pi_cH*pi_b*pi_tH*pi_tL*pi_n
                # Pt9_P0 = pi_r*pi_d*pi_cL*pi_cH*pi_b*pi_tH*pi_tL*pi_n

                if Pt9_P0 < ((gam_c+1)/2)**(gam_c/(gam_c-1)) and Pt9_P0>1:   #unchoked
                    Pt9_P9 = Pt9_P0
                elif Pt9_P0 > ((gam_c+1)/2)**(gam_c/(gam_c-1)):                                           #choked
                    Pt9_P9 = ((gam_c+1)/2)**(gam_c/(gam_c-1))   #Mach number is 1 
                else:
                    # print("Pt9_P0 is less than 1. Engine not feasible")
                    # return
                    if "Pt9_P9" not in locals():  #otherwise use its old value
                        Pt9_P9= 1.00001

                M9 = sqrt((2/(gam_c-1))*(Pt9_P9**((gam_c-1)/gam_c)-1))  #if Pt_P9 is <1 then pow(Pt_P9,-)-1 becomes neg.
                # print("M9",M9)

                P0_P9= Pt9_P9/Pt9_P0

                MFP_M19= self.MFP(gam_c,Rc,M19)
                if refEngine.parameters["AB"]=="Y":
                    gam_t= refEngine.parameters["gam_ab"]
                MFP_M9= self.MFP(gam_t,Rt,M9)
                MFP_M9_R= self.MFP(gam_t,Rt,M9_R)
                alp = alp_R*(pi_cH_R/pi_cH)*(pi_d_R/pi_d)*(MFP_M19/MFP_M9)*sqrt((Tt4_T0/(tau_r*tau_f))/(Tt4_T0_R/(tau_r_R*tau_f_R)))      
                # alp = alp_R*(pi_cH_R/pi_cH)*(pi_d_R/pi_d)*(MFP_M19/MFP_M9)*sqrt((Tt4_T0/(tau_r*tau_cL))/(Tt4_T0_R/(tau_r_R*tau_cL_R)))

                p1 = (1-tau_tL)/(1-tau_tL_R)
                p2 = (Tt4_T0/tau_r)/(Tt4_T0_R/tau_r_R)
                p3 = (1+alp_R)/(1+alp)
                tau_f = 1+ p1*p2*p3*(tau_f_R-1)

                tau_tL_1= tau_tL                    #stores its old value

                pi_tL = pi_tL_R*(MFP_M9_R/MFP_M9)*sqrt(tau_tL/tau_tL_R)

                tau_tL = pi_tL**((gam_t-1)*peta_t/gam_t)

                if num_iter>100:  #iteration not converging
                    break
                num_iter+=1


        elif engineType=="turbojet":
            tau_cL= 1+ (Tt4_T0/Tt4_T0_R)*(tau_r_R/tau_r)*(tau_cL_R-1)

            pi_cL= pow(tau_cL,gam_c*peta_c/(gam_c-1))

            tau_cH= 1+ (Tt4_T0/Tt4_T0_R)*(tau_r_R*tau_cL_R/(tau_r*tau_cL))*(tau_cH_R -1)  

            pi_cH= pow(tau_cH,gam_c*peta_c/(gam_c-1))

            pi_c= pi_cL*pi_cH
            tau_tH= refEngine.tau_tH  #since Station 4 and 4.5 are choked
            tau_tL= refEngine.tau_tL  #assuming M8=1
            pi_tH= refEngine.pi_tH
            pi_tL= refEngine.pi_tL
            alp= alp_R                #0

            P0_P9= P0_P9_R
            P0_P19= P0_P19_R


        elif engineType=="ramjet":
            #everything remains the same
            alp= alp_R
            pi_f= pi_f_R
            pi_cL= pi_cL_R
            pi_cH= pi_cH_R
            pi_c= pi_cL*pi_cH

            P0_P9= P0_P9_R
            P0_P19= P0_P19_R     

        #we assume tau_f== tau_lpc and pi_f= pi_lpc
        if engineType=="turbofan":
            pi_cL= pi_f               #mattingly assumption for turbofan
            tau_cL= tau_f
            # pi_f= pi_cL                 #Suppose you have dual spool turbofan engine. Then pi_f= pi_lpc= 3.8 sets here. Then you surely get a math error bcz pi_f is soo big. Hence we need to set pi_cL= pi_f
            # tau_f= tau_cL
            pi_c= pi_cL*pi_cH
        else:
            pi_f= refEngine.parameters["pi_f"]   #1
            
        #we use PCA to get the results of testEngine
        testEngine= initialisingComponents(engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType).get_engine()
        [f,ST,TSFC]= testEngine.get_engineDetails()

        #finding m_dot   #common for both turbojet and ramjet
        f_R= refEngine.f
        f= testEngine.f
        term1= P0*pi_cH*pi_cL*pi_d*pi_d
        term2= P0_R*pi_cH_R*pi_cL_R*pi_d_R
        m_dot= self.m_dot_R*((1+alp)/(1+alp_R))*sqrt(Tt4_R/Tt4)*(term1/term2)*(1+f_R)/(1+f)

        #Thrust T_test of testEngine
        Thrust_test= testEngine.ST*m_dot

        return testEngine,m_dot




#Alternate itertation scheme for Turbofan EPA

#calc of pi_c pi_lpc pi_hpc of the turbojet test engine using refEngine compressor pressure ratios
        # Tt4_T0= Tt4/T0
        # tau_rR= refEngine.tau_r
        # Tt4_T0R= refEngine.Tt4_T0
        # gam_c= refEngine.parameters["gam_c"]
        # tau_r= 1+ 0.5*(gam_c-1)*pow(M0,2)
        # tau_cL= 1+ (Tt4_T0/Tt4_T0R)*(tau_rR/tau_r)*(refEngine.tau_cL-1)

        # peta_c= refEngine.parameters["peta_c"]
        # pi_lpc= pow(tau_cL,gam_c*peta_c/(gam_c-1))
        
        # tau_cH= 1+ (Tt4_T0/Tt4_T0R)*(tau_rR*refEngine.tau_cL/(tau_r*tau_cL))*(refEngine.tau_cH -1)  #since tau_cH for refEngine(single) is 1. tau_cH will be 0
        # pi_hpc= pow(tau_cH,gam_c*peta_c/(gam_c-1))

        # pi_c= pi_lpc*pi_hpc

        #calc of tau_tL, M9, M19, tau_f, tau_hpc, alp
        #we assume tau_f= tau_lpc and pi_f= pi_lpc




#Doing the calculations using sympy
        # def myFunction(z):
        #     tau_tL= z[0]
        #     pi_tL= z[1]
        #     tau_cL= z[2]
        #     pi_cL= z[3] 
        #     tau_cH= z[4]
        #     pi_cH= z[5]
        #     M9= z[6]
        #     M19= z[7]
        #     alp= z[8]

        #     tau_tHR= refEngine.tau_tH
        #     tau_tH= tau_tHR
        #     pi_tHR= refEngine.pi_tH
        #     pi_tH= pi_tHR

        #     gam_t= refEngine.parameters["gam_t"]
        #     if refEngine.parameters["AB"]=="Y":
        #         gam_t= refEngine.parameters["gam_ab"] 
        #     Rt= refEngine.parameters["Rt"]
        #     g_R_term= (gam_t/Rt)**0.5
        #     in_term= 1+0.5*(gam_t-1)*(M9**2)
        #     pow_term= -(gam_t+1)/(2*(gam_t-1))
        #     MFP_M9 = g_R_term*M9*((in_term)**(pow_term))

        #     M9R= refEngine.M9
        #     in_termR= 1+0.5*(gam_t-1)*(M9R**2)
        #     MFP_M9R= g_R_term*M9R*(in_termR)**(pow_term)

        #     F= np.empty(9)
        #     #equation 1
        #     tau_tLR= refEngine.tau_tL
        #     pi_tLR= refEngine.pi_tL

        #     if refEngine.parameters["AB"]=="N":
        #         F[0]= pi_tL*MFP_M9/(tau_tL**0.5)- pi_tLR*MFP_M9R/(tau_tLR**0.5) 
        #     else:
        #         Tt7_Tt4R= refEngine.parameters["Tt7"]/refEngine.parameters["Tt4"]
        #         Tt7_Tt4= Tt7_Tt4R
        #         F[0]= pi_tL*MFP_M9/(Tt7_Tt4**0.5)-pi_tLR*MFP_M9R/(Tt7_Tt4R**0.5)

        #     #equation 1
        #     gam_c= refEngine.parameters["gam_c"]
        #     pi_fn= refEngine.parameters["pi_fn"]
        #     P0_P19= refEngine.P0_P19
        #     tau_r= 1+ 0.5*(gam_c-1)*pow(M0,2)
        #     pi_r= pow(tau_r, gam_c/(gam_c-1))

        #     gam_term= 2/(gam_c-1)
        #     in_term= pi_fn*pi_cL*pi_r*P0_P19
        #     pow_term= (gam_c-1)/gam_c
        #     F[1]= M19- (gam_term*(in_term**pow_term-1))**0.5

        #     #equation M9
        #     gam_t= refEngine.parameters["gam_t"]
        #     if refEngine.parameters["AB"]=="Y":
        #         gam_t= refEngine.parameters["gam_ab"]
        #     pi_n= refEngine.parameters["pi_n"]
        #     pi_b= refEngine.parameters["pi_b"]

        #     pi_d_max= refEngine.parameters["pi_d_max"]
        #     eta_r= 1 if M0<1 or pi_d_max==1 else 1-0.075*pow((M0-1),1.35)
        #     global pi_d
        #     pi_d= eta_r*pi_d_max

        #     pi_ab= refEngine.parameters["pi_ab"]
        #     P0_P9= refEngine.P0_P9
        #     gam_term= 2/(gam_t-1)
        #     if refEngine.parameters["AB"]=="Y":
        #         in_term= pi_n*pi_tL*pi_tH*pi_b*pi_cH*pi_cL*pi_d*pi_r*P0_P9
        #     else:
        #         in_term= pi_n*pi_ab*pi_tL*pi_tH*pi_b*pi_cH*pi_cL*pi_d*pi_r*P0_P9
        #     pow_term= (gam_t-1)/gam_t
        #     F[2]= M9- (gam_term*(in_term**pow_term-1))**0.5

        #     #equation 2
        #     Rc= refEngine.parameters["Rc"]
        #     g_R_term= (gam_c/Rc)**0.5
        #     in_term= 1+0.5*(gam_c-1)*(M19**2)
        #     pow_term= -(gam_c+1)/(2*(gam_c-1))
        #     MFP_M19 = g_R_term*M19*((in_term)**(pow_term))

        #     M19R= refEngine.M19
        #     in_termR= 1+0.5*(gam_t-1)*(M19R**2)
        #     MFP_M19R= g_R_term*M19R*(in_termR)**(pow_term)

        #     alpR= refEngine.parameters["alp"]
        #     tau_fR= refEngine.tau_f
        #     tau_rR= refEngine.tau_r
        #     Tt4_T0= Tt4/T0
        #     Tt4_T0R= refEngine.Tt4_T0
        #     pi_cHR= refEngine.parameters["pi_hpc"]
        #     pi_dR= refEngine.pi_d
        #     F[3]= alp-alpR*((tau_fR*tau_rR*Tt4_T0/(tau_cL*tau_r*Tt4_T0R))**0.5)*(pi_cHR*pi_dR/(pi_cH*pi_d))*MFP_M19/MFP_M19R

        #     #equation 3
        #     tau_cHR= refEngine.tau_cH
        #     F[4]= (tau_cH-1)*tau_r*tau_cL/((1-tau_tH)*Tt4_T0)-(tau_cHR-1)*tau_rR*tau_fR/((1-tau_tHR)*Tt4_T0R)

        #     #equation 4
        #     F[5]= (tau_cL-1)*tau_r*(1+alp)/(Tt4_T0*tau_tH*(1-tau_tL))-(tau_fR-1)*tau_rR*(1+alpR)/(Tt4_T0R*tau_tHR*(1-tau_tLR))

        #     #equation 5-7
        #     peta_t= refEngine.parameters["peta_t"]
        #     F[6]= pi_tL- tau_tL**(gam_t/((gam_t-1)*peta_t))
        #     peta_c= refEngine.parameters["peta_c"]
        #     F[7]= pi_cL- tau_cL**(gam_c*peta_c/(gam_c-1))
        #     F[8]= pi_cH- tau_cH**(gam_c*peta_c/(gam_c-1))

        #     return F
        # z_guess= np.array([1,1,1,1,1,1,1,1,1])
        
        # res= fsolve(myFunction,z_guess)

        # print(res)

        # tau_tL= res[0]
        # pi_tL= res[1]
        # tau_cL= res[2]
        # pi_cL= res[3] 
        # tau_cH= res[4]
        # pi_cH= res[5]
        # M9= res[6]
        # M19= res[7]
        # alp= res[8]
         

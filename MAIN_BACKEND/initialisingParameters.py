from initialisingComponents_file import initialisingComponents

class initialisingParameters:
    def __init__(self):
        pass
    def get_T0_P0_from_alt(self,altitude):                  
            # Constants
            To = 288.16  # Standard temperature at sea level in K
            Po = 101325  # Standard pressure at sea level in Pa
            L = 0.0065   # Temperature lapse rate in K/m
            R = 287.05   # Specific gas constant for dry air in J/(kg·K)
            g = 9.80665  # gravity
            M = 0.02896968 # Molar mass of dry air (kg/mol)
            Lo = 0.00976 # temperature lapse rate used for pressure (K/m)
            Ro = 8.314462618 # universal gas constant (J/(mol.K))

            if altitude < 0:
                altitude= 0

            if altitude < 11000:
                T = To - L * altitude
            elif altitude > 11000 and altitude < 25000:
                T = 216.67
            else:
                T = 216.7    
            P = Po*((1 - Lo*altitude/To)**(g*M/(Ro*Lo)))

            return (T,P)

    def get_engine(self):
        #Basic parameters
        global engineType,AB,alt,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType

        #5th gen engine air-fuel properties
        gam_c=1.4
        gam_t=1.3
        gam_ab=1.3  
        Cpc=1.0048e+3
        Cpt=1.2351e+3
        Cpab=1.235106e+3 
        Rc = (gam_c-1)*Cpc/gam_c
        Rt = (gam_t-1)*Cpt/gam_t
        Rab = (gam_ab-1)*Cpab/gam_ab


        engineType= input("\nEnter the engine type (turbofan/turbojet/ramjet): ").lower()

#for turbofan
        if engineType=="turbofan":
            alt= 0
            T0=216.66
            P0=19.403e+3
            M0=0.83
            Tt4=1800
            Hpr=42800e+3
            pi_c=25
            pi_cL=1.65
            pi_cH=pi_c/pi_cL 
            alp=8
            pi_f=1.65

            eta_b=0.98
            eta_m=0.99
            eta_ab= 0.97
            pi_d_max=0.95     
            pi_b=0.94
            pi_ab= 0.96
            pi_n=0.96
            peta_f=0.89
            peta_c=0.89
            peta_t=0.89

            #afterburner property
            Tt7= 2000

            #perfect expansion or not
            P0_P9= 1 
            P0_P19= 1


            sep_mixed_flow= input("\nDo you want a separate or mixed flow (S/M): ")

            if sep_mixed_flow=="M":
                AB= input("\nDo you want a afterburner (Y/N): ")   
            else:
                AB= "N"            

            if AB=="N":
                Tt7= "NA"
                eta_ab= 1
                pi_ab= 1
                gam_ab= gam_t
                Cpab= Cpt
                Rab= Rt


            spool= input("\nDo you want Single/Dual (S/D): ")
            if spool=="S":
                pi_cL= pi_c
                pi_cH= 1                                   #just plugging in pi_cH to 1 will nullify the HPC and the HPT alongwith it

            nozzleType= input("\nDo you want a Converging nozzle or a CD nozzle(C/CD): ")

            if nozzleType=="C":
                P0_P9=  "NA"                                #its value will be calculated
                P0_P19= "NA"



            ideal_real= input("\nDo you want ideal or real (I/R): ")
            if ideal_real=="I":                                   #for ideal cycle analysis
                Cpt= Cpc
                Cpab= Cpt
                gam_t= gam_c
                gam_ab= gam_t
                Rt= Rc
                Rab= Rt
                eta_b=1
                eta_m=1
                eta_ab=1
                pi_d_max=1
                pi_b=1
                pi_n=1
                pi_ab=1
                pi_fn=1
                peta_f=1
                peta_c=1
                peta_t=1                

            if sep_mixed_flow=="M":
                M6= 0.4
                P0_P19= P0_P9           #bcz P19= P9 since there is only one exhaust
                pi_fn= "NA"
                alp= "NA"               #bcz alp is calculated for mixed flow turbofan such that Pt6= Pt16 using pi_f
                if ideal_real=="R":
                    pi_m_max= 0.98
                else:
                    pi_m_max="NA"       #bcz we for real mixed_exhaust turbofan pi_m_max is such that pi_m is 1. Hence pi_m_max is not required
            else:
                M6= "NA"
                pi_m_max= "NA"
                pi_fn=0.98
                peta_f=0.89


#for turbojet
        elif engineType =="turbojet":
            alt=0
            T0=216.66
            P0=19.403e+3
            M0=1.5
            Tt4=1800
            Hpr=42800e+3
            pi_c=25
            pi_cL=1.65
            pi_cH=pi_c/pi_cL 

            alp=0
            pi_f=1

            eta_b=0.98
            eta_m=0.99
            eta_ab= 0.97
            pi_d_max=0.95     
            pi_b=0.94
            pi_ab= 0.96
            pi_n=0.96
            peta_c=0.89
            peta_t=0.89


            #perfect expansion or not
            P0_P9= 1 
            P0_P19= 1
            
            sep_mixed_flow= "S"                #all other engines are separate flow engines

           
            AB= input("\nDo you want a afterburner (Y/N): ")   

            if AB=="N":
                Tt7= "NA"
                eta_ab= 1
                pi_ab= 1
                gam_ab= gam_t
                Cpab= Cpt
                Rab= Rt
            else:
                Tt7= 2000


            spool= input("\nDo you want Single/Dual (S/D): ")
            if spool=="S":
                pi_cL= pi_c
                pi_cH= 1                                # Just plugging pi_hpc to 1 will nullify the HPC and the HPT alongwith it

            nozzleType= "CD"

            ideal_real= input("\nDo you want ideal or real (I/R): ")
            if ideal_real=="I":                                   #for ideal cycle analysis
                Cpt= Cpc
                Cpab= Cpt
                gam_t= gam_c
                gam_ab= gam_t
                Rt= Rc
                Rab= Rt
                eta_b=1
                eta_m=1
                eta_ab=1
                pi_d_max=1
                pi_b=1
                pi_n=1
                pi_ab=1
                pi_fn=1
                peta_f=1
                peta_c=1
                peta_t=1                


            M6= "NA"
            pi_m_max= "NA"

            pi_fn=1
            peta_f=1

#for ramjet
        elif engineType=="ramjet":
            alt=0
            T0=216.66
            P0=19.403e+3
            M0=2.5
            Tt4=1800
            Hpr=42800e+3
            pi_c=1
            pi_cL=1
            pi_cH=pi_c/pi_cL 
            alp=0
            pi_f=1

            eta_b=0.98
            eta_m= 1
            eta_ab= 1
            pi_d_max=0.95     
            pi_b=0.94
            pi_ab= 1
            pi_n=0.96
            peta_c=1
            peta_t=1


            #perfect expansion or not
            P0_P9= 1 
            P0_P19= 1
            
            sep_mixed_flow= "S"                


            AB= "N"       #no afterburner in ramjet
            Tt7= "NA"
            gam_ab= gam_t
            Cpab= Cpt
            Rab= Rt
 
            nozzleType= "CD"

            ideal_real= input("\nDo you want ideal or real (I/R): ")
            if ideal_real=="I":                                   #for ideal cycle analysis
                Cpt= Cpc
                Cpab= Cpt
                gam_t= gam_c
                gam_ab= gam_t
                Rt= Rc
                Rab= Rt
                eta_b=1
                eta_m=1
                eta_ab=1
                pi_d_max=1
                pi_b=1
                pi_n=1
                pi_ab=1
                pi_fn=1
                peta_f=1
                peta_c=1
                peta_t=1                

            M6= "NA"
            pi_m_max= "NA"
            pi_fn=1
            peta_f=1

        

        #showing them the finalised parameters
        # print("\nThese are the engine parameters ")

        # list1= ["engineType","AB","alt","T0","P0","M0","M6","alp","gam_c","gam_t","gam_ab","Rc","Rt","Rab","Cpc","Cpt","Cpab","Tt4","Tt7","Hpr","eta_b","eta_m","eta_ab","pi_d_max","pi_f","pi_c","pi_cL","pi_cH","pi_b","pi_m_max","pi_ab","pi_n","pi_fn","peta_f","peta_c","peta_t","P0_P9","P0_P19","sep_mixed_flow","nozzleType"]
        # table1= PrettyTable(["Parameter","Value"])
        # dict1= dict(globals().items())
        # for i in list1:
        #     table1.add_row([i,dict1[i]])
        # print(table1)
        

        #we let the user alter the parameter values 
        temp= input("\nDo you want any changes in them (Y/N): ")
        if temp== "Y":
            d= dict(globals().items())
            keys= list(d.keys())

            print("\nEnter variable alongwith values Eg. Tt4 2000. Enter 'None' in the end")
            inpt= input("Variable with value: ")
            while inpt != "None":
                var1,val1= inpt.split()
                if var1 in keys:
                    globals()[var1]= float(val1) 

                    if var1=="alt":         #exception case. If the user changes the altitude, we need to update T0 and P0. Otherwise if they change T0,P0 we dont need to change alt
                        (globals()["T0"],globals()["P0"])= self.get_T0_P0_from_alt(globals()["alt"])

                inpt= input("Variable with value: ")
            
            # showing them the finalised parameters
            # print("\nThese are the finalised engine parameters ")

            # list1= ["engineType","AB","alt","T0","P0","M0","M6","alp","gam_c","gam_t","gam_ab","Rc","Rt","Cpc","Cpt","Cpab","Tt4","Tt7","Hpr","eta_b","eta_m","eta_ab","pi_d_max","pi_f","pi_c","pi_cL","pi_cH","pi_b","pi_m_max","pi_ab","pi_n","pi_fn","peta_f","peta_c","peta_t","P0_P9","P0_P19","sep_mixed_flow","nozzleType"]
            # table1= PrettyTable(["Parameter","Value"])
            # dict1= dict(globals().items())
            # for i in list1:
            #     table1.add_row([i,dict1[i]])
            # print(table1)

        engine= initialisingComponents(engineType,AB,T0,P0,M0,M6,alp,gam_c,gam_t,gam_ab,Rc,Rt,Rab,Cpc,Cpt,Cpab,Tt4,Tt7,Hpr,eta_b,eta_m,eta_ab,pi_d_max,pi_f,pi_c,pi_cL,pi_cH,pi_b,pi_m_max,pi_ab,pi_n,pi_fn,peta_f,peta_c,peta_t,P0_P9,P0_P19,sep_mixed_flow,nozzleType).get_engine()
        [f,ST,TSFC]= engine.get_engineDetails()

        return engine
    

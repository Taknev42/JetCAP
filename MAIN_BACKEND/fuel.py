"""class to store all fuel and air chemical properties"""
class fuel:
    def __init__(self,gam_c,gam_t,gam_ab,Rc,Rt,Cpc,Cpt,Cpab,Hpr):
        self.gam_c= gam_c
        self.gam_t= gam_t
        self.gam_ab= gam_ab
        self.Rc= Rc
        self.Rt= Rt
        self.Cpc= Cpc
        self.Cpt= Cpt
        self.Cpab= Cpab
        self.Hpr= Hpr
        
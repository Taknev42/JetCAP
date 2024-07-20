class nozzle:
    def __init__(self,pi_n):
        self.pi_n= pi_n
        self.tau_n=1

    def get_PnT(self,Pt_in,Tt_in):
        Pt_out= self.pi_n*Pt_in
        Tt_out= self.tau_n*Tt_in

        return (Pt_out,Tt_out)
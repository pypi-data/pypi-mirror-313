"""This module contains a variety of kinetic models to be used"""
import numpy as np
import ray 

ray.init(log_to_driver=False,ignore_reinit_error=True)
EPS=1e-6

    
TOY_REACTIONS = [
    "S_import",
    "S_to_I1",
    "I1_to_P",
    "S_to_NT",
    "NT_to_NA",
    "I1_to_Li",
    "S_to_g",
    "g_to_S",
    "I1_to_e",
    "P_export",
    "e_and_li_to_W",
    "e_to_enzymes",
    "e8_decay",
    "e9_decay",
    "maintenance"
    ]

TOY_SPECIES = [
    "S_env",
    "S",
    "I1",
    "P",
    "P_env",
    "NT",
    "NA",
    "Li",
    "g",
    "e",
    "t1",
    "t2",
    "e2",
    "e3",
    "e4",
    "e5",
    "e6",
    "e7",
    "e8",
    "e9",
    "E",
    "W"
]
    

    
class Kinetic:
    """Objects of this class represent a kinetic model"""
    def __init__(self, name:str, parameters:dict)->None:
        self.name = name
        for key, value in parameters.items():
            setattr(self, key, value)
    
    def __str__(self) -> str:
        param_print=""
        for key, value in self.__dict__.items():
            param_print += f"{key} = {value}\n"
        return f"{self.name} kinetic model with parameters:\n{param_print}"

        
class Hill(Kinetic):
    """Objects of this class represent a Hill kinetic model"""
    def __init__(self,parameters:dict)->None:
        if {"n", "k"} != set(parameters.keys()):
            raise ValueError("Hill kinetic model requires only parameters n and k")
        super().__init__("Hill", parameters)

    def __call__(self,x)->float:
        return max(0,x**self.n/(self.k**self.n + x**self.n))

class MichaelisMenten(Kinetic):
    """Objects of this class represent a Michaelis Menten kinetic model"""
    def __init__(self, parameters:dict)->None:
        if {"k", "kcat"} != set(parameters.keys()):
            raise ValueError("Michaelis Menten kinetic model requires only parameters k and kcat")
        super().__init__("MichaekisMenten", parameters)

    def __call__(self,x:float)->float:
        return max(0,self.kcat*x/(self.k + x))

class PingPong(Kinetic):
    """Objects of this class represent a Ping Pong kinetic model"""
    def __init__(self, parameters:dict)->None:
        if {"ka", "kb","kab","vm"} != set(parameters.keys()):
            raise ValueError("Ping Pong kinetic model requires only parameters ka and kb and kab and vm")
        super().__init__("PingPong", parameters)

    def __call__(self,a:float,b:float)->float:
        return max(0,self.vm*a*b/(self.ka*a + self.kb*b + self.ka*self.kb))
    
class Linear(Kinetic):
    """Objects of this class represent a Linear kinetic model"""
    def __init__(self, parameters:dict)->None:
        if {"k"} != set(parameters.keys()):
            raise ValueError("Linear kinetic model requires only parameters k")
        super().__init__("Linear", parameters)

    def __call__(self,x:float)->float:
        return max(0,self.k*x)

def map_to_pos(x:float)->float:
    return 1 if x>0 else 0

def toy_model_stoichiometry(model)->np.ndarray:
    """This function returns the stoichiometry of the toy model. Here is a look at the governing rules:
    r[1]: S -> S_in                     ::: r=PingPong(ka1, kb1, kab1, vm1)([S]   ,[t1])
    r[2]: S_in -> p21 I_1 + p22 E       ::: r=PingPong(ka2, kb2, kab2, vm2)([S_in],[e2])
    r[3]: I_1 -> p31 P + p32 E          ::: r=PingPong(ka3, kb3, kab3, vm3)([I_1] ,[e3])
    r[4]: S_in + r41 E ->  p42 NTP      ::: r=PingPong(ka4, kb4, kab4, vm4)([S_in],[e4])
    r[5]: NTP -> p51 NA                 ::: r=PingPong(ka5, kb5, kab5, vm5)([NTP] ,[e5])
    r[6]: I_1 + r61 E -> p62 Li         ::: r=PingPong(ka6, kb6, kab6, vm6)([I_1] ,[e6])
    r[7]: I_1 + r71 E -> p72 AA         ::: r=PingPong(ka7, kb7, kab7, vm7)([I_1] ,[e7])
    r[8]: AA + r81 E -> p82 e           ::: r=PingPong(ka8, kb8, kab8, vm8)([AA]  ,[e8])
    r[9]: P->P_out                      ::: r=Hill(n1,k1)([t2])
    r[10]: r101 AA + r102 Li -> W       ::: r=PingPong(ka10, kb10, kab10, vm10)([AA],[Li]) -> Should be very fast    
    _________________________________________________________________________________________________________
    e=e1+e2+e3+e4+e5+e6+e7+e8+t1       
    #Q: is this okay?

    r[]:e->t1
    r[]:e->e1
    r[]:e->e2
    r[]:e->e3
    r[]:e->e4
    r[]:e->e5
    r[]:e->e6
    r[]:e->e7
    r[]:e->e8
    r[]:e->t2
    ____________________________________________________________________________________________
    
    """
    s=np.zeros((len(model.state_variables),len(model.reactions)))
    
    s[[model.state_variables.index("S_env"),model.state_variables.index("S")],model.reactions.index("S_import")] = [-1,1]
    
    s[list(map(model.state_variables.index,["S","I1", "E"])),model.reactions.index("S_to_I1")] = [-1,model.parameters["p21"],model.parameters["p22"]]
    
    s[list(map(model.state_variables.index,["I1","P","E"])),model.reactions.index("I1_to_P")] =  [-1,model.parameters["p31"],model.parameters["p32"]]

    
    
    s[list(map(model.state_variables.index,["S","E","NT"])),model.reactions.index("S_to_NT")] = [-1,model.parameters["p41"],model.parameters["p42"]]
    
    s[list(map(model.state_variables.index,["NT","E","NA"])),model.reactions.index("NT_to_NA")] = [-1,model.parameters["r51"],model.parameters["p52"]]
    
    s[list(map(model.state_variables.index,["I1","E","Li"])),model.reactions.index("I1_to_Li")] = [-1,model.parameters["r61"],model.parameters["p62"]]
    
    s[list(map(model.state_variables.index,["I1","E","e"])),model.reactions.index("I1_to_e")] = [-1,model.parameters["r71"],model.parameters["p72"]]
    
        
    s[[model.state_variables.index("P"),model.state_variables.index("P_env")],model.reactions.index("P_export")] = [-1,1]
    
    s[list(map(model.state_variables.index,["e","Li","W"])),model.reactions.index("e_and_li_to_W")] = [model.parameters["r101"],model.parameters["r102"],model.parameters["pw"]]
    s[list(map(model.state_variables.index,["S","E","g"])),model.reactions.index("S_to_g")] = [-1,model.parameters["r111"],model.parameters["p112"]]
    s[list(map(model.state_variables.index,["g","S","E"])) ,model.reactions.index("g_to_S")] = [model.parameters["r121"],model.parameters["p122"],model.parameters["p123"]]
        

    s[list(map(model.state_variables.index,["e","t1","t2","e2","e3","e4","e5", "e6", "e7","e8","e9"])),model.reactions.index("e_to_enzymes")] = [-1,
                                                                                                                                                 model.parameters["k_t1"],
                                                                                                                                                 model.parameters["k_t2"],
                                                                                                                                                 model.parameters["k_e2"],
                                                                                                                                                 model.parameters["k_e3"],
                                                                                                                                                 model.parameters["k_e4"],
                                                                                                                                                 model.parameters["k_e5"],
                                                                                                                                                 model.parameters["k_e6"],
                                                                                                                                                 model.parameters["k_e7"],
                                                                                                                                                 model.parameters["k_e8"],
                                                                                                                                                 model.parameters["k_e9"],
                                                                                                                                                 ]

    s[list(map(model.state_variables.index,["e8"])),model.reactions.index("e8_decay")] = [-1]
    s[list(map(model.state_variables.index,["e9"])),model.reactions.index("e9_decay")] = [-1]

    s[list(map(model.state_variables.index,["E"])),model.reactions.index("maintenance")] = [-1]
    
    return s

def toy_model_ode(t:float, y:np.ndarray, model)->np.ndarray:
    ### First we update the dimensions of the cell
    if y[model.state_variables.index("E")]<0:
        model.reward=-1
    else:
        model.reward=0
        
    y[y<0]=0
    model.shape.set_dimensions({key:y[model.state_variables.index(key)] for key in model.shape.dimensions.keys()})
    y[model.volume_index]=model.shape.volume
    actions=model.decide()[0]
    a=actions.clip(0,1000).detach().numpy()
    model.parameters.update(dict(zip(model.controlled_params,a)))

    if model.can_double():
        model.shape.set_dim_from_volume(model.shape.volume/2)
        for dim,val in model.shape.get_dimensions().items():
            y[model.state_variables.index(dim)] = val
        
        
        y[model.cell_metabolites]=y[model.cell_metabolites]/2
        
        model.state[model.number_index]=model.state[model.number_index]*2
        model.reward+=1
    else:
        pass
        


                
    scaler=1
    ### Now we calculate the fluxes for each reaction
    fluxes = np.zeros(len(model.reactions))
    fluxes[model.reactions.index("S_import")] = PingPong({"ka": model.parameters["ka1"],
                                                                                    "kb": model.parameters["kb1"],
                                                                                    "kab":model.parameters["kab1"],
                                                                                    "vm": model.parameters["vm1"]})\
                                                                            (y[model.state_variables.index("S_env")],
                                                                             y[model.state_variables.index("t1")]/model.shape.area)*model.shape.area*scaler
    
    fluxes[model.reactions.index("S_to_I1")] = PingPong({"ka":  model.parameters["ka2"],
                                                                                  "kb":  model.parameters["kb2"],
                                                                                  "kab": model.parameters["kab2"],
                                                                                  "vm":  model.parameters["vm2"]})\
                                                                            (y[model.state_variables.index("S")]/model.shape.volume,
                                                                             y[model.state_variables.index("e2")]/model.shape.volume)*model.shape.volume*scaler
    
    fluxes[model.reactions.index("I1_to_P")] = PingPong({"ka": model.parameters["ka3"],
                                                                                    "kb": model.parameters["kb3"],
                                                                                    "kab":model.parameters["kab3"],
                                                                                    "vm": model.parameters["vm3"]})\
                                                                             (y[model.state_variables.index("I1")]/model.shape.volume,
                                                                              y[model.state_variables.index("e3")]/model.shape.volume)*model.shape.volume*scaler
    
    fluxes[model.reactions.index("S_to_NT")] = PingPong({"ka":  model.parameters["ka4"], 
                                                                                     "kb":  model.parameters["kb4"], 
                                                                                     "kab": model.parameters["kab4"], 
                                                                                     "vm":  model.parameters["vm4"]})\
                                                                                (y[model.state_variables.index("S")]/model.shape.volume,
                                                                                y[model.state_variables.index("e4")]/model.shape.volume)*model.shape.volume*scaler
    
    fluxes[model.reactions.index("NT_to_NA")] = PingPong({"ka":  model.parameters["ka5"],
                                                                                      "kb":   model.parameters["kb5"],
                                                                                      "kab":  model.parameters["kab5"],
                                                                                      "vm":   model.parameters["vm5"]})\
                                                                                (y[model.state_variables.index("NT")]/model.shape.volume,
                                                                                 y[model.state_variables.index("e5")]/model.shape.volume)*model.shape.volume*scaler*map_to_pos(y[model.state_variables.index("E")])
    
    
    fluxes[model.reactions.index("I1_to_Li")] =PingPong({"ka":  model.parameters["ka6"],
                                                                                      "kb":  model.parameters["kb6"],
                                                                                      "kab": model.parameters["kab6"],
                                                                                      "vm":  model.parameters["vm6"]})\
                                                                                (y[model.state_variables.index("I1")]/model.shape.volume,
                                                                                 y[model.state_variables.index("e6")]/model.shape.volume)*model.shape.volume*scaler*map_to_pos(y[model.state_variables.index("E")])
    
    fluxes[model.reactions.index("I1_to_e")] = PingPong({  "ka": model.parameters["ka7"],
                                                                                        "kb": model.parameters["kb7"],
                                                                                        "kab":model.parameters["kab7"],
                                                                                        "vm": model.parameters["vm7"]})\
                                                                                (y[model.state_variables.index("I1")]/model.shape.volume,
                                                                                 y[model.state_variables.index("e7")]/model.shape.volume)*model.shape.volume*scaler*map_to_pos(y[model.state_variables.index("E")])


                                                                            
    fluxes[model.reactions.index("P_export")] =PingPong({
                                                            "ka": model.parameters["ka9"],
                                                            "kb": model.parameters["kb9"],
                                                            "kab":model.parameters["kab9"],
                                                            "vm": model.parameters["vm9"]})(y[model.state_variables.index("P")]/model.shape.volume,
                                                            y[model.state_variables.index("t2")]/model.shape.area)*model.shape.area
                                                                            
    fluxes[model.reactions.index("e_and_li_to_W")] = PingPong({ "ka": model.parameters["ka10"],
                                                                                           "kb": model.parameters["kb10"],
                                                                                           "kab":model.parameters["kab10"],
                                                                                           "vm": model.parameters["vm10"]})\
                                                                                  (y[model.state_variables.index("e")]/model.shape.volume,
                                                                                    y[model.state_variables.index("Li")]/model.shape.volume)*model.shape.volume*scaler

    fluxes[model.reactions.index("S_to_g")] = PingPong({"ka": model.parameters["ka11"],
                                                                                        "kb": model.parameters["kb11"],
                                                                                        "kab":model.parameters["kab11"],
                                                                                        "vm": model.parameters["vm11"]})\
                                                                                    (y[model.state_variables.index("S")]/model.shape.volume,
                                                                                     y[model.state_variables.index("e8")]/model.shape.volume)*model.shape.volume*scaler*map_to_pos(y[model.state_variables.index("E")])
    
    fluxes[model.reactions.index("g_to_S")] = PingPong({"ka": model.parameters["ka12"],
                                                                                        "kb": model.parameters["kb12"],
                                                                                        "kab":model.parameters["kab12"],
                                                                                        "vm": model.parameters["vm12"]})\
                                                                                    (y[model.state_variables.index("g")]/model.shape.volume,
                                                                                     y[model.state_variables.index("e9")]/model.shape.volume)*model.shape.volume*scaler
    # This line will ensure that e won't go below zero
    
    fluxes[model.reactions.index("e_to_enzymes")] = Linear({"k":model.parameters["k_dist"]})\
                                                                            (y[model.state_variables.index("e")]/model.shape.volume)*model.shape.volume*1
    fluxes[model.reactions.index("e8_decay")] = Linear({"k":model.parameters["k_dec"]})\
                                                                            (y[model.state_variables.index("e8")]/model.shape.volume)*model.shape.volume*1
                                                                            
    fluxes[model.reactions.index("e9_decay")] = Linear({"k":model.parameters["k_dec"]})\
                                                                            (y[model.state_variables.index("e9")]/model.shape.volume)*model.shape.volume*1
             

                                       
    fluxes[model.reactions.index("maintenance")] = model.parameters["k_maintenance"]
                                                                        
    v=np.matmul(model.stoichiometry(model),fluxes)
    dvdt=v[model.state_variables.index("W")]/model.parameters["wall_density"]
    for dim in model.shape.dimensions.keys():
        v[model.state_variables.index(dim)] = model.shape.calculate_differentials(dvdt)[dim]
    
    for i in model.env_metabolites:
        v[i]*=model.number
        
    return v

def forward_euler(ode:callable,initial_conditions:np.ndarray,t:np.ndarray,args:tuple)->np.ndarray:
    """This function solves an ordinary differential equation using the forward Euler method"""
    y=np.zeros((len(initial_conditions),len(t)))
    y[:,0]=initial_conditions
    dt=t[1]-t[0]
    for i in range(1,len(t)):
        y[:,i]=y[:,i-1]+dt*ode(t[i-1],y[:,i-1],*args)
    return y

# if __name__ == "__main__":
    # s=Sphere({"r":0.01,"t":0.0001})
    # ic={i:0 for i in TOY_SPECIES}
    # ic["t1"]=0.001
    # ic["e2"]=0.0001
    # ic["e3"]=0.0001
    # ic["e4"]=0.0001
    # ic["e5"]=0.0001
    # ic["e6"]=0.0001
    # ic["e7"]=0.0001
    # ic["e8"]=0
    # ic["e9"]=0
    # ic["e"]=0.01
    # ic["E"]=4
    
    
    # cps=[
    #      "k_t1",
    #      "k_e2",
    #      "k_e3",
    #      "k_e4",
    #      "k_e5",
    #      "k_e6",
    #      "k_e7",
    #      "k_t2",
    #     "k_e8",
    #     "k_e9",
    #     #  "split_volume",

         
    #         ]
    # VMS=0.05
    # cell=Cell("Toy Model",
    #           toy_model_stoichiometry,
    #           toy_model_ode,
    #           {"ka1":0.0005,
    #            "kb1":0.0005,
    #            "kab1":0.000005,
    #            "vm1":VMS*100,
    #            "ka2":0.0005,
    #            "kb2":0.0005,
    #            "kab2":0.000005,
    #            "vm2":VMS*5,
    #            "ka3":0.0005,
    #            "kb3":0.0005,
    #            "kab3":0.000005,
    #            "vm3":VMS,
    #            "ka4":0.0005,
    #            "kb4":0.0005,
    #            "kab4":0.000005,
    #            "vm4":VMS,
    #            "ka5":0.0005,
    #            "kb5":0.0005,
    #            "kab5":0.000005,
    #            "vm5":VMS,
    #            "ka6":0.0005,
    #            "kb6":0.0005,
    #            "kab6":0.000005,
    #            "vm6":VMS,
    #            "ka7":0.005,
    #            "kb7":0.005,
    #            "kab7":0.00005,
    #            "vm7":VMS,
    #            "ka8":0.005,
    #            "kb8":0.005,
    #            "kab8":0.0001,
    #            "vm8":VMS,
    #            "ka9":0.005,
    #            "kb9":0.005,
    #            "kab9":0.00005,
    #            "vm9":VMS,
    #            "ka10":0.005,
    #            "kb10":0.005,
    #            "kab10":0.00005,
    #            "vm10":VMS,
    #             "ka11":0.005,
    #             "kb11":0.05,
    #             "kab11":0.00005,
    #             "vm11":VMS*20,
    #             "ka12":0.005,
    #             "kb12":0.005,
    #             "kab12":0.00005,
    #             "vm12":VMS,
    #            "k_t1":0.5,
    #            "k_e2":0.5,
    #            "k_e3":0.1,
    #            "k_e4":0.1,
    #            "k_e5":0.1,
    #            "k_e6":0.1,
    #            "k_e7":0.5,
    #             "k_e8":0,
    #             "k_e9":0,
    #            "k_t2":1,
    #            "p21":30,
    #            "p22":100,
    #            "p31":1,
    #            "p32":1,
    #            "p41":1,
    #            "p42":1,
    #            "r51":-0.1,
    #            "p52":0.1,
    #            "r61":-0.1,
    #            "p62":0.1,
    #            "r71":-0.1,
    #            "p72":1,
    #            "r81":-1,
    #            "p82":1,
    #            "r101":-0.01,
    #            "r102":-0.01,
    #            "pw":0.001,
    #             "r111":0,
    #             "p112":0.01,
    #             "r121":-0.01,
    #             "p122":1,
    #             "p123":0,
    #             "k_maintenance":2.5,
    #            "wall_density":0.1,
    #            "split_volume":0.02,
    #            "k_dist":10,
    #            "k_dec":0.1
    #            },
    #           TOY_REACTIONS,
    #           TOY_SPECIES,
    #           s,
    #           controlled_params=cps,
    #           ranges=[[0,1] for i in range(len(cps))],
    #           observable_states=["S_env"],
    #           initial_conditions=ic,
    #           grad_updates=10,
    #           policy_lr=0.0001,
    #           value_lr=0.001,
    #           clip=0.1,
    #           actor_variance=0.005,
    #           pretrain_actor=True,
    #     )
    
    # def S_controller(state:dict[str,float])->float:
    #     amplitude=50
    #     period=50
    #     # return amplitude*max(np.sin(2*np.pi*state["time_env"]/period),0)
    #     return (amplitude if state["time_env"]<25 else 0)
    #     # return max(amplitude-state["time_env"]*(amplitude)/25,0)
         
    # env=Environment(name="Toy Model Environment",
    #                 cells=[cell],
    #                 initial_conditions={"S_env":10},
    #                 extra_states=[],
    #                 controllers={"S_env":S_controller},
    #                 time_step=0.1)


    # trainer=Trainer(env,12,500,20000,100,"./step_with_maintenance_final",parallel_framework="ray")
    # trainer.train()
    
    




        
    
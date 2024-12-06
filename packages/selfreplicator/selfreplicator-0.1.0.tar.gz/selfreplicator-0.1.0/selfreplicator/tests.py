from models import Environment, Cell, Trainer,run_episode
import torch


class TestCell(Cell):
    
    def __init__(self,
                 name:str,
                 controlled_params:list[str],
                 ranges:list[list],
                 observable_states:list[str],
                 initial_conditions:dict[str,float],
                 actor_variance:float=0.1,
                 gamma:float=1,
                 grad_updates:int=20,
                 clip:float=0.1,
                 optimizer_policy:torch.optim.Optimizer=torch.optim.Adam,
                 optimizer_value:torch.optim.Optimizer=torch.optim.Adam,
                 policy_lr:float=0.001,
                 value_lr:float=0.01,
                 ):
        self.name = name
        self.controlled_params = controlled_params
        self.ranges = ranges
        self.counter = 0
        self.cov_var=torch.full(size=(len(controlled_params),), fill_value=actor_variance)
        self.covar_matrix=torch.diag(self.cov_var)
        self.observable_states = [i for i in range(len(observable_states))]
        self.state_variables = observable_states
        self._set_policy()
        self._set_value()
        self._initial_state=tuple([initial_conditions.get(i,0) for i in self.state_variables])
        self.gamma = gamma
        self.grad_updates=grad_updates
        self.clip=clip
        self.optimizer_policy=optimizer_policy
        self.optimizer_value=optimizer_value
        self.policy_lr=policy_lr
        self.value_lr=value_lr
        
        self.set_optimizers()
        
    
   
    
    
class TesterEnv:
    
    def __init__(self,
                 name:str,
                 cells:list[Cell],
                 
                 ):

        self.name = name
        self.cells = cells
        
    def reset(self):
        for cell in self.cells:
            cell.reset()
        
    def step(self):
        rewards={}
        actions={}
        previous_states={cell.name:cell.state.copy() for cell in self.cells}
        for cell in self.cells:
            cell.decide()
            actions[cell.name]=cell.actions
            rewards[cell.name]=cell.actions[0]+cell.actions[1]
            cell.state[0]+=1
            
        
        return ({cell.name:cell.state.copy() for cell in self.cells},rewards,actions,previous_states,{cell.name:cell.log_prob for cell in self.cells})
            
            
        
        
        


testcell=TestCell(name="testcell",
                  controlled_params=["l","r"],
                    ranges=[[-5,5],[-5,5]],
                    actor_variance=0.1,
                    observable_states=["counter"],
                    initial_conditions={"counter":0},
                  )

tester_env = TesterEnv(name="tester",
                       cells=[testcell],
                       )

run_episode(env=tester_env,
            num_steps=100,
        )

trainer=Trainer(env=tester_env,
        episodes_per_batch=4,
        steps_per_episode=10,
        number_of_batches=100,
        save_every=-1,
        save_path="",
        )


trainer.train()
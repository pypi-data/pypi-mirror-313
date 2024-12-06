import torch.nn as nn
import ray
import torch
from selfreplicator import shapes,models,training
import numpy as np
from torch.distributions import Normal,MultivariateNormal
from typing import Iterable
import pickle
import os
import pathlib
import json 

# ray.init(log_to_driver=False,ignore_reinit_error=True)
EPS=1e-6
class ActorNetwork(torch.nn.Module):
    
    def __init__(self,input_dim:int,output_dim:int,hidden_dim:int=20,activation=nn.ReLU,n_hidden:int=5)-> None:
        super(ActorNetwork,self).__init__()
        self.inlayer=nn.Sequential(nn.Linear(input_dim,hidden_dim),activation())
        # self.hidden=nn.Sequential(*[nn.Linear(hidden_dim,hidden_dim),activation()]*n_hidden)
        hidden_layers=[]
        for i in range(n_hidden):
            hidden_layers.append(nn.Linear(hidden_dim,hidden_dim))
            hidden_layers.append(activation())
        self.hidden=nn.Sequential(*hidden_layers)
        self.output=nn.Linear(hidden_dim,output_dim)
        self.relu=nn.ReLU()
        self.sigmoid=nn.Sigmoid()
        self.tanh=nn.Tanh()
        self.elu=nn.ELU(-0.5)
        self.softmax=nn.Softmax()

    
    def forward(self, obs:torch.FloatTensor)-> torch.FloatTensor:
        out=self.inlayer(obs)
        out=self.hidden(out)
        out=self.output(out)
        # out=self.tanh(out)*2
        out=self.softmax(out)
        return out
        
class CriticNetwork(torch.nn.Module):
    def __init__(self,input_dim:int,output_dim:int,hidden_dim:int=20,activation=nn.ReLU,n_hidden:int=3)-> None:
        super(CriticNetwork,self).__init__()
        self.inlayer=nn.Sequential(nn.Linear(input_dim,hidden_dim),activation())
        # self.hidden=nn.Sequential(*[nn.Linear(hidden_dim,hidden_dim),activation()]*n_hidden)
        hidden_layers=[]
        for i in range(n_hidden):
            hidden_layers.append(nn.Linear(hidden_dim,hidden_dim))
            hidden_layers.append(activation())
        self.hidden=nn.Sequential(*hidden_layers)
        self.output=nn.Linear(hidden_dim,output_dim)

    
    def forward(self, obs:torch.FloatTensor)-> torch.FloatTensor:
        out=self.inlayer(obs)
        out=self.hidden(out)
        out=self.output(out)
        return out
    
class Cell:
    """Objects of this class represent the biological function of a Cell"""
    def __init__(self,
                 name:str,
                 stoichiometry:callable,
                 ode_sys:callable, 
                 parameters:dict,
                 reactions:list,
                 compounds:list,
                 shape:shapes.Shape,
                 observable_states:list[str]|str,
                 controlled_params:list,
                 initial_conditions:dict[str,float],
                 gamma:float=1,
                 grad_updates:int=2,
                 policy_lr:float=0.005,
                 value_lr:float=0.01,
                 optimizer_policy:torch.optim.Optimizer=torch.optim.Adam,
                 optimizer_value:torch.optim.Optimizer=torch.optim.Adam,
                 clip:float=0.2,
                 actor_variance:float=0.1,
                 pretrain_actor:bool=False,
                 include_time:bool=True
                 ):
        self.name = name
        self.stoichiometry = stoichiometry
        self.ode_sys = ode_sys
        self.parameters = parameters
        self.shape=shape
        self.reactions = reactions
        self.compounds = compounds
        self.include_time=include_time
        if set(controlled_params).issubset(set(self.parameters.keys())):
            self.controlled_params=controlled_params
        else:
            raise Exception("The controlled parameters should be a subset of parameters")
        

        self.state_variables = self.get_state_variables()
        self.number_index=self.state_variables.index("number")
        self.volume_index=self.state_variables.index("volume")
        self.gamma=gamma
        self.kinetics={}
        self.cell_metabolites=[ind for ind,i in enumerate(self.state_variables) if not i.endswith("_env") and i not in ["number","volume"]+list(self.shape.dimensions.keys())]
        if observable_states=="all":
            observable_states=self.state_variables.copy()
        self.observable_states = [ind for ind,i in enumerate(self.state_variables) if i in observable_states]
        self._set_policy()
        self._set_value()
        self.policy_lr=policy_lr
        self.value_lr=value_lr
        self.optimizer_policy=optimizer_policy
        self.optimizer_value=optimizer_value
        self.set_optimizers()
        for dim,val in self.shape.get_dimensions().items():
            initial_conditions[dim]=val
        initial_conditions["volume"]=self.shape.volume
        initial_conditions["number"]=initial_conditions.setdefault("number",1)
        self._initial_state=tuple([initial_conditions.get(i,0) for i in self.state_variables])
        self.env_metabolites=[ind for ind,i in enumerate(self.state_variables) if i.endswith("_env")]
        self.environment=None
        self.reset()
        self.grad_updates=grad_updates
        self.clip=clip
        self.cov_var=torch.full(size=(len(controlled_params),), fill_value=actor_variance)
        self.covar_matrix=torch.diag(self.cov_var)
        if pretrain_actor:
            self._pretrain_actor()

        
        
        
    
    @property
    def initial_state(self)->np.ndarray:
        return np.array(self._initial_state,dtype=np.float64)
    
    @property
    def number(self)->float:
        return self.state[self.number_index]
    
    @property
    def volume(self)->float:
        return self.state[self.volume_index]
        
    def get_state_variables(self)->list:
        """
        This method returns the state variables of the cell. The state variables are the compounds and the shape variables\
        
        """
        state_variables = self.compounds.copy()
        shape_variables = [key for key in self.shape.dimensions.keys()]
        state_variables.extend(shape_variables)
        state_variables.append("volume")
        state_variables.append("number")
        if self.include_time:
            state_variables.append("time_env")
        return state_variables
    
    
    def can_double(self)->bool:
        if self.volume>=self.parameters["split_volume"]:
            return True
        else:
            return False
    
    def update_parameters(self,new_params:dict)->None:
        self.parameters.update(new_params)
    
    def decide(self)->tuple[torch.FloatTensor]:
        if self.controlled_params:
            outs=self.policy(torch.FloatTensor(self.state.take(self.observable_states)))        
            # dist=Normal(outs,0.1)
            dist=MultivariateNormal(outs,self.covar_matrix)
            self.actions=dist.sample()
            # self.actions[self.actions<0]=0
            # self.log_prob =torch.sum(dist.log_prob(self.actions)).detach()
            self.log_prob =dist.log_prob(self.actions).detach()
            return self.actions,self.log_prob
        else:
            self.actions=[]
            self.log_prob=[]
            return [],[]
    
    def evaluate(self,
                 batch_states:torch.FloatTensor,
                 batch_actions:torch.FloatTensor)->tuple[torch.FloatTensor]:
        if self.controlled_params:
            outs=self.policy(batch_states[:,self.observable_states])
            # dist=Normal(outs,0.1)
            dist=MultivariateNormal(outs,self.covar_matrix)

            # log_prob = torch.sum(dist.log_prob(batch_actions),dim=1)
            log_prob = dist.log_prob(batch_actions)
            v=self.value(batch_states[:,self.observable_states])
            # extra_loss=(torch.relu(self.ranges[:,0]-outs)+torch.relu(outs-self.ranges[:,1])).mean()
            return v,log_prob.unsqueeze(dim=1)

        else:
            return [],[]

    
    def _decision_to_params(self,decision:torch.FloatTensor)->dict:
        return dict(zip(self.controlled_params,decision))
    
    def _set_policy(self)->None:
        if self.controlled_params:
            self.policy = ActorNetwork(len(self.observable_states),len(self.controlled_params),hidden_dim=20,activation=nn.ReLU,n_hidden=5)
    
    def _set_value(self)->None:
        if self.controlled_params:
            self.value = CriticNetwork(len(self.observable_states),1,hidden_dim=20,activation=nn.ReLU,n_hidden=5)
    
    def reset(self)->None:
        self.state=self.initial_state
        self.reward=0
        return
    
    @property
    def state(self)->np.ndarray:
        return self._state
    
    @state.setter
    def state(self,state:np.ndarray)->None:
        self._state=state
    
    @property
    def reward(self)->float:
        return self._reward
    
    @reward.setter
    def reward(self,reward:float)->None:
        self._reward=reward

    def process_data(self,data:dict[str,np.ndarray])->None:
        data["s`"]=torch.FloatTensor(data["s`"])
        data["r"]=torch.FloatTensor(data["r"])
        data["a"]=torch.FloatTensor(data["a"])
        data["s"]=torch.FloatTensor(data["s"])
    
    def set_optimizers(self)->None:
        if self.controlled_params:
            self.optimizer_policy_=self.optimizer_policy(self.policy.parameters(),lr=self.policy_lr)
            self.optimizer_value_=self.optimizer_value(self.value.parameters(),lr=self.value_lr)
    def _pretrain_actor(self,num_iter:int=10000)->None:
        ### get random numbers for states
        if self.controlled_params:
            states=torch.FloatTensor(np.random.rand(1000,len(self.observable_states)))*100
            actions=torch.FloatTensor(np.ones((1000,len(self.controlled_params)))/10)
            for i in range(num_iter):
                outs=self.policy(states)
                self.optimizer_policy_.zero_grad()
                loss=torch.nn.MSELoss()(outs,actions)
                loss.backward()
                self.optimizer_policy_.step()
                print(f"Pretraining iteration {i} completed: Loss {loss}",end="\r")
        
    
    
class Environment:
    def __init__(self, 
                 name:str, 
                 cells:Iterable[Cell],
                 extra_states:Iterable[str],
                 initial_conditions:dict[str,float],
                 controllers:dict[str,callable],
                 time_step:float=0.1
                ):
        self.name = name
        self.cells = cells
        for cell in self.cells:
            cell.environment=self
            cell.dt=time_step
        self.environment_vars=self.resolve_env_vars(extra_state=extra_states)
        self.initial_conditions = initial_conditions
        for c_states,func in controllers.items():
            self.initial_conditions[c_states]=func(self.get_state_from_initial_conditions())
        for compound in set(self.environment_vars).difference(set(initial_conditions.keys())):
            self.initial_conditions[compound]=0
        self.state=self.get_state_from_initial_conditions()
        self.controllers=controllers
        self.time_step=time_step
    
    def resolve_env_vars(self,extra_state:Iterable[str])->list:
        env_vars=[]
        env_vars_mapping={}
        for cell in self.cells:
            env_vars_mapping[cell.name]={}
            env_comps=[i for i in enumerate(cell.state_variables) if i[1].endswith("_env")]
            for ind,comp in env_comps:
                env_vars_mapping[cell.name][comp]=ind
            env_vars.extend([i[1] for i in env_comps])
        env_vars=[i.name for i in self.cells]+sorted(list(set(env_vars)-set("time_env")))+extra_state+["time_env"] # Makes sure that time_env is the last variable and only appears once
        self.env_vars_mapping=env_vars_mapping
        return env_vars
    
    def get_state_from_initial_conditions(self)->dict[str,float]:
        return {key:self.initial_conditions.get(key,0) for key in self.environment_vars}
        
    def pass_env_states(self)->None:
        """A critical method to communicate environment states to the cells. This method updates the states of the cells with the environment states."""
        for cell in self.cells:
            for key,value in self.env_vars_mapping[cell.name].items():
                cell.state[value]=self.state[key]
        return
    def reset(self)->None:
        self.state=self.get_state_from_initial_conditions()
        for c_states,func in self.controllers.items():
            self.initial_conditions[c_states]=func(self.state)
        for cell in self.cells:
            cell.reset()
        self.pass_env_states()
        return
    
    @property
    def done(self)->bool:
        return self.state["time_env"]-(self.num_steps-1)*self.time_step>-0.00001
    
    def step(self)->dict[str,np.ndarray]:
        ### to update the information of the agents about the environment
        self.pass_env_states()
        previous_states={cell.name:cell.state.copy() for cell in self.cells}
        rewards={}
        actions={}
        ddt_collections={}
        for cell in self.cells:
            dydt=cell.ode_sys(self.state['time_env'],cell.state,cell)
            cell.state+=dydt*self.time_step
            
            # if self.done:
            #     cell.reward=cell.number
            # else:
            #     cell.reward=0
            
            rewards[cell.name]=cell.reward
            actions[cell.name]=cell.actions
            for comp,ind in self.env_vars_mapping[cell.name].items():
                ddt_collections[comp]=ddt_collections.get(comp,0)+dydt[ind]
        
        for key in ddt_collections:
            self.state[key]+=ddt_collections[key]
        
        self.state['time_env']+=self.time_step
        
        
        for c_states,func in self.controllers.items():
            self.state[c_states]=func(self.state)   
        
        self.pass_env_states()

        return ({cell.name:cell.state.copy() for cell in self.cells},rewards,actions,previous_states,{cell.name:cell.log_prob for cell in self.cells})
                
class Trainer:
    """This is a class to train the agents in a given environment"""
    def __init__(self,
                 env:Environment,
                 episodes_per_batch:int,
                 steps_per_episode:int,
                 number_of_batches:int,
                 save_every:int,
                 save_path:str,
                 parallel_framework:str="ray",
                 ):
    
        self.env=env
        self.episodes_per_batch=episodes_per_batch
        self.steps_per_episode=steps_per_episode
        self.env.num_steps=steps_per_episode
        self.number_of_batches=number_of_batches
        self.save_every=save_every
        self.save_path=save_path
        self.parallel_framework=parallel_framework
        

    
    def run_batch(self)->dict[dict]:
        if self.parallel_framework=="ray":
            results=ray.get([run_episode_ray.remote(self.env,self.steps_per_episode) for i in range(self.episodes_per_batch)])
        elif self.parallel_framework=="native":
            pass
        return results
    
    def train(self):
        returns={agent.name:[] for agent in self.env.cells}
        for i in range(self.number_of_batches):
            res=self.run_batch()
            data={agent.name:{} for agent in self.env.cells}
            sum_rewards={agent.name:list() for agent in self.env.cells}
            for episode in res:
                for step in episode:
                    for agent in self.env.cells:
                        data[agent.name].setdefault("r",list()).append(step[1][agent.name])
                        data[agent.name].setdefault("a",list()).append(step[2][agent.name])
                        data[agent.name].setdefault("s",list()).append(step[3][agent.name])
                        data[agent.name].setdefault("log_prob",list()).append(step[4][agent.name])
                for agent in self.env.cells:
                    data[agent.name].setdefault("rtgs",list()).extend(calculate_rtgs(data[agent.name]["r"][-len(episode):],agent.gamma))
                    sum_rewards[agent.name].append(np.sum(data[agent.name]["r"][-len(episode):]))
                    
            
        
            for agent in self.env.cells:
                
                data[agent.name]["r"]=torch.FloatTensor(np.array(data[agent.name]["r"]))
                data[agent.name]["a"]=torch.FloatTensor(np.array(data[agent.name]["a"]))
                data[agent.name]["s"]=torch.FloatTensor(np.array(data[agent.name]["s"]))
                data[agent.name]["rtgs"]=torch.FloatTensor(np.array(data[agent.name]["rtgs"])).unsqueeze(dim=1)
                data[agent.name]["log_prob"]=torch.FloatTensor(np.array(data[agent.name]["log_prob"])).unsqueeze(dim=1)
                returns[agent.name].append(np.mean(sum_rewards[agent.name]))
                data[agent.name]["avg_rewa"]=returns[agent.name]
                if agent.controlled_params:
                    for _ in range(agent.grad_updates):
                        v,_=agent.evaluate(data[agent.name]["s"],data[agent.name]["a"])
                        a_k=data[agent.name]["rtgs"]-v.detach()
                        a_k=(a_k - a_k.mean()) / (a_k.std() + 1e-5)
                        v,lps=agent.evaluate(data[agent.name]["s"],data[agent.name]["a"])
                        ratios = torch.exp( lps - data[agent.name]["log_prob"])
                        surr1 = ratios * a_k.detach()
                        surr2 = torch.clamp(ratios, 1-agent.clip, 1+agent.clip) * a_k
                        actor_loss = (-torch.min(surr1, surr2)).mean()
                        critic_loss = torch.nn.MSELoss()(v,data[agent.name]["rtgs"])
                        agent.optimizer_policy_.zero_grad()
                        actor_loss.backward(retain_graph=False)
                        agent.optimizer_policy_.step()
                        agent.optimizer_value_.zero_grad()
                        critic_loss.backward()
                        agent.optimizer_value_.step()
                print(f"Batch {i} completed:")
            
            for agent in self.env.cells:
                print(f"Avg reward for {agent.name} is {returns[agent.name][-1]}")
            if self.save_every!=-1:
                if i%self.save_every==0:
                    for agent in self.env.cells:
                        data[agent.name]["state_vars"]=agent.state_variables.copy()
                        data[agent.name]["action_vars"]=agent.controlled_params
                    if not os.path.exists(self.save_path):
                        os.makedirs(self.save_path)
                    with open(f"{self.save_path}/data_batch_{i}.pkl","wb") as f:
                        pickle.dump(data,f)
                        
    @classmethod
    def from_json_config(cls,config:str|pathlib.Path)->"Trainer":
        with open(config,"r") as f:
            config=json.load(f)
        cell=Cell(config["name"],
              getattr(globals()["models"],config["stoichiometric_matrix"]),
              getattr(globals()["models"],config["ode_system"]),
              config["model_parameters"],
              config["reactions"],
              config["species"],
              getattr(globals()["shapes"],config["shape"]["type"])(config["shape"]["parameters"]),
              controlled_params=config["controlled_parameters"],
              observable_states=config["observable_states"],
              initial_conditions=config["initial_conditions"],
              grad_updates=config["gradient_updates"],
              policy_lr=config["policy_lr"],
              value_lr=config["value_lr"],
              clip=config["clip"],
              actor_variance=config["actor_variance"],
              pretrain_actor=config["pre_train_actor"]
        )
        env=Environment(name=config["environment_name"],
                cells=[cell],
                initial_conditions=config["environment_initial_conditions"],
                extra_states=[],
                controllers={k:globals()[v] for k,v in config["controllers"].items()},
                time_step=config["time_step"])
        
        trainer=Trainer(env,
                config["episodes_per_batch"],
                config["episode_length"],
                config["number_of_batches"],
                config["save_every"],
                config.get("save_path",""),
                parallel_framework="ray")
        
        return trainer
        
                    
                    

                    
            
            

                
                
                           

                
                
def calculate_rtgs(rewards:np.ndarray,gamma:float)->np.ndarray:
    rtgs=[]
    rtg=0
    for i in reversed(rewards):
        rtg=i+gamma*rtg
        rtgs.insert(0,rtg)
    return rtgs
    
    
    
def run_episode(env:Environment,num_steps:int)->list[tuple[dict]]:
    env.num_steps=num_steps
    env.reset()
    return [env.step() for i in range(num_steps)]   

@ray.remote
def run_episode_ray(env:Environment,num_steps:int)->list[tuple[dict]]:
    env.reset()
    return [env.step() for i in range(num_steps)]


def S_controller(state:dict[str,float])->float:
    amplitude=50
    period=50
    # return amplitude*max(np.sin(2*np.pi*state["time_env"]/period),0)
    return (amplitude if state["time_env"]<25 else 0)
    # return max(amplitude-state["time_env"]*(amplitude)/25,0)
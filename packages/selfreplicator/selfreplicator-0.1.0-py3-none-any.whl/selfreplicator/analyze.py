import pickle as pkl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
from plotly.validators.scatter.marker import SymbolValidator
from typing import Iterable
import plotly.colors as pc
COLORS = px.colors.qualitative.Plotly+px.colors.qualitative.Dark24
class BatchDataProcessor:
    def __init__(self,
                 data:str,
                 batch_size:int,
                 ):
        self.data = data
        self.batch_size = batch_size
        
        with open(self.data, 'rb') as f:
            self._data = pkl.load(f)
        self.agents=list(self._data.keys())
        self.state_vars = {}
        self.action_vars={}
        for agent in self._data.keys():
            self.state_vars[agent]=list(self._data[agent]["state_vars"])
            self.action_vars[agent]=list(self._data[agent]["action_vars"])
        
    def visualize_actions(self,agent:str,actions:Iterable="all",**kwargs):
        all_data=[pd.DataFrame(self._data[agent]["a"].numpy().reshape((-1,self.batch_size,len(self.action_vars[agent])),order='F').mean(axis=1),columns=self.action_vars[agent]),
            pd.DataFrame(self._data[agent]["a"].numpy().reshape((-1,self.batch_size,len(self.action_vars[agent])),order='F').min(axis=1),columns=self.action_vars[agent]),
            pd.DataFrame(self._data[agent]["a"].numpy().reshape((-1,self.batch_size,len(self.action_vars[agent])),order='F').max(axis=1),columns=self.action_vars[agent])]
        fig=go.Figure()
        
        if actions=="all":
            present_var=self.action_vars[agent]
        else:
            present_var=actions
        for key,color in zip(present_var,COLORS,strict=False):
            fig.add_trace(go.Scatter(x=all_data[0].index,y=all_data[0][key],mode='lines',line={"color":color},legendgroup=key,name=key))
            fig.add_trace(go.Scatter(x=all_data[1].index.to_list()+all_data[2].index[::-1].to_list(),y=all_data[1][key].to_list()+all_data[2][key][::-1].to_list(),
                                 fill='toself',
                                 fillcolor='rgba'+str(pc.hex_to_rgb(color)+(0.2,)),
                                 name=key,
                                 legendgroup=key,
                                 showlegend=False,
                                 line=dict(color='rgba'+str(pc.hex_to_rgb(color)+(0,)),)))
                             
        fig.update_layout(
            **kwargs
        )
        return fig

    
    def visualize_states(self,agent:str,states:Iterable="all",**kwargs):
        all_data=[pd.DataFrame(self._data[agent]["s"].numpy().reshape((-1,self.batch_size,len(self.state_vars[agent])),order='F').mean(axis=1),columns=self.state_vars[agent]),
            pd.DataFrame(self._data[agent]["s"].numpy().reshape((-1,self.batch_size,len(self.state_vars[agent])),order='F').min(axis=1),columns=self.state_vars[agent]),
            pd.DataFrame(self._data[agent]["s"].numpy().reshape((-1,self.batch_size,len(self.state_vars[agent])),order='F').max(axis=1),columns=self.state_vars[agent])]
        fig=go.Figure()
        
        if states=="all":
            present_var=self.state_vars[agent]
        else:
            present_var=states
        for key,color in zip(present_var,COLORS,strict=False):
            fig.add_trace(go.Scatter(x=all_data[0].index,y=all_data[0][key],mode='lines',line={"color":color},legendgroup=key,name=key))
            fig.add_trace(go.Scatter(x=all_data[1].index.to_list()+all_data[2].index[::-1].to_list(),y=all_data[1][key].to_list()+all_data[2][key][::-1].to_list(),
                                 fill='toself',
                                 fillcolor='rgba'+str(pc.hex_to_rgb(color)+(0.2,)),
                                 name=key,
                                 legendgroup=key,
                                 showlegend=False,
                                 line=dict(color='rgba'+str(pc.hex_to_rgb(color)+(0,)),)))
                             
        fig.update_layout(
            **kwargs
        )
        return fig
        
        
    
    def visualize_rewards(self,agent:str,**kwargs):
        df=pd.DataFrame(self._data[agent]["avg_rewa"],columns=["rewards"])
        fig=px.line(df,x=df.index,y=df.columns)
        fig.update_layout(
            **kwargs
        )
        return fig
        

class CompareDataProcessor:
    def __init__(self,
                 data:dict[str:BatchDataProcessor],
                ):
        self.data = data
        
    def compare_states(self,agent:str,on:str='all')->None:
        collector={key:pd.DataFrame(pd.DataFrame(value._data[agent]["s"].numpy().reshape((-1,value.batch_size,len(value.state_vars[agent])),order='F').mean(axis=1),columns=value.state_vars[agent])) for key,value in self.data.items()}
        if on=='all':
            fig=go.Figure()
            for key,color in zip(collector.keys(),COLORS,strict=False):
                
                for state in collector[key].columns:
                    fig.add_trace(go.Scatter(x=collector[key].index,y=collector[key][state],mode='lines',line={"color":color},name=key+"_"+state))            
            fig.show()
        else:
            fig=go.Figure()
            for key in collector.keys():
                fig.add_trace(go.Scatter(x=collector[key].index,y=collector[key][on],mode='lines',name=key))

            fig.show()
    
    def compare_actions(self,agent:str,on:str='all')->None:
        
        collector={key:[pd.DataFrame(value._data[agent]["a"].numpy().reshape((-1,value.batch_size,len(value.action_vars[agent])),order='F').mean(axis=1),columns=value.action_vars[agent]),
                        pd.DataFrame(value._data[agent]["a"].numpy().reshape((-1,value.batch_size,len(value.action_vars[agent])),order='F').min(axis=1),columns=value.action_vars[agent]),
                        pd.DataFrame(value._data[agent]["a"].numpy().reshape((-1,value.batch_size,len(value.action_vars[agent])),order='F').max(axis=1),columns=value.action_vars[agent])]
                        for key,value in self.data.items()}
        
        if on=='all':
            fig=go.Figure()
            for key,color in zip(collector.keys(),COLORS,strict=False):
                for action in collector[key][0].columns:
                    fig.add_trace(go.Scatter(x=collector[key][0].index,y=collector[key][0][action],mode='lines',line={"color":color},legendgroup=key+action,name=key+"_"+action))
                    fig.add_trace(go.Scatter(x=collector[key][1].index.to_list()+collector[key][2].index[::-1].to_list(),y=collector[key][1][action].to_list()+collector[key][2][action][::-1].to_list(),
                                         fill='toself',
                                         fillcolor='rgba'+str(pc.hex_to_rgb(color)+(0.2,)),
                                         name=key,
                                         legendgroup=key+action,
                                         showlegend=False,
                                         line=dict(color='rgba'+str(pc.hex_to_rgb(color)+(0,)),)))

                                 
            fig.show()
        
        else:
            fig=go.Figure()
            for index,key in enumerate(collector.keys()):
                fig.add_trace(go.Scatter(x=collector[key][0].index,y=collector[key][0][on],mode='lines', legendgroup=key,name=key, line={"color":COLORS[index]}))
                fig.add_trace(go.Scatter(x=collector[key][1].index.to_list()+collector[key][2].index[::-1].to_list(),y=collector[key][1][on].to_list()+collector[key][2][on][::-1].to_list(),
                                         fill='toself',
                                         fillcolor='rgba'+str(pc.hex_to_rgb(COLORS[index])+(0.2,)),
                                         name=key,
                                         legendgroup=key,
                                         showlegend=False,
                                         line=dict(color='rgba'+str(pc.hex_to_rgb(COLORS[index])+(0,)), 
                                         )))
                

            fig.show()
    

    def make_actions_movie(self, agent: str, on: list[str]) -> None:
        # Collect data for each key in self.data
        collector = {
            key: [
                pd.DataFrame(
                    value._data[agent]["a"].numpy().reshape((-1, value.batch_size, len(value.action_vars[agent])), order='F').mean(axis=1),
                    columns=value.action_vars[agent]
                ),
                pd.DataFrame(
                    value._data[agent]["a"].numpy().reshape((-1, value.batch_size, len(value.action_vars[agent])), order='F').min(axis=1),
                    columns=value.action_vars[agent]
                ),
                pd.DataFrame(
                    value._data[agent]["a"].numpy().reshape((-1, value.batch_size, len(value.action_vars[agent])), order='F').max(axis=1),
                    columns=value.action_vars[agent]
                )
            ]
            for key, value in self.data.items()
        }

        frames = []
        for key in collector.keys():
            data=[]
            for index, action in enumerate(on):
                data.append(go.Scatter(
                            x=collector[key][0].index,
                            y=collector[key][0][action],
                            mode='lines',
                            legendgroup=action,
                            name=action,
                            line={"color": COLORS[index]}
                        ),)
                data.append(go.Scatter(
                            x=collector[key][1].index.to_list() + collector[key][2].index[::-1].to_list(),
                            y=collector[key][1][action].to_list() + collector[key][2][action][::-1].to_list(),
                            fill='toself',
                            fillcolor='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0.2,)),
                            name=action,
                            legendgroup=action,
                            showlegend=False,
                            line=dict(color='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0,))),
                        ))
            frames.append(go.Frame(data=data,
                                   layout=go.Layout(title=
                                                    {"text":key,
                                                     "x":0.5,
                                                     "font":{"size":30,'family':'Arial'}
                                                     },
                                                    font={"size":30,'family':'Arial'},
                                                    )))
                
        initial_data = []
        key=list(collector.keys())[0]
        for index, action in enumerate(on):
            initial_data.append(
                go.Scatter(
                    x=collector[key][0].index,
                    y=collector[key][0][action],
                    mode='lines',
                    legendgroup=action,
                    name=action,
                    line={"color": COLORS[index]}
                )
            )
            initial_data.append(
                go.Scatter(
                    x=collector[key][1].index.to_list() + collector[key][2].index[::-1].to_list(),
                    y=collector[key][1][action].to_list() + collector[key][2][action][::-1].to_list(),
                    fill='toself',
                    fillcolor='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0.2,)),
                    name=action,
                    legendgroup=action,
                    showlegend=False,
                    line=dict(color='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0,))),
                )
            )

        fig = go.Figure(
            data=initial_data,
            layout=go.Layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="Play",

                                method="animate",
                                args=[None]
                            )
                        ]
                    )
                ]
            ),
            frames=frames
        )
        fig.update_layout(
            title_text="Iteration: 0",
            title_x=0.5,
            font={"size": 30, 'family': 'Arial'},
        )
        fig.show()
        return fig
        
    def make_states_movie(self, agent: str, on: list[str],report_as_concentration:bool=False) -> None:
        # Collect data for each key in self.data
        if not report_as_concentration:
            collector = {
               key: 
                   [pd.DataFrame(value._data[agent]["s"].numpy().reshape((-1, value.batch_size, len(value.state_vars[agent])), order='F').mean(axis=1),
                   columns=value.state_vars[agent]),
                    pd.DataFrame(value._data[agent]["s"].numpy().reshape((-1, value.batch_size, len(value.state_vars[agent])), order='F').min(axis=1),
                   columns=value.state_vars[agent]),
                       pd.DataFrame(value._data[agent]["s"].numpy().reshape((-1, value.batch_size, len(value.state_vars[agent])), order='F').max(axis=1),
                   columns=value.state_vars[agent])
               ]
                   for key, value in self.data.items()
            }
        else:
                    collector = {
           key: 
               [pd.DataFrame((value._data[agent]["s"].numpy()/(value._data[agent]["s"].numpy()[:,value.state_vars[agent].index("volume")].reshape(-1,1))).reshape((-1, value.batch_size, len(value.state_vars[agent])), order='F').mean(axis=1),
               columns=value.state_vars[agent]),
                pd.DataFrame((value._data[agent]["s"].numpy()/(value._data[agent]["s"].numpy()[:,value.state_vars[agent].index("volume")].reshape(-1,1))).reshape((-1, value.batch_size, len(value.state_vars[agent])), order='F').min(axis=1),
                columns=value.state_vars[agent]),
                     pd.DataFrame((value._data[agent]["s"].numpy()/(value._data[agent]["s"].numpy()[:,value.state_vars[agent].index("volume")].reshape(-1,1))).reshape((-1, value.batch_size, len(value.state_vars[agent])), order='F').max(axis=1),
                columns=value.state_vars[agent])
           ]
               for key, value in self.data.items()
        }
           
        
                    

        frames = []
        for key in collector.keys():
            data=[]
            for index, state in enumerate(on):
                data.append(go.Scatter(
                            x=collector[key][0].index,
                            y=collector[key][0][state],
                            mode='lines',
                            legendgroup=state,
                            name=state,
                            line={"color": COLORS[index]}
                        ),)
                data.append(go.Scatter(
                            x=collector[key][1].index.to_list() + collector[key][2].index[::-1].to_list(),
                            y=collector[key][1][state].to_list() + collector[key][2][state][::-1].to_list(),
                            fill='toself',
                            fillcolor='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0.2,)),
                            name=state,
                            legendgroup=state,
                            showlegend=False,
                            line=dict(color='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0,))),
                        ))
            frames.append(go.Frame(data=data,
                                   layout=go.Layout(title=
                                                    {"text":key,
                                                     "x":0.5,
                                                     "font":{"size":30,'family':'Arial'}
                                                     },
                                                    font={"size":30,'family':'Arial'},
                                                    ))
                           )
            
        initial_data = []
        
        for index, state in enumerate(on):
            initial_data.append(
                go.Scatter(
                    x=collector[key][0].index,
                    y=collector[key][0][state],
                    mode='lines',
                    legendgroup=state,
                    name=state,
                    line={"color": COLORS[index]}
                )
            )
            initial_data.append(
                go.Scatter(
                    x=collector[key][1].index.to_list() + collector[key][2].index[::-1].to_list(),
                    y=collector[key][1][state].to_list() + collector[key][2][state][::-1].to_list(),
                    fill='toself',
                    fillcolor='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0.2,)),
                    name=state,
                    legendgroup=state,
                    showlegend=False,
                    line=dict(color='rgba' + str(pc.hex_to_rgb(COLORS[index]) + (0,))),
                )
            )
            
        fig = go.Figure(
            data=initial_data,
            layout=go.Layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="Play",

                                method="animate",
                                args=[None]
                            )
                        ]
                    )
                ]
            ),
            frames=frames
        )
        fig.update_layout(
            title_text="Iteration: 0",
            title_x=0.5,
            font={"size": 30, 'family': 'Arial'},
        )
        fig.show()
    
    def compare_rewards(self,agent:str,**kwargs)->go.Figure:
        collector={
            key:pd.DataFrame(value._data[agent]["avg_rewa"],columns=["rewards"])
            for key,value in self.data.items()
        }
        fig=go.Figure()
        for key in collector.keys():
            fig.add_trace(go.Scatter(x=collector[key].index,y=collector[key]["rewards"],mode='lines',name=key))
        fig.update_layout(**kwargs)
        return fig
        
    def make_rewards_movie(self, agent: str) -> None:
        collector={
            key:pd.DataFrame(value._data[agent]["avg_rewa"],columns=["rewards"])
            for key,value in self.data.items()
        }
        
        frames=[]
        for index,key in enumerate(collector.keys()):
            frames.append(go.Frame(data=[go.Scatter(x=collector[key].index,y=collector[key]["rewards"],
                                                    mode='lines',name=key,
                                                    legendgroup="Return of "+agent,
                                                    line={"color":COLORS[0]})],
                                 layout=go.Layout(title=
                                                    {"text":key,
                                                     "x":0.5,
                                                     "font":{"size":30,'family':'Arial'}
                                                     },
                                                    font={"size":30,'family':'Arial'},
                                                    )
                                   ))
    
        for key in collector.keys():
            initial_data=[go.Scatter(x=collector[key].index,y=collector[key]["rewards"],
                                     mode='lines',
                                     name=key,legendgroup="Return of "+agent,
                                     line=dict(color=COLORS[0]))]
            break
        
        fig=go.Figure(data=initial_data,
                        layout=go.Layout(
                            updatemenus=[
                                dict(
                                    type="buttons",
                                    buttons=[
                                        dict(
                                            label="Play",
                                            method="animate",
                                            args=[None]
                                        )
                                    ]
                                )
                            ]
                        ),
                        frames=frames
                        )
        fig.show()
        return fig
        
            
        
        
        
        
if __name__ == "__main__":
    base_dir="/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/sin_input_with_time/data_batch"
    # compare=CompareDataProcessor(
    #     {
    #         "data1":BatchDataProcessor(data1,8),
    #         "data2":BatchDataProcessor(data2,8),
    #     }
    # )
    # compare.compare_actions("Toy Model","k_t1")
    
    compare=CompareDataProcessor(
        {
            f"Batch {i}":BatchDataProcessor(base_dir+f"_{i}.pkl",12) for i in range(0,2001,100)
        }
        
            # {
            #     "Time_Aware":BatchDataProcessor("/Users/parsaghadermarzi/Desktop/Academics/Projects/Reinforcement_Learning_Modeling/selfreplicator/replication_with_time_sin_rep2/data_batch_5000.pkl",32),
            #     "Not_Time_Aware":BatchDataProcessor("/Users/parsaghadermarzi/Desktop/Academics/Projects/Reinforcement_Learning_Modeling/selfreplicator/replication_without_time_sin/data_batch_5000.pkl",32),
            # }
    )
    # compare.compare_rewards("Toy Model")
    # compare.compare_actions("Toy Model")
# BatchDataProcessor(data1,8).visualize_states("Toy Model")
    # BatchDataProcessor(data6,8).visualize_rewards("Toy Model")
    # compare.make_actions_movie("Toy Model",["k_t1","k_e2","k_e3","k_e4","k_e5","k_e6","k_e7","k_t2","k_e8","k_e9"]).write_html("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/actions.html")
    # # # compare.make_states_movie("Toy Model",["S_env","S","t1","t2","e2","e3","e4","e5","e6","e7"])
    # # # BatchDataProcessor(base_dir+f"_12900.pkl",8).visualize_states("Toy Model")
    # # # BatchDataProcessor(base_dir+f"_12900.pkl",8).visualize_rewards("Toy Model")
    # compare.make_rewards_movie("Toy Model").write_html("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/rewards.html")
    # compare.make_states_movie("Toy Model",["S_env","S","t1","t2","e2","e3","e4","e5","e6","e7","volume","e","E","g","I1","e8","e9","W"],report_as_concentration=False)
    

    # compare.compare_actions("Toy Model",on="k_e9")
    # compare.compare_actions("Toy Model",on="k_e8")
    # compare.compare_states("Toy Model",on="e9")
    # BatchDataProcessor(base_dir+f"_{0}.pkl",12).visualize_actions("Toy Model",actions=["k_t1","k_e8","k_e9","k_e7"],width=1000,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_0.svg")
    # BatchDataProcessor(base_dir+f"_{200}.pkl",12).visualize_actions("Toy Model",actions=["k_t1","k_e8","k_e9","k_e7"],width=1000,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_200.svg")
    # BatchDataProcessor(base_dir+f"_{1000}.pkl",12).visualize_actions("Toy Model",actions=["k_t1","k_e8","k_e9","k_e7"],width=1000,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_1000.svg")
    # BatchDataProcessor(base_dir+f"_{5000}.pkl",12).visualize_actions("Toy Model",actions=["k_t1","k_e8","k_e9","k_e7"],width=1000,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_5000.svg")
    # BatchDataProcessor(base_dir+f"_{10000}.pkl",12).visualize_actions("Toy Model",actions=["k_t1","k_e8","k_e9","k_e7"],width=1000,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_10000_sin.svg")
    # BatchDataProcessor(base_dir+f"_{10000}.pkl",12).visualize_states("Toy Model",states=["S_env"],width=1000,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_10000_sin_S_env.svg")
    # BatchDataProcessor(base_dir+f"_{10000}.pkl",12).visualize_states("Toy Model",states=["S","I1"],width=1000,height=600,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_10000_sin_I1_S.svg")
    # BatchDataProcessor(base_dir+f"_{10000}.pkl",12).visualize_rewards("Toy Model",width=1000,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_without_maintenance_rew_sin.svg")
    # bd.visualize_states("Toy Model",states=["g"],width=800,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_with_maintenance_g.svg")
    # bd.visualize_actions("Toy Model",actions=["k_e8","k_e9"],width=800,height=500,font={"size":20}).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/states_with_maintenance_actions.svg")
    # BatchDataProcessor(base_dir+f"_{19900}.pkl",8).visualize_actions("Toy Model",actions=["k_t1","k_e7"],width=1000,height=500,font={"size":20}).show()
    # cmp=CompareDataProcessor(
    #     {"With Time Sensor":BatchDataProcessor("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/sin_input_with_time/data_batch_1900.pkl",12),
    #     "Without Time Sensor":BatchDataProcessor("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/sin_input_without_time/data_batch_1900.pkl",12),}
    # )
    # fig=cmp.compare_rewards("Toy Model")
    # fig.update_layout(
    #     width=1200,
    #     height=800,
    #     font={
    #         "size":30
    #     },
    #     xaxis={
    #         "title":"Time"
    #     },
    #     yaxis={
    #         "title":"Average Batch Return"
    #     }
    # )
    # fig.data[0].line.width=5
    # fig.data[1].line.width=5
    # fig.write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/return_comparison.svg")
    BatchDataProcessor(base_dir+f"_{2000}.pkl",12).visualize_actions("Toy Model",font={"size":30},width=1000,height=800).write_image("/Users/parsaghadermarzi/Desktop/Academics/PhD_Dissertation/actions2000_with.svg")
import numpy as np

class Shape:
    """Objects of this class represent the shape of a cell"""
    def __init__(self, name:str,dimensions:tuple[dict[str,float]]):
        self.name = name
        self.dimensions = dimensions
        for key, value in dimensions.items():
            setattr(self, key, value)
    
    def __str__(self) -> str:
        dim_print=""
        for key, value in self.__dict__.items():
            dim_print += f"{key} = {value}\n"
        return f"{self.name} shape with dimensions:\n{dim_print}"
    
    def __repr__(self) -> str:
        return f"Shape({self.name},{self.dimensions})"
    
    @property
    def volume(self)->float:
        pass
    
    @property
    def area(self)->float:
        pass
    
    def calculate_differentials(self,dv:float)->dict[str,float]:
        pass
    def set_dim_from_volume(self,v:float)->None:
        pass
    

class Sphere(Shape):
    """Objects of this class represent a sphere. 
    NOTE: This is hollow sphere. So, the constructor takes in a dictionary with the following
    keys: r,t. r is the radius of the sphere and t is the thickness of the sphere.
    The assumption in this class is that the thickness is uniform and throughout the sphere.
    """
    def __init__(self, dimensions:dict[str,float])->None:
        if {"r","t"} != set(dimensions.keys()):
            raise ValueError("Sphere shape requires only parameter r")
        super().__init__("Sphere", dimensions)
    
    @property
    def volume(self)->float:
        return 4/3*np.pi*self.r**3
    
    @property
    def area(self)->float:
        return 4*np.pi*self.r**2
    
    def set_dimensions(self,dimensions:dict[str,float])->None:
        self.dimensions = dimensions
        for key, value in dimensions.items():
            setattr(self, key, value)
    
    def get_dimensions(self)->dict[str,float]:
        return {key:getattr(self,key) for key in self.dimensions.keys()}
        
    
    def set_dim_from_volume(self,v:float)->None:
        self.r = (3*v/(4*np.pi))**(1/3)

    def calculate_differentials(self,dv:float)->dict[str,float]:
        """V=4*pi*[3rt^3+3t^2r+t^3] this equation should be used:
        dV=4*pi*[6rt+3t^2]*dr
        dr=dv/(4*pi*[6rt+3t^2])
        """
        diffs={k:0 for k in self.dimensions.keys()}
        diffs.update({"r":dv/(4*np.pi*(6*self.r*self.t + 3*self.t**2))})
        return diffs
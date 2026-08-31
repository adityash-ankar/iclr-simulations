import numpy as np
import math
class Material:
    def __init__(self, Material):
        self.name = Material
        if self.name == 'Inconel718':
            self.poissonratio   = 0.28
            self.emissivity     = 0.3
        elif self.name == 'AlSi10Mg':
            self.poissonratio   = 0.33
            self.emissivity     = 0.650
        elif self.name == 'ABD900':
            self.poissonratio   = 0.28
            self.emissivity     = 0.3
    
    def surf_roughness(self, angle):
        if self.name == 'Inconel718':
            Surf_roughness      = np.array([54, 38, 12, 6, 5]) * 1e-6 * 10
            manufacturing_angle = np.array([30, 45, 60, 75, 90]) * math.pi/180
        elif self.name == 'AlSi10Mg':
            Surf_roughness      = np.array([66, 56, 21, 12, 8]) * 1e-6 * 10
            manufacturing_angle = np.array([30, 45, 60, 75, 90]) * math.pi/180
        elif self.name == 'ABD900':
            Surf_roughness      = np.array([54, 38, 12, 6, 5]) * 1e-6 * 0.7 * 10
            manufacturing_angle = np.array([30, 45, 60, 75, 90]) * math.pi/180
        else:
            raise ValueError("Unknown Material")
        
        return(np.interp(angle, manufacturing_angle, Surf_roughness))
    
    def conductivity(self, temp):
        if self.name == 'Inconel718':
            conductivity  = 12
        elif self.name == 'AlSi10Mg':
            conductivity        = 140
        elif self.name == 'ABD900':
            conductivity_array        = np.array([11, 12.6, 15.7, 18.8, 23.2, 26.4, 30.1])
            conductivity_temps  = np.array([25, 200, 400, 600, 800, 1000, 1200]) + 273.15
            conductivity        = np.interp(temp, conductivity_temps, conductivity_array)
        else:
            raise ValueError("Unknown Material")
        return conductivity
            
    def modulus(self, temp):
        if self.name == 'Inconel718':
            modulus_temps = np.array([21, 93, 204, 316, 427, 538, 649, 760, 871, 954]) + 273.15
            modulus       = np.array([208, 205, 202, 194, 186, 179, 172, 162, 127, 78]) * 1e9
            return np.interp(temp, modulus_temps, modulus)
        elif self.name == 'AlSi10Mg':
            modulus_temps = np.array([25, 50, 100, 150, 200, 250, 300, 350, 400]) + 273.15
            modulus       = np.array([77.6, 75.5, 72.8, 63.2, 60, 55, 45, 37, 28]) * 1e9
            return np.interp(temp, modulus_temps, modulus)
        elif self.name == 'ABD900':
            modulus_temps = np.array([25, 700, 800, 900]) + 273.15
            modulus       = np.array([192, 157, 131, 103]) * 1e9
            return np.interp(temp, modulus_temps, modulus)
        else:
            raise ValueError("Unknown Material")

    def yield_stress(self, temp):
        if self.name == 'Inconel718':
            yield_temps  = np.array([93, 204, 316, 427, 538, 649, 760]) + 273.15
            yield_values = np.array([1172, 1124, 1096, 1076, 1069, 1027, 758]) * 1e6
            return np.interp(temp, yield_temps, yield_values)
        elif self.name == 'AlSi10Mg':
            yield_temps  = np.array([298, 323, 373, 423, 473, 523, 573, 623, 673])
            yield_values = np.array([204, 198, 181, 182, 158, 132, 70, 30, 12]) * 1e6
            return np.interp(temp, yield_temps, yield_values)
        elif self.name == 'ABD900':
            yield_temps  = np.array([25, 427, 538, 649, 732, 760, 788, 816, 843, 871, 927]) + 273.15
            yield_values = np.array([978, 931, 903, 903, 758, 680, 600, 503, 434, 352, 221]) * 1e6
            return np.interp(temp, yield_temps, yield_values)
        else:
            raise ValueError("Unknown Material")

    def cte(self, temp):
        if self.name == 'Inconel718':
            return 16e-6
        elif self.name == 'AlSi10Mg':
            return 27e-6
        elif self.name == 'ABD900':
            cte_temps = np.array([50, 200, 400, 600, 800, 1000, 1200]) + 273.15
            cte_vals  = np.array([11.4, 12.9, 13.7, 14.4, 15.5, 17.5, 19.2]) * 1e-6
            return np.interp(temp, cte_temps, cte_vals)
        else:
            raise ValueError("Unknown Material")

            
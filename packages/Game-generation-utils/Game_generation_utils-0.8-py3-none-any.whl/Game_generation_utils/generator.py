from random import randint, random
from math import sqrt, pi, sin, cos, ceil
import os
import multiprocessing as mp

import opensimplex
import numpy as np
import plotly.express as px

class generator:
    #(Humedad altura temperatura), nombre del bioma, color en formato (r,g,b)
    BIOMAS = {
        0: ([-1, -1, -1], 'Oceano', (56, 148, 194)),
        1: ([-1, -1, -1], 'Oceano profundo', (27, 59, 140)),
        2: ([-1, -1, -1], 'Rios y lagos', (126, 180, 237)),
        3: ([0.5, 0.0, 0.5], 'Costa', (245, 240, 108)),
        4: ([0.75, 0.1, 0.05], 'Polo', (250, 250, 250)),
        5: ([0.8, 0.15, 0.45], 'Pantano', (33, 133, 99)),
        6: ([0.35, 0.25, 0.55], 'Dehesa', (128, 179, 30)),
        7: ([0.6, 0.3, 0.55], 'Selva', (0, 183, 10)),
        8: ([0.2, 0.3, 0.6], 'Savana', (228, 125, 28)),
        9: ([0.0, 0.3, 0.8], 'Desierto', (255, 211, 29)),
        10: ([0.8, 0.3, 0.3], 'Setas', (152, 3, 252)),
        11: ([0.65, 0.35, 0.45], 'Sakura', (235, 89, 235)),
        12: ([0.4, 0.4, 0.4], 'Bosque', (53, 118, 43)),
        13: ([0.2, 0.65, 0.7], 'Meseta', (110, 88, 66)),
        14: ([0.7, 0.8, 0.2], 'Tundra', (208, 208, 240)),
        15: ([0.15, 0.8, 0.85], 'Volcanico', (159, 16, 16)),
        16: ([0.35, 1, 0.35], 'Montaña', (125, 125, 125))
    }

    CHUNK_SIZE = 128

    def __init__(
        self, 
        seedTemp: int = None, seedAltu: int = None, seedHume: int = None, seedRios: int = None,
        varTemp: int = 256, varAltu: int = 512, varHume: int = 512, varRios: int = 128,
        dispTemp: int = 3, dispAltu: int = 4, dispHume: int = 3, dispRios: int = 4,
        nivelAgua: int = 0.5,
        tamRios: int = 5,
        itTemp: int = 3, itAltu: int = 5, itHume: int = 3, itRios: int = 4,
        ):
        """
        Initialize the PerlinNoise generator with various parameters.

        Parameters:
        seedTemp (int, optional): Seed for temperature noise. Defaults to a random value.
        seedAltu (int, optional): Seed for altitude noise. Defaults to a random value.
        seedHume (int, optional): Seed for humidity noise. Defaults to a random value.
        seedRios (int, optional): Seed for river noise. Defaults to a random value.
        varTemp (int, optional): Variation for temperature noise. Defaults to 256.
        varAltu (int, optional): Variation for altitude noise. Defaults to 512.
        varHume (int, optional): Variation for humidity noise. Defaults to 512.
        varRios (int, optional): Variation for river noise. Defaults to 128.
        dispTemp (int, optional): Displacement for temperature noise. Defaults to 2.
        dispAltu (int, optional): Displacement for altitude noise. Defaults to 4.
        dispHume (int, optional): Displacement for humidity noise. Defaults to 2.
        dispRios (int, optional): Displacement for river noise. Defaults to 4.
        nivelAgua (int, optional): Water level. Defaults to 0.5.
        tamRios (int, optional): Size of rivers. Defaults to 5.
        itTemp (int, optional): Iterations for temperature noise. Defaults to 3.
        itAltu (int, optional): Iterations for altitude noise. Defaults to 5.
        itHume (int, optional): Iterations for humidity noise. Defaults to 3.
        itRios (int, optional): Iterations for river noise. Defaults to 4.
        """
        self.SEEDTEMP = seedTemp if seedTemp != None else randint(-2**62, 2**62)
        self.SEEDALTU = seedAltu if seedTemp != None else randint(-2**62, 2**62)
        self.SEEDHUME = seedHume if seedTemp != None else randint(-2**62, 2**62)
        self.SEEDRIOS = seedRios if seedTemp != None else randint(-2**62, 2**62)
        self.VARTEMP = varTemp
        self.VARALTU = varAltu
        self.VARHUME = varHume
        self.VARRIOS = varRios
        self.DISPTEMP = dispTemp
        self.DISPALTU = dispAltu
        self.DISPHUME = dispHume
        self.DISPRIOS = dispRios
        self.NIVELAGUA = nivelAgua
        self.TAMRIOS = tamRios
        self.ITTEMP = itTemp
        self.ITALTU = itAltu
        self.ITHUME = itHume
        self.ITRIOS = itRios

    def getNoise(self, seed: int, x_in: int, y_in: int, iterations: int, size: int, disparity: int = 3) -> np.float16:
        opensimplex.seed(seed)
        ruido = 0
        for r in range(iterations):
            divisor = (size/2**r)
            exponenciador = (2**r)
            ruido += opensimplex.noise2(x=(x_in)/divisor, y=(y_in)/divisor)/exponenciador
            
        maximo = 4 * (1 - (1/2)**iterations)
        ruido = (ruido + maximo)/(2*maximo)

        for r in range(disparity):
            ruido = 0.5 + sin(pi*ruido - pi/2)/2
        return ruido

    def getNoiseArray(self, seed: np.int64, x_in: np.int64, y_in: np.int64, 
                      iterations: np.uint8, size: np.uint8, disparity: np.uint8 = 3) -> np.ndarray:
        x = self.CHUNK_SIZE*x_in
        y = self.CHUNK_SIZE*y_in
        opensimplex.seed(seed)

        rango = range(self.CHUNK_SIZE)
        noise_array = np.zeros(dtype=np.float16, shape=(self.CHUNK_SIZE, self.CHUNK_SIZE))

        for r in range(iterations):
            divisor = (size/2**r)
            exponenciador = (2**r)
            for i in rango:
                for j in rango:
                    noise_array[j, i] += opensimplex.noise2(x=(i+x)/divisor, y=(y+j)/divisor)/exponenciador
        
        maximo = 4 * (1 - (1/2)**iterations)
        for i in rango:
            for j in rango:
                valor = (noise_array[j, i] + maximo)/(2*maximo)     
                for r in range(disparity):
                    valor = 0.5 + sin(pi*valor - pi/2)/2
                noise_array[j, i] = valor
        return noise_array
    
    def getBioma(self, hume: np.float16, altu: np.float16, temp: np.float16, rios: np.float16) -> np.uint8:
        if(altu < self.NIVELAGUA):
            if (altu <= self.NIVELAGUA*0.8):
                return 1 #Oceano profundo
            else:
                return 0 #Oceano
        elif(0.5 - self.TAMRIOS/100 < rios < 0.5 + self.TAMRIOS/100):
            return 2 #Rios y lagos
        else:
            alt = (altu-self.NIVELAGUA)/self.NIVELAGUA
            tem = temp
            hum = hume
            mejorBioma = min(generator.BIOMAS.keys(), key=lambda r: np.linalg.norm(np.array(generator.BIOMAS[r][0]) - np.array([hum, alt, tem])))
            return np.uint8(mejorBioma)

    def getBioma2(self, x: np.int32, y: np.int32) -> np.uint8:
        temp = self.getNoise(self.SEEDTEMP, x, y, self.ITTEMP, self.VARTEMP, self.DISPTEMP)
        altu = self.getNoise(self.SEEDALTU, x, y, self.ITALTU, self.VARALTU, self.DISPALTU)
        hume = self.getNoise(self.SEEDHUME, x, y, self.ITHUME, self.VARHUME, self.DISPHUME)
        rios = self.getNoise(self.SEEDRIOS, x, y, self.ITRIOS, self.VARRIOS, self.DISPRIOS)
        
        if altu < self.NIVELAGUA:
            return 1 if altu <= self.NIVELAGUA * 0.8 else 0
        elif 0.5 - self.TAMRIOS / 100 < rios < 0.5 + self.TAMRIOS / 100:
            return 2
        else:
            arr = np.array([hume, (altu - self.NIVELAGUA) / self.NIVELAGUA, temp])
            mejorBioma = min(
                generator.BIOMAS.keys(),
                key=lambda r: np.linalg.norm(np.array(generator.BIOMAS[r][0]) - arr)
            )
            return np.uint8(mejorBioma)

    def getChunk(self, x: np.int16, y: np.int16) -> np.ndarray:
        if os.path.exists(f"./Chunks/T_{self.SEEDTEMP}A_{self.SEEDTEMP}H_{self.SEEDTEMP}/{x}/C_{y}.npy"):
            return np.load(f"./Chunks/T_{self.SEEDTEMP}A_{self.SEEDTEMP}H_{self.SEEDTEMP}/{x}/C_{y}.npy")
        else:
            temp = self.getNoiseArray(self.SEEDTEMP, x, y, self.ITTEMP, self.VARTEMP, self.DISPTEMP)
            altu = self.getNoiseArray(self.SEEDALTU, x, y, self.ITALTU, self.VARALTU, self.DISPALTU)
            hume = self.getNoiseArray(self.SEEDHUME, x, y, self.ITHUME, self.VARHUME, self.DISPHUME)
            rios = self.getNoiseArray(self.SEEDRIOS, x, y, self.ITRIOS, self.VARRIOS, self.DISPRIOS)
            array_biomas = np.vectorize(self.getBioma)(hume, altu, temp, rios)
            
            array_ruido = self.poisson_disc_samples(8)
            os.makedirs(f"./Chunks/T_{self.SEEDTEMP}A_{self.SEEDTEMP}H_{self.SEEDTEMP}/{x}", exist_ok=True)
            np.save(f"./Chunks/T_{self.SEEDTEMP}A_{self.SEEDTEMP}H_{self.SEEDTEMP}/{x}/C_{y}", array_biomas)
            np.save(f"./Chunks/T_{self.SEEDTEMP}A_{self.SEEDTEMP}H_{self.SEEDTEMP}/{x}/O_{y}", array_ruido)
            return array_biomas
    
    def isObject(self, x: np.int32, y: np.int32) -> bool:
        chunkX = x // self.CHUNK_SIZE
        chunkY = y // self.CHUNK_SIZE
        objects = np.load(f"./Chunks/T_{self.SEEDTEMP}A_{self.SEEDTEMP}H_{self.SEEDTEMP}/{chunkX}/O_{chunkY}.npy")
        if objects[x % self.CHUNK_SIZE, y % self.CHUNK_SIZE] == 1:
            return True
        return False

    def getChunksInRange(self, x_range: tuple[np.int16, np.int16], y_range: tuple[np.int16, np.int16]) -> np.ndarray:
        arr = None
        for i in range(x_range[0], x_range[1]):
            arr_proc = []
            for j in range(y_range[0], y_range[1]):
                arr_proc.append(mp.Process(target=self.getChunk, args=(i, j)))
                arr_proc[-1].start()
            for proc in arr_proc:
                proc.join()

            arr_line = None
            for j in range(y_range[0], y_range[1]):
                if arr_line is None:
                    arr_line = self.getChunk(i, j)
                else:
                    arr_line = np.vstack((arr_line, self.getChunk(i, j)))

            if arr is None:
                arr = arr_line
            else:
                arr = np.hstack((arr, arr_line))
        return arr

    def representation(self, x_range: tuple[int, int], y_range: tuple[int, int]) -> None:
        arr = self.getChunksInRange(x_range, y_range)
        shape = arr.shape
        color_arr = np.zeros((shape[0], shape[1], 3), dtype=np.uint8)
        biome_names = np.empty((shape[0], shape[1]), dtype=object)
        biome_colors = np.empty((shape[0], shape[1]), dtype=object)

        # Vectorized operations
        unique_biomes = np.unique(arr)
        biome_data = {biome: generator.BIOMAS[biome] for biome in unique_biomes}
        
        for biome, data in biome_data.items():
            mask = arr == biome
            color_arr[mask] = data[2]
            biome_names[mask] = data[1]
            biome_colors[mask] = f"rgb{data[2]}"

        fig = px.imshow(color_arr)
        fig.update_layout(
            width=1780,  # Add extra width for the legend
            height=1780 # Add extra height for the legend
        )

        # Add hover information
        fig.update_traces(
            hovertemplate='<b>Biome:</b> %{customdata}<extra></extra>',
            customdata=biome_names,

        )

        # Add legend
        legend_items = [
            dict(
                name=data[1],
                marker=dict(color=f"rgb{data[2]}", size=20),
                mode='markers',
                type='scatter',
                x=[None],
                y=[None]
            ) for data in biome_data.values()
        ]

        fig.add_traces(legend_items)
        fig.show()

    def getObstacles(self, r, k=30):
        tau = 2 * pi
        cellsize = r / sqrt(2)

        grid_width = ceil(self.CHUNK_SIZE / cellsize)
        grid_height = ceil(self.CHUNK_SIZE / cellsize)
        grid = np.full((grid_width, grid_height), None, dtype=object)

        def grid_coords(p):
            return int(p[0] // cellsize), int(p[1] // cellsize)

        def fits(p, gx, gy):
            for x in range(max(gx - 2, 0), min(gx + 3, grid_width)):
                for y in range(max(gy - 2, 0), min(gy + 3, grid_height)):
                    g = grid[x, y]
                    if g is not None and np.linalg.norm(p - g) <= r:
                        return False
            return True

        p = np.array([self.CHUNK_SIZE * random(), self.CHUNK_SIZE * random()])
        queue = [p]
        grid[grid_coords(p)] = p

        while queue:
            q = queue.pop(int(random() * len(queue)))
            for _ in range(k):
                alpha = tau * random()
                d = r * sqrt(3 * random() + 1)
                p = q + np.array([d * cos(alpha), d * sin(alpha)])
                if not (0 <= p[0] < self.CHUNK_SIZE and 0 <= p[1] < self.CHUNK_SIZE):
                    continue
                grid_x, grid_y = grid_coords(p)
                if fits(p, grid_x, grid_y):
                    queue.append(p)
                    grid[grid_x, grid_y] = p

        arr = np.zeros((self.CHUNK_SIZE, self.CHUNK_SIZE), dtype=np.uint8)
        for point in grid.flatten():
            if point is not None:
                arr[int(point[0]), int(point[1])] = 1

        # Remove points that are in the 4 bordering indexes of the array
        arr[0:4, :] = 0
        arr[-4:, :] = 0
        arr[:, 0:4] = 0
        arr[:, -4:] = 0
        return arr

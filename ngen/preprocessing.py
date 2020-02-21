import numpy as np
from PIL import Image


# Propiedades de los materiales
water = {
    'density': 997,
    'heat-capacity': 3500,
    'thermal-conductivity': 0.6
}

grass = {
    'density': 65,
    'heat-capacity': 1800,
    'thermal-conductivity': 0.038
}

tree = {
    'density': 414,
    'heat-capacity': 1700,
    'thermal-conductivity': 0.25
}


def img2matrix(img_path, pixel_size):
    """

    """
    img = np.array(Image.open(img_path))
    size = img.shape[:2]

    density = np.ones(size)
    temp_init = np.ones(size)
    heat_capacity = np.ones(size)
    thermal_conductivity = np.ones(size)

    if img_path == 'imgs/test1.jpg':
        thermal_conductivity[:400, :] = water['thermal-conductivity']
        thermal_conductivity[400:860, :] = grass['thermal-conductivity']
        thermal_conductivity[860:, :] = water['thermal-conductivity']

        density[:400, :] = water['density']
        density[400:860, :] = grass['density']
        density[860:, :] = water['density']

        heat_capacity[:400, :] = water['heat-capacity']
        heat_capacity[400:860, :] = grass['heat-capacity']
        heat_capacity[860:, :] = water['heat-capacity']

        temp_init = 298.15 * temp_init  # 25°C
        temp_init[458:562, 537:646] = 1873.15 # 1600°C
        temp_init[756:860, 435:549] = 1873.15 # 1600°C

    if img_path == 'imgs/test2.jpg':
        thermal_conductivity[:391, :] = water['thermal-conductivity']
        thermal_conductivity[391:866, :] = tree['thermal-conductivity']
        thermal_conductivity[866:, :] = water['thermal-conductivity']

        density[:391, :] = water['density']
        density[391:866, :] = tree['density']
        density[866:, :] = water['density']

        heat_capacity[:391, :] = water['heat-capacity']
        heat_capacity[391:866, :] = tree['heat-capacity']
        heat_capacity[866:, :] = water['heat-capacity']

        temp_init = 298.15 * temp_init  # 25°C
        temp_init[454:563, 546:660] = 1873.15 # 1600°C
        temp_init[756:856, 444:555] = 1873.15 # 1600°C

    return temp_init, density, heat_capacity, thermal_conductivity

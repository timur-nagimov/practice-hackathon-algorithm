from py3dbp import Packer, Bin, Item

import json
import copy
from pprint import pprint


class Cargo_group:
    def __init__(self, mass, size, count, cargo_id):
        self.mass = mass
        self.size = size
        self.count = count
        self.cargo_id = cargo_id

    def get_cargo_param(self, kind='height'):
        if kind == 'length':
            return int(self.size[2])
        elif kind == 'width':
            return int(self.size[0])
        elif kind == 'height':
            return int(self.size[1])
        elif kind == 'weight':
            return int(int(self.mass))
        elif kind == 'count':
            return int(self.count)
        else:
            raise ValueError("Разрешено только [length, width, height, value, instance]")


def get_cargo_size(data):  # получает размер контейнера в трех измерениях (длина, ширина, высота ) из t файла
    cargo_size_data = data['cargo_space']['size']
    return [int(cargo_size_data['width']), int(cargo_size_data['height']), int(cargo_size_data['length'])]

def get_cargo_mass(data):  # получает размер контейнера в трех измерениях (длина, ширина, высота ) из json файла
    cargo_mass_data = data['cargo_space']['mass']
    return int(cargo_mass_data)

def get_cargo_carrying_capacity(data):
    cargo_cp_data = data['cargo_space']['carrying_capacity']
    return int(cargo_cp_data)

def get_cargo_groups(data):  # заносит все виды ящиков в список с элементами класса Cargo_group
    cargo_groups = []
    for i in data['cargo_groups']:
        mass = int(i['mass'])
        size = [int(i['size']['length']), int(i['size']['width']), int(i['size']['height'])]
        count = int(i['count'])
        cargo_id = str(i['group_id'])

        cg = Cargo_group(mass, size, count, cargo_id)
        cargo_groups.append(cg)
    return cargo_groups


with open("136303_cl.json") as f:
    data = json.load(f)

cargo_size_data = get_cargo_size(data)
cargos = get_cargo_groups(data)

packer = Packer()

a = Bin('box', cargo_size_data[0], cargo_size_data[1], cargo_size_data[2], 100000000000)
packer.add_bin(a)
#a= Bin('large-3-box', 23.6875, 11.2, 35.0, 1000.0)
#packer.add_bin(Bin('small-envelope', 11.5, 6.125, 0.25, 10))
#packer.add_bin(Bin('large-envelope', 15.0, 12.0, 0.75, 15))
#packer.add_bin(Bin('small-box', 8.625, 5.375, 1.625, 70.0))
#packer.add_bin(Bin('medium-box', 11.0, 8.5, 5.5, 70.0))
#packer.add_bin(Bin('medium-2-box', 13.625, 11.875, 3.375, 70.0))
#packer.add_bin(Bin('large-box', 12.0, 12.0, 5.5, 70.0))
#packer.add_bin(Bin('large-2-box', 23.6875, 11.75, 3.0, 70.0))
#packer.add_bin(a)

'''
packer.add_item(Item('1', 3.9370, 1.9685, 11.9685, 1))
packer.pack()
#packer.add_item(Item('2', 23.6875, 11.2, 30, 10))
#packer.pack()
packer.add_item(Item('2', 3.9370, 1.9685, 1.9685, 2))
packer.pack()
packer.add_item(Item('3', 3.9370, 1.9685, 1.9685, 3))
packer.pack()

packer.add_item(Item('4', 7.8740, 3.9370, 1.9685, 4))
packer.pack()
packer.add_item(Item('5', 7.8740, 3.9370, 1.9685, 5))
packer.pack()
packer.add_item(Item('6', 7.8740, 3.9370, 1.9685, 6))
packer.pack()
packer.add_item(Item('7', 15.5, 6, 20, 6))
packer.pack()
packer.add_item(Item('8', 7.8740, 3.9370, 1.9685, 7))
packer.pack()
packer.add_item(Item('9', 7.8740, 3.9370, 1.9685, 8))
packer.pack()
packer.add_item(Item('10', 7.8740, 3.9370, 1.9685, 9))
packer.pack()
packer.add_item(Item('11', 7.8740, 3.9370, 1.9685, 10))
packer.pack()
packer.add_item(Item('12', 7.8740, 3.9370, 1.9685, 11))
packer.pack()
packer.add_item(Item('13', 7, 3.770, 3.9685, 11))
packer.pack()
packer.add_item(Item('14', 7.1, 3.770, 3.9685, 10))
packer.pack()
packer.add_item(Item('15', 7, 3.770, 28, 10))
packer.pack()
packer.add_item(Item('16', 7, 3.770, 20, 10))
packer.pack()
packer.add_item(Item('17', 7, 3.770, 20, 10))
packer.pack()
'''

cnt = 0
for item in cargos:
    for cargo in range(item.count):
        cnt += 1
        packer.add_item(Item(str(cnt), item.get_cargo_param('width'), item.get_cargo_param('height'), item.get_cargo_param('length'), item.get_cargo_param('weight'), item.cargo_id))
        packer.pack()


volume_used = 0
total_weight = 0
volume_not_used = 0

cargo_default_text = {
    "sort": 1,
    "stacking": True,
    "turnover": True,
    "type": "box"
}
packed_cargos = {}

for b in packer.bins:
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    count = 0

    for item in b.items:
        count+=1
        print("====> ", item.string())
        volume_used += item.get_volume()
        total_weight += item.weight
        #cnt += 1

    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("====> ", item.string())
        volume_not_used += item.get_volume()
        #cnt += 1

    print("***************************************************")
    print("***************************************************")

volume = cargo_size_data[0] * cargo_size_data[1] * cargo_size_data[2]
print("ЗАполненность:", volume_used / volume * 100)
#print(total_weight)
#print(volume_used)
print(volume_not_used)
volume_left = volume - volume_used
print(volume_left)
#print(volume)
#print(volume_used + volume_not_used)


#from mpl_toolkits.mplot3d import Axes3D
#import numpy as np
#import matplotlib.pyplot as plt

def cuboid_data(o, size=(1,1,1)):
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  
    y = [[-o[1], -o[1], -o[1] - w, -o[1] - w, -o[1]],  
         [-o[1], -o[1], -o[1] - w, -o[1] - w, -o[1]],  
         [-o[1], -o[1], -o[1], -o[1], -o[1]],          
         [-o[1] - w, -o[1] - w, -o[1] - w, -o[1] - w, -o[1] - w]]   
    z = [[o[2], o[2], o[2], o[2], o[2]],                       
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],   
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],               
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]               
    #return np.array(x), np.array(y), np.array(z)

def plotCubeAt(pos=(0,0,0), size=(1,1,1), ax=None,**kwargs):
    # Plotting a cube element at position pos
    if ax !=None:
        X, Y, Z = cuboid_data( pos, size )
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)
        
positions=[]
sizes=[]
colors=[]
for key, item in enumerate(a.items):
    (x, y, z) = item.position
    (w, h, d) = item.dimension
    position = (float(x), float(y), float(z))
    size = (float(w), float(h), float(d))
    color = (1 / (key+1), 1, 0.005 * key)
    positions.append(position)
    sizes.append(size)
    colors.append(color)


#fig = plt.figure()
#ax = fig.gca(projection='3d')
#ax.set_aspect('equal')

#for p, s, c in zip(positions, sizes, colors):
 #   plotCubeAt(pos=p, size=s, ax=ax, color=c)

print("ALl items: ", len(cargos))
print("In box items: ", count)
#plt.show()

# TO JSON


import nums_from_string

output_info = {
    'cargoSpace':
        {
            'loading_size':
                {
                    'height': b.string().split('x')[1].split('(')[1],
                    'length': b.string().split('x')[2],
                    'width': b.string().split('x')[3].split(',')[0]
                },

            'position':
                [
                    0.6,
                    1.1,
                    0.4
                ],
            'type': 'pallet'
        },
    'cargos': [
    ],
    'unpacked': []
}

for b in packer.bins:
    for item in b.items:
        output_info['cargos'].append({
            "calculated_size": {
                "height": item.string().split('x')[0].split('(')[1],
                "length": item.string().split('x')[1],
                "width": item.string().split('x')[2].split(',')[0]
            },
            "cargo_id": "???",
            "id": item.string().split('(')[0],
            "mas": item.string().split('x')[2].split(',')[0],
            "position": {
                "x": nums_from_string.get_nums(item.string()[item.string().find('[') + 1:item.string().find(']')])[0],
                "y": nums_from_string.get_nums(item.string()[item.string().find('[') + 1:item.string().find(']')])[1],
                "z": nums_from_string.get_nums(item.string()[item.string().find('[') + 1:item.string().find(']')])[2]
            },
            "size": {
                "height": item.string().split('x')[0].split('(')[1],
                "length": item.string().split('x')[2].split(',')[0],
                "width": item.string().split('x')[1]
            },

        })
output_info['cargos'].append(
    {
        "sort": 1,
        "stacking": "True",
        "turnover": "True",
        "type": "box"
    })

for b in packer.bins:
    for item in b.unfitted_items:
        output_info['unpacked'].append({
            "group_id": "???",
            "id": item.string().split('(')[0],
            "mass": item.string().split('x')[2].split(',')[0],
            "position": {
                "x": -50000,
                "y": -50000,
                "z": -50000
            },
            "size": {
                "height": item.string().split('x')[0].split('(')[1],
                "length": item.string().split('x')[2].split(',')[0],
                "width": item.string().split('x')[1]
            }
        })

output_info['unpacked'].append(
    {
        "sort": 1,
        "stacking": "True",
        "turnover": "True",
    })

pprint(output_info)

with open("products.json", "w", encoding='utf-8') as f:
    json.dump(output_info, f, ensure_ascii=False, indent=4)
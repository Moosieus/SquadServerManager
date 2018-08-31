import random as rand
import copy
from miscellaneous.squad_map_dictionary import squad_maps


def filter_gamemode(map_dict, gamemode):
    """Removes all maps that don't have the specified gamemode"""
    return_dict = copy.deepcopy(map_dict)
    for map, layers in map_dict.items():
        if len(layers[gamemode]) == 0:
            return_dict.pop(map)
    return return_dict


keywords = ['Invasion', 'PAAS', 'AAS', 'INS', 'ITC']


def generate_layer_list(current_layer):
    """Returns a pick dictionary of 3 categories, Invasion, AAS, PAAS"""
    for k in keywords:
        if k in current_layer:
            current_layer = current_layer.split(k)[0].strip(' ')
    pick_maps = copy.deepcopy(squad_maps)
    pick_maps.pop(current_layer)

    inv_map_dict = filter_gamemode(pick_maps, 'Invasion')
    inv_map = rand.choice(list(inv_map_dict.keys()))
    inv_layer = inv_map + ' Invasion v' + str(rand.choice(list(inv_map_dict[inv_map]['Invasion'])))

    aas_map_dict = filter_gamemode(pick_maps, 'AAS')
    aas_map = rand.choice(list(aas_map_dict.keys()))
    aas_layer = aas_map + ' AAS v' + str(rand.choice(aas_map_dict[aas_map]['AAS']))

    paas_map_dict = filter_gamemode(pick_maps, 'PAAS')
    paas_map = rand.choice(list(paas_map_dict.keys()))
    paas_layer = paas_map + ' PAAS v' + str(rand.choice(paas_map_dict[paas_map]['PAAS']))

    return {
        inv_layer: {
            'votes': 0,
            'image': ('http://squadmaps.com/images/' + inv_map.replace(' ', '_').replace("'", "") + inv_layer.replace(inv_map, "").replace(' ', '-') + '.jpg').lower().replace("'", "").replace('invasion', 'inv').replace("logar_valley", "logar"),
            'message': 'placeholder for discord embed'
        },
        aas_layer: {
            'votes': 0,
            'image': ('http://squadmaps.com/images/' + aas_map.replace(' ', '_') + aas_layer.replace(aas_map, "").replace(' ', '-') + '.jpg').lower().replace("'", "").replace("logar_valley", "logar"),
            'message': 'placeholder for discord embed'
        },
        paas_layer: {
            'votes': 0,
            'image': ('http://squadmaps.com/images/' + paas_map.replace(' ', '_').replace("'", "") + paas_layer.replace(paas_map, "").replace(' ', '-') + '.jpg').lower().replace("'", "").replace("logar_valley", "logar"),
            'message': 'placeholder for discord embed'
        }
    }

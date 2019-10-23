import configparser
import os

propertiesPath = '../server/server.properties'

def load_properties():
    properties_list = []
    with open(propertiesPath, 'r') as properties:
        for line in properties.readlines():
            line = [item.replace("\n", "") for item in line.split('=')]
            if line[0] != '':
                properties_list.append(line)
    return properties_list

def edit_properties(key, value):
    with open('../server/2server.properties', 'w') as test:
        for keys, values in load_properties():
            if key == keys:
                if value is not values:
                    values = value
            test.write(f"{''.join(list((keys+'=', values)))}\n")
    os.rename('../server/2server.properties', propertiesPath)

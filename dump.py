#!/usr/bin/env virt/bin/python
import xml.etree.ElementTree as ET
import fileinput
import re

f = open('/Users/pquiring/Documents/BeerSmith2/Recipe.bsmx')
def doctype(entities):
    ret = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" ['
    for e in entities:
        ret += "<!ENTITY {} ' '>".format(e)
    ret += ']>'
    return ret
def doc(s, entities):
    ret = doctype(entities)
    ret += s
    return ret

def read_beersmith():
    s = f.read()
    entities = []
    root = False
    while True:
        try:
            root = ET.fromstring(doc(s, entities))
            break
        except ET.ParseError as err:
            msg = err.msg
            print(msg)
            m = re.search('undefined entity &(.*?);', msg)
            undefined_entity = msg[m.regs[1][0]:m.regs[1][1]]
            print(undefined_entity)
            entities.append(undefined_entity)
    return root

def powells_recipes(root):
    for table in root.find('Data').iter('Table'):
        name = table.find('Name').text
        print(name)
        if name == 'Powell':
            recipes = table.find('Data').iter('Recipe')
            name2recipe = {recipe.find('F_R_NAME').text: recipe for recipe in recipes}
            return name2recipe

def choose_todays_recipe_names(name2recipe):
    '''Choose the last 4 of the numbered names 001 chinoo, 002 recipe, ...'''
    names_sorted = sorted([key for key in name2recipe.keys() if key[0:4].isdigit()])
    return [key for key in names_sorted[-4:]]

def lbs_oz(ozs):
    return divmod(ozs, 16)

def grain_print(name2recipe, names):
    for name in names:
        recipe = name2recipe[name]
        print(name)
        for grain in recipe.find('Ingredients').find('Data').iter('Grain'):
            grain_name = grain.find('F_G_NAME').text
            grain_oz = float(grain.find('F_G_AMOUNT').text)
            (lbs, oz) = lbs_oz(grain_oz)
            print('{} lbs {} ozs - {}'.format(lbs, oz, grain_name))


def hops_print(name2recipe, names):
    for name in names:
        recipe = name2recipe[name]
        print(name, recipe)
        for hop in recipe.find('Ingredients').find('Data').iter('Hops'):
            print(hop)
            hop_name = grain.find('F_G_NAME').text
            hop_oz = float(grain.find('F_G_AMOUNT').text)

root = read_beersmith()
name2recipe = powells_recipes(root)
names = choose_todays_recipe_names(name2recipe)
grain_print(name2recipe, names)
hops_print(name2recipe, names)

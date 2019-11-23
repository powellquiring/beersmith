#!/usr/bin/env virt/bin/python
import xml.etree.ElementTree as ET
import fileinput
import re
import collections

Ingrediant = collections.namedtuple("Ingrediant", ["name", "oz"])


def doctype(entities):
    ret = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" ['
    for e in entities:
        ret += "<!ENTITY {} ' '>".format(e)
    ret += "]>"
    return ret


def doc(s, entities):
    ret = doctype(entities)
    ret += s
    return ret


def read_beersmith(f):
    # f = open('/Users/pquiring/Documents/BeerSmith2/Recipe.bsmx')
    # f = open(path)
    s = f.read()
    entities = []
    root = False
    while True:
        try:
            root = ET.fromstring(doc(s, entities))
            break
        except ET.ParseError as err:
            msg = err.msg
            m = re.search("undefined entity &(.*?);", msg)
            undefined_entity = msg[m.regs[1][0] : m.regs[1][1]]
            entities.append(undefined_entity)
    return root


def named_recipes(root, name):
    for table in root.find("Data").iter("Table"):
        recipe_name = table.find("Name").text
        if recipe_name == name:
            recipes = table.find("Data").iter("Recipe")
            named_recipes = {recipe.find("F_R_NAME").text: recipe for recipe in recipes}
            return named_recipes


def highest_numbered_recipes(recipes, count):
    """receipe names start with a number, return the highest numbered"""
    names_sorted = sorted([key for key in recipes.keys() if key[0:4].isdigit()])
    return [key for key in names_sorted[-count:]]


def grains(recipe):
    ret = []
    for grain in recipe.find("Ingredients").find("Data").iter("Grain"):
        grain_name = grain.find("F_G_NAME").text
        grain_oz = float(grain.find("F_G_AMOUNT").text)
        ret.append(Ingrediant(grain_name, grain_oz))
    return ret


def hops(recipe):
    ret = []
    for hop in recipe.find("Ingredients").find("Data").iter("Hops"):
        hop_name = hop.find("F_H_NAME").text
        hop_oz = float(hop.find("F_H_AMOUNT").text)
        ret.append(Ingrediant(hop_name, hop_oz))
    return ret

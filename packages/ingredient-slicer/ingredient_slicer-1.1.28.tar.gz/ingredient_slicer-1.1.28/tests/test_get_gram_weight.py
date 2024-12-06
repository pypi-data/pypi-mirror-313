# pytest library
import pytest

import re

from ingredient_slicer import _constants, _utils
# from ingredient_slicer import IngredientSlicer

# -------------------------------------------------------------------------------
# ---- _get_gram_weight() tests ----
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# ---- _get_gram_weight() test for converting simple weights ----
# -------------------------------------------------------------------------------
    
# grams_map = _utils._get_gram_weight("flour" "1", "cup", "levenshtein")

def test_get_gram_weight_one_ounce():
    gram_weights = _utils._get_gram_weight("chicken", "1", "ounce")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 28
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_one_ounce_plural():
    gram_weights = _utils._get_gram_weight("chicken", "1", "ounces")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 28
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_one_ounce_plural_capitalized():
    gram_weights = _utils._get_gram_weight("chicken", "1", "Ounces")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 28
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_one_ounce_plural_uppercase():
    gram_weights = _utils._get_gram_weight("chicken", "1", "OUNCES")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 28
    assert min_gram_weight == None
    assert max_gram_weight == None


def test_get_gram_weight_multiple_ounces_plural():
    gram_weights = _utils._get_gram_weight("chicken", "10", "ounces")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 284
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_multiple_decimal_ounce():
    gram_weights = _utils._get_gram_weight("chicken", "10.5", "ounce")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 298
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_one_pound():
    gram_weights = _utils._get_gram_weight("chicken", "1", "pound")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 454
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_one_pound_plural():
    gram_weights = _utils._get_gram_weight("chicken", "1", "pounds")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 454
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_multiple_pound_plural():
    gram_weights = _utils._get_gram_weight("chicken", "10", "pounds")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 4536
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_multiple_decimal_pound():
    gram_weights = _utils._get_gram_weight("chicken", "10.5", "pound")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 4763
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_one_gram():
    gram_weights = _utils._get_gram_weight("chicken", "1", "gram")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 1
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_multiple_grams_plural():
    gram_weights = _utils._get_gram_weight("chicken", "10", "grams")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 10
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_multiple_decimal_grams():
    gram_weights = _utils._get_gram_weight("chicken", "10.5", "grams")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 10
    assert min_gram_weight == None
    assert max_gram_weight == None

def test_get_gram_weight_one_kilogram():
    gram_weights = _utils._get_gram_weight("chicken", "1", "kilogram")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 1000
    assert min_gram_weight == None
    assert max_gram_weight == None

# -------------------------------------------------------------------------------
# ---- _get_gram_weight2() test for converting volumes ----
# -------------------------------------------------------------------------------

def test_get_gram_weight_one_milliliter_olive_oil():
    food         = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "milliliter", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 1
    assert min_gram_weight == 1
    assert max_gram_weight == 1

    # gram_weights = _utils._get_gram_weight("olive oil", "1", "milliliters")
    gram_weights = _utils._get_gram_weight(food, "1", "milliliters", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 1
    assert min_gram_weight == 1
    assert max_gram_weight == 1

    gram_weights = _utils._get_gram_weight(food, "1", "mL", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 1
    assert min_gram_weight == 1
    assert max_gram_weight == 1

def test_get_gram_weight_one_teaspoon_olive_oil():
    food         = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "teaspoon", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 4
    assert min_gram_weight == 4
    assert max_gram_weight == 5

    gram_weights = _utils._get_gram_weight(food, "1", "tsp", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 4
    assert min_gram_weight == 4
    assert max_gram_weight == 5

    gram_weights = _utils._get_gram_weight(food, "1", "tsps", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 4
    assert min_gram_weight == 4
    assert max_gram_weight == 5


def test_get_gram_weight_one_tablespoon_olive_oil():
    food         = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "tablespoon", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 13
    assert min_gram_weight == 13
    assert max_gram_weight == 14

    gram_weights = _utils._get_gram_weight(food, "1", "tbsp", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 13
    assert min_gram_weight == 13
    assert max_gram_weight == 14

    gram_weights = _utils._get_gram_weight(food, "1", "tbsps", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 13
    assert min_gram_weight == 13
    assert max_gram_weight == 14

def test_get_gram_weight_one_cup_olive_oil():
    food         = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)


    gram_weights = _utils._get_gram_weight(food, "1", "cup", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 215
    assert min_gram_weight == 208
    assert max_gram_weight == 227

    gram_weights = _utils._get_gram_weight(food, "1", "cups", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 215
    assert min_gram_weight == 208
    assert max_gram_weight == 227

def test_get_gram_weight_one_pint_olive_oil():
    food         = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)


    gram_weights = _utils._get_gram_weight(food, "1", "pint", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 431
    assert min_gram_weight == 416
    assert max_gram_weight == 454

    gram_weights = _utils._get_gram_weight(food, "1", "pints", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 431
    assert min_gram_weight == 416
    assert max_gram_weight == 454

def test_get_gram_weight_one_quart_olive_oil():
    food         = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "quart", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 862
    assert min_gram_weight == 833
    assert max_gram_weight == 908

    gram_weights = _utils._get_gram_weight(food, "1", "quarts", densities) 

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 862
    assert min_gram_weight == 833
    assert max_gram_weight == 908

def test_get_gram_weight_one_gallon_olive_oil():
    food         = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "gallon", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 3448
    assert min_gram_weight == 3331
    assert max_gram_weight == 3634

    gram_weights = _utils._get_gram_weight(food, "1", "gallons", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 3448
    assert min_gram_weight == 3331
    assert max_gram_weight == 3634

    gram_weights = _utils._get_gram_weight(food, "1", "gals", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 3448
    assert min_gram_weight == 3331
    assert max_gram_weight == 3634


def test_get_gram_weight_one_teaspoon_flour():
    food         = "flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "teaspoon", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 3
    assert min_gram_weight == 2
    assert max_gram_weight == 5

def test_get_gram_weight_one_tsp_flour():
    food         = "flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "tsp", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 3
    assert min_gram_weight == 2
    assert max_gram_weight == 5

def test_get_gram_weight_one_teaspoon_almond_flour():
    food         = "almond flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "teaspoon", densities) 

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 3
    assert min_gram_weight == 2
    assert max_gram_weight == 5

def test_get_gram_weight_one_teaspoon_oat_flour():
    food         = "oat flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)
    
    gram_weights = _utils._get_gram_weight(food, "1", "teaspoon", densities)
    # gram_weights = _utils._get_gram_weight("oat flour", "1", "teaspoon")


    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 3
    assert min_gram_weight == 2
    assert max_gram_weight == 5

def test_get_gram_weight_one_tablespoon_complex_flours():
    food        = "whole wheat oat flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "tablespoon", densities)
    # gram_weights = _utils._get_gram_weight("whole wheat oat flour", "1", "tablespoon")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 9
    assert min_gram_weight == 5
    assert max_gram_weight == 16

def test_get_gram_weight_one_tablespoon_complex_flours2():
    food        = "whole grain wheat oat flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "tablespoon", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 9
    assert min_gram_weight == 5
    assert max_gram_weight == 16

def test_get_gram_weight_one_tablespoon_white_flour():
    food         = "white flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "tablespoon", densities)
    
    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 9
    assert min_gram_weight == 5
    assert max_gram_weight == 16


def test_get_gram_weight_one_cup_complex_flours():
    food         = "whole wheat oat flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "cup", densities)    

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 137
    assert min_gram_weight == 83
    assert max_gram_weight == 253

def test_get_gram_weight_one_cup_complex_flours2():
    food         = "whole grain wheat oat flour"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, "1", "cup", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 137
    assert min_gram_weight == 83
    assert max_gram_weight == 253

def test_get_gram_weight_integer_as_quantity_olive_oil():
    food = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, 1, "teaspoon", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 4
    assert min_gram_weight == 4
    assert max_gram_weight == 5

def test_get_gram_weight_decimal_as_quantity_olive_oil():
    food = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, 1.5, "teaspoon", densities)
    # gram_weights = _utils._get_gram_weight(food, 1.5, "teaspoon")

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 7
    assert min_gram_weight == 7
    assert max_gram_weight == 7

def test_get_gram_weight_zero_as_quantity():

    food = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    gram_weights = _utils._get_gram_weight(food, 0, "teaspoon", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight is None
    assert min_gram_weight is None
    assert max_gram_weight is None
    
def test_get_gram_weight_fraction_as_quantity():
    food = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    with pytest.raises(ValueError):
        _utils._get_gram_weight(food, "1/2", "teaspoon", densities)

# TODO: Need to refine behavior for foods that dont have a real unit or any unit at all
# TODO: Reference the _get_single_item_gram_weight() function that tries to take a food with no weight or volume unit 
# TODO: and get the gram weight. _get_single_item_gram_weight() assumes that if a food has no unit and or a Non weight/volume unit (i.e. 'heads') than the ingredient 
# TODO: is an individual item type ingredient where the food is also the unit (i.e. 2 eggs). There is a small/hacky SINGLE_ITEM_FOOD_WEIGHTS dictionary 
# TODO:  with an average gram weight of some common single item foods (primarly fruits, vegetables, and eggs)
def test_get_gram_weight_invalid_unit():
    food = "olive oil"
    fuzzy_method = "dice"
    densities    = _utils._get_food_density(food, fuzzy_method)

    expected = {"gram_weight": None, 
                "min_gram_weight": None, 
                "max_gram_weight": None}

    assert _utils._get_gram_weight(food, "1", "fgdhdjgfhdf", densities) == expected
    
# -------------------------------------------------------------------------------
# ---- _get_gram_weight2() empty / None densities dictionary values ----
# -------------------------------------------------------------------------------
def test_food_string_quantity_and_volume_unit_and_none_density_map():

    food        = "olive oil"
    fuzzy_method = "dice"
    densities    = None
    
    gram_weights = _utils._get_gram_weight("olive oil", "1", "cup", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 237
    assert min_gram_weight == 213
    assert max_gram_weight == 260

def test_food_string_quantity_and_volume_unit_and_default_density_map_values():

    food        = "olive oil"
    fuzzy_method = "dice"
    densities    = {"density": 1.0, "min_density": 0.9, "max_density":1.1}
    
    gram_weights = _utils._get_gram_weight("olive oil", "1", "cup", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 237
    assert min_gram_weight == 213
    assert max_gram_weight == 260

def test_food_string_quantity_and_volume_unit_and_density_map_all_none_values():

    food        = "olive oil"
    fuzzy_method = "dice"
    densities    = {"density": None, "min_density": None, "max_density": None}
    
    gram_weights = _utils._get_gram_weight("olive oil", "1", "cup", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 237
    assert min_gram_weight == 213
    assert max_gram_weight == 260

# TODO: if a density is given but NO min_density or max_density, 
# TODO: then the min_density and max_density should be the SAME as the density or None?
# TODO: Fix this in the _get_gram_weight2() function in _utils.py
def test_food_string_quantity_and_volume_unit_and_density_map_some_none_values():

    food        = "olive oil"
    fuzzy_method = "dice"
    densities    = {"density": 0.5, "min_density": None, "max_density": None}
    
    gram_weights = _utils._get_gram_weight("olive oil", "1", "cup", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 118
    assert min_gram_weight == 213
    assert max_gram_weight == 260

def test_food_string_quantity_and_volume_unit_and_density_map_empty_values():
    food        = "olive oil"
    fuzzy_method = "dice"
    densities    = {"density": "", "min_density": "", "max_density": ""}
    
    gram_weights = _utils._get_gram_weight("olive oil", "1", "cup", densities)

    gram_weight     = round(float(gram_weights["gram_weight"])) if gram_weights["gram_weight"] else None
    min_gram_weight = round(float(gram_weights["min_gram_weight"])) if gram_weights["min_gram_weight"] else None
    max_gram_weight = round(float(gram_weights["max_gram_weight"])) if gram_weights["max_gram_weight"] else None

    assert gram_weight == 237
    assert min_gram_weight == 213
    assert max_gram_weight == 260
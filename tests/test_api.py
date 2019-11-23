import beersmith
import pathlib


def test_api():
    bsmx = pathlib.Path(__file__).with_name("Recipe.bsmx")
    with bsmx.open() as f:
        root = beersmith.read_beersmith(f)
        recipes = beersmith.named_recipes(root, "Powell")
        latest4 = beersmith.highest_numbered_recipes(recipes, 4)
        assert set(latest4) == set(
            (
                "0234 Willamette Am Paler Ale - paler then Am Ale",
                "0235 Willamette Am Paler Ale - paler then Am Ale",
                "0236 Fresh Squeezed",
                "0237 Chinook dark++ DH - Arrogant Bastard light",
            )
        )
        grains = beersmith.grains(recipes[latest4[0]])
        assert grains == [
            beersmith.Ingrediant("Pale Malt (2 Row) US - GW", 176.0),
            beersmith.Ingrediant("Victory Malt", 8.0),
        ]
        hops = beersmith.hops(recipes[latest4[0]])
        assert hops == [
            beersmith.Ingrediant("Magnum", 1.0),
            beersmith.Ingrediant("Willamette", 1.0),
            beersmith.Ingrediant("Willamette", 1.0),
            beersmith.Ingrediant("Willamette", 1.0),
        ]

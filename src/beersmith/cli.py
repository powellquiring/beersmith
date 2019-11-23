import click
import beersmith
import pathlib


def lbs_oz(ozs):
    return divmod(ozs, 16)


@click.command(help="beersmith dump command, dump grain and hop")
@click.option(
    "-f",
    "--file",
    default="/Users/pquiring/Documents/BeerSmith2/Recipe.bsmx",
    help="path name to recipe file",
)
@click.option("-n", "--number", default=4, type=int, help="number of recipes")
def cli(file, number):
    reecipe_bsmx = pathlib.Path(file)
    with reecipe_bsmx.open() as f:
        root = beersmith.read_beersmith(f)
        recipes = beersmith.named_recipes(root, "Powell")
        names = beersmith.highest_numbered_recipes(recipes, number)
        click.echo("\n-------------- GRAINS\n")
        for name in names:
            grain_ingrediants = beersmith.grains(recipes[name])
            click.echo(name)
            for grain in grain_ingrediants:
                (lbs, oz) = lbs_oz(grain.oz)
                click.echo("  {} lbs {} ozs - {}".format(lbs, oz, grain.name))
        hops_name_2_oz = dict()
        click.echo("\n-------------- HOPS RECIPE\n")
        for name in names:
            hop_ingrediants = beersmith.hops(recipes[name])
            click.echo(name)
            for hop in hop_ingrediants:
                hops_name_2_oz[hop.name] = hops_name_2_oz.get(hop.name, 0) + hop.oz
                (lbs, oz) = lbs_oz(hop.oz)
                click.echo("  {} lbs {} ozs - {}".format(lbs, oz, hop.name))
        click.echo("\n-------------- HOPS CONSOLIDATED\n")
        for (name, oz) in hops_name_2_oz.items():
            click.echo(f"{oz:4.2f} oz {name}".format(oz, name))

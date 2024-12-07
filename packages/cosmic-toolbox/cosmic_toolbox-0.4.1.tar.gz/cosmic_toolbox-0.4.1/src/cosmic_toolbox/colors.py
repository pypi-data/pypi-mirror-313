import matplotlib.pyplot as plt
from cycler import cycler


def get_colors(cycle="silvan"):
    if cycle == "silvan":
        return {
            "b": "#0063B9",
            "r": "#BA1A13",
            "g": "#34BA09",
            "orange": "#ED6018",
            "violet": "#6E13BA",
            "brown": "#6E2C0B",
            "gray": "#808080",
            "pink": "#BA13A0",
            "olive": "#B0BA13",
            "bluegreen": "#09BAAF",
            "lightblue": "#1994FF",
            "lightred": "#FF3D33",
            "lightgreen": "#5CFF26",
            "lightorange": "#FFA547",
            "lightviolet": "#A333FF",
            "lightbrown": "#FFA541",
            "lightgray": "#BEBEBE",
            "lightpink": "#FF33E0",
            "lightolive": "#F1FF33",
            "lightbluegreen": "#33FFE7",
        }
    else:
        return cycle


def set_cycle(cycle="silvan"):
    colors = get_colors(cycle=cycle)
    if isinstance(colors, dict):
        col = colors.values()
    else:
        col = colors
    plt.rc("axes", prop_cycle=cycler(color=col))

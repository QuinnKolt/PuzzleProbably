import sys

from board import *
from rules import *
import json

from rules.area_rules import *
from rules.text_rules import *
from rules.cell_rules import *
from rules.edge_rules import *
from rules.vertex_rules import *

ENCODER = json.JSONEncoder()
DECODER = json.JSONDecoder()


def level(pack, lvl):
    if pack == 0:  # TUTORIAL PACK
        if lvl == 1:
            return tutorial_one()
        if lvl == 2:
            return tutorial_two()
        if lvl == 3:
            return tutorial_three()
        if lvl == 4:
            return tutorial_four()
        if lvl == 5:
            return tutorial_five()
        if lvl == 6:
            return tutorial_six()
        if lvl == 7:
            return tutorial_seven()
        if lvl == 8:
            return tutorial_eight()

    return level_default()

    # lvl = import_level_from_json("json_levels/default.json")
    # print(lvl)
    # return lvl



# TUTORIALS


def tutorial_one():
    wid, hei = 3, 3

    domain = basic_domain(wid, hei)

    rules = [BulletinInfo("Double click or hit enter to submit solution.")]

    starts = [(1, 1)]

    return domain, rules, starts, (wid, hei)


def tutorial_two():
    wid, hei = 3, 3

    domain = basic_domain(wid, hei)

    rules = [BulletinInfo("The white dot is a start point. If there are multiple start points, "
                          "you must click one to start with. Press ESC to deselect")]

    starts = [(0, 2), (2, 0)]

    return domain, rules, starts, (wid, hei)


def tutorial_three():
    wid, hei = 3, 3

    domain = basic_domain(wid, hei)

    rules = [BulletinInfo("If there is only one start point, it is selected by default.")]

    starts = [(1, 1)]

    return domain, rules, starts, (wid, hei)


def tutorial_four():
    wid, hei = 3, 3

    domain = basic_domain(wid, hei)

    rules = [BulletinInfo("To draw a connection between vertices, use WASD, arrow keys, or mouse to draw a straight line."),
             EdgesExactlyRule(5)]

    starts = [(1, 1)]

    return domain, rules, starts, (wid, hei)


def tutorial_five():
    wid, hei = 3, 3

    domain = basic_domain(wid, hei)

    rules = [FinishVertex((2, 2))]

    starts = [(0, 0)]

    return domain, rules, starts, (wid, hei)


def tutorial_six():
    wid, hei = 3, 3

    domain = basic_domain(wid, hei)

    domain[1].remove(((0, 0), (1, 0)))
    domain[1].remove(((2, 1), (2, 2)))
    domain[1].remove(((1, 0), (1, 1)))

    rules = [BulletinInfo("You can't draw a connection on a dotted edge."),
             EdgesExactlyRule(7)]

    starts = [(0, 0)]

    return domain, rules, starts, (wid, hei)


def tutorial_seven():
    wid, hei = 3, 3

    domain = basic_domain(wid, hei)

    domain[1].remove(((0, 0), (1, 0)))
    domain[1].remove(((2, 1), (2, 2)))
    domain[1].remove(((1, 0), (1, 1)))

    rules = [EdgesExactlyRule(7), FinishVertex((2, 2))]

    starts = [(0, 0), (1, 0)]

    return domain, rules, starts, (wid, hei)



def tutorial_eight():
    wid, hei = 1, 2

    domain = basic_domain(wid, hei)

    rules = [OneWayEdge((0, 0), (0, 1)),
             EdgesExactlyRule(1)]

    starts = [(0, 0), (0, 1)]

    return domain, rules, starts, (wid, hei)





# DEFAULT LEVEL

def level_default():
    wid, hei = 5, 7

    domain = basic_domain(wid, hei)

    rules = [EdgesGreaterThanRule(12), CellExactlyNVertex((3, 1), 2),
             EdgeExactlyOneVertex((3, 0), (3, 1)), CellExactlyNEdge((1, 4), 3),
             IncludeVertex((1, 4)), IncludeEdge((2, 3), (2, 4)),
             FinishVertex((3, 3)), GroupCell((0, 1), 2), GroupCell((3, 5), 1),
             ColorCell((1, 5)), ColorCell((3, 0), color="steel blue")]

    starts = [(0, 0), (3, 5)]

    return domain, rules, starts, (wid, hei)


def import_level_from_json(file):
    with open(file, "r") as json_file:
        data = DECODER.decode(json_file.read())
        domainLst = data["domain"]
        startsLst = data["starts"]
        vertices = []
        edges = []
        cells = []
        starts = []
        for vertex in domainLst[0]:
            vertices.append(tuple(vertex))
        for edge1, edge2 in domainLst[1]:
            edges.append((tuple(edge1), tuple(edge2)))
        for cell in domainLst[2]:
            cells.append(tuple(cell))
        for start in startsLst:
            starts.append(tuple(start))

        domain = (vertices, edges, cells)

        rules_txt = data["rulesTxt"]
        bounds = tuple(data["bounds"])



        rules = []
        for rule_txt in rules_txt:
            class_txt = rule_txt[0]
            cls = getattr(sys.modules[__name__], class_txt)
            rules.append(cls(*(tuple(data) if isinstance(data, list) else data for data in rule_txt[1:])))

        return domain, rules, starts, bounds


def export_level_to_json(file, domain, rules, starts, bounds):
    data = {"domain": domain, "rulesTxt": [], "starts": starts, "bounds": bounds}
    for rule in rules:
        ruledata = list(rule.essential_data)
        ruledata.insert(0, type(rule).__name__)
        data["rulesTxt"].append(ruledata)

    text = ENCODER.encode(data)
    with open(file, "w") as json_file:
        json_file.write(text)


if __name__ == "__main__":
    lev = level_default()
    export_level_to_json("json_levels/default.json", *lev)
    imp = import_level_from_json("json_levels/default.json")
    print(lev)
    print(imp)

    for i in range(len(lev[1])):
        print(lev[1][i].essential_data)
        print(imp[1][i].essential_data)



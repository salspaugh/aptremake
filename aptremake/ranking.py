
from languages import Task
from data import Type, Set, FunctionalDependency, CartesianProduct

quantitative = {
    Task.position: 0,
    Task.length: 1,
    Task.angle: 2,
    Task.slope: 3,
    Task.area: 4,
    Task.volume: 5,
    Task.density: 6,
    Task.saturation: 7,
    Task.hue: 8,
    Task.mark: 13
}

ordinal = {
    Task.position: 0,
    Task.density: 1,
    Task.saturation: 2,
    Task.hue: 3,
    Task.texture: 4,
    Task.connection: 5,
    Task.containment: 6,
    Task.length: 7,
    Task.angle: 8,
    Task.slope: 9,
    Task.area: 10,
    Task.volume: 11,
    Task.mark: 13
}

nominal = {
    Task.position: 0,
    Task.hue: 1,
    Task.texture: 2,
    Task.connection: 3,
    Task.containment: 4,
    Task.density: 5,
    Task.saturation: 6,
    Task.shape: 7,
    Task.length: 8,
    Task.angle: 9,
    Task.slope: 10,
    Task.area: 11,
    Task.volume: 12,
    Task.mark: 13
}

none = {
    Task.position: 100
}

ranking_lists = {
    "quantitative" : quantitative,
    "ordinal" : ordinal, 
    "nominal" : nominal,
    None: none
}

def rank(partition, designs):
    ranks = {}
    for design in designs:
        rank = []
        for (name, (type, task)) in design.tasks.iteritems():
            rank.append(ranking_lists[type][task])
        ranks[design] = "".join([str(r) for r in rank])
    ranks = sorted(ranks.items(), key=lambda x: x[1])
    return [r[0] for r in ranks]
    



from languages import Task
from data import Type, Set, FunctionalDependency, CartesianProduct

quantitative = [
    Task.position,
    Task.length,
    Task.angle,
    Task.slope,
    Task.area,
    Task.volume,
    Task.density,
    Task.saturation,
    Task.hue,
    Task.mark
]

ordinal = [
    Task.position,
    Task.density,
    Task.saturation,
    Task.hue,
    Task.texture,
    Task.connection,
    Task.containment,
    Task.length,
    Task.angle,
    Task.slope,
    Task.area,
    Task.volume,
    Task.mark
]

nominal = [
    Task.position,
    Task.hue,
    Task.texture,
    Task.connection,
    Task.containment,
    Task.density,
    Task.saturation,
    Task.shape,
    Task.length,
    Task.angle,
    Task.slope,
    Task.area,
    Task.volume,
    Task.mark
]

ranking_lists = {
    "QUANTITATIVE" : quantitative,
    "ORDINAL" : ordinal, 
    "NOMINAL" : nominal
}

def rank(partition, designs):
    type = None
    if isinstance(partition, Set):
        type = partition.type
    if isinstance(partition, FunctionalDependency):
        type = partition.dependent.type
    if isinstance(partition, CartesianProduct):
        type = partition.sets[0].type
    ranks = {}
    for design in designs:
        rank = []
        for (name, (type, task)) in design.tasks.iteritems():
            rank.append(ranking_lists[type].index(task))
        ranks[design] = "".join([str(r) for r in rank])
    ranks = sorted(ranks.items(), key=lambda x: x[1])
    return [r[0] for r in ranks]
    


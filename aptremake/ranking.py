
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
        type = partition.range.type
    if isinstance(partition, CartesianProduct):
        type = partition.sets[0].type
    ranking_list = ranking_lists[type]
    ranks = {}
    for design in designs:
        ranks[design] = ranking_list.index(design.task)
    ranks = sorted(ranks.items(), key=lambda x: x[1])
    return [r[0] for r in ranks]
    



from metadata import read_metadata
from apt import generate_presentation

def run_all_tests():
    test_fdnn_fdnn()
    test_fdnn_fdno()    
    test_fdnn_fdnq()
    test_fdno_fdnn()
    test_fdno_fdno()    
    test_fdno_fdnq()
    test_fdnq_fdnn()
    test_fdnq_fdno()    
    test_fdnq_fdnq()
    test_fdnq_fdnq_fdnq()

def test_fdnn_fdnn():
    print "CASE: {FD: nominal -> nominal, FD: nominal -> nominal}"
    test_columns(["Car nationality for 1979", "Car nationality for 1979"])

def test_fdnn_fdno():
    print "CASE: {FD: nominal -> nominal, FD: nominal -> ordinal}"
    test_columns(["Car nationality for 1979", "Repair record for 1979"])

def test_fdnn_fdnq():
    print "CASE: {FD: nominal -> nominal, FD: nominal -> quantitative}"
    test_columns(["Car nationality for 1979", "Car weight for 1979"])

def test_fdno_fdnn():
    print "CASE: {FD: nominal -> ordinal, FD: nominal -> nominal}"
    test_columns(["Car nationality for 1979", "Car nationality for 1979"])

def test_fdno_fdno():
    print "CASE: {FD: nominal -> ordinal, FD: nominal -> ordinal}"
    test_columns(["Car nationality for 1979", "Repair record for 1979"])

def test_fdno_fdnq():
    print "CASE: {FD: nominal -> ordinal, FD: nominal -> quantitative}"
    test_columns(["Car nationality for 1979", "Car weight for 1979"])

def test_fdnq_fdnn():
    print "CASE: {FD: nominal -> nominal, FD: nominal -> nominal}"
    test_columns(["Car mileage for 1979", "Car nationality for 1979"])

def test_fdnq_fdno():
    print "CASE: {FD: nominal -> quantitative, FD: nominal -> ordinal}"
    test_columns(["Car mileage for 1979", "Repair record for 1979"])

def test_fdnq_fdnq():
    print "CASE: {FD: nominal -> quantitative, FD: nominal -> quantitative}"
    test_columns(["Car mileage for 1979", "Car weight for 1979"])

def test_fdnq_fdnq_fdnq():
    print "CASE: {FD: nominal -> quantitative, FD: nominal -> quantitative, FD: nominal -> quantitative}"
    test_columns(["Car mileage for 1979", "Car weight for 1979", "Car price for 1979"])

def test_columns(keys):
    metadata = read_test_metadata()
    db = metadata["database"]
    relations = [metadata[k] for k in keys]
    query = construct_test_query(relations)
    labels = [r.name for r in relations]
    visualization_generator = generate_presentation(db, relations, query, labels)
    for visualization in visualization_generator:
        print_visualization_type(visualization)

def print_visualization_type(visualization):
    type = ""
    if is_scatterplot(visualization):
        type = "scatterplot"
    if is_barchart(visualization):
        type = "barchart"
    if is_column_barcharts(visualization):
        type = "column barcharts"
    if type and uses_color(visualization):
        type = "color " + type
    elif type:
        type = "bw " + type
    if type:
        print "\t" + type

def read_test_metadata():
    car_metadata = "/Users/salspaugh/classes/visualization/project/aptremake/specs/json/cars.spec"
    return read_metadata(car_metadata) 

def construct_test_query(relations):
    columns = tuple([r.dependent.name for r in relations])
    blanks = ", ".join(["%s"]*len(relations))
    return " ".join(["SELECT APTREMAKEID,", blanks, "FROM cars"]) % columns 

def uses_color(design):
    return design["hasColor"]

def is_single_axis(design):
    if len(design["subplots"]) == 1:
        plot = design["subplots"][0] 
        if plot_is_single_axis(plot):
            return True
    return False

def is_scatterplot(design):
    if len(design["subplots"]) == 1:
        plot = design["subplots"][0] 
        if plot_is_scatterplot(plot):
            return True
    return False

def is_barchart(design):
    if len(design["subplots"]) == 1:
        plot = design["subplots"][0]
        if plot_is_barchart(plot):
            return True
    return False

def is_column_barcharts(design):
    if design["nrows"] > 1 and design["ncols"] == 1:
        for plot in design["subplots"]:
            if not plot_is_scatterplot(plot):
                return False
        return True
    return False

def plot_is_single_axis(plot):
    if plot["hpos"] and not plot["vpos"] and plot["markType"] == "point":
        return True
    if not plot["hpos"] and plot["vpos"] and plot["markType"] == "point":
        return True
    return False

def plot_is_scatterplot(plot):
    if plot["hpos"] and plot["vpos"] and plot["markType"] == "point":
        return True
    return False

def plot_is_barchart(plot):
    if plot["hpos"] and plot["vpos"] and plot["markType"] == "bar":
        return True
    return False

if __name__ == "__main__":
    run_all_tests()

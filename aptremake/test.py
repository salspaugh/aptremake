
from metadata import read_metadata, View
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

    test_fdnn_fdnq_fdnn()
    test_fdnn_fdnq_fdno()    
    test_fdnn_fdnq_fdnq()
    
    #test_fdnn_fdnn_fdnn()
    #test_fdnn_fdnn_fdno()    
    #test_fdnn_fdnn_fdnq()
    
    test_fdno_fdnq_fdnn()
    test_fdno_fdnq_fdno()    
    test_fdno_fdnq_fdnq()
    
    #test_fdno_fdno_fdnn()
    #test_fdno_fdno_fdno()    
    #test_fdno_fdno_fdnq()
    
    test_fdnq_fdnq_fdnn()
    test_fdnq_fdnq_fdno()    
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

def test_fdnn_fdnq_fdnn():
    print "CASE: {FD: nominal -> nominal, nominal -> nominal, FD: nominal -> nominal}"
    test_columns(["Car nationality for 1979", "Car mileage for 1979", "Car nationality for 1979"])

def test_fdnn_fdnq_fdno():
    print "CASE: {FD: nominal -> nominal, nominal -> quantitative, FD: nominal -> ordinal}"
    test_columns(["Car nationality for 1979", "Car mileage for 1979", "Repair record for 1979"])

def test_fdnn_fdnq_fdnq():
    print "CASE: {FD: nominal -> nominal, nominal -> quantitative, FD: nominal -> quantitative, FD: nominal -> quantitative}"
    test_columns(["Car nationality for 1979", "Car weight for 1979", "Car price for 1979"])

def test_fdno_fdnq_fdnn():
    print "CASE: {FD: nominal -> ordinal, nominal -> nominal, FD: nominal -> nominal}"
    test_columns(["Repair record for 1979", "Car mileage for 1979", "Car nationality for 1979"])

def test_fdno_fdnq_fdno():
    print "CASE: {FD: nominal -> ordinal, nominal -> quantitative, FD: nominal -> ordinal}"
    test_columns(["Repair record for 1979", "Car mileage for 1979", "Repair record for 1979"])

def test_fdno_fdnq_fdnq():
    print "CASE: {FD: nominal -> ordinal, FD: nominal -> quantitative, FD: nominal -> quantitative}"
    test_columns(["Repair record for 1979", "Car weight for 1979", "Car price for 1979"])

def test_fdnq_fdnq_fdnn():
    print "CASE: {FD: nominal -> quantitative, nominal -> nominal, FD: nominal -> nominal}"
    test_columns(["Car weight for 1979", "Car mileage for 1979", "Car nationality for 1979"])

def test_fdnq_fdnq_fdno():
    print "CASE: {FD: nominal -> quantitative, nominal -> quantitative, FD: nominal -> ordinal}"
    test_columns(["Car weight for 1979", "Car mileage for 1979", "Repair record for 1979"])

def test_fdnq_fdnq_fdnq():
    print "CASE: {FD: nominal -> quantitative, FD: nominal -> quantitative, FD: nominal -> quantitative}"
    test_columns(["Car weight for 1979", "Car mileage for 1979", "Car weight for 1979", "Car price for 1979"])

def test_columns(keys):
    metadata = read_test_metadata()
    db = metadata["database"]
    table = metadata["table"]
    relations = [metadata["relations"][k] for k in keys]
    query = construct_test_query(relations, table)
    keys = [r.name for r in relations]
    view = View(relations, db, query, keys) 
    visualization_generator = generate_presentation(view)
    for visualization in visualization_generator:
        print_visualization_type(visualization)

def print_visualization_type(visualization):
    type = ""
    if is_scatterplot(visualization):
        type = "scatterplot"
    if is_single_axis(visualization):
        type = "single axis"
    if is_barchart(visualization):
        type = "barchart"
    if is_column_barcharts(visualization):
        type = "column barcharts"
    if is_row_barcharts(visualization):
        type = "row barcharts"
    if type and uses_color(visualization):
        type = "color " + type
    elif type:
        type = "bw " + type
    if type:
        print "\t" + type
    else:
        del visualization["data"]
        print visualization
        print "\tuncategorized"

def read_test_metadata():
    car_metadata = "/Users/salspaugh/classes/visualization/project/aptremake/specs/json/cars_coded.spec"
    return read_metadata(car_metadata) 

def construct_test_query(relations, table):
    r = relations[0]
    if len(relations) == 1:
        columns = [r.determinant.name, r.dependent.name]
    else:
        columns = [r.determinant.name] + [r.dependent.name for r in relations]
    blanks = ", ".join(["%s"]*len(columns))
    return " ".join(["SELECT APTREMAKEID,", blanks, "FROM %s"]) % tuple(columns + [table]) 

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
            if not plot_is_barchart(plot):
                return False
        return True
    return False

def is_row_barcharts(design):
    if design["ncols"] > 1 and design["nrows"] == 1:
        for plot in design["subplots"]:
            if not plot_is_barchart(plot):
                return False
        return True
    return False

def plot_is_single_axis(plot):
    return (plot["hasHaxis"] and not plot["hasVaxis"] and plot["markType"] == "point") \
        or (not plot["hasHaxis"] and plot["hasVaxis"] and plot["markType"] == "point")

def plot_is_scatterplot(plot):
    return plot["hasHaxis"] and plot["hasVaxis"] and plot["markType"] == "point"

def plot_is_barchart(plot):
    return plot["hasHaxis"] and plot["hasVaxis"] and plot["markType"] == "bar"

if __name__ == "__main__":
    run_all_tests()

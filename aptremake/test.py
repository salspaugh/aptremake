
from metadata import read_metadata
from apt import generate_presentation

"""
Test Cases:
    (nominal -> nominal)
    (nominal -> ordinal)
    (nominal -> quantitative)
    (nominal -> nominal), (nominal -> nominal)
    (nominal -> ordinal), (nominal -> nominal)
    (nominal -> quantitative), (nominal -> nominal)
    (nominal -> nominal), (nominal -> ordinal)
    (nominal -> ordinal), (nominal -> ordinal)
    (nominal -> quantitative), (nominal -> ordinal)
    (nominal -> nominal), (nominal -> quantitative)
    (nominal -> ordinal), (nominal -> quantitative)
    - (nominal -> quantitative), (nominal -> quantitative)
"""

def run_all_tests():
    #test_fdnn_fdnn()
    #test_fdno_fdnn()
    test_fdnq_fdnn()
    test_fdnq_fdno()    
    test_fdnq_fdnq()
    test_fdnq_fdnq_fdnq()

def test_fdnq_fdnn():
    print "CASE: {fdnq, fdnn}"
    test_columns(["Car mileage for 1979", "Car nationality for 1979"])

def test_fdnq_fdno():
    print "CASE: {fdnq, fdno}"
    test_columns(["Car mileage for 1979", "Repair record for 1979"])

def test_fdnq_fdnq():
    print "CASE: {fdnq, fdnq}"
    test_columns(["Car mileage for 1979", "Car weight for 1979"])

def test_fdnq_fdnq_fdnq():
    print "CASE: {fdnq, fdnq, fdnq}"
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

def is_scatterplot(design):
    if len(design["subplots"]) == 1:
        plot = design["subplots"][0] 
        if plot["markType"] == "point":
            return True
    return False

def is_barchart(design):
    if len(design["subplots"]) == 1:
        plot = design["subplots"][0]
        if plot["markType"] == "bar":
            return True
    return False

if __name__ == "__main__":
    run_all_tests()

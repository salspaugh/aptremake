{
    "database": "aptremake.db",
    "table": "cars_coded",
    "relations": [
        {
            "name": "Car",
            "label": "Fahrzeug",
            "class": "Set",
            "type": "nominal",
            "domain": "Car",
            "arity": 1,
            "coding":{
                    "1": "Kleines Accord",
                    "2": "Kleines AMC Pacer", 
                    "3": "Kleines Audi 5000",
                    "4": "Kleines BMW 320i", 
                    "5": "Kleines Champ", 
                    "6": "Kleines Chev Nova", 
                    "7": "Kleines Civic", 
                    "8": "Kleines Datsun 210", 
                    "9": "Kleines Datsun 810", 
                    "10":"Kleines Deville", 
                    "11":"Kleines Le Car", 
                    "12":"Kleines Linc Cont", 
                    "13":"Kleines Horizon", 
                    "14":"Kleines Mustang", 
                    "15":"Kleines Peugot", 
                    "16":"Kleines Saab 900", 
                    "17":"Kleines Subaru", 
                    "18":"Kleines Volvo 260", 
                    "19":"Kleines VW Dasher"
                },
            "data": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
        },
        {
            "name": "Nation",
            "label": "Land",
            "class": "Set",
            "type": "nominal",
            "arity": 1,
            "coding":{
                    "1":"Schoener USA", 
                    "2":"Schoener Japan", 
                    "3":"Schoener Germany", 
                    "4":"Schoener France", 
                    "5":"Schoener Sweden"
            },
            "data": ["1", "2", "3", "4", "5"]
        },
        {
            "name": "Car nationality for 1979",
            "label": "Nationalitaet fuer Fahrzeug am 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Nation",
            "arity": 2,
            "data": [["1", "2"], ["2", "1"], ["3", "3"], ["4", "3"], ["5", "1"], ["6", "1"], ["7", "2"], ["8", "2"], ["9", "2"], ["10", "1"], ["11", "4"], ["12", "1"], ["13", "1"], ["14", "1"], ["15", "4"], ["16", "5"], ["17", "2"], ["18", "5"], ["19", "3"]]
        },
        {
            "name": "Price",
            "label": "Preis",
            "class": "Set",
            "type": "quantitative",
            "domain": "Price",
            "arity": 1,
            "data": [5900, 4250, 10000, 10100, 4000, 3700, 4000, 4100, 8250, 11250, 3650, 11500, 4000, 3850, 13000, 9000, 3600, 12000, 7000]
        }, 
        {
            "name": "Car price for 1979",
            "label": "Preis fuer Fahrzeug am 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Price",
            "arity": 2,
            "data": [["1", 5799], ["2", 4749], ["3", 9690], ["4", 9735], ["5", 4425], ["6", 3955], ["7", 4499], ["8", 4589], ["9", 8128], ["10", 11385], ["11", 3895], ["12", 11497], ["13", 4482], ["14", 4187], ["15", 12990], ["16", 9348], ["17", 3798], ["18", 11995], ["19", 7140]]
        },
        {
            "name": "Repair",
            "label": "Zustand",
            "class": "Set",
            "type": "ordinal",
            "domain": "Repair",
            "coding":{
                    "5":"Toll",
                    "4":"Gut", 
                    "3":"OK",
                    "2":"Schlect", 
                    "1":"Sehr Schlecht"
            },
            "ordering": {
                "5": 5,
                "4": 4,
                "3": 3,
                "2": 2,
                "1": 1
            },
            "arity": 1,
            "data": ["5", "4", "3", "2", "1"]
        },
        {
            "name": "Repair record for 1979",
            "label": "Zustand von Fahrzeug am 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Repair",
            "arity": 2,
            "data": [["1", "5"], ["2", "1"], ["3", "2"], ["4", "4"], ["5", "4"], ["6", "3"], ["7", "4"], ["8", "5"], ["9", "4"], ["10", "3"], ["11", "3"], ["12", "4"], ["13", "3"], ["14", "3"], ["15", "3"], ["16", "2"], ["17", "4"], ["18", " 1"], ["19", "3"]]
        },
        {
            "name": "Mileage",
            "label": "Kraftstoffverbrauch",
            "class": "Set",
            "type": "quantitative",
            "domain": "Mileage",
            "arity": 1,
            "data": [25, 17, 17, 25, 32, 18, 28, 35, 20, 13, 25, 12, 23, 20, 15, 20, 33, 17, 22]
        },
        {
            "name": "Car mileage for 1979",
            "label": "Kraftsoffverbrauch am 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Mileage",
            "arity": 2,
            "data": [["1", 25], ["2", 17], ["3", 17], ["4", 25], ["5", 32], ["6", 18], ["7", 28], ["8", 35], ["9", 20], ["10", 13], ["11", 25], ["12", 12], ["13", 23], ["14", 20], ["15", 15], ["16", 20], ["17", 33], ["18", 17], ["19", 22]]
        },
        {
            "name": "Weight",
            "label": "Gewicht is a German word for Weight and this axis label is so very long that I hope it can wrap yes I think we need to wrap this one and my how I am bad at JS",
            "class": "Set",
            "type": "quantitative",
            "domain": "Weight",
            "arity": 1,
            "data": [2000, 3200, 3000, 2900, 1600, 3200, 1600, 1700, 3000, 4000, 1550, 4500, 2200, 3000, 3500, 3000, 1800, 3100, 1800]
        },
        {
            "name": "Car weight for 1979",
            "label": "Gewicht von Fahrzeug am 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Weight",
            "arity": 2,
            "data": [["1", 2000], ["2", 3200], ["3", 3000], ["4", 2900], ["5", 1600], ["6", 3200], ["7", 1600], ["8", 1700], ["9", 3000], ["10", 4000], ["11", 1550], ["12", 4500], ["13", 2200], ["14", 3000], ["15", 3500], ["16", 3000], ["17", 1800], ["18", 3100], ["19", 1800]]
        }
    ]
}

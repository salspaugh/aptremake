{
    "database": "aptremake.db",
    "table": "cars",
    "relations": [
        {
            "name": "Car",
            "class": "Set",
            "type": "nominal",
            "domain": "Car",
            "arity": 1,
            "data": ["Accord", "AMC Pacer", "Audi 5000", "BMW 320i", "Champ", "Chev Nova", "Civic", "Datsun 210", "Datsun 810", "Deville", "Le Car", "Linc Cont", "Horizon", "Mustang", "Peugot", "Saab 900", "Subaru", "Volvo 260", "VW Dasher"]
        },
        {
            "name": "Nation",
            "class": "Set",
            "type": "nominal",
            "arity": 1,
            "data": ["USA", "Japan", "Germany", "France", "Sweden"]
        },
        {
            "name": "Car nationality for 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Nation",
            "arity": 2,
            "data": [["Accord", "Japan"], ["AMC Pacer", "USA"], ["Audi 5000", "Germany"], ["BMW 320i", "Germany"], ["Champ", "USA"], ["Chev Nova", "USA"], ["Civic", "Japan"], ["Datsun 210", "Japan"], ["Datsun 810", "Japan"], ["Deville", "USA"], ["Le Car", "France"], ["Linc Cont", "USA"], ["Horizon", "USA"], ["Mustang", "USA"], ["Peugot", "France"], ["Saab 900", "Sweden"], ["Subaru", "Japan"], ["Volvo 260", "Sweden"], ["VW Dasher", "Germany"]]
        },
        {
            "name": "Price",
            "class": "Set",
            "type": "quantitative",
            "domain": "Price",
            "arity": 1,
            "data": [5900, 4250, 10000, 10100, 4000, 3700, 4000, 4100, 8250, 11250, 3650, 11500, 4000, 3850, 13000, 9000, 3600, 12000, 7000]
        }, 
        {
            "name": "Car price for 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Price",
            "arity": 2,
            "data": [["Accord", 5799], ["AMC Pacer", 4749], ["Audi 5000", 9690], ["BMW 320i", 9735], ["Champ", 4425], ["Chev Nova", 3955], ["Civic", 4499], ["Datsun 210", 4589], ["Datsun 810", 8128], ["Deville", 11385], ["Le Car", 3895], ["Linc Cont", 11497], ["Horizon", 4482], ["Mustang", 4187], ["Peugot", 12990], ["Saab 900", 9348], ["Subaru", 3798], ["Volvo 260", 11995], ["VW Dasher", 7140]]
        },
        {
            "name": "Repair",
            "class": "Set",
            "type": "ordinal",
            "domain": "Repair",
            "ordering": {
                "Great": 5,
                "Good": 4,
                "OK": 3,
                "Bad": 2,
                "Terrible": 1
            },
            "arity": 1,
            "data": ["Great", "Good", "OK", "Bad", "Terrible"]
        },
        {
            "name": "Repair record for 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Repair",
            "arity": 2,
            "data": [["Accord", "Great"], ["AMC Pacer", "Terrible"], ["Audi 5000", "Bad"], ["BMW 320i", "Good"], ["Champ", "Good"], ["Chev Nova", "OK"], ["Civic", "Good"], ["Datsun 210", "Great"], ["Datsun 810", "Good"], ["Deville", "OK"], ["Le Car", "OK"], ["Linc Cont", "Good"], ["Horizon", "OK"], ["Mustang", "OK"], ["Peugot", "OK"], ["Saab 900", "Bad"], ["Subaru", "Good"], ["Volvo 260",  "Terrible"], ["VW Dasher", "OK"]]
        },
        {
            "name": "Mileage",
            "class": "Set",
            "type": "quantitative",
            "domain": "Mileage",
            "arity": 1,
            "data": [25, 17, 17, 25, 32, 18, 28, 35, 20, 13, 25, 12, 23, 20, 15, 20, 33, 17, 22]
        },
        {
            "name": "Car mileage for 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Mileage",
            "arity": 2,
            "data": [["Accord", 25], ["AMC Pacer", 17], ["Audi 5000", 17], ["BMW 320i", 25], ["Champ", 32], ["Chev Nova", 18], ["Civic", 28], ["Datsun 210", 35], ["Datsun 810", 20], ["Deville", 13], ["Le Car", 25], ["Linc Cont", 12], ["Horizon", 23], ["Mustang", 20], ["Peugot", 15], ["Saab 900", 20], ["Subaru", 33], ["Volvo 260", 17], ["VW Dasher", 22]]
        },
        {
            "name": "Weight",
            "class": "Set",
            "type": "quantitative",
            "domain": "Weight",
            "arity": 1,
            "data": [2000, 3200, 3000, 2900, 1600, 3200, 1600, 1700, 3000, 4000, 1550, 4500, 2200, 3000, 3500, 3000, 1800, 3100, 1800]
        },
        {
            "name": "Car weight for 1979",
            "class": "FunctionalDependency",
            "determinant": "Car",
            "dependent": "Weight",
            "arity": 2,
            "data": [["Accord", 2000], ["AMC Pacer", 3200], ["Audi 5000", 3000], ["BMW 320i", 2900], ["Champ", 1600], ["Chev Nova", 3200], ["Civic", 1600], ["Datsun 210", 1700], ["Datsun 810", 3000], ["Deville", 4000], ["Le Car", 1550], ["Linc Cont", 4500], ["Horizon", 2200], ["Mustang", 3000], ["Peugot", 3500], ["Saab 900", 3000], ["Subaru", 1800], ["Volvo 260", 3100], ["VW Dasher", 1800]]
        }
    ]
}

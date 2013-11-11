[
    {
        "name": "Class",
        "class": "Set",
        "type": "NOMINAL",
        "domain": "Class",
        "data": ["AdvDB", "AIProg", "Compilers", "DB", "FundAI", "FundCS", "FundMTC", "OS", "PL"]
    },
    {
        "name": "Quarters",
        "class": "Set",
        "type": "ORDINAL",
        "domain": "Quarters",
        "data": ["Fall85", "Winter86", "Spring86", "Fall86"]
    },
    {
        "name": "Class Prerequisites",
        "class": "CrossProduct",
        "data": [["FundAI", "AI Prog"], ["FundMTC", "AdvDB"], ["FundCS", "DB"], ["FundCS", "PL"], ["DB", "AdvDB"], ["PL", "Compilers"], ["PL", "OS"]]
    },
    {
        "name": "Class Schedule",
        "class": "FunctionalDependency",
        "data": [["AdvDB", "Winter86"], ["AIProg", "Fall86"], ["Compilers", "Fall86"], ["DB", "Spring86"], ["FundAI", "Spring86"], ["FundCS", "Fall85"], ["FundMTC", "Fall85"], ["OS", "Spring86"], ["PL", "Winter86"]]
    }
]

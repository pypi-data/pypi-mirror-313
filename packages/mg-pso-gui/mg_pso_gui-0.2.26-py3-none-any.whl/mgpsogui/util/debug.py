from recosu.pso import global_best

# 1) COSU steps, definition of parameters to calibrate
steps = [
    {  # step 1
        "param": [
            {"name": "soilOutLPS", "bounds": (0.0, 2.0)},
            {"name": "lagInterflow", "bounds": (10.0, 80.0)},
        ],
        "objfunc": [
            {
                "name": "ns",  # Name (Must be unique)
                "of": "ns",  # Objective Function
                "data": (
                    "obs_data02_14.csv/obs/orun[1]",
                    "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                )
                # Optional Weight parameter. If not specified it is 1 or evenly distributed between all objective functions
            }
        ],
    },
    {  # step 2
        "param": [
            {"name": "flowRouteTA", "bounds": (0.4, 5.0)},
            {"name": "soilMaxDPS", "bounds": (0.0, 5.0)},
        ],
        "objfunc": [
            {
                "name": "ns",
                "of": "ns",
                "data": (
                    "obs_data02_14.csv/obs/orun[1]",
                    "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                ),
            }
        ],
    },
]

steps = [
    {
        "param": [
            {
                "name": "soilOutLPS",
                "bounds": (0.0, 2.0),
                "default_value": 1.0,
                "optimal_value": 0.0,
                "type": "float",
                "calibration_strategy": "none",
            },
            {
                "name": "lagInterflow",
                "bounds": (10.0, 80.0),
                "default_value": 1.0,
                "optimal_value": 0.0,
                "type": "float",
                "calibration_strategy": "none",
            },
        ],
        "objfunc": [
            {
                "name": "ns",
                "of": "ns",
                "weight": 1.0,
                "data": (
                    "obs_data02_14.csv/obs/orun[1]",
                    "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                ),
            }
        ],
    },
    {
        "param": [
            {
                "name": "flowRouteTA",
                "bounds": (0.4, 5.0),
                "default_value": 1.0,
                "optimal_value": 0.0,
                "type": "float",
                "calibration_strategy": "none",
            },
            {
                "name": "soilMaxDPS",
                "bounds": (0.0, 5.0),
                "default_value": 1.0,
                "optimal_value": 0.0,
                "type": "float",
                "calibration_strategy": "none",
            },
        ],
        "objfunc": [
            {
                "name": "ns",
                "of": "ns",
                "weight": 1.0,
                "data": (
                    "obs_data02_14.csv/obs/orun[1]",
                    "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                ),
            }
        ],
    },
]

# 2) static ages parameters
args = {
    "param": [
        {"name": "startTime", "value": "2002-01-01"},
        {"name": "endTime", "value": "2006-12-31"},
        {"name": "dataStartTime", "value": "2002-01-01"},
        {"name": "dataEndTime", "value": "2006-12-31"},
        {"name": "cal_startTime", "value": "2003-01-01"},
        {"name": "cal_endTime", "value": "2006-12-31"},
        {"name": "parallelismThreads", "value": "2"},
        {"name": "flagLoadState", "value": "True"},
        {"name": "payload", "value": "false"},
        {"name": "project", "value": "SFIR3"},
    ],
    # the service url
    "url": "http://csip.engr.colostate.edu:8087/csip-oms/m/ages/0.3.0",
    # the files to attach for each run
    "files": {},
}

args = {
    "param": [
        {"name": "startTime", "value": "2002-01-01"},
        {"name": "endTime", "value": "2006-12-31"},
        {"name": "dataStartTime", "value": "2002-01-01"},
        {"name": "dataEndTime", "value": "2006-12-31"},
        {"name": "cal_startTime", "value": "2003-01-01"},
        {"name": "cal_endTime", "value": "2006-12-31"},
        {"name": "parallelismThreads", "value": "2"},
        {"name": "flagLoadState", "value": "True"},
        {"name": "payload", "value": "false"},
        {"name": "project", "value": "SFIR3"},
    ],
    "url": "http://csip.engr.colostate.edu:8087/csip-oms/m/ages/0.3.0",
    "mode": "Optimization: MG-PSO",
    "files": {},
}

if "mode" in args:
    del args["mode"]

# 3. perform optimization
optimizer, trace = global_best(
    steps,  # step definition
    rounds=(1, 2),  # min/max number of rounds
    args=args,  # static arguments
    n_particles=10,  # number of particle candidates for each param
    iters=20,  # max # of iterations
    n_threads=10,  # number of threads to use
    # ftol=0.00000001,                          # min cost function delta for convergence
    options={"c1": 2, "c2": 2, "w": 0.8},  # hyperparameter
    oh_strategy={
        "w": "adaptive",
        "c1": "adaptive",
        "c2": "adaptive",
    },  # adaptive hyperparameter adjustments based on current and max # of iterations
    conf={
        "service_timeout": 400.0,
        "http_retry": 5,
        "http_allow_redirects": True,
        "async_call": False,
        "http_conn_timeout": 10,
        "http_read_timeout": 400,
        "particles_fail": 5,
        "step_trace": "./step_trace.json",
    },
)

step_trace = {
    "dir": "/Users/robertcordingly/Library/Python/3.8/lib/python/site-packages/mgpsogui/gui",
    "start": "2024-05-28 14:25:53.793407",
    "min_rounds": 1,
    "max_rounds": 2,
    "iters": 20,
    "ftol": "-inf",
    "ftol_iter": 1,
    "rtol": 0.001,
    "rtol_iter": 1,
    "n_threads": 10,
    "n_particles": 10,
    "n_steps": 2,
    "steps": [
        {
            "param": [
                {
                    "name": "soilOutLPS",
                    "bounds": (0.0, 2.0),
                    "default_value": 1.0,
                    "optimal_value": 0.0,
                    "type": "float",
                    "calibration_strategy": "none",
                },
                {
                    "name": "lagInterflow",
                    "bounds": (10.0, 80.0),
                    "default_value": 1.0,
                    "optimal_value": 0.0,
                    "type": "float",
                    "calibration_strategy": "none",
                },
            ],
            "objfunc": [
                {
                    "name": "ns",
                    "of": "ns",
                    "weight": 1.0,
                    "data": (
                        "obs_data02_14.csv/obs/orun[1]",
                        "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                    ),
                }
            ],
        },
        {
            "param": [
                {
                    "name": "flowRouteTA",
                    "bounds": (0.4, 5.0),
                    "default_value": 1.0,
                    "optimal_value": 0.0,
                    "type": "float",
                    "calibration_strategy": "none",
                },
                {
                    "name": "soilMaxDPS",
                    "bounds": (0.0, 5.0),
                    "default_value": 1.0,
                    "optimal_value": 0.0,
                    "type": "float",
                    "calibration_strategy": "none",
                },
            ],
            "objfunc": [
                {
                    "name": "ns",
                    "of": "ns",
                    "weight": 1.0,
                    "data": (
                        "obs_data02_14.csv/obs/orun[1]",
                        "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                    ),
                }
            ],
        },
    ],
    "args": "{'param': [{'name': 'startTime', 'value': '2002-01-01'}, {'name': 'endTime', 'value': '2006-12-31'}, {'name': 'dataStartTime', 'value': '2002-01-01'}, {'name': 'dataEndTime', 'value': '2006-12-31'}, {'name': 'cal_startTime', 'value': '2003-01-01'}, {'name': 'cal_endTime', 'value': '2006-12-31'}, {'name': 'parallelismThreads', 'value': '2'}, {'name': 'flagLoadState', 'value': 'True'}, {'name': 'payload', 'value': 'false'}, {'name': 'project', 'value': 'SFIR3'}], 'url': 'http://csip.engr.colostate.edu:8087/csip-oms/m/ages/0.3.0', 'files': {}}",
    "r1s1": {
        "time": "2024-05-28 14:28:27.648143",
        "best_costs": [0.4962544759194877, "inf"],
        "steps": [
            {
                "param": [
                    {
                        "name": "soilOutLPS",
                        "bounds": (0.0, 2.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 1.4277364777450963,
                    },
                    {
                        "name": "lagInterflow",
                        "bounds": (10.0, 80.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 65.31198215742819,
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
                "cost": 0.4962544759194877,
            },
            {
                "param": [
                    {
                        "name": "flowRouteTA",
                        "bounds": (0.4, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                    },
                    {
                        "name": "soilMaxDPS",
                        "bounds": (0.0, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
            },
        ],
    },
    "r1s2": {
        "time": "2024-05-28 14:30:53.464613",
        "best_costs": [0.4962544759194877, 0.4159144385219078],
        "steps": [
            {
                "param": [
                    {
                        "name": "soilOutLPS",
                        "bounds": (0.0, 2.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 1.4277364777450963,
                    },
                    {
                        "name": "lagInterflow",
                        "bounds": (10.0, 80.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 65.31198215742819,
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
                "cost": 0.4962544759194877,
            },
            {
                "param": [
                    {
                        "name": "flowRouteTA",
                        "bounds": (0.4, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 1.9846472555222765,
                    },
                    {
                        "name": "soilMaxDPS",
                        "bounds": (0.0, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 4.619363774024649,
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
                "cost": 0.4159144385219078,
            },
        ],
    },
    "r1": {
        "time": "2024-05-28 14:30:53.465478",
        "round_cost": 0.9121689144413955,
        "best_costs": [0.4962544759194877, 0.4159144385219078],
        "improvements": [False, False],
    },
    "r2s1": {
        "time": "2024-05-28 14:33:23.457742",
        "best_costs": [0.41218845540212334, 0.4159144385219078],
        "steps": [
            {
                "param": [
                    {
                        "name": "soilOutLPS",
                        "bounds": (0.0, 2.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 1.3832527609622032,
                    },
                    {
                        "name": "lagInterflow",
                        "bounds": (10.0, 80.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 71.21736822883048,
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
                "cost": 0.41218845540212334,
            },
            {
                "param": [
                    {
                        "name": "flowRouteTA",
                        "bounds": (0.4, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 1.9846472555222765,
                    },
                    {
                        "name": "soilMaxDPS",
                        "bounds": (0.0, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 4.619363774024649,
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
                "cost": 0.4159144385219078,
            },
        ],
    },
    "r2s2": {
        "time": "2024-05-28 14:35:50.514486",
        "best_costs": [0.41218845540212334, 0.4121061580572347],
        "steps": [
            {
                "param": [
                    {
                        "name": "soilOutLPS",
                        "bounds": (0.0, 2.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 1.3832527609622032,
                    },
                    {
                        "name": "lagInterflow",
                        "bounds": (10.0, 80.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 71.21736822883048,
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
                "cost": 0.41218845540212334,
            },
            {
                "param": [
                    {
                        "name": "flowRouteTA",
                        "bounds": (0.4, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 1.9461260670740506,
                    },
                    {
                        "name": "soilMaxDPS",
                        "bounds": (0.0, 5.0),
                        "default_value": 1.0,
                        "optimal_value": 0.0,
                        "type": "float",
                        "calibration_strategy": "none",
                        "value": 3.7734465992198514,
                    },
                ],
                "objfunc": [
                    {
                        "name": "ns",
                        "of": "ns",
                        "weight": 1.0,
                        "data": (
                            "obs_data02_14.csv/obs/orun[1]",
                            "output/csip_run/out/Outlet.csv/output/catchmentSimRunoff",
                        ),
                    }
                ],
                "cost": 0.4121061580572347,
            },
        ],
    },
    "r2": {
        "time": "2024-05-28 14:35:50.521162",
        "round_cost": 0.8242946134593581,
        "best_costs": [0.41218845540212334, 0.4121061580572347],
        "improvements": [False, False],
    },
    "rounds": 2,
    "end": "2024-05-28 14:35:51.017597",
    "time": "0:09:56.726582",
}

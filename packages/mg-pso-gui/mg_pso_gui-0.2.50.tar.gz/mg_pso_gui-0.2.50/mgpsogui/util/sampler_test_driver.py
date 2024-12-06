from typing import List, Dict, Iterable
from recosu.sampling.sampler import run_sampler


def main():
    steps: List[Dict[str, any]] = [
        {
            "param": [
                {
                    "name": "Ksink",
                    "bounds": [
                        0.0,
                        5.0
                    ],
                    "default_value": 1.0,
                    "type": "float",
                    "calibration_strategy": "none"
                },
                {
                    "name": "a_rain",
                    "bounds": [
                        5.0,
                        10.0
                    ],
                    "default_value": 1.0,
                    "type": "float",
                    "calibration_strategy": "none"
                },
                {
                    "name": "flowRouteTA",
                    "bounds": [
                        0.01,
                        0.1
                    ],
                    "default_value": 1.0,
                    "type": "float",
                    "calibration_strategy": "none"
                },
                {
                    "name": "soilMaxDPS",
                    "bounds": [
                        0.001,
                        10.0
                    ],
                    "default_value": 1.0,
                    "type": "float",
                    "calibration_strategy": "none"
                }
            ],
            "objfunc": [
                {
                    "name": "ns",
                    "of": "ns",
                    "weight": 1.0,
                    "data": [
                        "orun5minall.csv/Runoff/orun[0]",
                        "output/csip_run/out/subDailyOutlet.csv/output/subDailyCatchmentSimRunoff"
                    ]
                }
            ]
        }
    ]

    args: Dict[str, any] = {
        "param": [
            {
                "name": "startTime",
                "value": "2011-06-08"
            },
            {
                "name": "endTime",
                "value": "2011-07-13"
            },
            {
                "name": "dataStartTime",
                "value": "2011-06-08"
            },
            {
                "name": "dataEndTime",
                "value": "2011-07-13"
            },
            {
                "name": "cal_startTime",
                "value": "2011-06-08"
            },
            {
                "name": "cal_endTime",
                "value": "2011-07-13"
            },
            {
                "name": "parallelismThreads",
                "value": "8"
            },
            {
                "name": "flagLoadState",
                "value": "True"
            },
            {
                "name": "payload",
                "value": "false"
            },
            {
                "name": "project",
                "value": "drake58hru-5min"
            }
        ],
        "url": "http://csip.engr.colostate.edu:8087/csip-oms/m/ages/1.0.1_sub",
        "files": []
    }

    conf: Dict[str, any] = {
        "service_timeout": 400,
        "http_retry": 5,
        "allow_redirects": True,
        "async_call": True,
        "conn_timeout": 10,
        "read_timeout": 400,
    }

    trace = run_sampler(steps, args, 10, 2, "halton", conf=conf, trace_file="halton_trace.csv", offset=5)
    print(trace)
    
    
    trace = run_sampler(steps, args, 10, 2, "random", conf=conf, trace_file="random_trace.csv")
    print(trace)


if __name__ == "__main__":
    main()

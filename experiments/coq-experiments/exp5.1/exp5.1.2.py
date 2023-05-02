
# This experiment is the second fuzzing experiment.
# It'll run the new fuzzer with different power schedule parameters
# for every task(except IFC for now), every variant, and every property.
# We expect it to solve approximately 1/3 of the tasks.
# It takes approximately 6-8 hours to run with IFC, 3-4 hours without IFC.
# 174 tasks, 10 trials with 60 seconds
# If any trial times out, we stop running that task

# Notes:
# - This is going to run slightly faster than the trials we ran in the paper.
#   This is because the parameter is using OCaml ints rather than Coq nats.

import json
import os

from benchtool.Coq import Coq
from benchtool.Types import TrialConfig, ReplaceLevel, LogLevel
import itertools

RESULTS = f'{os.getcwd()}/results/Coq/exp5.1.2'
tool = Coq(results=RESULTS, log_level=LogLevel.INFO, replace_level=ReplaceLevel.SKIP)


## Part 1: BST and RBT

benches = (bench for bench in tool.all_benches() if bench.name in ['BinarySearchTree', 'RedBlack'])

for bench in benches:

    tool._preprocess(bench)
    variants = tool.all_variants(bench)
    variants.remove(next(variant for variant in variants if variant.name == 'base'))
    properties = tool.all_properties(bench)
    methods = list(method for method in tool.all_methods(bench) if method.name == 'TypeBasedFuzzer')

    cfg = json.load(open(f'experiments/coq-experiments/{bench.name}_exp_cfg.json'))
    tasks = cfg['tasks']
    finished = set(os.listdir(RESULTS))
    all_tasks = set(map(lambda vpm: f"{bench.name},{vpm[2].name},{vpm[0].name},test_{vpm[1]}.json" if f"test_{vpm[1]}" in tasks[vpm[0].name] else None, itertools.product(variants, properties, methods)))
    all_tasks.remove(None)
    remaining_tasks = all_tasks - finished
    remaining_variants = list(set(map(lambda e: e.split(".json")[0].split(",")[2], remaining_tasks)))

    for variant in (variant for variant in tool.all_variants(bench) if ((variant.name in tasks.keys()) and (variant.name in remaining_variants))):
        run_trial = tool.apply_variant(bench, variant, no_base=True)
        for property in (property for property in tool.all_properties(bench) if "test_" + property in tasks[variant.name]):
            print(f'Running {variant.name} {property}...')
            for method in (method for method in tool.all_methods(bench) if method.name == 'TypeBasedFuzzer'):
                for size in [7, 100, 1000, 10000]:
                    os.environ['PICKNEXTFUEL'] = str(size)
                    print(f'Running {variant.name} {property} with size {size}...')
                    file = f'{size:02},{bench.name},{method.name},{variant.name},{property}'
                    cfg = TrialConfig(bench=bench,
                                      method=method.name,
                                      property="test_" + property,
                                      label=f'{method.name}{size}',
                                      trials=10,
                                      timeout=60,
                                      file=file
                                      )
                    run_trial(cfg)


## Part 2: STLC

benches = (bench for bench in tool.all_benches() if bench.name in ['STLC'])

for bench in benches:

    tool._preprocess(bench)
    variants = tool.all_variants(bench)
    variants.remove(next(variant for variant in variants if variant.name == 'base'))
    properties = tool.all_properties(bench)
    methods = list(method for method in tool.all_methods(bench) if method.name == 'TypeBasedFuzzer')


    finished = set(os.listdir(RESULTS))
    all_tasks = set(map(lambda vpm: f"{bench.name},{vpm[2].name},{vpm[0].name},test_{vpm[1]}.json", itertools.product(variants, properties, methods)))
    remaining_tasks = all_tasks - finished
    remaining_variants = list(set(map(lambda e: e.split(".json")[0].split(",")[2], remaining_tasks)))

    for variant in (variant for variant in tool.all_variants(bench) if (variant.name in remaining_variants)):
        run_trial = tool.apply_variant(bench, variant, no_base=True)
        for property in (property for property in tool.all_properties(bench)):
            print(f'Running {variant.name} {property}...')
            for method in (method for method in tool.all_methods(bench) if method.name == 'TypeBasedFuzzer'):
                for size in [7, 100, 1000, 10000]:
                    os.environ['PICKNEXTFUEL'] = str(size)
                    print(f'Running {variant.name} {property} with size {size}...')
                    file = f'{size:02},{bench.name},{method.name},{variant.name},{property}'
                    cfg = TrialConfig(bench=bench,
                                      method=method.name,
                                      property="test_" + property,
                                      label=f'{method.name}{size}',
                                      trials=10,
                                      timeout=60,
                                      file=file
                                      )
                    run_trial(cfg)

## Part 3: IFC

# benches = (bench for bench in tool.all_benches() if bench.name in ['IFC'])

# for bench in benches:

#     tool._preprocess(bench)
#     variants = tool.all_variants(bench)
#     variants.remove(next(variant for variant in variants if variant.name == 'base'))
#     properties = ['propSSNI_smart']
#     methods = list(method for method in tool.all_methods(bench) if method.name in ['TypeBasedFuzzer', 'Variational Fuzzer'])


#     finished = set(os.listdir(RESULTS))
#     all_tasks = set(map(lambda vpm: f"{bench.name},{vpm[2].name},{vpm[0].name},test_{vpm[1]}.json", itertools.product(variants, properties, methods)))
#     remaining_tasks = all_tasks - finished
#     remaining_variants = list(set(map(lambda e: e.split(".json")[0].split(",")[2], remaining_tasks)))

#     for variant in (variant for variant in tool.all_variants(bench) if (variant.name in remaining_variants)):
#         run_trial = tool.apply_variant(bench, variant, no_base=True)
#         for property in properties:
#             print(f'Running {variant.name} {property}...')
#             for method in methods:
#                 cfg = TrialConfig(bench=bench,
#                                 method=method.name,
#                                 label=method.name,
#                                 property="test_" + property,
#                                 trials=10,
#                                 timeout=60)
#                 run_trial(cfg)

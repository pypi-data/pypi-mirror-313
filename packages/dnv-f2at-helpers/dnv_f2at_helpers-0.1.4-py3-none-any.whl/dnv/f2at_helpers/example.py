"""
Script to test the f2at_helpers module
"""
import json
import asyncio
import os
from pathlib import Path
import pandas
import dnv.f2at_helpers.f2at_helpers as f2at_helpers
from dnv.onecompute import Environment


async def run_f2at():
    """
    Run an F²AT calculation
    """
    input_file = Path(os.path.realpath(__file__)).parent \
        / '../../../tests' / 'simple-with-damping.json'

    with open(input_file, 'r', encoding='utf8') as f:
        input_data = json.load(f)

    results = await f2at_helpers.run_f2at_async(input_data)
    along_pile = pandas.DataFrame(results['results_along_the_pile'])
    print(f'Results along the pile\n{along_pile.head()}')

    result_file = str(input_file).replace(".json", "-pisa-results.json")
    with open(result_file, 'w', encoding='utf8') as f:
        json.dump(results, f)


async def run_calibration():
    """
    Run a Splice calibration
    """
    input_file = Path(os.path.realpath(__file__)).parent \
        / '../../../tests' / 'simple-with-damping.json'
    pisa_file = Path(os.path.realpath(__file__)).parent \
        / '../../../tests' / 'simple-with-damping-pisa-results.json'

    with open(input_file, 'r', encoding='utf8') as f:
        input_data = json.load(f)

    with open(pisa_file, 'r', encoding='utf8') as f:
        pisa_results = json.load(f)

    results = await f2at_helpers.run_f2at_splice_calibration_async(
        input_data,
        pisa_results,
        environment=Environment.Testing)

    print(results)


if __name__ == '__main__':
    #asyncio.run(run_f2at())
    asyncio.run(run_calibration())

from typing import Union
import json

from Supplychain.Run.helpers import select_csv_or_amqp_consumers
from Supplychain.Wrappers.simulator import CosmoEngine, set_log_level


def run_simple_simulation(simulation_name: str,
                          simulation_path: str = 'Simulation',
                          amqp_consumer_adress: Union[str, None] = None,
                          modifications: Union[dict, None] = None,
                          output_dir: Union[str, None] = None,
                          log_level: Union[str, None] = None) -> bool:
    simulator = CosmoEngine.LoadSimulator(simulation_path)

    set_log_level(CosmoEngine, log_level)

    if modifications:
        for datapath, stringvalue in modifications.items():
            valuetoset = stringvalue if isinstance(stringvalue, str) else json.dumps(stringvalue)
            simulator.FindAttribute(datapath).SetAsString(valuetoset)

    select_csv_or_amqp_consumers(
        simulation_name=simulation_name,
        simulator=simulator,
        output_dir=output_dir,
        amqp_consumer_adress=amqp_consumer_adress,
    )

    # Run simulation
    simulator.Run()
    return simulator.IsFinished()

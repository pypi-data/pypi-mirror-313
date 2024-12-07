from typing import Union
from copy import deepcopy

import pandas
import comets as co
import numpy as np

from Supplychain.Wrappers.simulator import CosmoEngine
from Supplychain.Generic.adx_and_file_writer import ADXAndFileWriter
from Supplychain.Generic.timer import Timer
from Supplychain.Run.simulation import run_simple_simulation
from Supplychain.Run.consumers import (
    StockConsumer,
    PerformanceConsumer,
    StocksAtEndOfSimulationConsumer,
)
from Supplychain.Run.uncertainty_analysis_helper_functions import (
    get_max_time_step,
    get_attribute,
    get_stocks,
    get_transports,
    collect_transport_information,
    extend_dic,
    add_tag_to_parameterset,
    collect_simulated_stock_final_output,
    collect_simulated_stock_output,
    collect_simulated_transport_output,
    transform_data,
    transform_performances_data,
    create_transport_distribution_sampling,
    create_demand_generator,
)
from Supplychain.Schema.default_values import parameters_default_values

default_parameters = {
    "simulation_name": "Default Simulation",
    "simulation_path": "Simulation",
    "sample_size": parameters_default_values["Configuration"]["FinalSampleSizeUncertaintyAnalysis"],
    "batch_size": 100,
    "amqp_consumer_adress": None,
    "consumers": parameters_default_values["Configuration"]["UncertaintyAnalysisOutputData"],
    "validation_folder": None,
    "cold_inputs": {},
    "timer": None,
    "n_jobs": parameters_default_values["Configuration"]["MaxNumberOfSimInParallel"],
    "seed": parameters_default_values["Configuration"]["UncertaintyAnalysisSeed"],
    "adx_writer": None,
    "output_dir": None,
}


class UncertaintyAnalyzer:
    """
    Object in charge of performing the different steps of the uncertainty analysis.
    Its main method is "execute".

    Args:
        simulation_name (str): Name of simulation, used by the probes
        simulation_path (str): Name of the simulation file (typically Simulation)
        sample_size (int): Number of simulations runs by the uncertainty analysis
        batch_size (int): Number of simulations runs that are run in a same batch by the uncertainty analysis
        amqp_consumer_adress (Union[str, None], optional): Adress of consumer to send probe results to.
        consumers (list, optional): Which consumers are activated.
        validation_folder (str, optional): Local folder to which results are written to, used by the tests.
        cold_inputs (dict, optional): Parameters that are passed to the simulator at each simulation and don't change during the analysis.
        timer (Timer object, optional): Timer object that can be used for logs and counting time.
    """

    def __init__(
        self,
        simulation_name=default_parameters["simulation_name"],
        simulation_path=default_parameters["simulation_path"],
        sample_size=default_parameters["sample_size"],
        batch_size=default_parameters["batch_size"],
        amqp_consumer_adress=default_parameters["amqp_consumer_adress"],
        consumers=default_parameters["consumers"],
        validation_folder=default_parameters["validation_folder"],
        cold_inputs=default_parameters["cold_inputs"],
        timer=default_parameters["timer"],
        n_jobs=default_parameters["n_jobs"],
        seed=default_parameters["seed"],
    ):
        if timer is None:
            self.t = Timer("[Run Uncertainty]")
        else:
            self.t = timer
        self.simulation_name = simulation_name
        self.simulation_path = simulation_path
        self.amqp_consumer_adress = amqp_consumer_adress
        self.sample_size = sample_size
        self.batch_size = batch_size
        self.validation_folder = validation_folder
        if amqp_consumer_adress is None and "PerformanceAMQP" in consumers:
            consumers.remove("PerformanceAMQP")
        self.consumers = consumers
        self.cold_inputs = cold_inputs
        self.seed = seed
        if self.batch_size > self.sample_size:
            self.batch_size = self.sample_size

        self.n_jobs = n_jobs

    def execute(self):
        """Setup and run the uncertainty analysis

        Returns:
            dict: dictionary with keys among the non AMQP consumers
                containing the output tables. Which table is available depends on the specified
                consumers of the UncertaintyAnalyzer.
        """
        self.t.split("Initialize uncertainty analysis")
        self.initialize_simulator_interface()
        self.collect_simulation_parameters()
        self.create_encoder()
        self.create_get_outcomes()
        self.create_sampling()
        self.create_task(self.cold_inputs)
        self.t.split(
            "Ended uncertainty analysis initialization : {time_since_last_split}"
        )

        self.t.display_message("Run uncertainty analysis")
        self.run_experiment()
        self.t.split("Ended uncertainty analysis run : {time_since_last_split}")

        self.t.display_message("Reformat uncertainty analysis results")
        self.reformat_results()
        if self.validation_folder:
            self.write_results_locally()
        self.t.split(
            "Ended uncertainty analysis reformatting : {time_since_last_split}"
        )

        return self.results

    def initialize_simulator_interface(self):
        used_probes = []
        used_consumers = []
        custom_consumers = []

        if "Stocks" in self.consumers:
            used_probes.append("Stocks")
            custom_consumers.append((StockConsumer, "LocalConsumer", "Stocks"))
        if "StocksAtEndOfSimulation" in self.consumers:
            used_probes.append("StocksAtEndOfSimulation")
            custom_consumers.append(
                (StocksAtEndOfSimulationConsumer, "StocksAtEndOfSimulationConsumer", "StocksAtEndOfSimulation")
            )
        if "Performances" in self.consumers:
            used_probes.append("PerformanceIndicators")
            custom_consumers.append(
                (
                    PerformanceConsumer,
                    "LocalPerformanceConsumer",
                    "PerformanceIndicators",
                )
            )
        if "PerformanceAMQP" in self.consumers:
            used_consumers.append("PerformanceIndicatorsAMQP")

        self.simulator_interface = co.CosmoInterface(
            simulator_path=self.simulation_path,
            custom_sim_engine=CosmoEngine,
            simulation_name=self.simulation_name,
            amqp_consumer_address=self.amqp_consumer_adress,
            used_consumers=used_consumers,
            used_probes=used_probes,
            custom_consumers=custom_consumers,
            use_clone=(self.n_jobs == 1),
            controlPlaneTopic=("PerformanceAMQP" in self.consumers)  # Prevent the SDK from sending any data to ADX when not required
        )

    def collect_simulation_parameters(self):
        """
        Collect values of attributes of the model
        Used to retrieve the probability distribution parameters, the theoretical transport duration, etc...
        """
        # Load simulator to be able to access attributes of the model
        self.simulator_interface.initialize()

        # Retrieving model information
        self.max_time_step = get_max_time_step(self.simulator_interface)
        self.ActivateCorrelatedDemandUncertainties = get_attribute(
            self.simulator_interface, "Model::@ActivateCorrelatedDemandUncertainties"
        )
        self.DemandCorrelations = get_attribute(
            self.simulator_interface, "Model::@DemandCorrelations"
        )
        self.transport_distribution = get_attribute(
            self.simulator_interface,
            "Model::@TransportUncertaintiesProbabilityDistribution",
        )
        self.ActivateUncertainties = get_attribute(
            self.simulator_interface,
            "Model::@ActivateUncertainties",
        )
        self.SubDataset = get_attribute(
            self.simulator_interface,
            "Model::@SubDataset",
        )

        # Getting the name of all the stocks with uncertain demand
        if self.ActivateCorrelatedDemandUncertainties:
            self.uncertain_stocks = get_stocks(self.simulator_interface)
        else:
            self.uncertain_stocks = []

        # Getting the name of all the transport operations
        self.all_transports = get_transports(self.simulator_interface)

        # Collect information about transports:
        # which transport have uncertain durations, what are the schedule for the theoretical transport duration
        # and for the parameters of the probability distribution
        (
            self.transports_with_uncertain_duration,
            self.actual_duration_schedule,
            uncertainty_param_1,
            uncertainty_param_2,
            uncertainty_param_3,
            uncertainty_param_4,
        ) = collect_transport_information(self.simulator_interface, self.all_transports)

        # Collect model information about demands of each stock
        demands = {}
        for stock in self.uncertain_stocks:
            demands[stock] = get_attribute(
                self.simulator_interface,
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{stock}::@Demand",
            )

        self.simulator_interface.terminate(remove_sim_clone=True)
        self.transport_distribution_params = co.DistributionRegistry.information[
            str(self.transport_distribution)
        ]["parameters"]

        # Extending the dictionaries above for scheduled attributes so that all time steps are present
        self.extended_actual_duration = extend_dic(
            self.actual_duration_schedule, self.max_time_step
        )
        self.extended_param_1 = extend_dic(uncertainty_param_1, self.max_time_step)
        self.extended_param_2 = extend_dic(uncertainty_param_2, self.max_time_step)
        self.extended_param_3 = extend_dic(uncertainty_param_3, self.max_time_step)
        self.extended_param_4 = extend_dic(uncertainty_param_4, self.max_time_step)
        self.extended_demands = extend_dic(demands, self.max_time_step)

        if not self.ActivateUncertainties:
            # Remove uncertain transports and stocks if ActivateUncertainties is false
            self.transports_with_uncertain_duration = []
            self.uncertain_stocks = []

    def create_encoder(self):
        """Create encoder of the task"""

        def encoder(
            parameters,
            extended_demands=self.extended_demands,
            transports_with_uncertain_duration=self.transports_with_uncertain_duration,
            extended_actual_duration=self.extended_actual_duration,
            uncertain_stocks=self.uncertain_stocks,
            max_time_step=self.max_time_step,
        ):
            """
            The encoder takes a parameterset containing the input parameters that are changing at each simulation.
            It has the following format :
            {'{Model} [..] Seed': 3251851028, 'T_@_0': 1.7504164949122698, 'T_@_1': 3.05256524351985, [...],
            'T_@_10': 3.2371899035525793, 'StockA':[1.1, 2., ..., 3.4]}
            The parameters correspond either to:
            - the Seed datapath and its value
            - transport_name +_@_ + time_step, and the duration of this transport at this time step
            - stock_name, and a list of demands for this stock
            It returns a parameterset where the keys are datapaths in the model.
            The values for each transport's duration is transformed in one dictionary {TimeStep: value} and updated as follows:
            new_transport_duration = max(0, round(old_transport_duration +
                sample input drawn from the distribution))
            The values for each stock's demand is set to its ExternalDemand in the attribute Demand, which is a dictionary
            {TimeStep: Composite attribute}.
            {'Model [..] T::@ActualDurationSchedule': {'0': 5, '1': 6, [..] '10': 44},
                '{Model}Model::{Attribute}Seed': 3209521878, ...}
            """
            encoded_parameterset = {}
            if "{Model}Model::{Attribute}Seed" in parameters:
                encoded_parameterset = {
                    "{Model}Model::{Attribute}Seed": parameters[
                        "{Model}Model::{Attribute}Seed"
                    ],
                }
            for transports in transports_with_uncertain_duration:
                ActualDurationSchedule = {}
                for i in range(len(extended_actual_duration[transports])):
                    ActualDurationSchedule[str(i)] = max(
                        0,
                        round(
                            extended_actual_duration[transports][i]
                            + parameters[f"{transports}_@_{i}"]
                        ),
                    )
                encoded_parameterset[
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transports}::@ActualDurationSchedule"
                ] = ActualDurationSchedule
            for stock in uncertain_stocks:
                sample_demand = parameters[f"{stock}"]
                demand_attribute = deepcopy(extended_demands[f"{stock}"])
                for i in range(max_time_step):
                    demand_attribute[i]["ExternalDemand"] = sample_demand[i]
                encoded_parameterset[
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{stock}::@Demand"
                ] = demand_attribute
            return encoded_parameterset

        self.encoder = encoder

    def create_get_outcomes(self):
        """Create the get_outcomes function of the task"""

        def get_outcomes(
            modelinterface,
            consumers=self.consumers,
            all_transports=self.all_transports,
            max_time_step=self.max_time_step,
        ):
            """
            Returns a parameter set with all the model's output. More precisely, the parameter set is the
            the result of the concatenation of up to four parameter sets, depending on the consumers that have been chosen.
            In front of the name of each parameter, we add a '1_', '2_', '3_' or '4_' to identify the 4 original parametersets.
            The first one looks like this:
            {'1_U__&@&__0': 5, '1_U__&@&__1': 5, [...], '1_U__&@&__10': 6}.
            The keys correspond to transport_name + __&@&__ + time_step,
            and the value to the duration of the transport at this time step.
            The second parameter set looks like this:
            {'2_A__&@&__ServedQuantity__&@&__0': 0.0, '2_A__&@&__UnservedQuantity__&@&__0': 0.0}.
            The keys correspond to stock + __&@&__ + category (Demand, ServedQuantity,...)  + __&@&__ +  time_step
            The third parameter set contains the performance indicators {'3_OPEX': 0.0, '3_Profit': 1.0, ...}.
            The fourth parameter set looks like:
            {'4_A__&@&__TotalDemand': 1.0}.
            The keys correspond to stock name + __&@&__ + category (TotalDemand, TotalServedQuantity, OnTimeAndInLateFillRateServiceLevel, CycleServiceLevel)
            """

            output_parameterset = {}
            if "Transports" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "1_",
                        collect_simulated_transport_output(
                            all_transports, modelinterface, max_time_step
                        ),
                    )
                )
            if "Stocks" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "2_",
                        collect_simulated_stock_output(
                            modelinterface.LocalConsumer.memory
                        ),
                    )
                )
            if "Performances" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "3_", modelinterface.LocalPerformanceConsumer.memory[0]
                    )
                )
            if "StocksAtEndOfSimulation" in consumers:
                output_parameterset.update(
                    add_tag_to_parameterset(
                        "4_",
                        collect_simulated_stock_final_output(
                            modelinterface.StocksAtEndOfSimulationConsumer.memory
                        ),
                    )
                )
            return output_parameterset

        self.get_outcomes = get_outcomes

    def create_sampling(self):
        """Create the sampling of the uncertainty analysis"""
        # Creating the sampling on transport durations
        self.sampling = create_transport_distribution_sampling(
            self.transport_distribution,
            self.extended_param_1,
            self.extended_param_2,
            self.extended_param_3,
            self.extended_param_4,
            self.transports_with_uncertain_duration,
            self.transport_distribution_params,
            self.max_time_step,
        )
        # Add the seed as an uncertain parameter
        self.sampling.append(
            {
                "name": "{Model}Model::{Attribute}Seed",
                "sampling": "seed_generator",
            }
        )

        # Add the generator of samples on the demand
        if self.ActivateCorrelatedDemandUncertainties:
            self.sampling += create_demand_generator(
                self.extended_demands, self.max_time_step, self.DemandCorrelations
            )

    def create_task(self, cold_inputs={}):
        """Create the task on which the uncertainty analysis will be performed

        Args:
            cold_inputs (dict): ParameterSet containing parameters of the simulator
                that will be applied to each evaluation of the task.
                Allows to modify other attributes than those modified by the uncertainty analysis.
        """
        if (
            self.ActivateCorrelatedDemandUncertainties
        ):  # Correlated demands are not compatible with demands drawn inside the model
            cold_input_parameter_set = {
                "{Model}Model::{Attribute}ActivateUncertainties": 0
            }
        else:
            cold_input_parameter_set = {}

        cold_input_parameter_set.update(cold_inputs)

        self.simulationtask = co.ModelTask(
            modelinterface=self.simulator_interface,
            encode=self.encoder,
            get_outcomes=self.get_outcomes,
            cold_input_parameter_set=cold_input_parameter_set,
        )

    def run_experiment(self):
        """Create and run the uncertainty analysis experiment"""
        if self.validation_folder is not None:
            save_task_history = True
        else:
            save_task_history = False

        if self.seed == -1:
            np.random.seed()
        else:
            np.random.seed(self.seed)

        self.experiment = co.UncertaintyAnalysis(
            task=self.simulationtask,
            sampling=self.sampling,
            stop_criteria={"max_evaluations": self.sample_size},
            analyzer=["standard", "quantiles"],
            n_jobs=self.n_jobs,
            save_task_history=save_task_history,
        )

        self.experiment.run()

    def reformat_results(self):
        """Reformat results of the experiment so that they are compatible with the output tables"""
        self.results = {}
        # Separating the results data on the different types of outputs (stock, transport, performances, stocksatendofsimulation)
        self.experiment.results["statistics"].reset_index(inplace=True)
        self.experiment.results["statistics"]["OutputType"] = (
            self.experiment.results["statistics"]["index"]
            .str.split(pat="_", expand=False, n=1)
            .str[0]
        )
        self.experiment.results["statistics"]["index"] = (
            self.experiment.results["statistics"]["index"]
            .str.split(pat="_", expand=False, n=1)
            .str[1]
        )
        if "Transports" in self.consumers:
            df_transport_duration = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "1"
            ]
            df_transport_duration = df_transport_duration.drop("OutputType", axis=1)
            df_transport_final = transform_data(df_transport_duration)
            self.results["Transports"] = df_transport_final
        if "Stocks" in self.consumers:
            df_probe_data = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "2"
            ]
            df_probe_data = df_probe_data.drop("OutputType", axis=1)
            df_stock_final = transform_data(df_probe_data)
            self.results["Stocks"] = df_stock_final
        if "Performances" in self.consumers:
            performances = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "3"
            ]
            performances = performances.drop("OutputType", axis=1)
            performances = transform_performances_data(performances)
            performances["SubDataset"] = self.SubDataset
            self.results["Performances"] = performances
        if "StocksAtEndOfSimulation" in self.consumers:
            df_stocksatendofsimulationconsumer = self.experiment.results["statistics"][
                self.experiment.results["statistics"]["OutputType"] == "4"
            ]
            df_stocksatendofsimulationconsumer = df_stocksatendofsimulationconsumer.drop("OutputType", axis=1)
            df_stocksatendofsimulationconsumer = transform_data(df_stocksatendofsimulationconsumer, timestep=False)
            self.results["StocksAtEndOfSimulation"] = df_stocksatendofsimulationconsumer

    def write_results_locally(self):
        """Write the results tables locally to csv files"""

        # Get all demands directly from the experiment, before aggregation of statistics
        demands = []
        j = 0
        for i in self.experiment.task_history["outputs"]:

            for (k, v) in i.items():
                if "__&@&__Demand__&@&__" in k:
                    demand_result_dict = {}
                    demand_result_dict["Simulation"] = j
                    demand_result_dict["Entity"] = k.split("__&@&__Demand__&@&__")[
                        0
                    ].split("_", 1)[1]
                    demand_result_dict["TimeStep"] = k.split("__&@&__Demand__&@&__")[1]
                    demand_result_dict["Demand"] = v

                    demands.append(demand_result_dict)
            j += 1
        demand_df = pandas.DataFrame(demands)
        demand_df.to_csv(
            str(self.validation_folder) + "/df_all_demands.csv", index=False
        )
        self.results["Stocks"].to_csv(
            str(self.validation_folder) + "/final_df_comets.csv", index=False
        )
        self.results["StocksAtEndOfSimulation"].to_csv(
            str(self.validation_folder) + "/df_stocksatendofsimulation.csv", index=False
        )
        self.results["Transports"].to_csv(
            str(self.validation_folder) + "/df_transport.csv", index=False
        )
        self.results["Performances"].to_csv(
            str(self.validation_folder) + "/df_performances.csv", index=False
        )


def uncertainty_analysis(
    simulation_name: str = default_parameters["simulation_name"],
    simulation_path: str = default_parameters["simulation_path"],
    amqp_consumer_adress: Union[str, None] = default_parameters["amqp_consumer_adress"],
    sample_size: int = default_parameters["sample_size"],
    batch_size: int = default_parameters["batch_size"],
    n_jobs: int = default_parameters["n_jobs"],
    adx_writer: Union[ADXAndFileWriter, None] = default_parameters["adx_writer"],
    validation_folder: Union[str, None] = default_parameters["validation_folder"],
    cold_inputs: dict = default_parameters["cold_inputs"],  # Additional parameters that might be passed to the simulator at each task evaluation
    output_dir: Union[str, None] = default_parameters["output_dir"],
    seed: int = default_parameters["seed"],
    consumers: list = default_parameters["consumers"],
):

    with Timer("[Run Uncertainty Analysis]") as t:

        ua = UncertaintyAnalyzer(
            simulation_name=simulation_name,
            simulation_path=simulation_path,
            amqp_consumer_adress=amqp_consumer_adress,
            sample_size=sample_size,
            batch_size=batch_size,
            n_jobs=n_jobs,
            validation_folder=validation_folder,
            consumers=consumers,
            cold_inputs=cold_inputs,
            timer=t,
            seed=seed,
        )

        results = ua.execute()

        if adx_writer is not None:
            t.split("Sending stats to ADX")
            if "Performances" in consumers:
                performances_df = results["Performances"]
                renaming = {
                    "KPI": "Category",
                    "mean": "Mean",
                    "sem": "SE",
                    "std": "STD",
                    "confidence interval of the mean at 95%": "CI95",
                }
                for i in range(5, 100, 5):
                    renaming[f"quantile {i}%"] = "Percentile{i}"
                performances_df = performances_df.rename(columns=renaming)
            result_names = [
                ("Stocks", "StockUncertaintyStatistics"),
                ("StocksAtEndOfSimulation", "StocksAtEndOfSimulationUncertaintyStatistics"),
                ("Transports", "TransportUncertaintyStatistics"),
                ("Performances", "PerformanceIndicatorUncertaintyStatistics"),
            ]
            for consumer, table in result_names:
                if consumer in consumers:
                    adx_writer.write_target_file(results[consumer].to_dict("records"), table)

            t.split("Sent stats to ADX : {time_since_last_split}")

        t.display_message("Running simple simulation to fill ADX")
        # Put back log level to Info for final simulation
        # Reduce log level to Error during optimization
        logger = CosmoEngine.LoggerManager.GetInstance().GetLogger()
        logger.SetLogLevel(logger.eInfo)

        stop_uncertainty = {"Model::@ActivateUncertainties": "false"}

        run_simple_simulation(
            simulation_name=simulation_name,
            simulation_path=simulation_path,
            amqp_consumer_adress=amqp_consumer_adress,
            modifications=stop_uncertainty,
            output_dir=output_dir,
        )
        t.split("Final simulation succeeded : {time_since_last_split}")

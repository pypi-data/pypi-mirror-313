from copy import deepcopy
import comets as co
from Supplychain.Wrappers.simulator import CosmoEngine
from Supplychain.Wrappers.environment_variables import EnvironmentVariables

"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
Helper functions used in the uncertainty analysis
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""


"""
-------------------------------------------------
Simple helper functions
-------------------------------------------------
"""


def extend_simple_dic(my_dic, number_of_iterations):
    """Function to extend dictionaries of schedulable attributes.

    Args:
        my_dic (dict): dictionary of scheduled values such as {0: 3, 6: 4, 7: 3, 8: 2, 9: 8, 10: 40}
        number_of_iterations (int): total number of time steps of the schedule

    Returns:
        dict: extended dictionary for all time steps {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 4, 7: 3, 8: 2, 9: 8, 10: 40}
    """
    if my_dic != {}:  # checking that the dic isn't empty
        extended_dic = {
            0: my_dic[0]
        }  # We assume that the uncertainty starts at the first time step
        for i in range(1, number_of_iterations):
            if i in my_dic:
                extended_dic[i] = deepcopy(my_dic[i])
            else:
                extended_dic[i] = deepcopy(extended_dic[i - 1])
    else:
        extended_dic = {}
    return extended_dic


def extend_dic(my_dic, number_of_iterations):
    """Function to extend dictionaries of schedulable attributes.

    Args:
        my_dic (dict): dictionary of dictionary of scheduled values
        number_of_iterations (int): total number of time steps of the schedule

    Returns:
        dict: dictionary containing extended dictionary for all time steps
    """
    extended_dic = {}
    for entity in my_dic.keys():
        extended_dic[entity] = extend_simple_dic(my_dic[entity], number_of_iterations)
    return extended_dic


def add_tag(tag, name):
    return tag + name


def add_tag_to_parameterset(tag, parameterset):
    """Add string tag in front of the keys of a parameterset"""
    return {add_tag(tag, key): value for key, value in parameterset.items()}


def check_distrib_parameters(my_distribution, param1, param2, param3, param4):
    """Transform distribution parameters that don't match CoMETS format

    Args:
        my_distribution (str): name of distribution
        param1 (float): dictionary of values for first parameter
        param2 (float): dictionary of values for second parameter
        param3 (float): dictionary of values for third parameter
        param4 (float): dictionary of values for fourth parameter

    Returns:
        list: list containing dictionaries with modified values for param1, 2, 3 and 4
    """
    # In CoMETS the upper bound of the discreteuniform distribution is excluded.
    # However, in supply chain it is included. Therefore, we need to add 1 to the upper bound
    # so it matches CoMETS
    if my_distribution == "discreteuniform":
        for entity in param2.keys():
            for keys in param2[entity].keys():
                param2[entity][keys] += 1

    # In CoMETS the two arguments of the uniform distribution are loc and scale
    # and the interval of the distribution is the following:  [loc, loc+scale]
    # However, in supply chain the two parameters of the uniform distribution are
    # [lower, upper]. Therefor, upper needs to be mapped to scale
    if my_distribution == "uniform":
        for entity in param2.keys():
            for keys in param2[entity].keys():
                param2[entity][keys] = param2[entity][keys] - param1[entity][keys]

    if my_distribution == "betabinom":
        for entity in param1.keys():
            for keys in param1[entity].keys():
                param1[entity][keys] = round(param1[entity][keys])

    if my_distribution == "binomial":
        for entity in param1.keys():
            for keys in param1[entity].keys():
                param1[entity][keys] = round(param1[entity][keys])

    if my_distribution == "hypergeom":
        for entity in param1.keys():
            for keys in param1[entity].keys():
                param1[entity][keys] = round(param1[entity][keys])
                param2[entity][keys] = round(param2[entity][keys])
                param3[entity][keys] = round(param3[entity][keys])

    return [param1, param2, param3, param4]


"""
-------------------------------------------------
Functions that collect simulator attributes before the analysis
-------------------------------------------------
"""


def get_transports(cosmo_interface):
    """Function to get the list of all the transports in the simulation"""
    transports_list = []
    transports = cosmo_interface.sim.get_entities_names_by_type(
        entity_type="TransportOperation"
    )
    for keys in transports:
        transports_list.append(keys)
    return transports_list


def get_stocks(cosmo_interface):
    """Function to get the list of all the stocks that have uncertain demand"""
    uncertain_stocks = []
    for stock in cosmo_interface.sim.get_entities_by_type("Stock"):
        demands = CosmoEngine.DataTypeMapInterface.Cast(stock.GetAttribute("Demand"))
        stock_name = stock.GetName()
        for time_step in demands.GetKeys():
            demand = demands.GetAt(time_step)
            if demand.GetAttribute("DemandRelativeUncertainty").Get() > 0:
                uncertain_stocks.append(stock_name)
                break
    return uncertain_stocks


def get_attribute(cosmo_interface, attribute):
    """Get value of attribute in the model"""
    return cosmo_interface.get_outputs([attribute])[attribute]


def get_max_time_step(cosmo_interface):
    time_step_per_cycle = get_attribute(cosmo_interface, "Model::@TimeStepPerCycle")
    number_of_cycle = get_attribute(cosmo_interface, "Model::@NumberOfCycle")
    max_time_step = time_step_per_cycle * number_of_cycle
    return max_time_step


def collect_transport_information(cosmo_interface, transports_names):
    """Collect information regarding transports in the model:
    which transports have uncertain duration,
    what are the theoretical durations,
    what are the parameters of the probability distribution of transport duration for each transport.
    """
    list_of_transports = transports_names.copy()
    actual_duration_schedule = {}
    uncertainty_param_1 = {}
    uncertainty_param_2 = {}
    uncertainty_param_3 = {}
    uncertainty_param_4 = {}
    for transport in transports_names:

        # If their is no ActualDuration in the TransportSchedules column of the dataset,
        # we use by default the attribute duration, in the Transport column of the dataset.
        if (
            cosmo_interface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
                ]
            )[
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
            ]
            == {}
        ):
            duration = cosmo_interface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@Duration"
                ]
            )[f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@Duration"]

            # Use a dict format so that the function "extended_dict" defined below can be applied
            actual_duration_schedule[transport] = {0: duration}
        else:
            actual_duration_schedule[transport] = cosmo_interface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
                ]
            )[
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
            ]

        uncertainty_param_1[transport] = cosmo_interface.get_outputs(
            [
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter1"
            ]
        )[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter1"
        ]
        uncertainty_param_2[transport] = cosmo_interface.get_outputs(
            [
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter2"
            ]
        )[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter2"
        ]
        uncertainty_param_3[transport] = cosmo_interface.get_outputs(
            [
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter3"
            ]
        )[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter3"
        ]
        uncertainty_param_4[transport] = cosmo_interface.get_outputs(
            [
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter4"
            ]
        )[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@TransportUncertaintiesParameter4"
        ]
        # If the transport has no parameters, its transport duration will not be part of the uncertainty analysis
        if (
            uncertainty_param_1[transport] == uncertainty_param_2[transport]
            and uncertainty_param_1[transport] == {}
        ):
            list_of_transports.remove(transport)

    return (
        list_of_transports,
        actual_duration_schedule,
        uncertainty_param_1,
        uncertainty_param_2,
        uncertainty_param_3,
        uncertainty_param_4,
    )


"""
-------------------------------------------------
Functions that collect simulator outputs
-------------------------------------------------
"""


def collect_simulated_transport_output(transports_names, modelinterface, max_time_step):
    """
    Function that returns a parameterset with the transport duration for each transport at the end of the simulation
    The transport duration is separated for each time step. The output parameterset (for a simulation
    with 1 TransportOperation: U) will have the following format:
    {Model[...]U::@ActualDurationSchedule__&@&__0': 10,
           [...],
      Model[...]U::@ActualDurationSchedule__&@&__10': 7}
    """
    transport_duration = {}
    transport_duration_transformed = {}
    for transport in transports_names:
        if (
            modelinterface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
                ]
            )[
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
            ]
            == {}
        ):
            duration = modelinterface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@Duration"
                ]
            )[f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@Duration"]
            # Use a dict format so that the function "extend_dict" can be applied
            actual_duration_schedule = {0: duration}
        else:
            actual_duration_schedule = modelinterface.get_outputs(
                [
                    f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
                ]
            )[
                f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
            ]
        transport_duration[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
        ] = extend_simple_dic(
            actual_duration_schedule,
            max_time_step,
        )
        time_step = 0
        for value in transport_duration[
            f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{transport}::@ActualDurationSchedule"
        ].values():
            transport_duration_transformed[f"{transport}__&@&__ActualDuration__&@&__{time_step}"] = value
            time_step += 1
    return transport_duration_transformed


def collect_simulated_stock_output(consumer_memory):
    """
    This function transforms the consumer memory from a list of list to a dict of
    ParameterSet. Note that each sublist in the initial format is transformed into
    len(sublist) - 2 ParameterSets.
    """
    measures = (
      "Demand",
      "RemainingQuantity",
      "ServedQuantity",
      "UnservedQuantity",
      "OnTimeAndInLateFillRateServiceLevel",
      "Value",
      "OnTimeFillRateServiceLevel",
    )
    parametersets = {}
    for fact in consumer_memory:
        stock = fact[0]
        time_step = fact[1]
        for i, measure in enumerate(measures, 2):
            parametersets[f"{stock}__&@&__{measure}__&@&__{time_step}"] = fact[i]
    return parametersets


def collect_simulated_stock_final_output(consumer_memory):
    """
    This function transforms the consumer memory from a list of dict to a dict of
    ParameterSet, where one ParameterSet is used for each stock-measure.
    """
    return {
        f"{fact['id']}__&@&__{measure}": fact[measure]
        for fact in consumer_memory
        for measure in fact
        if measure != 'id'
    }


"""
-------------------------------------------------
Functions that create the uncertainty analysis "sampling"
-------------------------------------------------
"""


def create_transport_distribution_sampling(
    distribution,
    param1,
    param2,
    param3,
    param4,
    transports,
    distribution_parameters,
    number_of_time_steps,
):
    """
    Function to create the uncertainty analysis sampling for the transport durations according to CoMETS format
    This function will create one variable for each time step of each transports

    Args:
        distribution (str): name of the probability distribution used
        param1 (float): values by transport by time step for the first parameter of the distribution
        param2 (float): values by transport by time step for the second parameter of the distribution
        param3 (float): values by transport by time step for the third parameter of the distribution
        param4 (float): values by transport by time step for the fourth parameter of the distribution
        transports (list):list of all the uncertain transports names
        distribution_parameters (str): list of the parameters names required by CoMETS sampler for the given distribution
        number_of_time_steps (int): number of simulated time steps


    Returns:
        list: list of sampling variables according to CoMETS format
    """
    sampling = []
    all_parameters = check_distrib_parameters(
        distribution, param1, param2, param3, param4
    )
    for transport in transports:
        considered_parameters = [
            (position, parameter)
            for position, parameter in enumerate(distribution_parameters)
            if all_parameters[position][transport]
        ]
        for t in range(number_of_time_steps):
            parameters = {
                parameter: all_parameters[position][transport][t]
                for position, parameter in considered_parameters
            }
            sampling.append(
                {
                    "name": f"{transport}_@_{t}",
                    "sampling": distribution,
                    "parameters": parameters,
                }
            )
    return sampling


def create_demand_generator(extended_demands, number_of_time_steps, DemandCorrelations):
    """Function to create the uncertainty analysis sampling for the demands according to CoMETS format.
    Defines a generator of uncertain time series for each stock.

    Args:
        extended_demands (dict): Demand attributes obtained from the simulator
        number_of_time_steps (int): _description_
        DemandCorrelations (float): amount of correlation between consecutive time steps

    Returns:
        list: list of sampling variables according to CoMETS format
    """
    sampling = []
    for stock, demand_attribute in extended_demands.items():
        mean_demand = []
        uncertainties = []
        for t in range(number_of_time_steps):

            demand = demand_attribute[t]["ExternalDemand"]
            mean_demand.append(demand)
            uncertainties.append(
                demand * demand_attribute[t]["DemandRelativeUncertainty"]
            )  # Uncertainty proportional to demand, DemandRelativeUncertainty*Demand is the standard deviation
        sampling.append(
            {
                "name": f"{stock}",
                "sampling": co.TimeSeriesSampler(
                    correlation=DemandCorrelations,
                    dimension=number_of_time_steps,
                    forecast=mean_demand,
                    uncertainties=uncertainties,
                    minimum=0,
                ),
            }
        )
    return sampling


"""
-------------------------------------------------
Functions that reformat the outputs of the uncertainty analysis
-------------------------------------------------
"""


def transform_data(data, timestep=True):
    """
    Transform output data so that it matches the ADX table format
    """
    df = data.copy()
    index_cols = [
        "id",
        "Category",
        "TimeStep"
    ]
    if not timestep:
        index_cols.remove("TimeStep")
    if not df.empty:
        df.loc[:, "SimulationRun"] = EnvironmentVariables.simulation_id
        df[index_cols] = df["index"].str.split(pat="__&@&__", expand=True)
    else:
        index_cols.insert(0, "SimulationRun")
        df[index_cols] = None
    cols = [
        "SimulationRun",
        "TimeStep",
        "id",
        "Category",
        "quantile 5%",
        "quantile 25%",
        "quantile 50%",
        "quantile 75%",
        "quantile 95%",
        "mean",
        "sem",
    ]
    if not timestep:
        cols.remove("TimeStep")
    df = df[cols]
    df.rename(
        columns={
            "quantile 5%": "FirstVigintile",
            "quantile 25%": "FirstQuartile",
            "quantile 50%": "Median",
            "quantile 75%": "LastQuartile",
            "quantile 95%": "LastVigintile",
            "mean": "Mean",
            "sem": "SE",
        },
        inplace=True,
    )
    return df


def transform_performances_data(data):
    """
    Transform output data so that it matches the ADX table format
    """
    df = data.copy()
    df.loc[:, "SimulationRun"] = EnvironmentVariables.simulation_id
    cols = [
        "SimulationRun",
        "index",
        "quantile 5%",
        "quantile 10%",
        "quantile 15%",
        "quantile 20%",
        "quantile 25%",
        "quantile 30%",
        "quantile 35%",
        "quantile 40%",
        "quantile 45%",
        "quantile 50%",
        "quantile 55%",
        "quantile 60%",
        "quantile 65%",
        "quantile 70%",
        "quantile 75%",
        "quantile 80%",
        "quantile 85%",
        "quantile 90%",
        "quantile 95%",
        "mean",
        "sem",
        "std",
        "confidence interval of the mean at 95%",
    ]
    df = df[cols]
    df = df.rename(columns={"index": "KPI"})
    return df

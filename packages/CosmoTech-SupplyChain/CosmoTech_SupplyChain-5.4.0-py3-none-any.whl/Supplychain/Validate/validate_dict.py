from Supplychain.Generic.folder_io import FolderReader
from Supplychain.Generic.timer import Timer
from Supplychain.Schema.validation_schemas import ValidationSchemas
from Supplychain.Schema.default_values import parameters_default_values

from collections import Counter

import itertools
import jsonschema


class DictValidator(Timer):

    def __init__(self,
                 reader: FolderReader,
                 run_type: str = "None"):
        Timer.__init__(self, prefix="[Validation]")

        self.reader = reader

        self.schema = ValidationSchemas()

        self.run_type = run_type

        self.errors = []

        self.lookup_memory = dict()

    def validate(self) -> bool:
        checks = [self.validate_files(), self.validate_graph(), self.specific_validations()]
        if all(checks):
            self.display_message("Dataset is valid")
            return True
        else:
            self.display_message("Dataset is invalid")
            return False

    def validate_graph(self) -> bool:
        self.errors = []
        self.display_message("Validate graph")
        for file_to_validate in sorted(self.schema.graph.keys()):
            self.__validate_graph(file_to_validate)
        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                self.display_message(f" - {filename}: {item_id}: {err}")
            return False
        self.__validate_acyclicity()
        if self.errors:
            self.display_message("1 error found in the files")
            self.display_message(self.errors[0])
            return False
        self.display_message("Graph is valid")
        return True

    def validate_files(self) -> bool:
        self.errors = []
        self.display_message("Validate file content")
        for file_to_validate in sorted(self.schema.schemas.keys()):
            self.__validate_file(file_to_validate)

        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                message = err.message.replace("{", "{{").replace("}", "}}")
                path = '/'.join(str(loc) for loc in err.path)
                self.display_message(f" - {filename}: {item_id}: {path}: {message}")
        else:
            self.display_message("Individual files are valid")
            return True
        return False

    def __validate_file(self, file_name: str):
        for item in self.reader.files[file_name]:
            validator = jsonschema.Draft7Validator(schema=self.schema.schemas[file_name])
            errors = validator.iter_errors(item)
            item_id = 0
            if "id" in item:
                item_id = item["id"]
            elif "Label" in item:  # TODO specific for relationship here transport (only Transport relationship is validated) to be replaced by RelationshipId when available from azure-digital-twins-simulator-connector
                item_id = item["Label"]
            elif 'source' in item or 'target' in item:
                item_id = item.get('source', "") + " -> " + item.get('target', "")
            for error in errors:
                self.errors.append((file_name, item_id, error))
        self.split(f"\t{file_name}" + ": {time_since_last_split:6.4f}s")

    def __validate_graph(self, file_name: str):
        config = self.schema.graph[file_name]
        source_file, source_id = config['links']['source']
        target_file, target_id = config['links']['target']

        source_entities = set(entity[source_id] for entity in self.reader.files[source_file])
        target_entities = set(entity[target_id] for entity in self.reader.files[target_file])

        arcs = [
            (arc[config['source']], arc[config['target']])
            for arc in self.reader.files[file_name]
        ]
        sources, targets = zip(*arcs) if arcs else ((), ())
        source_vertices = set(sources)
        target_vertices = set(targets)

        # Check relation existences
        for check, entities, vertices, entity_file in [
            (config['all_source_present'], source_entities, source_vertices, source_file),
            (config['all_target_present'], target_entities, target_vertices, target_file),
        ]:
            if check:
                if entities and not vertices:
                    self.errors.append((entity_file, 'all', f"have no relations in {file_name} which is empty"))
                else:
                    for entity in entities - vertices:
                        self.errors.append((entity_file, entity, f"has no relations in {file_name}"))

        # Check entity existences
        for entities, vertices, entity_file in [
            (source_entities, source_vertices, source_file),
            (target_entities, target_vertices, target_file),
        ]:
            if vertices and not entities:
                self.errors.append((file_name, 'all', f"do not exist in {entity_file} which is empty"))
            else:
                for vertex in vertices - entities:
                    self.errors.append((file_name, vertex, f"does not exist in {entity_file}"))

        # Check cardinalities
        indegree, outdegree = config['cardinalities'].split(':')
        for vertices, occurrences, cardinality, entity_file in [
            (source_vertices, sources, outdegree, source_file),
            (target_vertices, targets, indegree, target_file),
        ]:
            if cardinality == "1":
                for vertex in vertices:
                    if occurrences.count(vertex) > 1:
                        self.errors.append((entity_file, vertex, f"has more than one relation in {file_name}"))

        self.split(f"\t{file_name}" + ": {time_since_last_split:6.4f}s")

    def __validate_acyclicity(self):
        arcs_by_file_name = {
            file_name: [
                (i[config['source']], i[config['target']])
                for i in self.reader.files[file_name]
            ]
            for file_name, config in self.schema.graph.items()
        }
        arcs = [
            arc
            for arcs_of_file in arcs_by_file_name.values()
            for arc in arcs_of_file
        ]
        if arcs:
            vertices = set(itertools.chain(*arcs))
            targets_by_source = {
                vertex: set()
                for vertex in vertices
            }
            for source, target in arcs:
                targets_by_source[source].add(target)
            visited = set()
            loop = []

            def visit(vertex):
                if vertex in visited:
                    return False
                if vertex in loop:
                    loop.append(vertex)
                    return True
                vertices.discard(vertex)
                loop.append(vertex)
                for next_vertex in targets_by_source[vertex]:
                    if visit(next_vertex):
                        return True
                visited.add(loop.pop())

            while vertices:
                if visit(vertices.pop()):
                    break
            if loop:
                loop = loop[loop.index(loop[-1]):]
                vertex_types = []
                file_names = []
                for arc in zip(loop[:-1], loop[1:]):
                    for file_name, arcs_of_file in arcs_by_file_name.items():
                        if arc in arcs_of_file:
                            break
                    vertex_types.append(self.schema.graph[file_name]['links']['source'][0])
                    file_names.append(file_name)
                spacing = max(
                    max(map(len, vertex_types)),
                    max(map(len, file_names)) - 2,
                )
                vertex_types.append(vertex_types[0])
                sep = '\n\t'
                relations = [sep] + [
                    f'{file_name:>{spacing + 2}} ↓{sep}'
                    for file_name in file_names
                ]
                loop_links = [
                    f"{relation}[{vertex_type:^{spacing}}] {vertex}"
                    for relation, vertex_type, vertex in zip(relations, vertex_types, loop)
                ]
                self.errors.append(f"The graph contains at least one loop:{sep.join(loop_links)} (same as first)")

    def specific_validations(self) -> bool:
        # If specific validations are required add them here
        self.errors = []
        self.display_message("Specific validations")

        self.__transports_specific_checks()
        self.split("\ttransports_specific_checks: {time_since_last_split:6.4f}s")
        for filename, id_column in [('Transport', 'Label'),  # TODO replace by
                                    ('ProductionOperation', 'id'),
                                    ('ProductionResource', 'id'),
                                    ('Stock', 'id'),
                                    ('OptimizationConstraints', 'id'),
                                    ('OptimizationDecisionVariables', 'id'),
                                    ('OptDecisionVariableGroups', 'id'),
                                    ('Tags', 'id')]:
            self.__unique_id_validation(filename, id_column)
        self.split("\tunique_id_validation: {time_since_last_split:6.4f}s")

        if self.run_type != "Simulation":
            self.__part_retention_validation()
            self.split("\tpart_retention_validation: {time_since_last_split:6.4f}s")

        self.__infinite_stocks_checks()
        self.split("\tinfinite_stocks_checks: {time_since_last_split:6.4f}s")

        self.__obsolescence_check()
        self.split("\tobsolescence_check: {time_since_last_split:6.4f}s")

        self.__sourcing_proportions_check()
        self.split("\tsourcing_proportions_check: {time_since_last_split:6.4f}s")

        self.__dispatch_proportions_check()
        self.split("\tdispatch_proportions_check: {time_since_last_split:6.4f}s")

        self.__production_proportions_check()
        self.split("\tproduction_proportions_check: {time_since_last_split:6.4f}s")

        self.__check_resource_dependencies()
        self.split("\tcheck_resource_dependencies: {time_since_last_split:6.4f}s")

        self.__mandatory_attributes_check()
        self.split("\tmandatory_attributes_check: {time_since_last_split:6.4f}s")

        if self.errors:
            self.display_message(f"{len(self.errors)} error{'s' if len(self.errors) > 1 else ''} found in the files")
            for filename, item_id, err in self.errors:
                self.display_message(f" - {filename}: {item_id}: {err}")
        else:
            self.display_message("Specific checks are valid")
            return True
        return False

    def __part_retention_validation(self):
        stocks = self.reader.files['Stock']
        transports = self.reader.files['Transport']
        outputs = self.reader.files['input']
        isdp = None
        if self.reader.files['Configuration']:
            isdp = self.reader.files['Configuration'][0].get('IntermediaryStockDispatchPolicy')
        if isdp is None:
            isdp = parameters_default_values['Configuration']['IntermediaryStockDispatchPolicy']
        if isdp == 'DispatchAll':
            non_final_stocks = set()
            for t in transports:
                non_final_stocks.add(t['source'])
            for o in outputs:
                non_final_stocks.add(o['source'])
            for stock in stocks:
                if stock['id'] not in non_final_stocks:
                    continue
                stock_demands = stock.get('Demands')
                if stock_demands is None:
                    continue
                if any(stock_demands.values()):
                    self.errors.append(("Stock",
                                        stock['id'],
                                        "has demands and is not a final stock,"
                                        " set IntermediaryStockDispatchPolicy to AllowRetention"))

    def __unique_id_validation(self, filename: str, id_column: str):
        _file = self.reader.files[filename]

        _ids = Counter(item[id_column] for item in _file)

        for _id, count in _ids.items():
            if count > 1:
                self.errors.append((filename,
                                    _id,
                                    f"{id_column} is not unique, found {count} times"))

    def __transports_specific_checks(self):
        transports = self.reader.files['Transport']
        for transport in transports:
            initial_transported_quantities = transport.get('InitialTransportedQuantities', {})
            initial_transported_values = transport.get('InitialTransportedValues', {})
            key_errors = [
                k
                for k in initial_transported_values
                if k not in initial_transported_quantities
            ]
            for k in key_errors:
                self.errors.append(("Transports",
                                    transport.get('Label'),
                                    f"InitialTransportedValues: key {k} has no quantities associated"))

    def __infinite_stocks_checks(self):
        transports = self.reader.files['Transport']
        stocks = self.reader.files['Stock']

        infinite_stocks = [stock for stock in stocks if stock.get('IsInfinite')]

        infinite_stocks_ids = set(stock['id'] for stock in infinite_stocks)

        def check_attribute(stock, attribute, strict=True, timed=False):
            value = stock.get(attribute)
            attribute_errors = []
            if value is not None:
                if timed:
                    for t, v in value.items():
                        if (v > 0 if strict else v >= 0):
                            attribute_errors.append(f"Timestep {t}: {v}")
                else:
                    if (value > 0 if strict else value >= 0):
                        attribute_errors.append(value)
            for error in attribute_errors:
                self.errors.append((
                    "Stock",
                    stock['id'],
                    f"Is infinite and has {'strictly positive ' if strict else ''}{attribute}: {error}"
                ))

        for stock in infinite_stocks:
            check_attribute(stock, 'InitialStock')
            check_attribute(stock, 'InitialValue')
            check_attribute(stock, 'MinimalStock', False)
            check_attribute(stock, 'MaximalStock', False)
            check_attribute(stock, 'MaximizationWeight')
            check_attribute(stock, 'StorageUnitCosts', timed=True)
            check_attribute(stock, 'Demands', timed=True)

        transports_from_infinite_stocks = [transport
                                           for transport in transports
                                           if transport['source'] in infinite_stocks_ids]
        for transport in transports_from_infinite_stocks:
            self.errors.append(("Stock",
                                transport.get('source'),
                                f"Is infinite and has outgoing transport: {transport.get('Label')}"))

    def __obsolescence_check(self):
        empty_obsolete_stocks = None
        if self.reader.files['Configuration']:
            empty_obsolete_stocks = self.reader.files['Configuration'][0].get('EmptyObsoleteStocks')
        if empty_obsolete_stocks is None:
            empty_obsolete_stocks = parameters_default_values['Configuration']['EmptyObsoleteStocks']
        if empty_obsolete_stocks:
            stocks = self.reader.files['Stock']
            for stock in stocks:
                stock_demands = stock.get('Demands')
                if stock_demands is None:
                    continue
                has_demands = any(stock_demands.values())
                stock_policy = stock.get('StockPolicy')
                if stock_policy is None:
                    stock_policy = parameters_default_values['Stock']['StockPolicy']
                has_stock_policy = stock_policy != 'None'
                if has_demands and has_stock_policy:
                    self.errors.append(('Configuration',
                                        'EmptyObsoleteStocks',
                                        'The stock obsolescence option is not compatible with stock policies.'))
                    break

    def __sourcing_proportions_check(self):
        sources_by_stock = {}
        sourcing_proportions = {}

        for output in self.reader.files.get('output', []):
            sources_by_stock.setdefault(output['target'], []).append(output['source'])
        for operation in self.reader.files.get('ProductionOperation', []):
            sourcing_proportions[operation['id']] = operation.get('SourcingProportions')
        for transport in self.reader.files.get('Transport', []):
            sources_by_stock.setdefault(transport['target'], []).append(transport['Label'])
            sourcing_proportions[transport['Label']] = transport.get('SourcingProportions')

        e = 1e-2
        for stock, sources in sources_by_stock.items():
            considered_sources = {source for source in sources if sourcing_proportions[source] is not None}
            if considered_sources:
                time_steps = sorted(set(
                    t
                    for source in considered_sources
                    for t in sourcing_proportions[source]
                ), key=int)
                proportions = {}
                errors = []
                for time_step in time_steps:
                    for source in considered_sources:
                        if time_step in sourcing_proportions[source]:
                            proportions[source] = sourcing_proportions[source][time_step]
                    proportions_sum = sum(proportions.values())
                    if proportions_sum < 1 - e or proportions_sum > 1 + e:
                        errors.append(time_step)
                if errors:
                    self.errors.append(('ProductionOperationSchedules/TransportSchedules',
                                        'SourcingProportions',
                                        f"The sum of the {stock} sources proportions ({', '.join(sources)}) is not equal to one for the time step{'s' if len(errors) > 1 else ''}: {', '.join(errors)}"))

    def __dispatch_proportions_check(self):
        operations_by_stock = {}
        dispatch_proportions = {}
        retain_proportions = {}

        for i in self.reader.files.get('input', []):
            operations_by_stock.setdefault(i['source'], []).append(i['target'])
            dispatch_proportions[(i['source'], i['target'])] = i.get('DispatchProportions')
        for transport in self.reader.files.get('Transport', []):
            operations_by_stock.setdefault(transport['source'], []).append(transport['Label'])
            dispatch_proportions[(transport['source'], transport['Label'])] = transport.get('DispatchProportions')
        for stock in self.reader.files.get('Stock', []):
            retain_proportions[stock['id']] = stock.get('RetainProportions')

        e = 1e-2
        for stock, operations in operations_by_stock.items():
            considered_operations = {operation for operation in operations if dispatch_proportions[(stock, operation)] is not None}
            retain = retain_proportions[stock] is not None
            if considered_operations or retain:
                time_steps = set(
                    t
                    for operation in considered_operations
                    for t in dispatch_proportions[(stock, operation)]
                )
                if retain:
                    time_steps |= set(t for t in retain_proportions[stock])
                time_steps = sorted(time_steps, key=int)
                proportions = {}
                errors = []
                for time_step in time_steps:
                    for operation in considered_operations:
                        if time_step in dispatch_proportions[(stock, operation)]:
                            proportions[operation] = dispatch_proportions[(stock, operation)][time_step]
                    if retain and time_step in retain_proportions[stock]:
                        proportions[stock] = retain_proportions[stock][time_step]
                    proportions_sum = sum(proportions.values())
                    if proportions_sum < 1 - e or proportions_sum > 1 + e:
                        errors.append(time_step)
                if errors:
                    self.errors.append(('inputSchedules',
                                        'DispatchProportions',
                                        f"The sum of the {stock} dispatch proportions to ({', '.join(operations)}) is not equal to one for the time step{'s' if len(errors) > 1 else ''}: {', '.join(errors)}"))

    def __production_proportions_check(self):
        operations_by_resource = {}
        production_proportions = {}

        for contains in self.reader.files.get('contains', []):
            operations_by_resource.setdefault(contains['source'], []).append(contains['target'])
        for operation in self.reader.files.get('ProductionOperation', []):
            production_proportions[operation['id']] = operation.get('ProductionProportions')

        e = 1e-2
        for resource, operations in operations_by_resource.items():
            considered_operations = {operation for operation in operations if production_proportions[operation] is not None}
            if considered_operations:
                time_steps = sorted(set(
                    t
                    for operation in considered_operations
                    for t in production_proportions[operation]
                ), key=int)
                proportions = {}
                errors = []
                for time_step in time_steps:
                    for operation in considered_operations:
                        if time_step in production_proportions[operation]:
                            proportions[operation] = production_proportions[operation][time_step]
                    proportions_sum = sum(proportions.values())
                    if proportions_sum < 1 - e or proportions_sum > 1 + e:
                        errors.append(time_step)
                if errors:
                    self.errors.append(('ProductionOperationSchedules',
                                        'ProductionProportions',
                                        f"The sum of the {resource} operations proportions ({', '.join(operations)}) is not equal to one for the time step{'s' if len(errors) > 1 else ''}: {', '.join(errors)}"))

    def find_relations_by_id(self, relation_name: str, looked_id: str, relation_column: str):
        if (relation_name, looked_id, relation_column) not in self.lookup_memory:
            self.lookup_memory[(relation_name, looked_id, relation_column)] = [
                row
                for row in self.reader.files[relation_name]
                if row.get(relation_column) == looked_id
            ]
        return self.lookup_memory[(relation_name, looked_id, relation_column)]

    parent_operations_mem = dict()

    def __find_parent_operations(self, stock_id: str):
        if stock_id in self.parent_operations_mem:
            return self.parent_operations_mem[stock_id]

        _ret = []
        self.parent_operations_mem[stock_id] = _ret
        # transports won't increment the current level
        for _transport in self.find_relations_by_id('Transport', stock_id, 'target'):
            for operation in self.__find_parent_operations(_transport.get('source')):
                _ret.append(operation)

        for _output in self.find_relations_by_id('output', stock_id, 'target'):
            _operation_id = _output.get('source')
            _ret.append(_operation_id)
        return _ret

    def __check_resource_dependencies(self):
        # A resource should not have a "loop" dependency
        # It means if any operation in the resource is dependant on another operation in the same resource
        # the dataset validation should fail
        # A dependency is either a direct parent operation, or an operation in the same resource as a parent

        contains = self.reader.files['contains']

        direct_dependencies = dict()
        operations_per_resource = dict()
        resource_per_operation = dict()

        # fill dependencies
        for contain in contains:
            operation_id = contain.get('target')
            resource_id = contain.get('source')
            operations_per_resource.setdefault(resource_id, [])
            operations_per_resource[resource_id].append(operation_id)
            resource_per_operation[operation_id] = resource_id
            direct_dependencies.setdefault(operation_id, set())
            for _input in self.find_relations_by_id('input', operation_id, 'target'):
                direct_dependencies[operation_id].update(self.__find_parent_operations(_input.get('source')))

        for operations in operations_per_resource.values():
            dependencies = set()
            for operation_id in operations:
                dependencies.update(direct_dependencies[operation_id])
                direct_dependencies[operation_id] = dependencies

        full_dependencies = dict()

        def find_dependencies(operation_id: str):
            if operation_id in full_dependencies:
                return full_dependencies[operation_id]
            _ret = set()
            full_dependencies[operation_id] = _ret
            _dependencies = direct_dependencies.get(operation_id, set())
            for dependency in _dependencies:
                _ret.add(dependency)
                _ret.update(find_dependencies(dependency))
            return _ret

        for operation_id, resource_id in resource_per_operation.items():
            if operation_id in find_dependencies(operation_id):
                self.errors.append(('Graph',
                                    'Resource dependency',
                                    f'In resource {resource_id}, the operation {operation_id} requires itself'))
                return

    def __mandatory_attributes_check(self):
        demand = any(
            len(stock_demands.values())
            for stock in self.reader.files['Stock']
            for stock_demands in (stock.get('Demands'),)
            if stock_demands
        )
        if not demand:
            self.errors.append(('Stock',
                                'Demands',
                                'There is no demand.'))
        # for future warnings:
        """
        for resource in self.reader.files['ProductionResource']:
            if 'OpeningTimes' not in resource:
                self.display_message(f"Production resource {resource['id']} has no opening time.")
        for operation in self.reader.files['ProductionOperation']:
            if 'CycleTimes' not in operation:
                self.display_message(f"Production operation {operation['id']} has no opening time.")
        for transport in self.reader.files['Transport']:
            if 'Duration' not in transport:
                self.display_message(f"Transport {transport['Label']} has no duration.")
        """

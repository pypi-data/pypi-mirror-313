"""
Dettectinator - The Python library to your DeTT&CT YAML files.
Authors:
    Martijn Veken, Sirius Security
    Ruben Bouman, Sirius Security
License: GPL-3.0 License
"""
import datetime
import json
import sys
import os
import importlib
import inspect

from collections import OrderedDict
from dettectinator import DettectTechniquesAdministration, DettectDataSourcesAdministration, DettectGroupsAdministration
from plugins.technique_import import TechniqueBase
from plugins.datasources_import import DatasourceBase
from plugins.groups_import import GroupBase
from argparse import ArgumentParser, Namespace


class CommandLine:

    @staticmethod
    def _get_raw_commandline(argument_names: list) -> str:
        """
        Some arguments need to be read from the command line before being processed with ArgumentParser.
        This function provides a way to read these values from the command line in a simple way.
        It's ugly, but it works :)
        :return: The value of the requested argument.
        """
        prev = ''
        value = ''
        for item in sys.argv:
            if prev in argument_names:
                value = item
                break
            prev = item
        return value

    @staticmethod
    def _print_plugins(import_plugins: dict) -> None:
        """
        Prints the list of available data import plugins in a module
        :param import_plugins: dictionary containing the plugins
        """
        for name in import_plugins.keys():
            print(f' - {name}')

    @staticmethod
    def _get_plugins() -> dict:
        """
        Retrieves all plugins from the plugin folder
        :return: dict containing plugins and modules
        """
        import_plugins = {}
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')
        for module in [x for x in os.listdir(path) if x[-3:] == '.py']:
            plugin_mod = importlib.import_module('plugins.' + module[:-3])
            for name, cls in inspect.getmembers(plugin_mod, inspect.isclass):
                if ('Technique' in name or 'Datasource' in name or 'Group' in name) and 'Base' not in name:
                    import_plugins[name] = plugin_mod
        return import_plugins

    @staticmethod
    def _set_default_params(parser: ArgumentParser):
        """
        Set the default command line arguments
        """
        required = parser.add_argument_group('required arguments')
        parser.add_argument('-c', '--config', help='Configuration file location.')
        required.add_argument('-p', '--plugin', help='Data import plugin name.', required=True)
        parser.add_argument('-a', '--applicable_to',
                            help='Systems that the detections are applicable to (comma seperated list).')
        parser.add_argument('-d', '--domain',
                            help='The ATT&CK domain (default = enterprise). This argument is ignored if a domain is specified in the YAML file.',
                            required=False, choices=['enterprise', 'ics', 'mobile'])
        parser.add_argument('-i', '--input_file', help='YAML filename for input.', default=None)
        parser.add_argument('-o', '--output_file', help='YAML filename for output.', default=None)
        parser.add_argument('-n', '--name', help='Value for the name attribute in the YAML file.', default=None)
        parser.add_argument('-s', '--stix_location', help='Local STIX repository location.', default=None)
        parser.add_argument('-lf', '--log_file', help='Log to write results and warnings to.', default=None)
        parser.add_argument('-lp', '--log_parameters', action='store_true', help='Add the configuration parameters to the log.')
        parser.add_argument('-ch', '--check_unused', action='store_true', help='Check unused detections.')
        parser.add_argument('-cl', '--clean_unused', action='store_true',
                            help='Clean unused detections. When using this option, including the check_unused option is necessary.')

    def _get_argument_values_from_config_file(self) -> dict:
        """
        Read the command line arguments from the config file if applicable
        """
        config_file_name = self._get_raw_commandline(['-c', '--config'])
        if config_file_name:
            print(f'Reading settings from "{config_file_name}".')
            with open(config_file_name, 'r') as f:
                config_file_arguments = json.load(f)
        else:
            config_file_arguments = {}
        return config_file_arguments

    @staticmethod
    def _create_log_file(arguments: Namespace, output: list, plugin_name: str) -> None:
        sep_single = '-' * 100 + '\n'
        sep_double = "=" * 100 + '\n'
        with open(arguments.log_file, 'a') as log_file:
            log_file.write(sep_double)
            log_file.write(f'Result from plugin {plugin_name} at {datetime.datetime.now()}:\n')
            log_file.write(sep_single)
            if arguments.log_parameters:
                log_file.writelines([f'{k}: {v}\n' for k, v in OrderedDict(sorted(vars(arguments).items())).items()])
                log_file.write(sep_single)
            log_file.writelines([f'{o}\n' for o in output])
            log_file.write(sep_double)
            log_file.write('\n')

    @staticmethod
    def process_techniques(applicable_to: list, arguments: Namespace, plugin: TechniqueBase) -> tuple:
        """
        Process all techniques from the source system
        """
        # Get the technique data
        techniques = plugin.get_attack_techniques(applicable_to)
        # Convert data to yaml
        print('Generating techniques YAML file.')
        dettect = DettectTechniquesAdministration(arguments.input_file, domain=arguments.domain,
                                                  local_stix_path=arguments.stix_location)

        location_prefix_unused_detections = arguments.location_prefix if arguments.clean_unused_location_prefix else ''

        warnings, results = dettect.update_detections(techniques, check_unused_detections=arguments.check_unused,
                                                      clean_unused_detections=arguments.clean_unused,
                                                      location_prefix_unused_detections=location_prefix_unused_detections)
        return dettect, results, warnings

    @staticmethod
    def process_datasource(applicable_to: list, arguments: Namespace, plugin: DatasourceBase) -> tuple:
        """
        Process all data sources from the source system
        """
        # Get the data source data
        datasources = plugin.get_attack_datasources(applicable_to)
        # Convert data to yaml
        print('Generating datasources YAML file.')
        dettect = DettectDataSourcesAdministration(arguments.input_file, domain=arguments.domain,
                                                   local_stix_path=arguments.stix_location)
        warnings, results = dettect.update_data_sources(datasources, check_unused_data_sources=arguments.check_unused,
                                                        clean_unused_data_sources=arguments.clean_unused)
        return dettect, results, warnings

    @staticmethod
    def process_groups(arguments: Namespace, plugin: GroupBase) -> tuple:
        """
        Process all groups from the source
        """
        # Get the group data
        groups = plugin.get_attack_groups()
        # Get the notes
        notes = plugin.get_notes()
        # Convert data to yaml
        print('Generating groups YAML file.')
        dettect = DettectGroupsAdministration(arguments.input_file, domain=arguments.domain,
                                              local_stix_path=arguments.stix_location)
        warnings, results = dettect.add_groups(groups)
        if notes:
            dettect.add_notes(notes)
        return dettect, results, warnings

    def start(self) -> None:
        """
        Dettectinator has been started from the commandline.
        Process the command line arguments and launch the appropriate plugin.
        """

        # Load default argument values from the config file
        config_file_arguments = self._get_argument_values_from_config_file()

        # Retrieve all available plugins
        plugins = self._get_plugins()

        # Get the plugin name from the arguments
        plugin_name = config_file_arguments.get('plugin', self._get_raw_commandline(['-p', '--plugin']))

        if plugin_name:
            # Get the plugin class if it exists
            if plugin_name in plugins.keys():
                plugin_class = getattr(plugins[plugin_name], plugin_name)
                print(f'Plugin "{plugin_name}" has been found.')
            else:
                print(f'data import plugin "{plugin_name}" does not exist. Valid plugins:')
                self._print_plugins(plugins)
                sys.exit(1)

            # Add the default command line params
            parser = ArgumentParser(add_help=True, conflict_handler='error', )
            self._set_default_params(parser)

            # Add the parameters from the plugin
            plugin_group = parser.add_argument_group(plugin_name)
            plugin_class.set_plugin_params(plugin_group)

            # Set the default values from the config file
            # Default and required don't work together, so set required to False
            parser.set_defaults(**config_file_arguments)
            for action in parser._actions:
                if action.dest in config_file_arguments.keys():
                    action.required = False

            # Evaluate command line arguments
            arguments = parser.parse_args()
            applicable_to = [at.strip() for at in arguments.applicable_to.split(',')] if arguments.applicable_to else []
            output_file = arguments.output_file or arguments.input_file

            # Read the data from the source
            print(f'Using "{plugin_name}" to collect data.')
            plugin = plugin_class(vars(arguments))

            if plugin_name.startswith('Technique'):
                dettect, results, warnings = self.process_techniques(applicable_to, arguments, plugin)
            elif plugin_name.startswith('Datasource'):
                dettect, results, warnings = self.process_datasource(applicable_to, arguments, plugin)
            else:
                dettect, results, warnings = self.process_groups(arguments, plugin)

            if arguments.name:
                dettect.set_name(arguments.name)

            dettect.save_yaml_file(output_file)
            print(f'DeTT&CT YAML file written: {dettect.get_filename()}')

            output = sorted(list(set(warnings + results)))

            if arguments.log_file:
                self._create_log_file(arguments, output, plugin_name)

            if len(output) > 0:
                print('\nPlease review the following items:')
                print(' - ' + '\n - '.join(output))
        else:
            print('Please specify a valid data import plugin using the "-p" argument:')
            self._print_plugins(plugins)

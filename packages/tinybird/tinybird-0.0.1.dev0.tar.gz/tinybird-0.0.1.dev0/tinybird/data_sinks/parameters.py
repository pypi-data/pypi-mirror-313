import re

from tinybird.data_sinks.config import FILE_TEMPLATE_PROPERTIES_REGEX


def replace(parameters):
    def replace(match):
        parameter_name = match.group(1)
        parameter_value = parameters.get(parameter_name)

        if parameter_value:
            return f'{parameter_value}{match.group("separator")}'

        return match.group()

    return replace


def replace_parameters_in_file_template(file_template: str, parameters: dict):
    if "{" not in file_template or "}" not in file_template:
        return file_template

    return re.sub(FILE_TEMPLATE_PROPERTIES_REGEX, replace(parameters), file_template)

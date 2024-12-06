"""Code generation to build automation manager jobs for the platform and click commands for the RegScale CLI"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from regscale.models.integration_models.synqly_models.synqly_model import SynqlyModel

SUPPORTED_CONNECTORS = ["ticketing"]


def generate_dags() -> None:
    """Generate Airflow DAGs for the platform"""
    from regscale.core.app.utils.app_utils import check_file_path
    from regscale.models.integration_models.synqly_models.synqly_model import SynqlyModel

    model = SynqlyModel()
    configs = model._get_integrations_and_secrets(True)
    # iterate through connectors and generate DAGs
    for connector in SUPPORTED_CONNECTORS:
        connector_configs = {
            integration: configs[integration] for integration in configs if connector in integration.lower()
        }
        description = _build_description(configs=connector_configs, connector=connector)
        # check airflow/dags for existing DAGs and skip them
        for integration, config in connector_configs.items():
            save_dir = f"airflow/dags/{integration.split('_')[0].lower()}"
            integration_name = integration[integration.find("_") + 1 :]
            # check if the directory exists, if not create it
            check_file_path(save_dir)
            _create_and_save_dag(
                model=model,
                integration=integration,
                config=config,
                integration_name=integration_name,
                description=description,
                save_dir=save_dir,
            )


def _create_and_save_dag(
    model: "SynqlyModel", integration: str, config: dict, integration_name: str, description: str, save_dir: str
) -> None:
    """
    Create and save a DAG for the given integration

    :param SynqlyModel model: The model to use for the DAG
    :param str integration: The integration to create the DAG for
    :param dict config: The config for the integration
    :param str integration_name: The name of the integration
    :param str description: The description for the DAG
    :param str save_dir: The directory to save the DAG to
    :rtype: None
    """
    import re

    capabilities = config.get("capabilities", [])
    op_kwargs = ""
    doc_string = f"{description}\nimage: {integration.split('_')[0]}.png\ndocs: None\n"
    # replace the integration config with a flattened version
    config = model._flatten_secrets(integration=integration, return_secrets=True)
    for param_type in ["expected_params", "optional_params", "required_secrets"]:
        op_kwargs, doc_string = _build_op_kwargs_and_docstring(
            config=config,
            integration=integration,
            param_type=param_type,
            op_kwargs=op_kwargs,
            doc_string=doc_string,
            capabilities=capabilities,
        )
    # this indent is important to keep the code valid python
    dag_code = f"""
from airflow import DAG

from regscale.airflow.config import DEFAULT_ARGS, yesterday
from regscale.airflow.hierarchy import AIRFLOW_CLICK_OPERATORS as OPERATORS
from regscale.airflow.tasks.groups import setup_task_group

DAG_NAME = "{integration}"

dag = DAG(
    DAG_NAME,
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    start_date=yesterday(),
    description=__doc__,
    is_paused_upon_creation=False,
    render_template_as_native_obj=True,
)

setup = setup_task_group(dag, setup_tag=DAG_NAME)

integration_operator = OPERATORS["{integration.split('_')[0].lower()}__sync_{integration_name.lower()}"]["lambda"](
    dag=dag,
    suffix=DAG_NAME,
    op_kwargs={{{op_kwargs}\n    }},
)

setup >> integration_operator
            """
    with open(f"{save_dir}/{integration_name.lower()}.py", "w") as f:
        f.write("# flake8: noqa E501\n# pylint: disable=line-too-long\n")
        f.write('"""')
        # replace all instances of "synqly" with the integration name
        f.write(re.sub(r"(?i)synqly", integration_name, doc_string))
        f.write('"""\n')
        f.write("# pylint: enable=line-too-long\n")
        # replace all instances of "synqly" with the integration name
        f.write(re.sub(r"(?i)synqly", integration_name, dag_code))
    print(f"Generated DAG for {integration_name}.")


def _build_description(configs: dict[str, dict], connector: str) -> str:
    """
    Build the description for the DAG

    :param dict[str, dict] configs: The configs for the integrations
    :return: The description for the DAG
    :rtype: str
    """
    sync_attachments = []
    integrations = []
    for integration, config in configs.items():
        integration_name = integration.split("_")[-1]
        integrations.append(integration_name)
        capabilities = config.get("capabilities", [])
        if connector == "ticketing" and "create_attachment" in capabilities and "download_attachment" in capabilities:
            sync_attachments.append(integration_name)
    description = f"Sync {connector.capitalize()} data between {', '.join(integrations)} and RegScale data."
    if sync_attachments:
        description += f" You are also able to sync attachments between {', '.join(sync_attachments)} and RegScale."
    return description


def _build_op_kwargs_and_docstring(
    config: dict, integration: str, param_type: str, op_kwargs: str, doc_string: str, capabilities: list[str]
) -> tuple[str, str]:
    """
    Build the op_kwargs and docstring for the DAG

    :param dict config: The config for the integration
    :param str integration: The name of the integration, typically connector_integration
    :param str param_type: The type of parameter to build
    :param str op_kwargs: The op_kwargs to add to the DAG
    :param str doc_string: The docstring to add to the DAG
    :param list[str] capabilities: The capabilities of the integration
    :return: The op_kwargs and docstring
    :rtype: tuple[str, str]
    """
    proper_type = param_type.replace("_", " ").title()
    if param_type == "expected_params":
        regscale_id_jinja = "'regscale_id'"
        regscale_module_jinja = "'regscale_module'"
        op_kwargs += f'\n        "regscale_id": "{{{{ dag_run.conf[{regscale_id_jinja}] }}}}",'
        op_kwargs += f'\n        "regscale_module": "{{{{ dag_run.conf[{regscale_module_jinja}] }}}}",'
        doc_string += "Expected Params:\n"
        doc_string += "    regscale_id: INTEGER ID from RegScale of the RegScale object\n"
        doc_string += "    regscale_module: STRING name of the RegScale module to use with the provided ID\n"
        op_kwargs, doc_string = add_connector_specific_params(capabilities, integration, op_kwargs, doc_string)
    if config.get(param_type):
        if proper_type not in doc_string:
            doc_string += f"{proper_type}:\n"
        for param in config[param_type]:
            param_name = f"{integration.lower()}_{param}" if param_type == "required_secrets" else param
            jinja_key = f"'{param_name}'"
            if param_type == "optional_params":
                op_kwargs += f'\n        "{param_name}": "{{{{ dag_run.conf[{jinja_key}] if {jinja_key} in dag_run.conf else None }}}}",'
                doc_string += f"    {param_name}: {config[param_type][param].expected_type.upper()} {config[param_type][param].description or proper_type} (Default: None)\n"
            else:
                op_kwargs += f'\n        "{param_name}": "{{{{ dag_run.conf[{jinja_key}] }}}}",'
                doc_string += f"    {param_name}: {config[param_type][param].expected_type.upper()} {config[param_type][param].description or proper_type}\n"
    return op_kwargs, doc_string


def add_connector_specific_params(
    capabilities: list[str], integration: str, op_kwargs: str, doc_string: str
) -> tuple[str, str]:
    """
    Updated the op_kwargs and docstring for the DAG to include specific params for the connector based on capabilities

    :param list[str] capabilities: The capabilities of the integration
    :param str integration: The name of the integration, typically connector_integration
    :param str op_kwargs: The op_kwargs to add to the DAG
    :param str doc_string: The docstring to add to the DAG
    :return: The updated op_kwargs and docstring
    :rtype: tuple[str, str]
    """
    if "ticketing" in integration and "create_attachment" in capabilities and "download_attachment" in capabilities:
        sync_attachments_jinja = "'sync_attachments'"
        op_kwargs += f'\n        "sync_attachments": "{{{{ dag_run.conf[{sync_attachments_jinja}] if {sync_attachments_jinja} in dag_run.conf else False }}}}",'
        doc_string += "    sync_attachments: BOOLEAN Whether to sync attachments between integration and RegScale\n"
    return op_kwargs, doc_string


def generate_click_connectors() -> None:
    """Generate Click Connectors for the RegScale CLI"""
    from regscale.core.app.utils.app_utils import check_file_path
    from regscale.models.integration_models.synqly_models.synqly_model import SynqlyModel

    model = SynqlyModel()
    configs = model._get_integrations_and_secrets(True)
    # iterate through connectors and generate DAGs
    for connector in SUPPORTED_CONNECTORS:
        save_dir = "regscale/integrations/commercial/synqly"
        check_file_path(save_dir)
        connector_configs = {
            integration: configs[integration] for integration in configs if connector in integration.lower()
        }
        # check airflow/dags for existing DAGs and skip them
        _create_and_save_click_command(
            model=model,
            connector=connector,
            integration_configs=connector_configs,
            save_dir=save_dir,
        )
        # add the new click group to regscale.py
        _add_command_to_regscale(connector)


def _create_and_save_click_command(
    model: "SynqlyModel", connector: str, integration_configs: dict[str, dict], save_dir: str
) -> None:
    """
    Create and save a click command for the given integration and connector

    :param SynqlyModel model: The model to use for the DAG
    :param str connector: The connector type to create click commands for
    :param dict[str, dict] integration_configs: Dictionary containing the integration configs for the given connector
    :param str save_dir: The directory to save the DAG to
    :rtype: None
    """
    integrations_count = 0
    doc_string = f"{connector.capitalize()} connector commands for the RegScale CLI"
    # this indent is important to keep the code valid python
    cli_code = f"""
\"\"\"{doc_string}\"\"\"\n
import click
from regscale.models import regscale_id, regscale_module
from regscale.models.integration_models.synqly_models.connectors import Ticketing


@click.group()
def {connector}() -> None:
    \"\"\"{doc_string}\"\"\"
    pass
"""

    # replace the integration config with a flattened version
    for integration, config in integration_configs.items():
        capabilities = config.get("capabilities", [])
        integration_name = integration[integration.find("_") + 1 :]
        config = model._flatten_secrets(integration=integration, return_secrets=True)
        click_options_and_command = _build_click_options_and_command(
            config=config,
            connector=connector,
            integration_name=integration_name,
            capabilities=capabilities,
        )
        cli_code += f"\n\n{click_options_and_command}"
        integrations_count += 1

    with open(f"{save_dir}/{connector.lower()}.py", "w") as f:
        f.write("# flake8: noqa E501\n# pylint: disable=line-too-long\n")
        f.write(cli_code)
        f.write("# pylint: enable=line-too-long\n")
    print(f"Generated click commands for {integrations_count} {connector} connector(s).")


def _build_click_options_and_command(
    config: dict, connector: str, integration_name: str, capabilities: list[str]
) -> str:
    """
    Function to use the config to build the click options and command for the integration

    :param dict config: The config for the integration
    :param str connector: The connector type
    :param str integration_name: The name of the integration
    :param list[str] capabilities: The capabilities of the integration
    :return: The click options as a string
    :rtype: str
    """
    # add regscale_ssp_id as a default option
    click_options = ["@regscale_id()", "@regscale_module()"]
    function_params = ["regscale_id: int", "regscale_module: str"]
    function_kwargs = ["regscale_id=regscale_id", "regscale_module=regscale_module"]
    for param_type in ["expected_params", "optional_params"]:
        for param in config.get(param_type, []):
            param_data = config[param_type][param]
            if not param_data.click_type:
                continue
            # indentation is important to keep the code valid python
            click_option = f"""@click.option(
    '--{param}',
    type={param_data.click_type},
    help='{config[param_type][param].description}',
    required={not param_data.optional},
    {"prompt='" + config[param_type][param].description + "'," if not param_data.optional else ""}
)"""
            function_params.append(f"{param}: {param_data.data_type}")
            function_kwargs.append(f"{param}={param}")
            click_options.append(click_option)
    if "ticketing" == connector and "create_attachment" in capabilities and "download_attachment" in capabilities:
        click_options.append(
            f"""@click.option(
    '--sync_attachments',
    type=click.BOOL,
    help='Whether to sync attachments between {integration_name} and RegScale',
    required=False,
    default=True,
)"""
        )
        function_params.append("sync_attachments: bool")
        function_kwargs.append("sync_attachments=sync_attachments")
    click_options = "\n".join(click_options)
    function_params = ", ".join(function_params)
    # indentation is important to keep the code valid python
    click_command = f"""@{connector}.command(name="sync_{integration_name}")
{click_options}
def sync_{integration_name}({function_params}) -> None:
    \"\"\"Sync data {connector.title()} between {integration_name} and RegScale.\"\"\"
    {connector}_{integration_name} = Ticketing('{integration_name}')
    {connector}_{integration_name}.run_sync({', '.join(function_kwargs)})
"""
    return click_command


def _add_command_to_regscale(connector: str) -> None:
    """
    Add the new click group and command to the regscale.py file

    :param str connector: The connector type
    :rtype: None
    """
    import_section = 'burp = import_command_with_timing("regscale.integrations.commercial.burp", "burp")'
    command_section = "cli.add_command(burp)  # add Burp File Integration"
    with open("regscale/regscale.py", "r") as f:
        regscale_code = f.read()
    if connector in regscale_code:
        print(f"{connector.title()} click commands already exists in regscale.py.")
        return
    import_line = f'{connector} = import_command_with_timing("regscale.integrations.commercial.synqly.{connector}", "{connector}")'
    regscale_code = regscale_code.replace(import_section, f"{import_section}\n{import_line}")
    regscale_code = regscale_code.replace(
        command_section, f"{command_section}\ncli.add_command({connector})  # add {connector.capitalize()} connector"
    )
    with open("regscale/regscale.py", "w") as f:
        f.write(regscale_code)
    print(f"Added {connector} click group to regscale.py.")

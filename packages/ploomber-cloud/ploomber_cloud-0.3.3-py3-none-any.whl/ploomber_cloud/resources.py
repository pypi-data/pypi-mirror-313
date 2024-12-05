import click
import json

from importlib import resources as impresources

from ploomber_cloud.config import PloomberCloudConfig
from ploomber_cloud.exceptions import BasePloomberCloudException
from ploomber_cloud import configurations
from ploomber_cloud.models import UserTiers
from ploomber_cloud.util import get_user_type


def _check_for_config(force):
    """Check for existing config and return it"""
    config = PloomberCloudConfig()
    config.load()
    if not config.exists():
        raise BasePloomberCloudException(
            "Project not initialized. "
            "Run 'ploomber-cloud init' to initialize your project."
        )
    if not force:
        if "resources" in config.data:
            current_resources = config.data["resources"]
            cpu, ram, gpu = (
                current_resources["cpu"],
                current_resources["ram"],
                current_resources["gpu"],
            )
            raise BasePloomberCloudException(
                "Resources already configured: \n"
                f"{cpu} CPU, {ram} RAM, {gpu} GPU\n"
                "Run 'ploomber-cloud resources --force' to re-configure them. "
            )
    return config


def _get_resource_config_for_user_type(user_type: UserTiers):
    imp_file = impresources.files(configurations).joinpath(f"{user_type.value}.json")

    with open(imp_file, "rt") as f:
        return json.loads(f.read())


def _prompt_for_cpu_choice(cpu_configs):
    """Determine CPU options and prompt user for choice"""
    cpu_options = [
        option
        for option in cpu_configs.keys()
        if cpu_configs[option]["enabled"] is True
    ]
    cpu_options_prompt = [f"{option} CPUs" for option in cpu_options]
    for i in range(len(cpu_options_prompt)):
        current_cpu_option = cpu_configs[cpu_options[i]]
        if "pricePerHour" in current_cpu_option:
            cpu_options_prompt[
                i
            ] += f" (${current_cpu_option['pricePerHour']} per hour)"

    prompt = "\n".join(cpu_options_prompt)
    prompt += "\n\nSelect number of CPUs"

    while True:
        cpu_choice = click.prompt(prompt, default=cpu_options[0], show_default=False)
        if cpu_choice in cpu_options:
            break
        click.secho("Invalid entry. Please select an option from the list.", fg="red")

    click.secho(f"You chose {cpu_choice} CPUs.\n", fg="green")
    return cpu_choice


def _prompt_for_ram_choice(cpu_ram_configs, cpu_choice):
    """Determine RAM options and prompt user for choice"""
    ram_options = [
        option[0]
        for option in cpu_ram_configs[cpu_choice]["ramOptions"]
        if option[1] is True
    ]
    ram_options_prompt = [f"{option} GB" for option in ram_options]
    for i in range(len(ram_options_prompt)):
        current_ram_option = cpu_ram_configs[cpu_choice]["ramOptions"][i]
        if len(current_ram_option) == 3:  # If ram options contains pricing info
            ram_options_prompt[
                i
            ] += f" (${current_ram_option[2]} per hour)"  # Show pricing info

    prompt = "\n".join(ram_options_prompt)
    prompt += "\n\nSelect amount of RAM"

    while True:
        ram_choice = click.prompt(prompt, default=ram_options[0], show_default=False)
        if ram_choice in ram_options:
            break
        click.secho("Invalid entry. Please select an option from the list.", fg="red")

    click.secho(f"You chose {ram_choice} GBs.\n", fg="green")
    return ram_choice


def _prompt_for_gpu_choice(gpu_configs):
    """Determine GPU options and prompt user for choice"""
    gpu_options = [
        gpu for gpu, values in gpu_configs.items() if values["enabled"] is True
    ]

    gpu_options_prompts = []

    for option in gpu_options:
        if "pricePerHour" in gpu_configs[option]:
            price = gpu_configs[option]["pricePerHour"]
            option_prompt = f"{option} GPUs (${price} per hour)"
        else:
            option_prompt = f"{option} GPUs"
        gpu_options_prompts.append(option_prompt)

    prompt = "\n".join(gpu_options_prompts)

    prompt += "\n\nSelect number of GPUs"

    while True:
        gpu_choice = click.prompt(prompt, default=gpu_options[0], show_default=False)

        if gpu_choice in gpu_options:
            break
        click.secho("Invalid entry. Please select an option from the list.", fg="red")

    click.secho(f"You chose {gpu_choice} GPUs.\n", fg="green")
    return gpu_choice


def _get_resource_choices():
    project_config = _check_for_config(force=True)
    cpu_choice = project_config.data["resources"]["cpu"]
    resource_config = _get_resource_config_for_user_type(get_user_type())

    cpu_options = [
        option
        for option in resource_config["cpuToRamMapping"].keys()
        if resource_config["cpuToRamMapping"][option]["enabled"] is True
    ]

    # If CPU choice is invalid, pick the closest available choice
    # and base the ram options off of that
    if cpu_choice not in cpu_options:
        # This chooses the cpu option with the min absolute difference
        # from our original cpu choice and returns it as a string
        cpu_choice = str(
            min(cpu_options, key=lambda x: abs(float(x) - float(cpu_choice)))
        )

    ram_options = [
        option[0]
        for option in resource_config["cpuToRamMapping"][cpu_choice]["ramOptions"]
        if option[1] is True
    ]

    gpu_options = [
        gpu for gpu, enabled in resource_config["gpu"].items() if enabled is True
    ]

    return cpu_options, ram_options, gpu_options


def resources(force=False):
    # Make sure project has already been initialized
    project_config = _check_for_config(force)

    # Determine if user is PRO and set resource configurations
    resource_config = _get_resource_config_for_user_type(get_user_type())

    # Prompt for GPU
    gpu_choice = int(_prompt_for_gpu_choice(gpu_configs=resource_config["gpu"]))
    if gpu_choice > 0:
        cpu_choice = 4.0
        ram_choice = 12
        click.secho(
            "CPU and RAM options are fixed when you select 1 or more GPUs.", fg="yellow"
        )
    else:
        # Prompt for CPU
        cpu_choice = _prompt_for_cpu_choice(
            cpu_configs=resource_config["cpuToRamMapping"]
        )

        # Prompt for RAM
        ram_choice = _prompt_for_ram_choice(
            cpu_ram_configs=resource_config["cpuToRamMapping"], cpu_choice=cpu_choice
        )

    # Set resources in project config
    project_config["resources"] = {
        "cpu": float(cpu_choice),
        "ram": int(ram_choice),
        "gpu": int(gpu_choice),
    }

    click.echo(
        "Resources successfully configured: "
        f"{cpu_choice} CPUs, {ram_choice} GB RAM, {gpu_choice} GPUs.",
    )

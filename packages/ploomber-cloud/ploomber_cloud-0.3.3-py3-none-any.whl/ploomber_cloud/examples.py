import requests
import json
from pathlib import Path
import os
from zipfile import ZipFile
import shutil
import click
from datetime import datetime
from ploomber_cloud import util, api_key
from ploomber_cloud.exceptions import PloomberCloudRuntimeException

HOME_PATH = Path("~", ".ploomber").expanduser()
CLONED_REPO_PATH = HOME_PATH / "doc-repo"
METADATA_PATH = HOME_PATH / ".ploomber-cloud-metadata"
MISSING_API_KEY_MSG = """To deploy, you need an API key. Get one here:
https://docs.cloud.ploomber.io/en/latest/quickstart/apikey.html \n
Then run:\n$ ploomber-cloud key YOUR-KEY"""
INVALID_CHOICE_ERROR_MSG = (
    "Invalid example choice. {reason}"
    "Command should be in the format:\n\n \
$ ploomber-cloud examples framework/example-name\n\n \
or to select from a menu of examples:\n\n \
$ ploomber-cloud examples\n\nTo clear the cache:\n\n \
$ ploomber-cloud examples --clear-cache"
)


def _get_docs_repo():
    """Download zip archive of ploomber/doc and extract it"""
    url = "https://api.github.com/repos/ploomber/doc/zipball/main"
    headers = {
        "Accept": "application/vnd.github+json",
    }
    res = requests.get(url, headers)

    if Path("doc.zip").exists():
        Path("doc.zip").unlink()

    with open("doc.zip", "wb") as zipfile:
        zipfile.write(res.content)

    subpath = None
    with ZipFile("doc.zip") as zipfile:
        subpath = zipfile.infolist()[0].filename
        zipfile.extractall(CLONED_REPO_PATH)

    Path("doc.zip").unlink()

    return subpath[:-1]


def _load_metadata():
    """Load metadata from ~/.ploomber/.ploomber-cloud-metadata"""
    try:
        return json.loads(Path(METADATA_PATH).read_text())
    except Exception as e:
        raise PloomberCloudRuntimeException(
            "Error loading metadata",
        ) from e


def _validate_metadata():
    """Validate metadata file exists and is current"""
    if not Path(METADATA_PATH).exists():
        return False

    data = _load_metadata()
    if not data:
        return False

    last_updated = data["timestamp"]
    then = datetime.fromtimestamp(last_updated)
    now = datetime.now()
    elapsed = (now - then).days
    is_more_than_one_day_old = elapsed >= 1

    return not is_more_than_one_day_old


def _save_metadata(examples):
    """Save metadata into metadata file in JSON format"""
    timestamp = datetime.now().timestamp()
    metadata = json.dumps(dict(timestamp=timestamp, examples=examples), indent=4)
    Path(METADATA_PATH).write_text(metadata)


def parse_readme_for_title_description(path):
    """Parse an example's README.md for title and description"""
    title, description = "", ""
    with open(path, "r", encoding="utf-8") as rm:
        lines = rm.readlines()
        for i, line in enumerate(lines):
            if line.startswith("#"):
                line = line.replace("#", "")
                line = line.replace("\n", "")
                line = line.lstrip()
                title = line
            elif title and not line.isspace():
                for nextline in lines[i:]:
                    if nextline.isspace():
                        break
                    description += nextline.replace("\n", "")
                break

    return title, description


def _parse_directory_tree(directory, indent=0):
    """Parse doc/examples to collect each framework and example into dict"""
    if indent > 2:
        return
    elif indent == 2:
        tree = {"title": None, "description": None, "path": directory, "parsed": False}
    else:
        tree = {}

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if indent == 2 and "readme" in item_path.lower():
            tree["title"], tree["description"] = parse_readme_for_title_description(
                item_path
            )
            tree["parsed"] = True
        elif indent < 2 and os.path.isdir(item_path):
            tree[item] = _parse_directory_tree(item_path, indent + 1)

    if indent == 2 and tree["parsed"] is not True:
        tree["title"] = directory.split("/")[-1]
        tree["description"] = ""

    return tree


def _prompt_user_for_example_choice(examples):
    """Prompt user with a list of possible frameworks and examples"""
    frameworks = [fw for fw in examples.keys() if fw != "docker"]
    selected_framework = util.prompt_for_choice_from_list(
        frameworks, "\nChoose a framework", ignore_case=True
    )

    if selected_framework is None:
        quit()

    examples_choices = []
    for ex in examples[selected_framework].keys():
        title = examples[selected_framework][ex]["title"]
        description = examples[selected_framework][ex]["description"]
        examples_choices.append(f"{title}: {description}")

    selected_example_index = util.prompt_for_choice_from_list(
        examples_choices, f"\nChoose a {selected_framework} example", index=True
    )

    if selected_example_index is None:
        quit()

    selected_example_title = list(examples[selected_framework].keys())[
        selected_example_index
    ]
    path_to_example = examples[selected_framework][selected_example_title]["path"]
    example_title = examples[selected_framework][selected_example_title]["title"]

    return path_to_example, example_title


def _prompt_user_for_location(default_location):
    """Prompt user for the location to download example"""
    location = click.prompt(
        f"Enter the location (defaults to '{default_location}/')...",
        default="",
        show_default=False,
    )
    if not location:
        return default_location

    while location[-1] == "/":
        location = location[:-1]

    return f"{location}/"


def _copy_selected_example(location, path_to_example, example_title):
    """Copy example from docs folder into user specified location"""

    click.echo(f"\nDownloading example {example_title} in `{location}`...")

    try:
        shutil.copytree(path_to_example, location)
    except FileExistsError as e:
        raise PloomberCloudRuntimeException(
            "File already exists in this path. Choose a different location."
        ) from e

    click.echo("Done.")
    if location.startswith("./"):
        location = location[2:]

    return location


def _show_user_instructions(location):
    """Show user instructions to initialize and deploy project"""
    click.echo("Run the following to deploy your project:\n")
    try:
        key = api_key.get()
        if not key:
            click.echo(MISSING_API_KEY_MSG)
    except Exception:
        click.echo(MISSING_API_KEY_MSG)

    click.echo(f"$ cd {location}")
    click.echo("$ ploomber-cloud init")
    click.echo("$ ploomber-cloud deploy\n")


def examples(name=None, clear_cache=False):
    """Download an example app from the ploomber/docs/examples repo"""
    # Check if metadata exists and is current
    metadata_updated = _validate_metadata() if not clear_cache else False
    if not metadata_updated:
        # Download GH doc repo
        subpath = _get_docs_repo()
        # Parse into metadata file
        examples_data = _parse_directory_tree(
            f"{CLONED_REPO_PATH}/{subpath}/examples", 0
        )
        _save_metadata(examples_data)
        click.echo("Downloaded latest examples...\n")

    examples = _load_metadata()["examples"]
    _save_metadata(examples)

    path_to_example, example_title = None, None

    # Prompt user for example choice
    if name:
        # Validate
        if "/" not in name:
            error_msg = INVALID_CHOICE_ERROR_MSG.format(
                reason="Either the framework or the project is missing.\n"
            )
            raise PloomberCloudRuntimeException(error_msg)

        framework, name = name.split("/", 1)

        if framework == "docker" and name not in examples[framework]:
            raise PloomberCloudRuntimeException(
                f"{framework}/{name} does not exist. " f"Please enter a valid project."
            )

        if framework not in examples:
            error_msg = INVALID_CHOICE_ERROR_MSG.format(
                reason=f"Couldn't find framework: {framework}.\n"
            )
            raise PloomberCloudRuntimeException(error_msg)

        if name not in examples[framework]:
            error_msg = INVALID_CHOICE_ERROR_MSG.format(
                reason=f"Couldn't find project: {name}.\n"
            )
            raise PloomberCloudRuntimeException(error_msg)

        path_to_example = examples[framework][name]["path"]
        example_title = examples[framework][name]["title"]

    if not path_to_example or not example_title:
        path_to_example, example_title = _prompt_user_for_example_choice(examples)

    # Prompt user for location
    default_location = Path(path_to_example).name

    location = _prompt_user_for_location(default_location)

    location = _copy_selected_example(location, path_to_example, example_title)

    _show_user_instructions(location)

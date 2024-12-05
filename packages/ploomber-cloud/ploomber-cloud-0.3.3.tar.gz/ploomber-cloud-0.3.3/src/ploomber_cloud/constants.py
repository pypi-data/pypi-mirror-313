VALID_PROJECT_TYPES = {
    "voila",
    "streamlit",
    "docker",
    "panel",
    "solara",
    "shiny-r",
    "dash",
    "flask",
    "chainlit",
}

VALID_DOCKER_PROJECT_TYPES = {
    "fastapi",
    "gradio",
    "shiny",
}

FORCE_INIT_MESSAGE = (
    "You may re-initialize a new project by running 'ploomber-cloud init --force'.\n"
    "For re-initializing an existing project, run "
    "'ploomber-cloud init --from-existing --force'"
)

RETAINED_RESOURCES_WARNING = (
    "WARNING: your previous resources configuration "
    "has been carried over: {cpu} CPU, {ram} RAM, {gpu} GPU\n"
    "To change resources, run: 'ploomber-cloud resources --force'"
)

RETAINED_LABELS_WARNING = (
    "WARNING: your previously added labels "
    "have been carried over: {labels}.\n"
    "To add more labels, run: 'ploomber-cloud resources --add' "
    "or to delete labels run 'ploomber-cloud resources --delete'"
)

CONFIGURE_RESOURCES_MESSAGE = (
    "To configure resources for this project, run "
    "'ploomber-cloud resources' or to deploy with default "
    "configurations, run 'ploomber-cloud deploy'"
)

import questionary

from schemas import ComponentType, ApiType


prompts: dict[str, dict[str, questionary.Question]] = {
    'base': {
        'component_type': questionary.select(
            "Do you want to create a module or a project?",
            choices=[type.value for type in ComponentType]
        ),
        'api_type': questionary.select(
            "Choose the API type:",
            choices=[type.value for type in ApiType]
        ),
        'name': questionary.text(
            "Enter a name:",
            validate=lambda x: True if x.strip() != "" else "The name cannot be empty"
        ),
    },
    'project': {
        'generate_venv': questionary.confirm(
            "Create a virtual environment with installed dependencies?",
            default=False
        )
    },
    'module': {}
}


source_code_root_dir = './../templates'
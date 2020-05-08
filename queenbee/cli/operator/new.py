import os

from ...base.parser import parse_file
from ...operator import Operator

try:
    import click
    from click_plugins import with_plugins
except ImportError:
    raise ImportError(
        'click modules not installed. Try `pip install queenbee[cli]` command.'
    )

MODULE_PATH = os.path.abspath(os.path.dirname(__file__))

@click.command('new')
@click.argument('name')
@click.option(
    '-p',
    '--path',
    help='The path at which to create the new operator'
)
def new(name, path):
    """create a new operator folder"""

    folder_path = name

    if path is not None:
        folder_path = os.path.join(path, folder_path)

    folder_path = os.path.abspath(folder_path)

    if os.path.exists(folder_path):
        raise click.ClickException(f'Cannot create new operator at path {folder_path} because there is already something there')

    path = os.path.join(MODULE_PATH, "../assets/new-operator.yaml")
    input_dict = parse_file(path)
    input_dict['metadata']['name'] = name

    operator = Operator.parse_obj(input_dict)
    
    # Create entire path to folder if it does not exist
    os.makedirs(folder_path, exist_ok=True)

    operator.to_folder(folder_path=folder_path)
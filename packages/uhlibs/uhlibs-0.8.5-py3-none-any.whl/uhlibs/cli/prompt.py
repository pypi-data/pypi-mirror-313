import sys

from rich.prompt import Prompt
from rich.console import Console
from rich.theme import Theme
from rich.table import Table

def create_table(**kwargs):
    # Default values for certain parameters
    kwargs.setdefault('show_header', True)
    kwargs.setdefault('header_style', 'bold red')
    kwargs.setdefault('show_lines', False)
    kwargs.setdefault('show_edge', False)
    kwargs.setdefault('columns', {'Index': 'red', 'Option Name': 'italic'})
    columns = kwargs.pop('columns')

    # Create the table with all kwargs
    table = Table(**kwargs)

    # Add columns to the table
    for column, style in columns.items():
        table.add_column(column, style=style)

    return table

def create_theme(**kwargs):
    # Default values for certain parameters
    kwargs.setdefault('success', 'green')
    kwargs.setdefault('error', 'bold red')
    kwargs.setdefault('warning', 'yellow')
    kwargs.setdefault('info', 'italic blue')

    # Create a theme with the merged settings
    theme = Theme({**kwargs})

    return theme


def create_console(**kwargs):
    theme = kwargs.get('theme', None)
    if theme is None:
        theme = create_theme()

    console = Console(theme=theme)
    return console

# Function to prompt the user for selection
def prompt_user_selection(selection_options: list):
    """
    Prompt the user to select an option from a list.

    Args:
        selection_options (list): List of options to display to the user.

    Returns:
        obj : The selected option.
    """

    table = create_table()
    console = create_console()

    # Display the selection options in a table
    console.print('Selection Options: \n', style='bold red')

    for i, item in enumerate(selection_options):
        table.add_row(f'[{i}]', f'{item}')

    console.print(table)
    console.print('\n')

    # Get user input
    user_input = Prompt.ask(
        '[bold]Please enter the index of the item you would like to select[/bold]')

    try:
        # Convert user input to integer
        user_selection = int(user_input)
    except ValueError:
        console.print('Invalid input. Please enter a valid selection.', style="error")
        sys.exit()

    try:
        selection = selection_options[user_selection]
    except IndexError:
        console.print('Invalid selection. Please enter a number within the valid selection options.', style="error")
        sys.exit()

    console.print(f'You have selected: {selection}', style="success")

    return selection

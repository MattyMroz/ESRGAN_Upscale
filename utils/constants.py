"""
    This script defines various paths to files and folders that are used in the project.
    It also includes definitions of styles for the rich library, which is used for printing colored text in the console.

    * Example usage:
        from constants import console

    Variables:
        - console: Instance of the Console class from the rich library, defined with various styles.
"""

from rich.console import Console
from rich.theme import Theme

# Rich print styles
console: Console = Console(theme=Theme({
    "purple_bold": "purple bold",
    "purple_italic": "purple italic",
    "pink_bold": "pale_violet_red1 bold",
    "pink_italic": "pale_violet_red1 italic",
    "red_bold": "bright_red bold",
    "red_italic": "bright_red italic",
    "brown_bold": "rgb(180,82,45) bold",
    "brown_italic": "rgb(180,82,45) italic",
    "orange_bold": "rgb(255,135,70) bold",
    "orange_italic": "rgb(255,135,70) italic",
    "yellow_bold": "bright_yellow bold",
    "yellow_italic": "bright_yellow italic",
    "green_bold": "green bold",
    "green_italic": "green italic",
    "blue_bold": "dodger_blue2 bold",
    "blue_italic": "dodger_blue2 italic",
    "white_bold": "white bold",
    "white_italic": "white italic",
    "normal_bold": "bold",
    "normal_italic": "italic",
    "black_bold": "rgb(0,0,0) on white bold",
    "black_italic": "rgb(0,0,0) on white italic",
    "repr.number": "bright_red bold",
}))

# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="purple_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="purple_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="pink_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="pink_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="red_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="red_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="brown_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="brown_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="orange_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="orange_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="yellow_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="yellow_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="green_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="green_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="blue_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="blue_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="white_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="white_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="normal_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="normal_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="black_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="black_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="repr.number")
# input()

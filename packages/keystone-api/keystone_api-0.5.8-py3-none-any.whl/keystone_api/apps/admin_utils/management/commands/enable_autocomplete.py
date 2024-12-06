"""A Django management command that enables Bash autocompletion for the keystone-api command."""

import shutil
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Enable Bash autocompletion for the keystone-api commandline tool."""

    help = __doc__

    def handle(self, *args, **options) -> None:
        """Handle the command execution.

        Args:
          *args: Additional positional arguments.
          **options: Additional keyword arguments.
        """

        try:
            self._handle()

        except KeyboardInterrupt:
            print()  # Move bash prompt to a new line
            exit(1)

    def _handle(self) -> None:
        """Execute the application logic."""

        if not self.prompt_for_confirmation():
            return

        # Find the user's .bash_prf le or .bashrc file
        profile_path = self.get_profile_path()
        if profile_path is None:
            self.stderr.write(f'No .bash_profile or .bashrc file found.')
            exit(1)

        # Copy the completion script into the user's home directory
        completion_script_src = Path(__file__).parent.resolve() / 'keystone_autocomplete'
        completion_script_dest = Path.home() / '.keystone_autocomplete'
        shutil.copyfile(completion_script_src, completion_script_dest)

        # Source the completion file in the user's shell configuration
        with profile_path.open(mode='a') as file:
            file.write('\nsource ~/.keystone_autocomplete\n')

    @staticmethod
    def prompt_for_confirmation() -> bool:
        """Prompt the user to confirm executing of the parent command.

        Args:
            A boolean indicating whether the user confirmed execution.
        """

        print(
            'This command will make the following changes:\n',
            '  - A file `.keystone_autocomplete` will be add to your home directory\n'
            '  - A line of setup code will be added to your .bash_profile or .bashrc file`\n'
        )

        while True:
            answer = input('Do you want to continue? [y/N]: ').lower()
            if answer == 'y':
                return True

            elif answer in ('n', ''):
                return False

            print('Unrecognized input.')

    @staticmethod
    def get_profile_path() -> Path | None:
        """Search the user's home directory .bash_profile or .bashrc file.

        The .bash_profile file is given preference over .bashrc.

        Returns:
            The file path object if a file is found, otherwise `None`.
        """

        bash_profile_path = Path.home() / '.bash_profile'
        bashrc_path = Path.home() / '.bashrc'
        for file in (bash_profile_path, bashrc_path):
            if file.exists():
                return file

        return None

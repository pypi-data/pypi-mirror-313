from subprocess import call
import requests
import typer


def check_package_for_updates(
        pypi_package_name: str,
        internal_package_name: str,
        installed_version: str,
        auto_update_enabled: bool = False,
        warning_message_disabled: bool = False
):
    # Get version information from PyPi
    version_info = requests.get(f'https://pypi.org/pypi/{pypi_package_name}/json')
    latest_version = version_info.json()['info']['version']

    # Check if currently installed version equals the latest available on PyPi
    if latest_version != installed_version:
        # If auto update is enabled, then run update command
        if auto_update_enabled:
            typer.secho(
            f'--------------------------------------------------------------------------------------------'
                    f'\nNew {internal_package_name} version available. '
                    f'\nYour current {internal_package_name} version is {installed_version}. '
                    f'Latest version available is {latest_version}. '
                    f'\nAuto update detected, updating package now. '
                    f'\n--------------------------------------------------------------------------------------------',
                    fg="red", bold=True
            )
            # update
            call(['pip', 'install', '--upgrade'] + [pypi_package_name])
            typer.secho(
                f'{internal_package_name} update complete, please re-run previous command.',
                        fg="red", bold=True
            )
            typer.Exit()

        else:
            if not warning_message_disabled:
                typer.secho(
                f'--------------------------------------------------------------------------------------------'
                        f'\nNew {internal_package_name} version available. '
                        f'\nYour current {internal_package_name} version is {installed_version}. '
                        f'Latest version available is {latest_version}. '
                        f'\nConsider enabling auto update by running `bigeye configure set auto_update_enabled true`. '
                        f'\nTo hide this message run `bigeye configure set disable_auto_update_message true`. '
                        f'\n--------------------------------------------------------------------------------------------',
                        fg="red", bold=True
                )

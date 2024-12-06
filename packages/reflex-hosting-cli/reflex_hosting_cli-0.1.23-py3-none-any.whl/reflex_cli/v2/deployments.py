"""The Hosting CLI deployments sub-commands."""

import json
from typing import List, Optional

import httpx
import pkg_resources
import typer
from packaging import version
from tabulate import tabulate
from typing_extensions import Annotated

from reflex_cli.v2 import constants
from reflex_cli.v2.utils import console
from reflex_cli.v2.utils.exceptions import NotAuthenticatedError

hosting_cli = typer.Typer()

TIME_FORMAT_HELP = "Accepts ISO 8601 format, unix epoch or time relative to now. For time relative to now, use the format: <d><unit>. Valid units are d (day), h (hour), m (minute), s (second). For example, 1d for 1 day ago from now."
MIN_LOGS_LIMIT = 50
MAX_LOGS_LIMIT = 1000


@hosting_cli.callback()
def check_version():
    """Callback to be invoked for all hosting CLI commands.

    Checks if the installed version of the package is up-to-date with the latest version available on PyPI.
    If a newer version is available, it prints a warning message and exits.

    Raises:
        Exit: If a newer version is available, prompting the user to upgrade.
    """
    package_name = "reflex-hosting-cli"
    try:
        installed_version = pkg_resources.get_distribution(package_name).version
        response = httpx.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]

        if version.parse(installed_version) < version.parse(latest_version):
            print(
                f"Warning: You are using {package_name} version {installed_version}. "
                f"A newer version {latest_version} is available."
            )
            console.error(f"Upgrade using: pip install --upgrade {package_name}")
            raise typer.Exit(1)
    except (
        pkg_resources.DistributionNotFound,
        httpx.RequestError,
        httpx.HTTPStatusError,
    ):
        # Silently pass if we can't check the version
        pass


@hosting_cli.command(name="project-create")
def create_project(
    name: str = typer.Argument(..., help="The name of the project."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """Create a new project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    project = hosting.create_project(name=name, token=token)
    if as_json:
        console.print(json.dumps(project))
        return
    if project:
        project = [project]
        headers = list(project[0].keys())
        table = [list(p.values()) for p in project]
        console.print(tabulate(table, headers=headers))
    else:
        console.print(str(project))


@hosting_cli.command(name="project-invite")
def invite_user_to_project(
    role: str = typer.Argument(..., help="The role ID to assign to the user."),
    user: str = typer.Argument(..., help="The user ID to invite."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Invite a user to a project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    try:
        result = hosting.invite_user_to_project(role_id=role, user_id=user, token=token)
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err

    if "failed" in result:
        console.error(f"Unable to invite user to project: {result}")
        raise typer.Exit(1)
    console.success("Successfully invited user to project.")


@hosting_cli.command(name="project-select")
def select_project(
    project: str = typer.Argument(..., help="The project ID to select."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Select a project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    result = hosting.select_project(project=project, token=token)
    if "failed" in result:
        console.error(result)
        raise typer.Exit(1)
    console.success(result)


@hosting_cli.command(name="project-get-select")
def get_select_project(
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    token: Optional[str] = typer.Option(None, help="The authentication token."),
):
    """Get the currently selected project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    project = hosting.get_selected_project()
    if project:
        try:
            project_details = hosting.get_project(project_id=project, token=token)
            console.print(
                tabulate(
                    [[project, project_details["name"]]],
                    headers=["Selected Project ID", "Project Name"],
                )
            )
        except NotAuthenticatedError:
            console.error(
                "You are not authenticated. Run `reflex loginv2` to authenticate."
            )
            typer.Exit(1)
        except Exception as e:
            console.error(f"Unable to get the currently selected project: {e}")
    else:
        console.warn(
            "no selected project. run `reflex apps project-select` to set one."
        )


@hosting_cli.command(name="secrets-list")
def get_secrets(
    app_id: str = typer.Argument(..., help="The ID of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in JSON format."
    ),
):
    """Retrieve secrets for a given application."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:
        secrets = hosting.get_secrets(app_id=app_id, token=token)
        if "failed" in secrets:
            console.error(secrets)
            raise typer.Exit(1)
        if as_json:
            console.print(secrets)
            return
        if secrets:
            headers = ["Keys"]
            table = [[key] for key in secrets]
            console.print(tabulate(table, headers=headers))
        else:
            console.print(str(secrets))
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="secrets-update")
def update_secrets(
    app_id: str = typer.Argument(..., help="The ID of the application."),
    envfile: Optional[str] = typer.Option(
        None,
        "--envfile",
        help="The path to an env file to use. Will override any envs set manually.",
    ),
    envs: List[str] = typer.Option(
        list(),
        "--env",
        help="The environment variables to set: <key>=<value>. Required if envfile is not specified. For multiple envs, repeat this option, e.g. --env k1=v2 --env k2=v2.",
    ),
    reboot: bool = typer.Option(
        False,
        "--reboot",
        help="Automatically reboot your site with the new secrets",
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Update secrets for a given application."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    if envfile is None and not envs:
        console.error("--envfile or --env must be provided")
        raise typer.Exit(1)

    if envfile and envs:
        console.warn("--envfile is set; ignoring --env")

    secrets = {}

    if envfile:
        try:
            from dotenv import dotenv_values  # type: ignore

            secrets = dotenv_values(envfile)
        except ImportError:
            console.error(
                """The `python-dotenv` package is required to load environment variables from a file. Run `pip install "python-dotenv>=1.0.1"`."""
            )

    else:
        secrets = hosting.process_envs(envs)

    hosting.update_secrets(app_id=app_id, secrets=secrets, reboot=reboot, token=token)


@hosting_cli.command(name="secrets-delete")
def delete_secret(
    app_id: str = typer.Argument(..., help="The ID of the application."),
    key: str = typer.Argument(..., help="The key of the secret to delete."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    reboot: bool = typer.Option(
        False,
        "--reboot",
        help="Automatically reboot your site with the new secrets",
    ),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Delete a secret for a given application."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    try:
        result = hosting.delete_secret(
            app_id=app_id, key=key, reboot=reboot, token=token
        )
        if "failed" in result:
            console.error(result)
            raise typer.Exit(1)
        console.success("Successfully deleted secret.")
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="project-list")
def get_projects(
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """Retrieve a list of projects."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:
        projects = hosting.get_projects(token=token)
        if as_json:
            console.print(json.dumps(projects))
            return
        if projects:
            headers = list(projects[0].keys())
            table = [list(project.values()) for project in projects]
            console.print(tabulate(table, headers=headers))
        else:
            # If returned empty list, print the empty
            console.print(str(projects))
    except NotAuthenticatedError:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        typer.Exit(1)
    except Exception as e:
        console.error(f"Unable to get projects: {e}")
        raise typer.Exit(1) from e


@hosting_cli.command(name="project-usage")
def get_project_usage(
    project_id: Optional[str] = typer.Option(
        None,
        help="The ID of the project. If not provided, the selected project will be used. If no project is selected, it throws an error.",
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in JSON format."
    ),
):
    """Retrieve the usage statistics for a project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    try:
        if project_id is None:
            project_id = hosting.get_selected_project()
        if project_id is None:
            console.error(
                "no project_id provided or selected. Set it with `reflex apps project-usage --project-id \\[project_id]`"
            )
            raise typer.Exit(1)

        usage = hosting.get_project_usage(project_id=project_id, token=token)

        if as_json:
            console.print(json.dumps(usage))
            return
        if usage:
            headers = ["Deployments", "CPU (cores)", "Memory (gb)"]
            table = [
                [
                    f'{usage["deployment_count"]}/{usage["tier"]["deployment_quota"]}',
                    f'{usage["cpu_usage"]}/{usage["tier"]["cpu_quota"]}',
                    f'{usage["memory_usage"]}/{usage["tier"]["ram_quota"]}',
                ]
            ]
            console.print(tabulate(table, headers=headers))
        else:
            # If returned empty list, print the empty
            console.print(str(usage))
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="project-roles")
def get_project_roles(
    project_id: Optional[str] = typer.Option(
        None,
        help="The ID of the project. If not provided, the selected project will be used. If no project_id is provided or selected throws an error.",
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """Retrieve the roles for a project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:
        if project_id is None:
            project_id = hosting.get_selected_project()
        if project_id is None:
            console.error(
                "no project_id provided or selected. Set it with `reflex apps project-roles --project-id \\[project_id]`"
            )
            raise typer.Exit(1)

        roles = hosting.get_project_roles(project_id=project_id, token=token)

        if as_json:
            console.print(json.dumps(roles))
            return
        if roles:
            headers = list(roles[0].keys())
            table = [list(role.values()) for role in roles]
            console.print(tabulate(table, headers=headers))
        else:
            # If returned empty list, print the empty
            console.print(str(roles))
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="project-role-permissions")
def get_project_role_permissions(
    role_id: str = typer.Argument(..., help="The ID of the role."),
    project_id: Optional[str] = typer.Option(
        None,
        help="The ID of the project. If not provided, the selected project will be used. If no project is selected, it throws an error.",
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """Retrieve the permissions for a specific role in a project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    try:
        if project_id is None:
            project_id = hosting.get_selected_project()
        if project_id is None:
            console.error(
                "no project_id provided or selected. Set it with `reflex apps project-role-permissions --project-id \\[project_id]`."
            )
            raise typer.Exit(1)

        permissions = hosting.get_project_role_permissions(
            project_id=project_id, role_id=role_id, token=token
        )

        if as_json:
            console.print(json.dumps(permissions))
            return
        if permissions:
            headers = list(permissions[0].keys())
            table = [list(permission.values()) for permission in permissions]
            console.print(tabulate(table, headers=headers))
        else:
            # If returned empty list, print the empty
            console.print(str(permissions))
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="project-users")
def get_project_role_users(
    project_id: Optional[str] = typer.Option(
        None,
        help="The ID of the project. If not provided, the selected project will be used. If no project is selected, it throws an error.",
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """Retrieve the users for a project."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:
        if project_id is None:
            project_id = hosting.get_selected_project()
        if project_id is None:
            console.error(
                "no project_id provided or selected. Set it with `reflex apps project-users --project-id \\[project_id]`"
            )
            raise typer.Exit(1)

        users = hosting.get_project_role_users(project_id=project_id, token=token)

        if as_json:
            console.print(json.dumps(users))
            return
        if users:
            headers = list(users[0].keys())
            table = [list(user.values()) for user in users]
            console.print(tabulate(table, headers=headers))
        else:
            # If returned empty list, print the empty
            console.print(str(users))
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="history")
def app_history(
    app_id: str = typer.Argument(..., help="The ID of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """Retrieve the deployment history for a given application."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    try:
        history = hosting.get_app_history(app_id=app_id, token=token)

        if as_json:
            console.print(json.dumps(history))
            return
        if history:
            headers = list(history[0].keys())
            table = [list(deployment.values()) for deployment in history]
            console.print(tabulate(table, headers=headers))
        else:
            console.print(str(history))
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="app-status")
def app_status(
    app_id: str,
    token: Optional[str] = None,
    loglevel: constants.LogLevel = typer.Option(
        constants.LogLevel.INFO, help="The log level to use."
    ),
):
    """Retrieve the status of a specific app."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:
        status = hosting.get_app_status(app_id=app_id, token=token)
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err
    except Exception as e:
        status = f"Unable to get app status: {e}"

    console.info(status)

    return None


@hosting_cli.command("build-logs")
def deployment_build_logs(
    deployment_id: str = typer.Argument(..., help="The ID of the deployment."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
):
    """Retrieve the build logs for a specific deployment."""
    from reflex_cli.v2.utils import hosting

    try:
        logs = hosting.get_deployment_build_logs(
            deployment_id=deployment_id, token=token
        )
        console.print(logs)
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command("vmtypes")
def get_vm_types(
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """Retrieve the available VM types."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    vmtypes = hosting.get_vm_types()
    if as_json:
        console.print(json.dumps(vmtypes))
        return
    if vmtypes:
        ordered_vmtpes = []
        for vmtype in vmtypes:
            ordered_vmtpes.append(
                {key: vmtype.get(key) for key in ["id", "name", "cpu", "ram"]}
            )
        headers = list(["id", "name", "cpu (cores)", "ram (gb)"])
        table = [list(vmtype.values()) for vmtype in ordered_vmtpes]
        console.print(tabulate(table, headers=headers))
    else:
        console.print(str(vmtypes))


@hosting_cli.command(name="regions")
def get_deployment_regions(
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
):
    """List all the regions of the hosting service.
    Areas available for deployment are:
    ams	Amsterdam, Netherlands
    arn	Stockholm, Sweden
    atl	Atlanta, Georgia (US)
    bog	Bogotá, Colombia
    bom	Mumbai, India
    bos	Boston, Massachusetts (US)
    cdg	Paris, France
    den	Denver, Colorado (US)
    dfw	Dallas, Texas (US)
    ewr	Secaucus, NJ (US)
    eze	Ezeiza, Argentina
    fra	Frankfurt, Germany
    gdl	Guadalajara, Mexico
    gig	Rio de Janeiro, Brazil
    gru	Sao Paulo, Brazil
    hkg	Hong Kong, Hong Kong
    iad	Ashburn, Virginia (US)
    jnb	Johannesburg, South Africa
    lax	Los Angeles, California (US)
    lhr	London, United Kingdom
    mad	Madrid, Spain
    mia	Miami, Florida (US)
    nrt	Tokyo, Japan
    ord	Chicago, Illinois (US)
    otp	Bucharest, Romania
    phx	Phoenix, Arizona (US)
    qro	Querétaro, Mexico
    scl	Santiago, Chile
    sea	Seattle, Washington (US)
    sin	Singapore, Singapore
    sjc	San Jose, California (US)
    syd	Sydney, Australia
    waw	Warsaw, Poland
    yul	Montreal, Canada
    yyz	Toronto, Canada.
    """
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    list_regions_info = hosting.get_regions()
    if as_json:
        console.print(json.dumps(list_regions_info))
        return
    if list_regions_info:
        headers = list(list_regions_info[0].keys())
        table = [list(deployment.values()) for deployment in list_regions_info]
        console.print(tabulate(table, headers=headers))


@hosting_cli.command(name="status")
def deployment_status(
    deployment_id: str = typer.Argument(..., help="The ID of the deployment."),
    watch: Optional[bool] = typer.Option(
        False, help="Whether to continuously watch the status."
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Retrieve the status of a specific deployment."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:

        if watch:
            hosting.watch_deployment_status(deployment_id=deployment_id, token=token)
        else:
            status = hosting.get_deployment_status(
                deployment_id=deployment_id, token=token
            )
            console.error(status) if "failed" in status else console.print(status)
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="stop")
def stop_app(
    app_id: str = typer.Argument(..., help="The ID of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Stop a running application."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:
        result = hosting.stop_app(app_id=app_id, token=token)
        if result:
            console.error(result) if "failed" in result else console.success(result)
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="start")
def start_app(
    app_id: str = typer.Argument(..., help="The ID of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Start a stopped application."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)

    try:
        result = hosting.start_app(app_id=app_id, token=token)
        if result:
            console.error(result) if "failed" in result else console.success(result)
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="delete")
def delete_app(
    app_id: str = typer.Argument(
        ..., help="The ID of the application. Exception thrown if no app_id is provided"
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Delete an application."""
    from reflex_cli.v2.utils import hosting

    if not app_id:
        console.error("No app_id provided.")
        raise typer.Exit(1)

    console.set_log_level(loglevel)
    try:

        result = hosting.delete_app(app_id=app_id, token=token)
        if result:
            console.warn(result)
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="logs")
def app_logs(
    app_id: str = typer.Argument(
        ...,
        help="The ID of the application. If no app_id is provided start/end must both be provided.",
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    offset: Optional[int] = typer.Option(
        None, help="The offset in seconds from the current time."
    ),
    start: Optional[int] = typer.Option(
        None, help="The start time in Unix epoch format."
    ),
    end: Optional[int] = typer.Option(None, help="The end time in Unix epoch format."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Retrieve logs for a given application."""
    from reflex_cli.v2.utils import hosting

    if not app_id:
        console.error("No app_id provided.")
        raise typer.Exit(1)
    if offset is None and start is None and end is None:
        offset = 3600
    if offset is not None and start or end:
        console.error("must provide both start and end")
        raise typer.Exit(1)

    console.set_log_level(loglevel)

    try:
        result = hosting.get_app_logs(
            app_id=app_id, offset=offset, start=start, end=end, token=token
        )
        if result:
            if isinstance(result, list):
                result.reverse()
                for log in result:
                    console.warn(log)
            else:
                console.warn("Unable to retrieve logs.")
    except NotAuthenticatedError as err:
        console.error(
            "You are not authenticated. Run `reflex loginv2` to authenticate."
        )
        raise typer.Exit(1) from err


@hosting_cli.command(name="list")
def list_apps(
    project: Optional[str] = typer.Option(
        None, help="The project ID to filter deployments."
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in JSON format."
    ),
):
    """List all the hosted deployments of the authenticated user. Will exit if unable to list deployments."""
    from reflex_cli.v2.utils import hosting

    console.set_log_level(loglevel)
    if project is None:
        project = hosting.get_selected_project()
    try:
        deployments = hosting.list_apps(project=project, token=token)
    except Exception as ex:
        console.error("Unable to list deployments")
        raise typer.Exit(1) from ex

    if as_json:
        console.print(json.dumps(deployments))
        return
    if deployments:
        headers = list(deployments[0].keys())
        table = [list(deployment.values()) for deployment in deployments]
        console.print(tabulate(table, headers=headers))
    else:
        console.print(str(deployments))

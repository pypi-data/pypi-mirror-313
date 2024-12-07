import json
import sys

import click
from rich.console import Console
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from .api import rucio_list_content, rucio_list_dids, rucio_list_file_replicas
from .util import parse_did_filter_from_string_fe

console = Console()

@click.group()
def cli():
    """CLI for interacting with Rucio server without authentication."""
    pass

@cli.command()
@click.argument("did", required=True, type=str)
@click.option(
    "--filter", 
    default=None, 
    help="Optional filter to apply to the DIDs."
)
def list_dids(did, filter):
    """List DIDs by calling the FastAPI server."""
    table_data = []
    try:
        scope, name = did.split(":")
    except ValueError:
        click.echo("Error: DID should be in 'scope:name' format.")
        return
    try:
        filters, type_ = parse_did_filter_from_string_fe(filter, name)
    except ValueError:
        click.echo("Error: DID should be in 'scope:name' format.")
        return
    #except InvalidType as error:
    #    click.echo(error)
    #    return
    #except DuplicateCriteriaInDIDFilter as error:
    #    click.echo(error)
    #    return
    except SyntaxError as error:
        click.echo(error)
        return
    except ValueError as error:
        click.echo(error)
        return
    except Exception as e:
        click.echo(e)
        return

    result = rucio_list_dids(scope, filters=filters, did_type=type_, long=True)
    for did in result:
        if "error" in did:
            console.print(f"[bold red]Error: {did['error']}[/bold red]")
            if "status_code" in did:
                console.print(f"HTTP Status Code: {did['status_code']}")
            continue
        else:
            table_data.append([f"{did['scope']}:{did['name']}", Text(did['did_type'])])
    # table = generate_table(table_data, headers=['SCOPE:NAME', '[DID TYPE]'], col_alignments=['left', 'left'])
    
    if not table_data:
        console.print("[bold yellow]No DIDs found or errors occurred.[/bold yellow]")
        return
    # Generate and print the table using rich
    table = Table(title="DID List")
    table.add_column("SCOPE:NAME", justify="left")
    table.add_column("DID TYPE", justify="left")

    for row in table_data:
        table.add_row(row[0], row[1])
    console.print(table)
    # print_output(table, console=console, no_pager=args.no_pager)

@cli.command()
@click.argument("dids", required=True, nargs=-1, type=str)
def list_content(dids):
    table_data = []
    try:
        did_list = list(dids)
    except ValueError:
        click.echo("Error: DIDs should be comma separated did as 'scope:name' format.")
        return

    for did in did_list:
        try:
            did.split()
            scope, name = did.split(":")
        except ValueError:
            click.echo("Error: DIDs should be comma separated did as 'scope:name' format.")
            return 
        contents =  rucio_list_content(scope, name=name)
        for content in  contents:
            if "error" in content:
                console.print(f"[bold red]Error: {content['error']}[/bold red]")
                if "status_code" in did:
                    console.print(f"HTTP Status Code: {content['status_code']}")
                continue
            else:
                table_data.append([f"{content['scope']}:{content['name']}", Text(content['type'].upper())])
    if not table_data:
        console.print("[bold yellow]No DIDs found or errors occurred.[/bold yellow]")
        return
    # Generate and print the table using rich
    table = Table(title="DID List")
    table.add_column("SCOPE:NAME", justify="left")
    table.add_column("DID TYPE", justify="left")

    for row in table_data:
        table.add_row(row[0], row[1])
    console.print(table)

@cli.command()
@click.argument("dids", required=True, nargs=-1, type=str)
@click.option("--protocols", default=None, type=str, help="List of comma separated protocols. (i.e. https, root, srm)")
@click.option("--rses", default=None, type=str, help="Restrict replicas to a set of RSEs using rses expression.")
@click.option("--pfns", default=False, type=bool, is_flag=True, help="Show only the PFNs.")
#@click.option("--metalink", default=False, type=bool, help="Retrieve as metalink4+xml.")
@click.option("--all_states", default=False, type=bool,is_flag=True, help="Select all replicas (including unavailable ones).")
@click.option("--no_resolve_archives", default=True, type=bool, help="Find archives containing the replicas.")
@click.option("--domain", default=None, type=str, help="Define the domain. Default is 'wan'.")
@click.option("--sort", default=None, type=str, help="Replica sort algorithm. Options: geoip (default), random.")
def list_file_replicas(
    dids, protocols, rses, pfns, all_states, no_resolve_archives, domain, sort
):
    # Prepare the DIDs as list of dictionaries
    did_list = []
    for did in list(dids):
        try:
            did.split()
            scope, name = did.split(":")
            did_list.append({"scope": str(scope), "name": str(name)})
        except ValueError:
            click.echo("Error: DID should be in 'scope:name' format.")
            sys.exit(1)

    # Call the list_file_replicas function
    try:

        response_data = rucio_list_file_replicas(
            dids=did_list,
            schemes=protocols,
            rse_expression=rses,
            all_states=all_states,
            no_resolve_archives=no_resolve_archives,
            domain=domain,
            sort=sort,
        )
        table_data = []
        table = Table()

        if pfns:
            table.add_column("PFN")
        else:
            table.add_column("SCOPE")
            table.add_column("NAME")
            table.add_column("FILESIZE", justify="right", width=15)
            table.add_column("ADLER32", width=10)
            table.add_column("RSE: REPLICA")
        for replica in response_data:
            if "error" in replica:
                console.print(f"[bold red]Error: {replica['error']}[/bold red]")
                if "status_code" in did:
                    console.print(f"HTTP Status Code: {replica['status_code']}")
                continue
            else:
                if pfns:
                    for pfn in replica['pfns']:
                        rse = replica['pfns'][pfn]['rse']
                        if replica['rses'][rse]:
                            table_data.append(pfn)
                            table.add_row(pfn)
                else:
                    try:
                        rse_key = next(iter(replica['rses'].keys()))
                        replica_url = replica['rses'][rse_key][0]
                        rse_replica = f"{rse_key}: {replica_url}"
                        filesize = f"{replica['bytes']} B"
                        table_data.append([
                            replica['scope'],  # SCOPE
                            replica['name'],  # NAME
                            filesize,  # FILESIZE
                            replica['adler32'],  # ADLER32
                            rse_replica  # RSE: REPLICA
                        ])
                    except Exception as e:
                        console.print(f"[bold red]Error:[/bold red] {str(e)}")
                    # Generate and print the table using rich

                    table.add_row(
                        replica['scope'],  # SCOPE
                        replica['name'],  # NAME
                        filesize,  # FILESIZE
                        replica['adler32'],  # ADLER32
                        rse_replica  # RSE: REPLICA
                    )
        if not table_data:
            console.print("[bold yellow]No DIDs found or errors occurred.[/bold yellow]")
            return
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")



if __name__ == "__main__":
    cli()

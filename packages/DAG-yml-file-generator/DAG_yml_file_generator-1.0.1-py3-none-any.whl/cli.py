import click
import os
import yaml
import re
from tools.utils.build_index import builddex
from tools.utils.validate import validate

def name_present(engineers, name):
    present = False
    for engineer in engineers:
        if str(engineer['name']).lower() == str(name).lower():
            present = True
    return present

def extract_params(path):
    pattern = r'{{\s*params\.(\w+)\s*}}'
    with open(path, 'r') as file:
        sql_content = file.read()
    matches = re.findall(pattern, sql_content)
    unique = set(matches)
    return unique


@click.group(help="")
def awehflow():
    '''main command'''
    pass

@awehflow.command()
@click.option("-sql", "--path-to-sql", default=None, help="Specify the path to the SQL file", type=str)
def BuildDag(path_to_sql):

    partitioning_field = None
    partitioning_type = None
    cluster_fields = []
    param_fields = extract_params(path_to_sql)


    dag_name = click.prompt("Dag Name", type=str, default='', show_default=False)
    params = {key: None for key in param_fields}
    for key in params:
        params[key] = click.prompt(f"{key}", default='', show_default=False)
    if click.confirm("Partitioning?", default=False):
        partitioning_type = click.prompt("type", type=str, default='', show_default=False)
        partitioning_field = click.prompt("field", type=str, default='', show_default=False)
    if click.confirm("Clustering?", default=False):
        num_fields = click.prompt("How many clustering fields?")
        if int(num_fields)>4:
            click.echo("max number of fields: 4")
        for i in range(min(int(num_fields),4)):
            cluster_input = click.prompt("Enter field", type=str)
            cluster_fields.append(cluster_input)
    folder_name = os.path.basename(os.path.dirname(path_to_sql))

    base_yml_path = 'configs/base.yml'
    with open(base_yml_path, "r") as f:
        data = yaml.safe_load(f)
    catchup = str(data['catchup']).lower()
    if click.confirm(f"catchup: {data['catchup']}. Would you like to change this?"):
        catchup = 'true'

    engineers = data['engineers']
    click.echo("Engineers:")
    for engineer in data["engineers"]:
        click.echo(f" - {engineer['name']}")
    while click.confirm("Would you like to add or remove Engineers?", default=True):
        choice = click.prompt("Type add or delete")
        if not (str(choice).lower() == 'add' or str(choice).lower() == 'delete'):
            click.echo("Please enter a valid choice: 'add' or 'delete'")
            
        elif str(choice).lower() == 'add':
            name = click.prompt("name")
            email = click.prompt("email")
            slack = click.prompt("slack")
            new_eng = {
                "name": name,
                "email": email,
                "slack": slack
            }
            engineers.append(new_eng)
            click.echo("ENGINEERS:")
            for engineer in engineers:
                click.echo(f" - {engineer['name']}")

        elif str(choice).lower() == 'delete':
            for engineer in engineers:
                click.echo(f" - {engineer['name']}")
            del_name = click.prompt("type name of engineer to delete")
            if name_present(engineers, del_name):
                engineers = [entry for entry in engineers if entry['name'] != del_name] 
                click.echo(f"deleted engineer {del_name}")
                click.echo("\n")
                click.echo("ENGINEERS:")
                for engineer in engineers:
                    click.echo(f" - {engineer['name']}")
            else:
                click.echo(f"{del_name} not found. Please enter a valid name.")

    dag_args = data['default_dag_args']
    dag_args['use_legacy_sql'] = str( dag_args['use_legacy_sql'] ).lower()
    click.echo("Default Dag Args:")

    click.echo(f" 1 - gcp_conn_id: {dag_args['gcp_conn_id']}")
    click.echo(f" 2 - write_disposition: {dag_args['write_disposition']}")
    click.echo(f" 3 - use_legacy_sql: {dag_args['use_legacy_sql']}")

    while click.confirm("Would you like to change Default Dag Args", default=True):

        choice = click.prompt("enter the number as above (1,2,3) you would like to edit")
        choice = int(choice)
        if not (choice == 1 or choice == 2 or choice == 3 ):
            click.echo("Please enter a valid option: 1,2,3") 
        elif choice == 1:
            dag_args['gcp_conn_id'] = click.prompt("gcp_conn_id: ")
        elif choice == 3:
            if str(dag_args['use_legacy_sql']).lower() == 'true':
                dag_args['use_legacy_sql'] = 'false'
            else: dag_args['use_legacy_sql'] = 'true'
        elif choice == 2:
            dag_args['write_disposition'] = click.prompt("write_disposition: ")

        click.echo("Default Dag Args:")
        click.echo(f" 1 - gcp_conn_id: {dag_args['gcp_conn_id']}")
        click.echo(f" 2 - write_disposition: {dag_args['write_disposition']}")
        click.echo(f" 3 - use_legacy_sql: {dag_args['use_legacy_sql']}")
        
    



    inputs =  {
        "dag_name": dag_name,
        "engineers": engineers,
        "params": params,
        "partitioning_type": partitioning_type,
        "partitioning_field": partitioning_field,
        "cluster_fields" : cluster_fields,
        "sql_path": path_to_sql,
        "folder_name": folder_name,
        "catchup": catchup,
        "dag_args": dag_args
    }
    
    builddex(inputs)

@awehflow.command()
@click.option("-sql", "--path-to-sql", default=None, help="Specify the path to the SQL file", type=str)
@click.option("-index", "--path-to-index", default=None, help="Specify path to index.yml file", type=str)
def validate_dag(path_to_sql, path_to_index):
    validate(path_to_sql, path_to_index)
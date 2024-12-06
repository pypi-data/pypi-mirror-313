import logging

import civis

log = logging.getLogger(__name__)


class CivisUtilsError(ValueError):
    pass


class DBFunctionError(ValueError):
    pass


def create_client(api_key):
    if api_key is None:
        raise CivisUtilsError("Civis API key is missing")

    client = civis.APIClient(api_key)

    # INFO: Verify that the api key is valid and log user
    client_user = client.users.list_me()
    log.info(f"Civis client successfully created for {client_user.name}")

    return client


def map_columns_to_values(table_columns, table):
    """
    Maps column names to rows of values
    Parameters:
        table_columns (list): List of table columns
        table (list of lists): Contains lists of rows of values
    Returns:
        list: List of dictionaries

    Example:
        table_columns = ['id', 'name']
        table = [
            [1, 'Alice'],
            [2, 'Bob'],
            [3, 'Carol'],
        ]

        map_columns_to_values(table_columns, table) = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
            {'id': 3, 'name': 'Carol'},
        ]
    """
    dict_list = []

    for row in table:
        if len(table_columns) != len(row):
            raise ValueError("Number of columns must be equal to the number of values")

        result_dict = {column: row for column, row in zip(table_columns, row)}
        dict_list.append(result_dict)

    return dict_list


def query_civis(client, query, params, civis_database):
    """
    SQL query wrapper
    Parameters:
        client (APIClient): Civis API client
        query (str): Sql query
        params (dict): Dictonary of parameters
        civis_database (str): Name of civis database being queried
    Returns:
        list: List of dictionaries representing each row of result from 'read_civis_sql()'
    """
    try:
        sql_params_arguments = {"params": params}
        res = civis.io.read_civis_sql(query, civis_database, sql_params_arguments=sql_params_arguments, client=client)
        res_dict = map_columns_to_values(res[0], res[1:])
        return res_dict
    except Exception as err:
        raise DBFunctionError(f"Query failed: {err}")


def insert(client, insert_query, insert_params, civis_database):
    """
    Executes insert query and returns inserted id (assumes single row)
    Parameters:
        client (APIClient): Civis API client
        insert_query (str): Sql query
        insert_params (dict): Dictonary of parameters
        civis_database (str): Name of civis database being queried
    Returns:
        id: Result id
    """
    try:
        res = query_civis(client, insert_query, insert_params, civis_database)
        return res[0]['id']
    except Exception as err:
        raise DBFunctionError(f"Error occured performing insert query: {err}")

        
def select(client, select_query, select_params, civis_database):
    '''
    Execute seelct query and return results
    Parameters:
        client (APIClient): Civis API client
        insert_query (str): Sql query
        insert_params (dict): Dictonary of parameters
        civis_database (str): Name of civis database being queried
    Returns:
        id: Result of query
    '''
    try:
        res = query_civis(client, select_query, select_params, civis_database)
        return res
    except Exception as err:
        raise DBFunctionError(f"Error occured performing select query: {err}")

import logging
import pyodbc

log = logging.getLogger(__name__)

# This page has instructions for installing ODBC 17 & 18; my Windows laptop uses 17 & connects ok
# Debian "bookworm" (container image) == Debian 12
# https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server
DEFAULT_ODBC_DRIVER = '{ODBC Driver 18 for SQL Server}'
# echo msodbcsql18 msodbcsql/ACCEPT_EULA boolean true | sudo debconf-set-selections
# curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
# curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
# ** FAILED WITH KEY ERROR: sudo apt-get update ** NEXT LINE NOT FROM MICROSOFT
# sudo sed -i 's#/usr/share/keyrings/microsoft-prod.gpg#/etc/apt/trusted.gpg.d/microsoft.asc#' /etc/apt/sources.list.d/mssql-release.list
# sudo apt-get update                                 # now it should work
# sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
# echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
# sudo apt-get install -y unixodbc-dev
# sudo apt-get install -y libgssapi-krb5-2

DESCRIBE_TABLE_QUERY = """
    SELECT COLUMN_NAME, COLUMN_DEFAULT, IS_NULLABLE, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
    FROM information_schema.columns
    WHERE TABLE_NAME = ?
    ORDER BY ORDINAL_POSITION
"""

LIST_TABLES_QUERY = """
    SELECT DISTINCT TABLE_NAME
    FROM information_schema.columns
    ORDER BY TABLE_NAME
"""

def mkconnstr(host, dbname, username, password, driver=""):
    # in case e.g. STRIKEDB_ODBC_DRIVER is set to "" & passed in as empty
    # string, check for truthy value rather than adding default to signature
    if not driver:
        driver = DEFAULT_ODBC_DRIVER
    return ''.join([
        f'DRIVER={driver};',
        f'SERVER={host};',
        f'DATABASE={dbname};',
        f'UID={username};',
        f'PWD={password};',
        'TrustServerCertificate=yes',  # yuck
    ])

# https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
def get_cursor(connection_string, **connect_kwargs):
    with pyodbc.connect(connection_string, **connect_kwargs) as conn:
        log.info(f"conn = {conn}")
        # TODO: REVIEW THIS
        # Added in the belief that we want utf-8 everywhere
        # This page makes it sound like SQL Server probably does the right thing
        # https://github.com/mkleehammer/pyodbc/wiki/Unicode
        conn.setencoding('utf-8')
        with conn.cursor() as cur:
            return cur

def describe_table(cursor, table_name):
    """returns list of 5-tuples, one for each column in table:

    (column_name, default_value, is_nullable, data_type, max_len)"""
    result = cursor.execute(DESCRIBE_TABLE_QUERY, table_name).fetchall()
    return result

def list_tables(cursor):
    """returns list of table names"""
    result = cursor.execute(LIST_TABLES_QUERY).fetchall()
    return result

def exec_query(cur, sql, *args, as_generator=False):
    cur.execute(sql, *args)
    log.info(f"cur = {cur}")
    if as_generator:
        row = True
        while row:
            row = cur.fetchone()
            if row:
                yield row
    else:
        return cur.fetchall()

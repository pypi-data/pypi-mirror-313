"""
    db.py
    DB Class

    ...

    json types are possible as inputs, just pass a python dict as field value

"""
import asyncio
import asyncpg
import datetime
import re
from pathlib import Path
import orjson
import numpy as np
from dl2050utils.core import listify, oget, check_str, check_dict, check, now
from dl2050utils.log import BaseLog
from dl2050utils.fs import pickle_save, pickle_load

# TODO
#  - ERROR: Invalid input sinxtax for type int when input=='' ('' must be converted in NULL)
#  - db should Raise Error on insert/update/delete failures
#  - SELECT: nrows: returning 2 for results with one row, and 1 instead of zero when there are no results
#  - Consider unifying fs and sfs

# ####################################################################################################
# Helper functions
# ####################################################################################################

def strip(e):
    """Removes single and double quotes, and newlines from a string.
    Args: e (str): String to process.
    Returns: str: Cleaned string.
    """
    if type(e) != str:
        return e
    e = e.replace("'", "")
    e.replace('"', "")
    e.replace("\n", " ")
    return e

def get_repr(e):
    """Converts different data types into their SQL representation.
    Args: e: Value to convert.
    Returns: str: SQL-compatible representation of `e`.
    """
    if e is None:
        return "null"
    if type(e) == str:
        return f"'{strip(e)}'"
    if type(e) in [int, float]:
        return str(e)
    if type(e) == asyncpg.pgproto.pgproto.UUID:
        return f"'{e}'"
    if type(e) == datetime.datetime:
        s = e.strftime("%Y-%m-%d %H:%M:%S")
        return f"'{s}'"
    if type(e) == np.str_:
        return f"'{strip(str(e))}'"
    if np.issubdtype(type(e), np.str_):
        return f"'{strip(str(e))}'"
    if np.issubdtype(type(e), np.integer) or np.issubdtype(type(e), np.floating):
        return str(e)
    if type(e) == list:
        items = [f'"{str(e1)}"' for e1 in e]
        return f"'{{{' ,'.join(items)}}}'"
    if type(e) == dict:
        s = orjson.dumps(e, option=orjson.OPT_SERIALIZE_NUMPY).decode()
        return f"'{s}'"
    return str(e)


def fix_types(d):
    """Converts values in dict `d` to strings for compatibility with database storage.

    Args:
        d (dict): Dictionary to process.

    Returns:
        dict: Updated dictionary with standardized types.
    """
    for k in d.keys():
        if isinstance(d[k], str):
            d[k] = d[k].strip()
        if isinstance(d[k], datetime.datetime):
            d[k] = d[k].strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(d[k], datetime.date):
            d[k] = d[k].strftime("%Y-%m-%d")
    return d


def parse_filters(fs, tbl):
    """
    Filters can be either a list of dicts or a dict.
    When a dict, all attrs/values represent key,val conditions. dict filter is converted in list filters.
    List filter are lists with dict with one filter condition each, with col,val attrs, and optionally the op attr.
    The op attr can be =,<,>,<=,>=,!=
    """
    if fs is None or type(fs) != dict and type(fs) != list:
        return []
    if type(fs) == dict:
        fs = [{"col": e, "val": fs[e]} for e in fs]
    if type(fs) == list:
        fs2 = []
        for e in fs:
            f = check_dict(e, keys=["col", "val", "op"])
            if f is not None and "col" in f and "val" in f:
                f2 = {
                    "col": f"{tbl}.{f['col']}",
                    "val": f["val"],
                    "op": oget(f, ["op"], "="),
                }
                fs2.append(f2)
        return fs2
    if type(fs) == dict:
        return [
            {"col": check_str(e, n=1024), "val": check(fs[e]), "op": "="} for e in fs
        ]
    return []


def parse_join(join):
    """
    Used to filter the results based on a condition col=val in a join tbl.
    join is a dict with attrs:
        tbl2: the join tbl
        key1: the master tbl join col
        key2: the join tbl key
        col: col where condition is testes
        val: val of the condition
    Example:
        {'tbl2':'orgs', 'key1':'org', 'key2':'id', 'col':'name', 'val':'MHR'}
    """
    cols = ["tbl2", "key1", "key2", "col", "val"]
    if type(join) != dict:
        return None
    join2 = {**join}
    for e in cols:
        if e not in join2:
            return None
    return {e: check(join2[e]) for e in cols}


def parse_lookups(lookups):
    """
    Used to join with lookup tbls on lookup cols and extract lookup vals.
    lookups is a list of dicts with attrs:
        col: the lookup col from the master tbl
        tbl: the lookup tbl
        key: the key col of the lookup tbl, optional, defaults to id
        val: the val col of the lookup tbl, optional, defaults to name
    Example:
        [{'col':'org', 'tbl':'orgs', 'key':'id', 'val':'name',}]
    """
    if type(lookups) != list or not len(lookups):
        return []
    cols = ["col", "tbl", "key", "val"]
    lookups2 = []
    for l in lookups:
        if "col" not in l or "tbl" not in l:
            continue
        l["key"] = oget(l, ["key"], "id")
        l["val"] = oget(l, ["val"], "name")
        l2 = {e: check(l[e]) for e in cols}
        lookups2.append(l2)
    return lookups2


def get_select_q(
    tbl,
    join=None,
    lookups=None,
    filters=None,
    sfilters=None,
    cols=None,
    sort=None,
    ascending=True,
    offset=None,
    limit=None,
):
    """Constructs an SQL SELECT query with join and filtering options.

    Args:
        tbl (str): Table name.
        join, lookups, filters, sfilters: Join and filtering options.
        cols (list[str], optional): Columns to select.
        sort (str, optional): Column to sort by.
        ascending (bool, optional): Sort direction.
        offset, limit (int, optional): Pagination.

    Returns:
        str: SQL query string.
    """
    qcols = f"{tbl}.*" if cols is None else ", ".join(cols)
    # Parse filters and sfilters
    fs, sfs = parse_filters(filters, tbl), parse_filters(sfilters, tbl)
    # Insert filter by join condition
    qjoins = ""
    join = parse_join(join)
    if join is not None:
        qjoins += f" JOIN {join['tbl2']} ON {tbl}.{join['key1']}={join['tbl2']}.{join['key2']}"
        fs.append(
            {"col": f"{join['tbl2']}.{join['col']}", "val": join["val"], "op": "="}
        )
    # Insert lookups
    lookups = parse_lookups(lookups)
    for l in lookups:
        qcols += f", {tbl}.{l['col']} as {l['col']}_id, {l['tbl']}.{l['val']} as {l['col']}_name"
        qjoins += " LEFT OUTER JOIN "
        key_col = 'id' if 'key' not in l else l['key']
        qjoins += f"{l['tbl']} ON {tbl}.{l['col']}={l['tbl']}.{key_col} "
    # Prepare full filters and sfilters
    qwhere = ""
    if len(fs):
        qcond = " AND ".join([f"{e['col']}{e['op']}{get_repr(e['val'])}" for e in fs])
        qwhere = f" WHERE {qcond}"
    if len(sfs):
        qwhere += " WHERE " if not len(fs) else " AND "
        qwhere += " AND ".join([f"{e['col']} ILIKE '%{e['val']}%'" for e in sfs])
    # Insert order
    qorder = ""
    if isinstance(sort, str):
        qorder = f" ORDER BY {sort} " + ("ASC" if ascending else "DESC")
    # Insert offset and limit
    qpag = ""
    offset, limit = offset or 0, limit or 32
    if offset is not None:
        qpag += f" OFFSET {offset}"
    if limit is not None:
        qpag += f" LIMIT {limit}"
    # Prepare query and replace every '=null' by ' is null'
    q = f"SELECT {qcols} FROM {tbl}{qjoins}{qwhere}{qorder}{qpag};"
    q = re.sub(r"=null", " is null", q, flags=re.IGNORECASE)
    return q


def prep_query(q):
    """Ensures a LIMIT clause is present for SELECT queries.

    Args:
        q (str): SQL query string.

    Returns:
        str: Updated SQL query string with LIMIT clause if missing.
    """

    q = q.strip()
    if q[:6].upper() != "SELECT":
        return q
    has_semicolon = q.endswith(";")
    # If there's a semicolon, remove it temporarily
    if has_semicolon:
        q = q[:-1].strip()
    # Check if the query already contains 'LIMIT <int>' and append if not
    if not re.search(r"LIMIT \d+$", q, re.IGNORECASE):
        q += " LIMIT 32"
    # Re-append the semicolon if it was originally there
    if has_semicolon:
        q += ";"
    return q


async def calc_query_rows(con, q):
    """
    Returns the exepected number of rows in a query.
    The number of rows is obtained by changing the query to count(*) and dropping the sort.
    TODO: Implement Explain/Query Plan approach, currently faliling on joins
    """
    q1 = re.sub(r"SELECT .*? FROM", "SELECT count(*) FROM", q, flags=re.IGNORECASE)
    q1 = re.sub(r"ORDER BY .*?$", "", q1, flags=re.IGNORECASE)
    q1 = re.sub(r"OFFSET \d+", "", q1, flags=re.IGNORECASE)
    q1 = re.sub(r"LIMIT \d+", "", q1, flags=re.IGNORECASE)
    res = await con.fetchrow(q1)
    if res is None:
        return None
    res = dict(res)
    return oget(res, ["count"])
    # db.sync_select('pg_class', cols=['reltuples'], filters={'relname': 'diagsg'})
    # res = await con.fetchrow(f'explain(format json) {q}')
    # if res is None: return None
    # res = json.loads(res['QUERY PLAN'])
    # if res is None or not len(res): return None
    # return oget(res[0],['Plan','Plan Rows'])


# ####################################################################################################
# DB Class
#
#   startup
#   shutdown
#
#   query
#   select
#   select_one
#   insert
#   update
#   update_or_insert
#   delete
#   get_seq
#
# ####################################################################################################


class DB:
    """
    Class for managing interactions with a PostgreSQL database.

    Constructor Parameters:
            - cfg (dict, optional): DB connection parameters (default: None, and a basic connection is provided).
            - log (BaseLog, optional): Logging mechanism for error and status messages (default: None).
            - dbname (str, optional): Name of the database to connect to (default: None).

        Methods:
            - async startup(min_size=5, max_size=20, loop=None)
              Initiates the database connection pool with optional size and loop parameters.
            - shutdown()
              Gracefully closes the database connection pool.
            - async execute(q)
              Executes SQL queries (non-SELECT) and returns the result.
            - async def query(q, one=False, nrows=False, offset=None, limit=None)
              Executes SELECT queries and retrieves data.
            - async get_trows(tbl) (Internal)
              Retrieves the total number of rows that will result in a querty (through query planner).
            - async select(tbl, join=None, filters=None, sfilters=None, cols='*', sort=None, ascending=True, offset=None, limit=None, one=False)
              Retrieves data from a table with filtering, sorting, and pagination options.
            - async select_one(tbl, filters=[])
              Retrieves a single row from a table with optional filters.
            - async insert(tbl, d, return_key=None)
              Inserts data into a table and optionally returns the inserted key.
            - async update(tbl, ks, d)
              Updates rows in a table based on provided keys.
            - async update_or_insert(tbl, ks, d)
              Updates rows if they exist, otherwise inserts new rows.
            - async delete(tbl, k, v)
              Deletes rows from a table based on a key-value pair.
            - update_stats()
              Performs a vacuum analyze operation for database statistics update (needed for query planner to work properly)

            The DB class assumes the use of a PostgreSQL database and proper configuration parameters for connection.
            Error messages and context information are logged for debugging purposes, enhancing reliability and maintainability.
            Ensures data integrity and security by validating and sanitizing input data.

            The filtering in define by two optional distint ways:
                1) As an array of dict objects of the for {'col':col, 'val':val, 'op':op.} Op can be wither =,>,>=,<,<=,!=.
                2) Single dict with all the keys/vals.
    """

    def __init__(self, cfg=None, log=None, dbname=None, passwd=None):
        """Initializes database connection with optional configuration and logging.

        Args:
            cfg (dict, optional): Database connection configuration.
            log (BaseLog, optional): Logging mechanism.
            dbname (str, optional): Database name.
            passwd (str, optional): Password for database.
        """
        if cfg is None:
            cfg = {
                "db": {
                    "host": "db",
                    "port": 5432,
                    "user": "postgres",
                    "passwd": "rootroot",
                    "dbname": "postgres",
                }
            }
        self.cfg, self.LOG = cfg, log or BaseLog()
        host = oget(cfg, ["db", "host"], "db")
        port = oget(cfg, ["db", "port"], 5432)
        user = oget(cfg, ["db", "user"], "postgres")
        passwd = oget(cfg, ["db", "passwd"], passwd)
        if dbname is None:
            dbname = oget(cfg, ["db", "dbname"], "postgres")
        self.url = f"postgres://{user}:{passwd}@{host}:{port}/{dbname}"
        self.dbname = dbname

    async def startup(self, min_size=5, max_size=20, loop=None):
        """Starts a connection pool with specified min and max sizes.

        Args:
            min_size (int): Minimum pool size.
            max_size (int): Maximum pool size.
            loop (asyncio.AbstractEventLoop, optional): Event loop.

        Returns:
            bool: True if startup fails, otherwise False.
        """
        try:
            self.pool = await asyncpg.create_pool(
                self.url, min_size=min_size, max_size=max_size, loop=loop
            )
        except Exception as e:
            self.LOG(4, 0, label="DBPG", label2="STARTUP", msg=str(e))
            return True
        self.LOG(
            2, 0, label="DBPG", label2="STARTUP", msg=f"CONNECTED POOL to {self.dbname}"
        )
        return False

    def shutdown(self):
        """Terminates the connection pool and logs the shutdown."""
        self.pool.terminate()
        self.LOG(2, 0, label="DBPG", label2="shutdown", msg="DISCONNECTED")
        return False

    async def execute(self, q):
        """Executes a non-SELECT SQL query.

        Args:
            q (str): SQL query string.

        Returns:
            Result of query execution or None if it fails.
        """
        con = await self.pool.acquire()
        try:
            res = await con.execute(q)
        except Exception as err:
            self.LOG(
                4,
                0,
                label="DBPG",
                label2="execute",
                msg={"error_msg": str(err), "query": q},
            )
            return None
        finally:
            await self.pool.release(con)
        return res

    async def query(self, q, one=False, nrows=False):
        """Executes a SELECT SQL query with optional single-row and row-count options.

        Args:
            q (str): SQL query string.
            one (bool, optional): If True, returns a single row.
            nrows (bool, optional): If True, returns row count.

        Returns:
            list[dict] or dict: Query result data.
        """
        con = await self.pool.acquire()
        q = prep_query(q)
        nr = None
        if q[:6].upper() != "SELECT":
            one = True  # accounts for returning in insert
        if one:
            nrows = False
        try:
            if one:
                res = await con.fetchrow(q)
                if res is None:
                    await self.pool.release(con)
                    return None
            else:
                if nrows:
                    nr = await calc_query_rows(con, q)
                    if nr is None:
                        self.LOG(4, 0, label="DB", label2="calc_query_rows", msg=q)
                        await self.pool.release(con)
                        return None
                res = await con.fetch(q)
        except Exception as e:
            self.LOG(4, 0, label="DB", label2="query", msg=str(e))
            return None
        finally:
            await self.pool.release(con)
        if res is None:
            return None
        if one:
            return fix_types(dict(res))
        res = [fix_types(dict(row)) for row in res]
        if nrows:
            return {"data": res, "nrows": nr}
        return res

    async def get_trows(self, tbl):
        """Retrieves the estimated total number of rows in a table using PostgreSQL's `pg_class`.

        Args:
            tbl (str): Table name.

        Returns:
            int: Estimated row count for the specified table.
        """
        q = f"select reltuples as nrows from pg_class where relname='{tbl}'"
        con = await self.pool.acquire()
        res = await con.fetchrow(q)
        if res is None:
            return -1
        return int(dict(res)["nrows"])

    async def select(
        self,
        tbl,
        lookups=None,
        join=None,
        filters=None,
        sfilters=None,
        cols="*",
        sort=None,
        ascending=True,
        offset=None,
        limit=None,
        one=False,
    ):
        """Executes a SELECT query on a table with various options.

        Args:
            tbl (str): Table name.
            lookups (list[dict], optional): Lookup table configurations.
            join (dict, optional): Join conditions.
            filters (list[dict] or dict, optional): Exact match filters.
            sfilters (list[dict] or dict, optional): Search filters with wildcards.
            cols (str or list[str], optional): Columns to retrieve.
            sort (str, optional): Column to sort by.
            ascending (bool, optional): Sort direction.
            offset (int, optional): Query offset for pagination.
            limit (int, optional): Query limit for pagination.
            one (bool, optional): If True, returns a single row.

        Returns:
            list[dict] or dict: Query results as a list of dictionaries, or a single dictionary if `one=True`.
        """
        q = get_select_q(
            tbl,
            lookups=lookups,
            join=join,
            filters=filters,
            sfilters=sfilters,
            cols=cols,
            sort=sort,
            ascending=ascending,
            offset=offset,
            limit=limit,
        )
        return await self.query(q, one=one, nrows=True)

    async def select_one(self, tbl, filters=[]):
        """Retrieves a single row from a table based on filters.

        Args:
            tbl (str): Table name.
            filters (list[dict], optional): Filters for the selection.

        Returns:
            dict: A single row from the table that matches the filters, or None if not found.
        """
        return await self.select(tbl, filters=filters, one=True)

    async def insert(self, tbl, d, return_key=None):
        """Inserts a new row into a table and optionally returns the primary key.

        Args:
            tbl (str): Table name.
            d (dict): Data to insert.
            return_key (str, optional): Column name of the key to return.

        Returns:
            bool or value: True if the insertion was successful, False otherwise; if `return_key` specified, returns the key.
        """
        q = f"INSERT INTO {tbl} ("
        for k in d.keys():
            q += f"{k}, "
        q = q[:-2] + ") VALUES ("
        for k in d.keys():
            q = q + get_repr(d[k]) + ", "
        q = q[:-2] + ")"
        if return_key is not None:
            q += f" returning {return_key};"
            res = await self.query(q, one=True)
            if res is not None and len(res):
                return res[return_key]
            return None
        res = await self.execute(q)
        if res == "INSERT 0 1":
            return False
        return True

    async def update(self, tbl, ks, d):
        """Updates rows in a table based on specified keys.

        Args:
            tbl (str): Table name.
            ks (str or list[str]): Key column(s) to match.
            d (dict): Data for updating.

        Returns:
            bool: False if update succeeds, True if it fails.
        """
        ks = listify(ks)
        for k in ks:
            if not k in d:
                self.LOG(4, 0, label="DBPG", label2="update", msg=f"key error: {k}")
                return True
        setvars = ", ".join(
            [f"{k}={get_repr(d[k])}" for k in d if k not in ks + ["nrows"]]
        )
        q = f"UPDATE {tbl} SET {setvars}"
        filters = " AND ".join([f"{k}='{d[k]}'" for k in ks if d[k] is not None])
        q += f" WHERE {filters};"
        res = await self.execute(q)
        if res is None: return True
        n = int(res[7:])
        if n==0: return True
        return False

    async def update_or_insert(self, tbl, ks, d):
        """Updates an existing row if it exists, or inserts a new row otherwise.

        Args:
            tbl (str): Table name.
            ks (str or list[str]): Key column(s) to check for existing row.
            d (dict): Data for updating or inserting.

        Returns:
            bool: True if operation was successful, False otherwise.
        """
        ks = listify(ks)
        filters = {e: d[e] for e in ks}
        row = await self.select_one(tbl, filters=filters)
        if row is None:
            return await self.insert(tbl, d)
        return await self.update(tbl, ks, d)

    # Missing multi key delete
    async def delete(self, tbl, k, v):
        """Deletes rows from a table based on a key-value pair.

        Args:
            tbl (str): Table name.
            k (str): Column name to match.
            v: Value to match for deletion.

        Returns:
            bool: True if deletion fails, False otherwise.
        """
        if k is None or v is None:
            return True
        q = f"DELETE FROM {tbl} WHERE {k}='{v}'"
        res = await self.execute(q)
        if res is None:
            return True
        n = int(res[7:])
        if n == 0:
            return True
        return False

    async def get_seq(self, seqname):
        """Gets the next value of a specified sequence.

        Args:
            seqname (str): Sequence name.

        Returns:
            int: Next sequence value, or None if fails.
        """
        res = await self.query(f"select nextval('{seqname}')")
        return oget(res, [0, "nextval"])

    def set_seq(self, seqname):
        pass

    def update_stats(self):
        """Updates database statistics using VACUUM ANALYZE."""
        self.sync_query("vacuum analyze")

    def sync_startup(self, *args, **kwargs):
        """Synchronously initializes the database connection pool."""
        return asyncio.get_event_loop().run_until_complete(
            self.startup(*args, **kwargs)
        )

    def sync_query(self, *args, **kwargs):
        """Synchronously executes a SQL query."""
        return asyncio.get_event_loop().run_until_complete(self.query(*args, **kwargs))

    def sync_select(self, *args, **kwargs):
        """Synchronously executes a SELECT query with optional filtering."""
        return asyncio.get_event_loop().run_until_complete(self.select(*args, **kwargs))

    def sync_select_one(self, *args, **kwargs):
        """Synchronously retrieves a single row from a table."""
        return asyncio.get_event_loop().run_until_complete(
            self.select_one(*args, **kwargs)
        )

    def sync_insert(self, *args, **kwargs):
        """Synchronously inserts a row into a table."""
        return asyncio.get_event_loop().run_until_complete(self.insert(*args, **kwargs))

    def sync_update(self, *args, **kwargs):
        """Synchronously updates rows in a table based on specified keys."""
        return asyncio.get_event_loop().run_until_complete(self.update(*args, **kwargs))

    def sync_update_or_insert(self, *args, **kwargs):
        """Synchronously updates a row if exists or inserts otherwise."""
        return asyncio.get_event_loop().run_until_complete(
            self.update_or_insert(*args, **kwargs)
        )

    def sync_delete(self, *args, **kwargs):
        """Synchronously deletes rows from a table based on key-value match."""
        return asyncio.get_event_loop().run_until_complete(self.delete(*args, **kwargs))

    def sync_get_seq(self, *args, **kwargs):
        """Synchronously retrieves the next value in a sequence."""
        return asyncio.get_event_loop().run_until_complete(
            self.get_seq(*args, **kwargs)
        )

    async def enqueue(self, tbl, rec, status_col='qstatus', order_col='qts'):
        if type(rec)!=dict: rec = {}
        rec[status_col],rec[order_col] = 0,now().isoformat()
        return await self.insert(tbl, rec)

    def dequeue(self, tbl, uid_col, status_col='qstatus', order_col='qts'):
        """
        Implements a queue system with the table tbl.
        Fetches a task with status 0 (unprocessed) from the table.
        Locks the task by updating its status to 1. If the update fails, another process has locked the task.
        Returns the task id if successfully locked, or None if no task is available or already locked.
        If `order_col` is provided, it ensures tasks are fetched in a defined order, useful when external
          processing of tasks might be time-consuming, to avoid repeatedly checking the same task.
        When the task is complete its qstatus is set to 2 (DONE) or 99 (ERROR).
        """
        # Get a task with status 0
        res = self.sync_select(tbl, filters={status_col:0}, sort=order_col, ascending=True, limit=1)
        uid = oget(res,['data',0,uid_col])
        # If uid is None, no task is available
        if uid is None: return None
        # Otherwise update status to 1
        # If update fails, a concurrent process picked the same task, and the task is no longer available
        if self.sync_update(tbl, uid_col, {uid_col:uid, status_col:1}): return None
        # Task is safelly locked
        return uid

    def sync_startup(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.startup(*args, **kwargs))
    def sync_execute(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.execute(*args, **kwargs))
    def sync_query(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.query(*args, **kwargs))
    def sync_select(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.select(*args, **kwargs))
    def sync_select_one(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.select_one(*args, **kwargs))
    def sync_insert(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.insert(*args, **kwargs))
    def sync_update(self,  *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.update(*args, **kwargs))
    def sync_update_or_insert(self,  *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.update_or_insert(*args, **kwargs))
    def sync_delete(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.delete(*args, **kwargs))
    def sync_get_seq(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.get_seq(*args, **kwargs))

# ####################################################################################################
# Utility DB functions
# ####################################################################################################


def row_to_rec(row, lcols):
    """
    Adapts DB output to for front-end consuption.
    Row is produced in the DB Class and has _id and _name suffixes on lookups.
    Rec converts the suffix into an object to be sent to the front-end.
    row_to_rec converts a Row dict into a Rec dict, colapsing the id and name attrs into dicts with id,name attrs,
    for all cols with prefix incuded in lcols.

    Example for lcols=['org']:
        {'id':247, 'org_id':3215,'org_name':'RP'} -> {'id':247, 'org':{'id': 3215, 'name': 'RP'}}
    """
    exclude = [f"{e}_id" for e in lcols] + [f"{e}_name" for e in lcols]
    rec = {k: row[k] for k in row if k not in exclude}
    for e in lcols:
        rec[e] = {"id": row[f"{e}_id"], "name": row[f"{e}_name"]}
    return rec


def res_to_recs(res, lcols):
    """Applies row_to_rec to a list of res."""
    if type(lcols)!=list: return res
    if type(res)==dict:
        if not "data" in res: return None
        res = res["data"]
    if type(res)!=list: return None
    return [row_to_rec(e, lcols) for e in res]


def rec_to_row(rec):
    """
    Converts Front-end Rows with object columns with id,name attrs by colapsing all the lookup dicts into the id attr.
    Example:
        {'id':247, 'org': {'id':3215, 'name':'RP'}} -> {'id':247, 'org':3215}
    """
    return {k: rec[k]["id"] if type(rec[k]) == dict else rec[k] for k in rec}


def run_slq_cmds(db, q):
    """Executes multiple SQL commands sequentially from a string with semicolons.

    Args:
        db (DB): Database instance.
        q (str): SQL command string.
    """
    for q in q.split(";"):
        if len(q) < 10:
            continue
        db.sync_execute(q + ";")


def run_sql_file(db, fname):
    """Executes SQL commands from a file.

    Args:
        db (DB): Database instance.
        fname (str): File path containing SQL commands.
    """
    f = open(fname, "r")
    qs = f.read()
    for q in [q for q in qs.split(";")]:
        db.sync_execute(q)


def db_insert_df(db, tbl, df, dmap=None, delete=False):
    """Inserts a DataFrame into a database table.
    Args:
        db (DB): Database instance.
        tbl (str): Table name.
        df (pd.DataFrame): Data to insert.
        dmap (dict, optional): Column mapping dictionary.
        delete (bool, optional): If True, deletes existing rows in the table before insertion.

    Returns:
        bool: False if successful, True if an error occurs.
    """
    if delete:
        db.sync_execute(f"delete from {tbl}")
    if dmap is None:
        dmap = {c: c for c in df.columns}
    else:
        df = df.rename(columns=dmap)
    cols = [dmap[c] for c in dmap]
    df = df[cols]
    for i in range(len(df)):
        row = df.iloc[i]
        d = {c: row[c] for c in cols}
        if db.sync_insert(tbl, d):
            print("DB insert error")
    return False


def log_and_return(msg):
    print(msg)
    return msg


def db_export_tbl(db, p, tbl):
    """Exports a table to a pickle file.

    Args:
        db (DB): Database instance.
        p (str): Path to save the file.
        tbl (str): Table name.

    Returns:
        int: 0 if successful, 1 if an error occurs.
    """
    res = db.sync_select(tbl, limit=int(1e9))
    if res is None or not "data" in res:
        return 1
    return pickle_save(p, res["data"])


def db_import_tbl(db, p, tbl, delete=False):
    """Imports data from a pickle file into a table.

    Args:
        db (DB): Database instance.
        p (str): Path to the pickle file.
        tbl (str): Table name.
        delete (bool, optional): If True, deletes existing rows before import.

    Returns:
        int: 0 if successful, otherwise 1.
    """
    p = Path(p)
    if not p.with_suffix(".pickle").is_file():
        return log_and_return(f"Error importing {tbl}: file {p} not found")
    rows = pickle_load(p)
    if rows is None:
        return log_and_return(f"Cant read {p}")
    if delete:
        if db.sync_execute(f"delete from {tbl}"):
            return log_and_return(f"Error deleting tbl {tbl}")
    n = 0
    for row in rows:
        res = db.sync_insert(tbl, row)
        if res:
            return log_and_return(f"Error inserting record into {tbl}: {row}")
        n += 1
    print(f"Imported {n} records into {tbl}")
    return 0


def db_disable_serial(db, tbl, col):
    """Disables auto-increment on a table column.

    Args:
        db (DB): Database instance.
        tbl (str): Table name.
        col (str): Column name.
    """
    db.sync_execute(f"alter table {tbl} alter column {col} drop default")


def db_enable_serial(db, tbl, col):
    """Enables auto-increment on a table column.

    Args:
        db (DB): Database instance.
        tbl (str): Table name.
        col (str): Column name.
    """
    n = db.sync_execute(f"select max({col}) from {tbl}")[0]["max"]
    db.sync_execute(f"select pg_catalog.setval('public.{tbl}_{col}_seq', {n}, true)")
    db.sync_execute(
        f"alter table {tbl} alter column {col} set default nextval('{tbl}_{col}_seq')"
    )

import logging
import re
import os
import time
import numpy as np
# pip install mysql-connector-python (NOT mysql-connector)
import mysql.connector
from fitxf import DatastoreInterface, DbParams
from fitxf.math.utils.Lock import Lock
from fitxf.math.utils.Logging import Logging
from fitxf.math.utils.Env import Env


#
# Pull docker image, start it, then create test database
# >> docker pull mysql:8.4
# >> docker run -d --name test-mysql -e MYSQL_ROOT_PASSWORD=password123 -p 3307:3306 mysql:8.4
# >> docker exec -it test-mysql bash
#    bash-4.4# mysql --host=localhost --port=3306 -u root -p
#    mysql> CREATE DATABASE testdb;
# https://www.datacamp.com/tutorial/set-up-and-configure-mysql-in-docker
#
class MySql(DatastoreInterface):

    # Default column name created by ES to store text embedding
    COL_TEXT_ENCODE = 'text_encode'

    # https://www.w3schools.com/mysql/mysql_datatypes.asp
    MYSQL_STRING_DATA_TYPES_WITH_LENGTH = (
        'char', 'varchar', 'blob',
        # 'binary', 'varbinary',
        # 'bit', 'tinyint', 'smallint', 'mediumint', 'int', 'integer', 'bigint',
    )

    def __init__(
            self,
            db_params: DbParams,
            ignore_warnings = False,
            logger = None,
    ):
        super().__init__(
            db_params = db_params,
            ignore_warnings = ignore_warnings,
            logger = logger,
        )
        # Controls locking at least for a single instance
        #self.__mutex_mysql = threading.Lock()
        self.__mutex_name_1 = 'mutex_1'
        self.__mutex_lock = Lock(
            mutex_names = [self.__mutex_name_1],
            logger = self.logger,
        )

        self.create_table_columns_json = {}
        # Automatically convert create table to json format, to be able to extract more info about max lengths, etc.
        self.__convert_create_table_syntax_to_json(
            sql = self.db_params.db_create_table_sql,
        )
        self.logger.info('Create table SQL initialized as: ' + str(self.db_params.db_create_table_sql))
        self.logger.info('Create table SQL to JSON as: ' + str(self.create_table_columns_json))

        self.cursor = None

        # If you have multiple threads/workers accessing the same MySQL, set to True.
        # It seems MySQL can't handle simple synching issues, and need a new reconnection
        # to reflect the latest changes
        # NOTE: Closing cursor after every tx will not work, you need to close the whole connection
        self.close_cursor_after_every_tx = True
        self.close_connections_after_every_tx = True
        return

    def remove_stupid_msql_ticks(self, s):
        return re.sub(pattern="`", repl="", string=s)

    def __check_need_cleanup_every_time(self):
        if self.close_cursor_after_every_tx:
            self.__close_cursor()
        if self.close_connections_after_every_tx:
            self.__close_connection()
        return

    def __execute_sql_with_commit(
            self,
            sql,
            val = None,
            table = 'test',
    ):
        self.reconnect_forever(table=table)
        try:
            self.__mutex_lock.acquire_mutexes(
                id = '__execute_sql_with_commit',
                mutexes = [self.__mutex_name_1],
            )
            # TODO Handle when execute cursor hang forever
            # Put lots of logging here for problematic MySQL that can hang forever when another connection has the lock
            self.logger.info('Now will execute cursor for commit sql "' + str(sql) + '", values: ' + str(val))
            if val is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, val)
            self.logger.info('Executed cursor for commit sql "' + str(sql) + '", values ' + str(val))
            self.con.commit()
            self.logger.info('Committed sql "' + str(sql) + '", val ' + str(val))
            self.__check_need_cleanup_every_time()
        except Exception as ex:
            self.logger.error(
                'Error executing sql with commit "' + str(sql) + '", val ' + str(val) + '. Exception: ' + str(ex)
            )
            raise ex
        finally:
            self.__mutex_lock.release_mutexes(mutexes=[self.__mutex_name_1])
        return

    def __execute_sql_data_fetch(
            self,
            sql,
            table = 'test',
    ):
        self.reconnect_forever(table=table)
        try:
            self.__mutex_lock.acquire_mutexes(
                id = '__execute_sql_data_fetch',
                mutexes = [self.__mutex_name_1],
            )
            # TODO Handle when execute cursor hang forever
            # Put lots of logging here for problematic MySQL that can hang forever when another connection has the lock
            self.logger.info('Now will execute cursor for fetch sql "' + str(sql) + '"')
            self.cursor.execute(sql)
            self.logger.info('Executed cursor for commit sql "' + str(sql) + '"')
            resp = self.cursor.fetchall()
            self.logger.info('Executed sql with data fetchall "' + str(sql) + '"')
            self.__check_need_cleanup_every_time()
            # self.logger.info('Response type "' + str(type(resp)) + '": ' + str(resp))
            return resp
        except Exception as ex:
            self.logger.error('Error executing sql data fetch "' + str(sql) + '"')
            raise ex
        finally:
            self.__mutex_lock.release_mutexes(mutexes=[self.__mutex_name_1])

    def __create_table_if_not_exist(
            self,
            table,
    ):
        sql = "SHOW TABLES LIKE '" + str(table) + "'"
        res = self.__execute_sql_data_fetch(table=table, sql=sql)
        self.logger.info('Result for show tables like "' + str(table) + '": ' + str(res))
        exist = len(res) > 0

        if not exist:
            sql = re.sub(pattern="<TABLENAME>", repl=str(table), string=self.db_params.db_create_table_sql)
            self.__execute_sql_with_commit(table=table, sql=sql)
            self.logger.info('Created table "' + str(table) + '"')
        else:
            self.logger.info('Table "' + str(table) + '" already exists')
        return

    def __test_connection(
            self,
            table,
    ):
        try:
            if (self.con is None) or (self.cursor is None):
                return False

            sql = "SHOW TABLES LIKE '" + str(table) + "'"
            self.cursor.execute(sql)
            self.cursor.fetchall()
            return True
        except Exception as ex:
            self.logger.error('Error testing MySQL connection: ' + str(ex))
            return False

    def close(
            self,
    ):
        try:
            self.__mutex_lock.acquire_mutexes(
                id = 'close',
                mutexes = [self.__mutex_name_1],
            )
            self.__close_cursor()
            self.__close_connection()
        finally:
            self.__mutex_lock.release_mutexes(mutexes=[self.__mutex_name_1])

    #
    # Closing cursor and then obtaining a new one will not refresh the data updated by other threads, workers, etc.
    # So in a way this function is useless since we still need to close the whole connection everytime anyway
    #
    def __close_cursor(
            self,
    ):
        if self.cursor is not None:
            try:
                self.cursor.close()
                self.logger.info('Cursor closed successfully')
            except Exception as ex:
                self.logger.error('Error closing cursor: ' + str(ex))

        # Set to None no matter what happens
        self.cursor = None
        return

    def __close_connection(
            self,
    ):
        if self.con is not None:
            try:
                self.con.close()
                self.logger.info('Connection closed successfully')
            except Exception as ex:
                self.logger.error('Error closing connection: ' + str(ex))

        # Set to None no matter what happens
        self.con = None
        return

    def reconnect_forever(
            self,
            table,
            max_tries = 100,
    ):
        try:
            self.__mutex_lock.acquire_mutexes(
                id = 'reconnect_forever',
                mutexes = [self.__mutex_name_1],
            )
            try_count = 0
            while True:
                try:
                    if (self.con is not None) and self.close_cursor_after_every_tx:
                        self.cursor = self.con.cursor()
                except Exception as ex:
                    self.logger.error('Error obtaining cursor: ' + str(ex))
                    # We assume connection already broken
                    self.__close_cursor()
                    self.__close_connection()
                    continue

                if self.__test_connection(table=table):
                    self.logger.debug('MySQL connection still alive')
                    break
                else:
                    # We assume connection already broken
                    self.__close_cursor()
                    self.__close_connection()

                if try_count > max_tries:
                    raise Exception('Max tries to reconnect already reached ' + str(max_tries))

                try:
                    try_count += 1
                    self.__connect()
                    self.logger.info('Reconnected successfully at try #' + str(try_count))
                    break
                except Exception as ex:
                    self.logger.error('Connect try error #' + str(try_count) + ': ' + str(ex))
                    time.sleep(np.random.randint(low=2, high=5))
                    continue
        finally:
            self.__mutex_lock.release_mutexes(mutexes=[self.__mutex_name_1])

    def connect(
            self,
    ):
        try:
            self.__mutex_lock.acquire_mutexes(
                id = 'connect',
                mutexes = [self.__mutex_name_1],
            )
            return self.__connect()
        finally:
            self.__mutex_lock.release_mutexes(mutexes=[self.__mutex_name_1])

    def __connect(
            self,
    ):
        required_conn_params = [
            self.db_params.db_host, self.db_params.db_port, self.db_params.db_username, self.db_params.db_password
        ]
        for _ in required_conn_params:
            assert _ is not None, 'Cannot be empty ' + str(required_conn_params)

        self.logger.info(
            'Try connect to "' + str(self.db_params.db_host) + '", port "' + str(self.db_params.db_port)
            + '", DB "' + str(self.db_params.db_database)
            + '", via username "' + str(self.db_params.db_username) + '", timeout ' + str(self.timeout) + 's.'
        )

        self.con = mysql.connector.connect(
            user = self.db_params.db_username,
            password = self.db_params.db_password,
            host = self.db_params.db_host,
            port = self.db_params.db_port,
            database = self.db_params.db_database,
            connect_timeout = self.timeout,
        )
        # we only need 1 cursor
        self.cursor = self.con.cursor()
        self.logger.info(
            'Connected successfully to "' + str(self.db_params.db_host) + '", port "' + str(self.db_params.db_port)
            + '", DB "' + str(self.db_params.db_database) + '", via username "' + str(self.db_params.db_username)
            + '", timeout ' + str(self.timeout)
            + 's, connection ' + str(id(self.con)) + ', cursor ' + str(id(self.cursor))
        )
        return

    # To prevent burdensome & messy configurations, settings on column restrictions on env vars or config files,
    # we will extract these restrictions programmatically
    # To simplify code, your create table syntax must have ticks for all column names, e.g. `text`, `Faq Name`
    def __convert_create_table_syntax_to_json(
            self,
            sql,
    ):
        self.logger.info('Converting this create table sql: ' + str(sql))

        # remove front part of create table
        # E.g. "CREATE TABLE `<TABLENAME>` (`text` varchar(255) DEFAULT NULL,`label` varchar(255) DEFAULT NULL,)"
        cols_part = re.sub(
            # keep the part inside bracket beginning with a tick "`", thus your create table syntax column names
            # must all have ticks to enclose the column name
            pattern = ".*CREATE TABLE.*[(][\s\t\n\r]*(`.*)",
            repl = "\\1",
            string = sql,
            flags = re.IGNORECASE
        )
        # remove end part of create table
        cols_part = re.sub(pattern="[\s\t\n\r]*[)][\s\t\n\r]*$", repl="", string=cols_part, flags=re.IGNORECASE)
        # E.g. will become "`text` varchar(255) DEFAULT NULL, `label` varchar(255) DEFAULT NULL"
        self.logger.info('Create table sql columns part: ' + str(cols_part))

        cols_part = cols_part.split(sep=",")
        # remove front spaces, new lines, etc.
        cols_part = [str(s).strip() for s in cols_part]
        # E.g. will become ['`text` varchar(255) DEFAULT NULL', '`label_user` varchar(255) DEFAULT NULL']
        self.logger.info('Columns part as list: ' + str(cols_part))

        self.create_table_columns_json = {}
        for i, cpart in enumerate(cols_part):
            if re.match(pattern="^PRIMARY KEY.*", string=cpart):
                self.logger.info('Found constraint "' + str(cpart) + '", breaking from loop...')
            # Check for constraint statement
            if re.match(pattern='^PRIMARY KEY.*', string=cpart):
                self.logger.info('Found constraint "' + str(cpart) + '", breaking from loop..')
                break
            if len(cpart) == 0:
                self.logger.info('Skip empty cpart at #' + str(i))
                continue
            assert cpart[0] == "`", 'Column names must have ticks "' + str(cpart) + '"'
            colname = re.sub(pattern="^`(.*)`.*", repl="\\1", string=cpart)

            col_details = re.sub(pattern="`.*`(.*)", repl="\\1", string=cpart).strip()
            # Split to 2 parts, thus 1st part column type, and 2nd part is the remaining details like DEFAULT values
            col_details = col_details.split(sep=" ", maxsplit=1)
            assert len(col_details) == 2, 'Column details for "' + str(colname) + '" not 2 parts: ' + str(col_details)

            col_type = col_details[0].strip().lower()
            col_other = col_details[1]

            col_type_name = re.sub(pattern="[(].*", repl="", string=col_type)
            if col_type_name in self.MYSQL_STRING_DATA_TYPES_WITH_LENGTH:
                col_type_maxlen = re.sub(pattern=".*[(]([0-9]+)[)].*", repl="\\1", string=col_type)
                col_type_maxlen = int(col_type_maxlen)
            else:
                col_type_maxlen = None

            self.create_table_columns_json[colname] = {
                'type': col_type_name,
                'maxlen': col_type_maxlen,
                'other': col_other,
            }
        self.logger.info(
            'Columns part after convert to json: ' + str(self.create_table_columns_json)
        )
        return

    def get_column_names(
            self,
            tablename,
    ):
        assert tablename is not None, 'Table name cannot be None'
        sql = 'SHOW COLUMNS FROM `' + str(tablename) + '`'
        resp = self.__execute_sql_data_fetch(table=tablename, sql=sql)
        colnames = [self.remove_stupid_msql_ticks(s=a[0]) for a in resp]
        self.logger.info('Raw MySQL query "' + str(sql) + '" response: ' + str(resp))
        self.logger.info('For table "' + str(tablename) + '", column names: ' + str(colnames))
        return colnames

    def get(
            self,
            # e.g. {"answer": "take_seat"} or list of tuples [("answer", "take_seat"), ("question", "...")]
            match_phrase,
            match_condition = {'and': True, 'exact': True},
            tablename = None,
            request_timeout = 20.0,
    ):
        assert tablename is not None, 'Table name cannot be None'
        self.__create_table_if_not_exist(table=tablename)

        if type(match_phrase) is dict:
            match_phrase_tuples = [(k, v) for k, v in match_phrase.items()]
        elif type(match_phrase) in [list, tuple]:
            for pair in match_phrase:
                assert len(pair) == 2, 'Match phrase tuple must be length 2: ' + str(pair)
            match_phrase_tuples = match_phrase
        else:
            raise Exception('Wrong type for match phrase ' + str(type(match_phrase)))

        prm_cond_and = match_condition['and']
        prm_exact_match = match_condition['exact']

        self.logger.debug(
            'Get/Query from index "' + str(tablename) + '", condition AND = ' + str(prm_cond_and)
            + ', exact match = ' + str(prm_exact_match) + ' for query ' + str(match_phrase_tuples)
        )

        colnames = self.get_column_names(tablename=tablename)

        sql = 'SELECT * FROM `' + str(tablename) + '` WHERE '
        for i, (k, v) in enumerate(match_phrase_tuples):
            if i > 0:
                sql += " AND " if prm_cond_and else " OR "
            equal_or_like = '=' if prm_exact_match else 'LIKE'
            sql += '`' + str(k) + '`' + " " + equal_or_like \
                   + " '" + re.sub(pattern="'", repl=r"\'", string=str(v)) + "'"

        self.logger.debug('Try to select from sql "' + str(sql) + '"')
        resp = self.__execute_sql_data_fetch(table=tablename, sql=sql)
        self.logger.debug('Raw MySQL query response: ' + str(resp))
        records = [
            {self.remove_stupid_msql_ticks(s=k): v for k, v in list(zip(colnames, row))}
            for row in resp
        ]
        return records

    def get_all(
            self,
            key = None,
            # <= 0 means get ALL
            max_records = 0,
            tablename = None,
            request_timeout = 20.0,
    ):
        assert tablename is not None, 'Table name cannot be None'
        self.__create_table_if_not_exist(table=tablename)

        colnames = self.get_column_names(tablename=tablename)
        # Add MySQL quotations to columns
        colnames = ["`"+col+"`" for col in colnames]

        sql = 'SELECT ' + ', '.join(colnames) + ' FROM `' + str(tablename) + '`'
        if max_records > 0:
            sql += ' LIMIT ' + str(max_records)
        self.logger.info('Executing SQL: ' + str(sql))
        resp = self.__execute_sql_data_fetch(table=tablename, sql=sql)
        self.logger.debug('Raw MySQL query response: ' + str(resp))
        records = [
            {self.remove_stupid_msql_ticks(s=k): v for k, v in list(zip(colnames, row))}
            for row in resp
        ]
        return records

    def get_indexes(self):
        sql = 'SHOW TABLES'
        resp = self.__execute_sql_data_fetch(sql=sql)
        self.logger.info('Raw MySQL query response: ' + str(resp))
        records = [v[0] for v in resp]
        return records

    def delete_index(
            self,
            tablename,
    ):
        assert tablename is not None, 'Table name cannot be None'
        sql = 'DROP TABLE `' + str(tablename) + '`'
        self.__execute_sql_with_commit(table=tablename, sql=sql)
        self.logger.info('Deleted table "' + str(tablename) + '"')
        return

    def __process_record_values_before_insert_delete(
            self,
            # single record
            record,
    ):
        cols = list(record.keys())
        cols_maxlen = [self.create_table_columns_json[c]['maxlen'] for c in cols]
        self.logger.info('Columns and maxlens: ' + str(list(zip(cols, cols_maxlen))))
        vals = []
        for i, (k, v) in enumerate(record.items()):
            maxlen = cols_maxlen[i]
            if (maxlen is not None) and (type(v) is str):
                v_crop = v[0:min(len(v), maxlen)]
                vals.append(v_crop)
                if v != v_crop:
                    self.logger.warning(
                        'Cropped column value before insert to max length ' + str(maxlen)
                        + ', column "' + str(k) + '", value "' + str(v) + '", after crop "' + str(v_crop) + '"'
                    )
            else:
                vals.append(v)
        return vals

    def add(
            self,
            # list of dicts
            records,
            tablename = None,
            params_other = None,
    ):
        assert tablename is not None, 'Table name cannot be None'
        self.__create_table_if_not_exist(table=tablename)

        assert len(records) > 0, 'No records to insert into: ' + str(records)
        for record in records:
            cols = list(record.keys())
            for c in cols:
                assert c in self.create_table_columns_json.keys(), \
                    'Column to be inserted does not exist in json "' + str(c) \
                    + '" ' + str(self.create_table_columns_json)
            cols_maxlen = [self.create_table_columns_json[c]['maxlen'] for c in cols]
            self.logger.info('Columns and maxlens for sql INSERT: ' + str(list(zip(cols, cols_maxlen))))
            # Add MySQL quotations to columns
            cols = ["`"+cl+"`" for cl in cols]
            sql = 'INSERT INTO `' + str(tablename) + '` (' + ', '.join(cols) + ') VALUES (' \
                  + ', '.join(['%s']*len(cols)) + ')'
            val = self.__process_record_values_before_insert_delete(record=record)
            # val = [v for k,v in record.items()]
            self.logger.info('Try to insert with sql "' + str(sql) + '", values ' + str(val))
            res = self.__execute_sql_with_commit(table=tablename, sql=sql, val=val)
            self.logger.info('Insert result for sql "' + str(sql) + '", values ' + str(val) + ': ' + str(res))
        return

    def delete(
            self,
            match_phrase,
            match_condition = {'and': True, 'exact': True},
            tablename = None,
    ):
        assert type(match_phrase) is dict, 'Match phrase wrong type "' + str(type(match_phrase)) + '"'
        assert tablename is not None, 'Table name cannot be None'
        self.__create_table_if_not_exist(table=tablename)

        sql = 'DELETE FROM `' + str(tablename) + '` WHERE '
        values = self.__process_record_values_before_insert_delete(record=match_phrase)
        for i, (k, v) in enumerate(match_phrase.items()):
            if i > 0:
                and_or = 'AND' if match_condition['and'] else 'OR'
                sql += " " + str(and_or) + " "
            # sql += str(k) + " = '" + re.sub(pattern="'", repl="\\'", string=str(v)) + "'"
            # Use placeholder "%s" so we don't need to do messy escape of special characters
            eq_or_like = '=' if match_condition['exact'] else 'LIKE'
            sql += '`' + str(k) + '` ' + str(eq_or_like) + ' %s'
            # values.append(str(v))
        self.logger.info('Try to delete from sql "' + str(sql) + '"')
        self.__execute_sql_with_commit(table=tablename, sql=sql, val=values)
        # TODO How to get how many deleted successfully?
        return {'deleted': -1}

    def delete_by_raw_query(
            self,
            raw_query,
            tablename = None,
            params_other = None,
    ):
        assert tablename is not None, 'Table name cannot be None'
        self.__create_table_if_not_exist(table=tablename)

        params_other = {} if params_other is None else params_other
        self.__execute_sql_with_commit(
            sql = raw_query,
            table = tablename,
            val = None,
        )
        # TODO How to get how many deleted successfully?
        return {'deleted': -1}

    def delete_all(
            self,
            key,
            tablename = None,
    ):
        raise Exception('TODO')


class MySqlUnitTest:
    def __init__(
            self,
            db_params: DbParams,
            db_table_name,
            reconnect_after_every_tx,
            logger = None,
    ):
        self.db_params = db_params
        self.db_table_name = db_table_name
        self.reconnect_after_every_tx = reconnect_after_every_tx
        self.logger = logger if logger is not None else logging.getLogger()

        self.db_params.db_create_table_sql = """CREATE TABLE `<TABLENAME>` (
                `tex t` varchar(10) DEFAULT NULL,
                `label_user` varchar(255) DEFAULT NULL,
                `label_standardized` int DEFAULT NULL,
                `text_encoding` varchar(5000) DEFAULT NULL
                )"""
        self.my1 = MySql(
            db_params = self.db_params,
            ignore_warnings = True,
            logger = self.logger,
        )
        self.my1.close_connections_after_every_tx = self.reconnect_after_every_tx
        self.my2 = MySql(
            db_params = db_params,
            ignore_warnings = True,
            logger = self.logger,
        )
        self.my2.close_connections_after_every_tx = self.reconnect_after_every_tx
        return

    def connect(self, my: MySql):
        my.connect()
        self.logger.info('Connection ' + str(my) + ' connected')

    def test(self):
        self.connect(my=self.my1)
        self.connect(my=self.my2)

        records_1 = [
            {'tex t': "don't use ' character", 'label_user': 'test', 'label_standardized': 1, 'text_encoding': '+++'},
            {'tex t': "Hi hi", 'label_user': 'hi', 'label_standardized': 2, 'text_encoding': '+++'},
            {'tex t': "Yo yo", 'label_user': 'hi', 'label_standardized': 2, 'text_encoding': '+++'},
            {'tex t': "white", 'label_user': 'color', 'label_standardized': 3, 'text_encoding': '+++'},
            {'tex t': "white", 'label_user': 'color', 'label_standardized': 3, 'text_encoding': '+++'},
            {'tex t': "black", 'label_user': 'color', 'label_standardized': 3, 'text_encoding': '+++'},
        ]
        records_2 = [
            {'tex t': "missing 1", 'label_user': 'missing', 'label_standardized': 4, 'text_encoding': '+++'},
            {'tex t': "missing 2", 'label_user': 'missing', 'label_standardized': 4, 'text_encoding': '+++'},
        ]
        # delete all records
        for rec in records_1 + records_2:
            self.my1.delete(match_phrase=rec, tablename=self.db_table_name)
        for i, my in enumerate([self.my1, self.my2]):
            rows = my.get_all(tablename=self.db_table_name, max_records=0)
            assert len(rows) == 0, 'Rows not empty for i=' + str(i) + ': ' + str(rows)

        # for 1st connection, add only 1st batch
        self.my1.add(records=records_1, tablename=self.db_table_name)
        # self.my1.delete(
        #     match_phrase = {'text': "don't use ' character", 'label_standardized': 1},
        #     tablename = self.db_table_name,
        # )

        # for 2nd connection, only add 2nd batch
        self.my1.add(records=records_2, tablename=self.db_table_name)

        #--------------------------------------------------------------------------------------------------
        # IMPORTANT IN PRODUCTION
        #   An open connection will not be updated with latest data if another connection does an INSERT,
        #   DELETE, etc.
        #   This means in production, you must set the flag close_connections_after_every_tx to True
        #--------------------------------------------------------------------------------------------------
        # Must reconnect for both connections to be in sync, otherwise 2nd connection will return empty DB

        # Now both connections must retrieve the same data
        rows_retrieved = [[], []]
        for i, my_x in enumerate([self.my1, self.my2]):
            rows = my_x.get_all(tablename=self.db_table_name, max_records=0)
            print('Connection #' + str(i + 1) + ': (ALL) Type ' + str(type(rows)) + ':')
            [print('   ' + str(i + 1) + '. ' + str(r)) for i, r in enumerate(rows)]
            rows_retrieved[i] = rows
        if self.reconnect_after_every_tx:
            assert str(rows_retrieved[0]) == str(rows_retrieved[1]), \
                'Rows different\n' + '\n'.join([str(line) for line in rows_retrieved[0]]) \
                + '\nwith\n' + '\n'.join([str(line) for line in rows_retrieved[1]])
        else:
            assert len(rows_retrieved[1]) == 0, \
                'Expected no data in 2nd MySql connection due to not sync: ' + str(rows_retrieved[1])

        for mp, match_cond, exp_rows_count in [
            ({'label_user': 'color', 'tex t': "white"}, {"and": True, "exact": True}, 2),
            ({'label_user': 'color', 'tex t': "white"}, {"and": False, "exact": True}, 3),
            ({'tex t': "missing%"}, {"and": False, "exact": False}, 2),
            ({'tex t': "missing%"}, {"and": False, "exact": True}, 0),
            # Use tuples in match phrase for similar columns
            ([('tex t', 'white'), ('tex t', 'black')], {"and": True, "exact": True}, 0),
            ([('tex t', 'white'), ('tex t', 'black')], {"and": False, "exact": True}, 3),
            ([('tex t', 'white'), ('tex t', 'black')], {"and": False, "exact": False}, 3),
            ([('tex t', 'wh%'), ('tex t', 'bla%')], {"and": False, "exact": False}, 3),
        ]:
            rows = self.my1.get(
                match_phrase = mp,
                match_condition = match_cond,
                tablename = self.db_table_name,
            )
            assert len(rows) == exp_rows_count, \
                'For mp ' + str(mp) + ', prms ' + str(match_cond) + '.Got total rows ' + str(len(rows)) \
                + ' but expected ' + str(exp_rows_count) + ', rows ' + str(rows)

        limit = 3
        rows = self.my1.get_all(tablename=self.db_table_name, max_records=limit)
        print('(LIMIT) Type ' + str(type(rows)) + ':')
        [print('   ' + str(i + 1) + '. ' + str(r)) for i, r in enumerate(rows)]
        assert len(rows) == 3, 'Expected rows limit ' + str(limit) + ' but got ' + str(len(rows)) + ': ' + str(rows)

        rows = self.my1.get(match_phrase={'label_user': 'test'}, tablename=self.db_table_name)
        print('Type ' + str(type(rows)) + ': ' + str(rows))
        # assert len(rows) == len(records_1+records_2)

        rows = self.my1.get_all(tablename=self.db_table_name)
        # [print(rw) for rw in rows]
        self.my1.delete_by_raw_query(
            raw_query = "DELETE FROM `" + str(self.db_table_name) + "` WHERE `tex t` LIKE '%miss%'",
            tablename = self.db_table_name,
        )
        before_delete_count = len(rows)
        # print('***** AFTER DELETE')
        rows = self.my1.get_all(tablename=self.db_table_name)
        # [print(rw) for rw in rows]
        assert len(rows) == before_delete_count - 2, \
            'After delete row count ' + str(len(rows)) + ', before delete row count ' + str(before_delete_count)

        # Close 2nd connection so it won't lock table to be deleted
        self.my2.close()
        self.my1.delete_index(tablename=self.db_table_name)
        self.my1.close()
        self.logger.info('ALL TESTS PASSED OK')
        return


if __name__ == '__main__':
    lgr = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    er = Env()
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/.env.fitxf.math.ut.mysql')
    table_name = 'en-marktest'

    for recon in [True, False]:
        MySqlUnitTest(
            logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False),
            db_params = DbParams(
                identifier = 'testmysql',
                db_type = 'mysql',
                db_host = os.environ["DB_HOST"],
                db_port = os.environ["DB_PORT"],
                db_username = os.environ["DB_USERNAME"],
                db_password = os.environ["DB_PASSWORD"],
                db_database = os.environ["DB_DATABASE"],
            ),
            db_table_name = table_name,
            reconnect_after_every_tx = recon,
        ).test()

    # res = my1.get_indexes()
    # delete_unit_test_indexes = False
    # if delete_unit_test_indexes:
    #     # Must close 2nd connection first
    #     my2.close()
    #     for tbl in res:
    #         if re.match(pattern='intent_unit_test.*', string=tbl):
    #             print('Matched "' + str(tbl) + '"')
    #             my1.delete_index(tablename=tbl)
    #     exit(0)

    exit(0)

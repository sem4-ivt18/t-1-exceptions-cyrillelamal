"""
CRUD Model
"""
import sqlite3


class User:
    _CONN = None

    DEFAULT_TYPE = 'text'

    def __init__(self):
        self._pk_val = None  # Used to check if the instance is saved into the database

    @classmethod
    def columns(cls) -> dict:
        """Return dict of column names available in the data base with their properties"""
        return {
            'id': {'type': 'integer', 'autoincrement': True, 'pk': True},
            'first_name': {'type': 'text'},
            'last_name': {'type': 'text'},
            'email': {'type': 'text'},
            'gender': {'type': 'text'},
            'ip_address': {'type': 'text'}
        }

    @classmethod
    def pk(cls) -> str:
        """Return name of the column defining the primary key field of the table"""
        return 'id'

    @classmethod
    def table_name(cls) -> str:
        """Return the table name that contains the instances"""
        return cls.__name__.lower()

    @property
    def pk_val(self):
        """Return None if the instance is not saved else its PK value"""
        return self._pk_val

    @pk_val.setter
    def pk_val(self, val):
        """Set PK value"""
        self._pk_val = val

    # CRUD
    def save(self):
        """Create or update"""
        cls = type(self)
        return_last_insert = False  # When insert return last insert autoincrement id
        pk_val = self.pk_val

        # UPDATE
        if pk_val:
            sql, values = self._update()
        # INSERT
        else:
            return_last_insert = True
            sql, values = self._insert()
        # Commit
        c = cls.get_cursor()
        c.execute(sql, values)
        cls.get_connection().commit()
        if return_last_insert:
            c.execute('SELECT last_insert_rowid()')
            pk_val = c.fetchone()[0]
            self.pk_val = pk_val
            return pk_val

    def _update(self) -> tuple:
        """Return SQL statement and VALUES to be placed in"""
        cls = type(self)

        sql = f'UPDATE {cls.table_name()} SET '

        set_stm = ''
        values = []
        for col_name, col_prop in self.columns().items():
            if col_prop.get('autoincrement', False):
                continue
            # Else not ignore autoincrement fields
            set_stm += f'{col_name}=?, '
            values.append(getattr(self, col_name, None))

        if set_stm.endswith(', '):
            set_stm = set_stm[:-2]

        sql += f'{set_stm} WHERE {self.pk}={self.pk_val}'

        return sql, values

    def _insert(self) -> tuple:
        """Return SQL statement and VALUES to be placed in"""
        cls = type(self)

        sql = ''
        # sql += f'BEGIN TRANSACTION;\n'
        sql += f'INSERT INTO {cls.table_name()} ('

        columns = ''
        values = []
        for col_name, col_prop in self.columns().items():
            if col_prop.get('autoincrement', False):
                continue
            # Else not ignore autoincrement fields
            columns += f'{col_name}, '
            values.append(getattr(self, col_name, None))

        if columns.endswith(', '):
            columns = columns[:-2]
        escaping = '?, ' * len(values)
        if escaping.endswith(', '):
            escaping = escaping[:-2]

        sql += f'{columns}) VALUES ({escaping})'

        return sql, values

    def delete(self):
        """Delete instance from the database"""
        cls = type(self)

        sql = f'DELETE FROM {cls.table_name()} WHERE {cls.pk()}=?'
        values = [self.pk_val]

        cls.get_cursor().execute(sql, values)
        cls.get_connection().commit()

    @classmethod
    def get_by_pk(cls, pk_val) -> 'User':
        column_names = list(cls.columns().keys())
        columns = ', '.join(column_names)
        table = cls.table_name()
        pk = cls.pk()

        sql = f'SELECT {columns} FROM {table} WHERE {pk}=?'
        values = [pk_val]

        c = cls.get_cursor()
        c.execute(sql, values)
        res = c.fetchone()

        fetched_user = User()
        for col, val in zip(column_names, res):
            if col == pk:
                fetched_user.pk_val = val
            setattr(fetched_user, col, val)
        return fetched_user

    @classmethod
    def create_table(cls):
        table_name = cls.table_name()
        sql = f'CREATE TABLE IF NOT EXISTS {table_name} (\n'
        for col_name, col_prop in cls.columns().items():
            col_type = col_prop.get('type', cls.DEFAULT_TYPE).upper()
            sql += f'{col_name} {col_type}'
            # TODO: Other field properties
            if col_prop.get('pk', False):
                sql += ' PRIMARY KEY'
            if col_prop.get('autoincrement', False):
                sql += ' AUTOINCREMENT'
            sql += ',\n'
        if sql.endswith(',\n') or sql.endswith(', '):
            sql = sql[:-2]
        sql += '\n)'
        cls.get_cursor().execute(sql)
        cls.get_connection().commit()

    # Connection management
    @classmethod
    def set_connection(cls, dsn='') -> 'sqlite3.Connection':
        c = cls._CONN  # Alias

        if not dsn:
            raise Exception('DSN is not provided')

        if c is None:
            cls._CONN = sqlite3.connect(dsn)

        return cls._CONN

    @classmethod
    def get_connection(cls) -> 'sqlite3.Connection':
        return cls._CONN

    @classmethod
    def close_connection(cls, commit=True):
        c = cls._CONN  # Alias

        if commit:
            c.commit()
        c.close()

    @classmethod
    def get_cursor(cls) -> 'sqlite3.Cursor':
        return cls._CONN.cursor()

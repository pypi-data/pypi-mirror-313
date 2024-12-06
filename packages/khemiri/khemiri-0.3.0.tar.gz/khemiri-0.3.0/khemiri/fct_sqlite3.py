import sqlite3

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class BaseModel:
    database_name = ''
    table_name = ''
    fields = {}

    @classmethod
    def connect(cls):
        return sqlite3.connect(f'{cls.database_name}.db')

    @classmethod
    def create_table(cls):
        with cls.connect() as conn:
            fields_str = ', '.join([f"{name} {type}" for name, type in cls.fields.items()])
            conn.execute(f"CREATE TABLE IF NOT EXISTS {cls.table_name} (id INTEGER PRIMARY KEY, {fields_str})")

    @classmethod
    def save(cls, **kwargs):
        with cls.connect() as conn:
            columns = ', '.join(kwargs.keys())
            placeholders = ', '.join(['?' for _ in kwargs])
            values = tuple(kwargs.values())
            conn.execute(f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})", values)
            conn.commit()

    @classmethod
    def all(cls):
        with cls.connect() as conn:
            cursor = conn.execute(f"SELECT * FROM {cls.table_name}")
            rows = cursor.fetchall()
            return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in rows]

    @classmethod
    def delete(cls, **kwargs):
        with cls.connect() as conn:
            conditions = ' AND '.join([f"{key} = ?" for key in kwargs.keys()])
            values = tuple(kwargs.values())
            conn.execute(f"DELETE FROM {cls.table_name} WHERE {conditions}", values)
            conn.commit()

    @classmethod
    def update(cls, where, **kwargs):
        with cls.connect() as conn:
            set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
            where_clause = ' AND '.join([f"{key} = ?" for key in where.keys()])
            values = tuple(kwargs.values()) + tuple(where.values())
            conn.execute(f"UPDATE {cls.table_name} SET {set_clause} WHERE {where_clause}", values)
            conn.commit()

    @classmethod
    def filter(cls, **kwargs):
        with cls.connect() as conn:
            conditions = ' AND '.join([f"{key} = ?" for key in kwargs.keys()])
            values = tuple(kwargs.values())
            cursor = conn.execute(f"SELECT * FROM {cls.table_name} WHERE {conditions}", values)
            rows = cursor.fetchall()
            return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in rows]

    @classmethod
    def count(cls, **kwargs):
        with cls.connect() as conn:
            if kwargs:
                conditions = ' AND '.join([f"{key} = ?" for key in kwargs.keys()])
                values = tuple(kwargs.values())
                cursor = conn.execute(f"SELECT COUNT(*) FROM {cls.table_name} WHERE {conditions}", values)
            else:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {cls.table_name}")
            count = cursor.fetchone()[0]
            return count

    @classmethod
    def first(cls, **kwargs):
        with cls.connect() as conn:
            conditions = ' AND '.join([f"{key} = ?" for key in kwargs.keys()])
            values = tuple(kwargs.values())
            query = f"SELECT * FROM {cls.table_name}"
            if kwargs:
                query += f" WHERE {conditions}"
            query += " LIMIT 1"  # Limit the result to one record
            cursor = conn.execute(query, values)
            row = cursor.fetchone()
            if row:
                return cls(**dict(zip([column[0] for column in cursor.description], row)))
            return None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# class ticketsModel(BaseModel):
#     database_name = 'tickets'
#     table_name = 'tickets'
#     fields = {
#         'name': 'TEXT',
#         'created_at': 'TEXT'
#     }
#
# # Create the table
# ticketsModel.create_table()
#
# # Save a new record
# ticketsModel.save(name='Test Object', created_at=datetime.now().isoformat())
#
# # Query all records
# objects = ticketsModel.all()
# for obj in objects:
#     print(obj.name, obj.created_at)
#
# # Filter records
# filtered_objects = ticketsModel.filter(name='Test Object')
# for obj in filtered_objects:
#     print(f"Filtered: {obj.name}, {obj.created_at}")
#
# # Count records
# count_all = ticketsModel.count()
# print(f"Total count: {count_all}")
#
# count_filtered = ticketsModel.count(name='Test Object')
# print(f"Filtered count: {count_filtered}")
#
# # Update a record
# ticketsModel.update(where={'name': 'Test Object'}, name='Updated Object')
#
# # Query all records after update
# objects = ticketsModel.all()
# for obj in objects:
#     print(f"Updated: {obj.name}, {obj.created_at}")
#
# # Delete a record
# ticketsModel.delete(name='Updated Object')
#
# # Query all records after deletion
# objects = ticketsModel.all()
# for obj in objects:
#     print(f"After Deletion: {obj.name}, {obj.created_at}")
#
# # Count records after deletion
# count_all = ticketsModel.count()
# print(f"Total count after deletion: {count_all}")

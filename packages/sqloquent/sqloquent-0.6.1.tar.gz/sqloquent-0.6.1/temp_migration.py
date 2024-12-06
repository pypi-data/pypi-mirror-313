from sqloquent import Migration, Table


def create_table_things() -> list[Table]:
    t = Table.create('things')
    t.text('id').unique()
    t.blob('name').default(b'something').index()
    t.integer('amount').nullable().index()
    t.boolean('is_nothing').default(True).nullable().index()
    ...
    return [t]

def drop_table_things() -> list[Table]:
    return [Table.drop('things')]

def migration(connection_string: str = '') -> Migration:
    migration = Migration(connection_string)
    migration.up(create_table_things)
    migration.down(drop_table_things)
    return migration

from sqloquent import SqlModel, Default
class Thing(SqlModel):
    table = 'things'
    columns = ('id', 'name', 'amount', 'is_nothing')
    id: str
    name: bytes|Default[b'something']
    amount: int|None
    is_nothing: bool|None|Default[True]


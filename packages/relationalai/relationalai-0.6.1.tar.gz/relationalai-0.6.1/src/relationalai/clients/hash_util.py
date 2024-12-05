import hashlib

def hash_string(s: str, digits=32):
    return hashlib.md5(s.encode()).hexdigest()[:digits]

def database_name_from_sproc_name(sproc_name: str) -> str:
    if sproc_name.count(".") != 2:
        raise ValueError(f"Invalid stored procedure name: {sproc_name}")
    if len(sproc_name) < 32:
        return f"{sproc_name.replace('.', '_')}_{hash_string(sproc_name)}"
    database, schema, proc = sproc_name.split(".")
    database = database[:10]
    schema = schema[:10]
    proc = proc[:(31 - len(database) - len(schema))]
    hash = hash_string(sproc_name)
    return f"{database}_{schema}_{proc}_{hash}"
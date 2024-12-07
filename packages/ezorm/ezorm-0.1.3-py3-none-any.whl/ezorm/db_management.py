from ezorm.utils import remove_escape_characters
from ezorm.utils import create_directory
from typing import List, Type, get_args
from ezorm.variables import EzORM
from ezorm.validation import issubclass_ezorm
from ezorm.configuration import settings
from ezorm.utils import data_mapping

def create_tbl_query(table:Type[EzORM])->str:
    issubclass_ezorm(table)

    data_types = data_mapping(engine="duck")

    query = []

    for field, detail in table.model_fields.items():
        if field != 'table_name':
            proxy = []
            # annotation = detail.annotation
            is_optional = 'Optional' in str(detail.annotation)
            if is_optional:
                dtype, _ = get_args(detail.annotation)
            else:
                dtype = detail.annotation

            proxy.append(f"""{field} {data_types[dtype]}""")
            is_required = not is_optional
            
            if is_required:
                proxy.append(f"""NOT NULL""")
            else:
                default = detail.default
                if (default is not None) and (default != ""):
                    if isinstance(detail.default, bool):
                        proxy.append(f"""DEFAULT {str(default).upper()}""")
                    elif isinstance(detail.default, str):
                        proxy.append(f"""DEFAULT '{default}'""")
                    else:
                        # print("default", type(default), default)
                        proxy.append(f"""DEFAULT {default}""")
                        
            query.append(" ".join(proxy))

    query = ", ".join(query)
    query = remove_escape_characters(query).strip()

    QUERY = f"""CREATE TABLE IF NOT EXISTS {table.__table__} ( {query} );"""
    return QUERY

def delete_tbl_query(table:Type[EzORM])->str:
    issubclass_ezorm(table)
    QUERY = f"""DROP TABLE IF EXISTS {table.__table__};"""
    return QUERY

def create_tables(tables:List[EzORM]):
    create_directory(db_path=settings.database)
    for table in tables:
        query = create_tbl_query(table)
        # print(query)
        # execute(query, [])
        settings.db(query, [])
        print(f"Model: {table.__table__} created successfully")
    print("All tables created successfully")

def delete_tables(tables:List[EzORM]):
    for table in tables:
        query = delete_tbl_query(table)
        # print(query)
        # execute(query, [])
        settings.db(query, [])
        print(f"Model: {table.__table__} deleted successfully")
    print("All tables deleted successfully")
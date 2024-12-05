import sqlite3

class database:
    def __init__(self, database):
        self.database_name = database
        

    def init_db(self,table_definitions):
        """
        初始化数据库，根据传入的表定义参数创建表结构。

        :param table_definitions: 包含表定义信息的列表，每个元素是一个字典，格式如下:
            {
                "table": "表名",
                "fields": [
                    {
                        "field": "字段名",
                        "isNULL": 是否允许为空（可选，默认为False）,
                        "is_auto_increment": 是否为自增主键（可选，默认为False，仅用于INTEGER类型字段）
                    },
                 ...
                ],
                "FOREIGNKEY": [
                    {
                        "foreign_table": "关联的外部表名",
                        "local_field": "本表中关联的字段名",
                        "foreign_field": "外部表中关联的字段名"
                    },
                 ...
                ]
            }
        """
        try:
            with sqlite3.connect(self.database_name, check_same_thread=False) as conn:
                cursor = conn.cursor()

                for table_def in table_definitions:
                    table_name = table_def["table"]
                    fields = table_def["fields"]
                    foreign_keys = table_def["FOREIGNKEY"]

                    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

                    for field in fields:
                        field_name = field["field"]
                        is_null = "NULL" if field.get("isNULL", False) else "NOT NULL"
                        is_auto_increment = "AUTOINCREMENT" if field.get("is_auto_increment", False) else ""
                        if field.get("is_auto_increment", False):
                            create_table_query += f"{field_name} INTEGER PRIMARY KEY {is_auto_increment}, "
                        else:
                            create_table_query += f"{field_name} TEXT {is_null}, "

                    if foreign_keys:
                        for fk in foreign_keys:
                            foreign_table = fk["foreign_table"]
                            local_field = fk["local_field"]
                            foreign_field = fk["foreign_field"]
                            create_table_query += f"FOREIGN KEY ({local_field}) REFERENCES {foreign_table}({foreign_field}) ON DELETE CASCADE, "

                    create_table_query = create_table_query.rstrip(", ") + ")"

                    cursor.execute(create_table_query)

                conn.commit()
        except sqlite3.Error as e:
            conn.close()
            raise ValueError(f"init_db:{str(e)}") from e
        
    def create_table(self, table_definition):
        """
        创建单个表，基于传入的表定义字典。

        :param table_definition: 表定义字典，格式如下：
            {
                "table": "表名",
                "fields": [
                    {"field": "字段名", "isNULL": 是否允许为空, "is_auto_increment": 是否自增主键},
                    ...
                ],
                "FOREIGNKEY": [
                    {"foreign_table": "外部表名", "local_field": "本表中字段名", "foreign_field": "外部表字段名"}
                ]
            }
        """
        try:
            with sqlite3.connect(self.database_name, check_same_thread=False) as conn:
                cursor = conn.cursor()

                table_name = table_definition["table"]
                fields = table_definition["fields"]
                foreign_keys = table_definition.get("FOREIGNKEY", [])

                # 创建表的初始部分
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

                # 为每个字段生成 SQL
                for field in fields:
                    field_name = field["field"]
                    is_null = "NULL" if field.get("isNULL", True) else "NOT NULL"
                    is_auto_increment = "AUTOINCREMENT" if field.get("is_auto_increment", False) else ""

                    # 自增字段类型应该是INTEGER
                    if field.get("is_auto_increment", False):
                        create_table_query += f"{field_name} INTEGER PRIMARY KEY {is_auto_increment}, "
                    else:
                        create_table_query += f"{field_name} TEXT {is_null}, "  # 默认字段类型为TEXT

                # 外键约束部分
                if foreign_keys:
                    for fk in foreign_keys:
                        foreign_table = fk["foreign_table"]
                        local_field = fk["local_field"]
                        foreign_field = fk["foreign_field"]
                        create_table_query += f"FOREIGN KEY ({local_field}) REFERENCES {foreign_table}({foreign_field}) ON DELETE CASCADE, "

                # 移除多余的逗号并完成 SQL 语句
                create_table_query = create_table_query.rstrip(", ") + ")"

                # 执行创建表的 SQL
                cursor.execute(create_table_query)

                # 提交事务
                conn.commit()

        except sqlite3.Error as e:
            raise ValueError(f"Database error during table creation: {str(e)}") from e

    def fetch_all_by(self,table, params, page=None, fields=None, noTotal=False):
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')
            # 提取并处理排序参数
            _order = params.pop('_order', None)
            _by = params.pop('_by', None)
            if isinstance(_order, str):
                _order = [o.strip() for o in _order.split(',')]
            if isinstance(_by, str):
                _by = [b.strip() for b in _by.split(',')]

            if _by and _order and len(_order) != len(_by):
                raise ValueError("fetch_all_by:Length of _order and _by must be the same.")

            # 构建 WHERE 子句和查询参数
            where_clauses = []
            query_params = []
            _params = params.copy()
            if '_start' in params:
                del _params['_start']
            if '_count' in params:
                del _params['_count']
            for key, value in _params.items():
                if key.startswith('%'):
                    actual_key = key.lstrip('%')
                    where_clauses.append(f'{actual_key} LIKE ?')
                    query_params.append(f'%{value}%')
                elif key == 'startTime':
                    where_clauses.append('time >= ?')
                    query_params.append(value)
                elif key == 'endTime':
                    where_clauses.append('time <= ?')
                    query_params.append(value)
                else:
                    where_clauses.append(f'{key} = ?')
                    query_params.append(value)

            # 如果 noTotal 为 False，则查询总条数
            total = 0  # 默认值为0
            if not noTotal:
                count_query = f'SELECT COUNT(*) as __total FROM {table}'
                if where_clauses:
                    count_query += ' WHERE ' + ' AND '.join(where_clauses)
                cursor.execute(count_query, query_params)
                total = cursor.fetchone()['__total']

            # 构建数据查询
            if fields:
                # 如果提供了字段参数，则只查询指定字段
                fields_str = ', '.join(fields)
            else:
                # 否则查询所有字段
                fields_str = '*'

            query = f'SELECT {fields_str} FROM {table}'
            if where_clauses:
                query += ' WHERE ' + ' AND '.join(where_clauses)

            if _by and _order:
                order_by_clause = ', '.join([f'{field} {order}' for field, order in zip(_by, _order)])
                query += f' ORDER BY {order_by_clause}'

            if page and 'LIMIT' in page and 'OFFSET' in page:
                query += f' LIMIT {page["LIMIT"]} OFFSET {page["OFFSET"]}'

            cursor.execute(query, query_params)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                row_dict = {field: row[field] for field in row.keys()}
                result.append(row_dict)

            conn.close()

            return result, total
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_all_by:{str(e)}") from e

    def fetch_data_count(self,table, field, conditions=None):
        try:
            """
            从指定的表中查询指定字段的计数信息，并按该字段分组。

            :param table: 表名
            :param field: 字段名
            :param conditions: 一个包含查询条件的字典，键为列名，值为对应的过滤值
            :return: 一个包含字典的列表，每个字典包含 'field' 和 'count' 两个键
            """
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')
            # 构建查询条件
            where_clause = ""
            params = []

            if conditions:
                where_conditions = []
                for key, value in conditions.items():
                    where_conditions.append(f"{key} = ?")
                    params.append(value)
                where_clause = " WHERE " + " AND ".join(where_conditions)

            # 构建查询语句
            query = f'''
                SELECT {field}, COUNT(*) as count
                FROM {table}
                {where_clause}
                GROUP BY {field}
            '''
            # 执行查询获取数据
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # 将结果转换为列表
            result_list = [{field: row[field], 'count': row['count']} for row in rows]

            # 关闭数据库连接
            conn.close()

            return result_list
        except Exception as e:
            conn.close()
            raise ValueError(f"Unexpected error in fetch_data_count: {e}") from e
            
    def get_unique_name(self,table,base_name,project_id):
        try:
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')
            # 首先检查是否已经存在相同的基础名称
            count = self.fetch_total_by(table,{"name":base_name,"project_id":project_id})
    
            # 如果不存在相同的名称，直接返回基础名称
            if count == 0:
                conn.close()
                return base_name
    
            # 如果存在相同名称，则开始递增检查 "base_name(1)", "base_name(2)", ...
            index = 1
            new_name = f"{base_name}({index})"
            while True:
                count = self.fetch_total_by(table,{"name":new_name,"project_id":project_id})
                if count == 0:
                    conn.close()
                    return new_name
                index += 1
                new_name = f"{base_name}({index})"
        except Exception as e:
            conn.close()
            raise ValueError(f"get_unique_name:{str(e)}") from e
    
    
    def fetch_add(self,table, data):
        try:
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')
            # 获取data字典的键和值
            columns = ', '.join(data.keys())  # 列名
            placeholders = ', '.join(['?'] * len(data))  # 占位符
            values = list(data.values())  # 直接获取字典的值
    
            # 构建 SQL 查询语句
            sql = f'''
                INSERT INTO {table} ({columns})
                VALUES ({placeholders})
            '''
            # 执行插入操作
            cursor.execute(sql, values)
    
            # 获取最后插入的行ID
            last_id = cursor.lastrowid
    
            # 提交事务并关闭连接
            conn.commit()
            conn.close()
    
            return last_id
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_add:{str(e)}") from e

    def fetch_update(self,table, data, conditions):
        try:
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')

            # 构建 SET 子句（用于更新的键值对）
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            set_values = list(data.values())

            # 构建 WHERE 子句（用于条件判断的键值对）
            where_clause = ' AND '.join([f"{key} = ?" for key in conditions.keys()])
            where_values = list(conditions.values())

            # 构建 SQL 查询语句
            sql = f'''
                UPDATE {table}
                SET {set_clause}
                WHERE {where_clause}
            '''
            # 执行更新操作
            cursor.execute(sql, set_values + where_values)

            # 提交事务并关闭连接
            conn.commit()
            conn.close()

            return cursor.rowcount  # 返回受影响的行数
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_update:{str(e)}") from e

    def fetch_delete(self,table, conditions):
        try:
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')

            # 构建 WHERE 子句（用于条件判断的键值对）
            where_clause = ' AND '.join([f"{key} = ?" for key in conditions.keys()])
            where_values = list(conditions.values())

            # 构建 SQL 查询语句
            sql = f'''
                DELETE FROM {table}
                WHERE {where_clause}
            '''
            # 执行删除操作
            cursor.execute(sql, where_values)

            # 提交事务并关闭连接
            conn.commit()
            conn.close()

            return cursor.rowcount  # 返回受影响的行数
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_delete:{str(e)}") from e

    def fetch_all_as_dict(self,query):
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')
            cursor.execute(query)
            rows = cursor.fetchall()

            # 获取所有列名
            field_names = [description[0] for description in cursor.description]

            result = []
            for row in rows:
                # 自动将每一行转换为包含所有字段的字典
                row_dict = {field: row[field] for field in field_names}
                result.append(row_dict)
            conn.close()

            return result
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_all_as_dict:{str(e)}") from e

    def fetch_total_by(self,table, params, page=None):
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')

            # 构建 WHERE 子句和查询参数
            where_clauses = []
            query_params = []
            for key, value in params.items():
                if key not in ('LIMIT', 'OFFSET'):
                    if key.startswith('%'):  # 检查是否是模糊查询
                        actual_key = key[1:]  # 去掉前面的 % 符号
                        where_clauses.append(f'{actual_key} LIKE ?')
                        query_params.append(f'%{value}%')  # 添加模糊匹配符号
                    else:  # 精准查询
                        where_clauses.append(f'{key} = ?')
                        query_params.append(value)

            # 构建总条数查询
            count_query = f'SELECT COUNT(*) as __total FROM {table}'
            if where_clauses:
                count_query += ' WHERE ' + ' AND '.join(where_clauses)

            cursor.execute(count_query, query_params)
            total = cursor.fetchone()['__total']

            # 关闭数据库连接
            conn.close()

            return total
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_total_by:{str(e)}") from e

    def fetch_distinct_by(self,table,filed):
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')

            # 构建查询语句
            query = f'SELECT DISTINCT {filed} FROM {table}'
            # 执行查询获取数据
            cursor.execute(query)
            rows = cursor.fetchall()

            # 将结果转换为列表
            fileds = [row[filed] for row in rows]

            # 关闭数据库连接
            conn.close()

            return fileds
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_distinct_by:{str(e)}") from e
        
    def fetch_nearest_time(self, table_name, filter_time, max_minutes, limit_count, fields=None, exact_filter=None):
        try:
            """
            查询与给定时间最接近的数据，支持精确过滤条件，并动态选择返回字段。

            :param db_path: 数据库路径
            :param table_name: 表名称
            :param filter_time: 过滤时间（字符串格式:'YYYY-MM-DD HH:MM:SS'）
            :param max_minutes: 允许的最大时间差（单位:分钟）
            :param limit_count: 返回的最大记录数
            :param fields: 要查询的字段列表，如果为 None，则查询所有字段
            :param exact_filter: 精确过滤条件，字典形式，如 {plate_id: 2}
            :return: 查询结果（列表形式）和实际查询到的数量
            """
            # 连接到 SQLite 数据库
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')

            # 如果没有传入字段，则查询所有字段
            if fields is None:
                fields_str = '*'
            else:
                fields_str = ', '.join(fields)  # 将字段列表转为字符串

            # 基础查询 SQL
            sql = f"""
            SELECT {fields_str}
            FROM {table_name}
            WHERE ABS(JULIANDAY(time) - JULIANDAY(?)) * 24 * 60 <= ?  -- 时间差不超过N分钟
            """

            # 参数列表，先添加 filter_time 和 max_minutes
            params = [filter_time, max_minutes]

            # 添加精确过滤条件（例如 {plate_id: 2}）
            if exact_filter:
                for key, value in exact_filter.items():
                    sql += f" AND {key} = ?"
                    params.append(value)

            # 完整的排序和限制
            sql += f"""
            ORDER BY ABS(JULIANDAY(time) - JULIANDAY(?))  -- 排序，以确保返回最近的时间
            LIMIT ?  -- 限制返回的条数
            """
            params.append(filter_time)  # 再次添加 filter_time 用于排序
            params.append(limit_count)  # 添加 limit_count 参数

            # 执行查询
            cursor.execute(sql, tuple(params))

            # 获取查询结果
            rows = cursor.fetchall()

            # 获取字段名
            column_names = [description[0] for description in cursor.description]

            # 将查询结果转换为字典形式
            result = []
            for row in rows:
                row_dict = {column_names[i]: row[i] for i in range(len(row))}
                row_dict['filter_time'] = filter_time
                result.append(row_dict)
            # 根据时间进行二次排序  
            result.sort(key=lambda x: x['time'])
            # 获取实际查到的数量
            actual_count = len(result)

            # 关闭连接
            conn.close()

            return result, actual_count
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_nearest_time:{str(e)}") from e
        
    def fetch_field_total_for_group(self, table, group_field, count_field='*', where_clause=None, values=None):
        """ 
        查询表格中多个 group_field 的 count_field 总数，支持动态字段和查询条件
        """
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为 sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')

            # 如果没有提供 where_clause，则默认为空
            if where_clause is None:
                where_clause = ''

            # 构建查询语句，获取多个 group_field 对应的 count_field 总数
            placeholders = ', '.join(['?'] * len(values))  # 为查询构建占位符
            query = f'SELECT {group_field}, COUNT({count_field}) as total FROM {table} WHERE {group_field} IN ({placeholders}) {where_clause} GROUP BY {group_field}'
            
            # 执行查询获取数据
            cursor.execute(query, tuple(values))
            rows = cursor.fetchall()

            # 将查询结果转换为字典形式，group_field -> total
            result = {row[group_field]: row['total'] for row in rows}

            # 关闭数据库连接
            conn.close()

            return result

        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_field_total_for_group:{str(e)}") from e
        
    def fetch_data_by_field(self, table, field, values, columns=None):
        """ 
        查询表格中符合条件的记录，支持动态字段、字段多条件匹配。
        
        :param table: 表名
        :param field: 用于匹配条件的字段名（如：id、name等）
        :param values: 字段值列表，支持 IN 查询
        :param columns: 需要返回的字段列表，如果为 None，则返回所有字段
        :return: 查询结果，格式为 [{field1: value1, field2: value2, ...}, {...}, ...]
        """
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为 sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')
    
            # 选择要返回的字段
            if columns:
                columns_str = ', '.join(columns)
            else:
                columns_str = '*'  # 如果没有指定字段，则查询所有字段
            
            # 构建 IN 查询条件的占位符
            placeholders = ', '.join(['?'] * len(values))  # 为查询构建占位符
            query = f'SELECT {columns_str} FROM {table} WHERE {field} IN ({placeholders})'
    
            # 执行查询获取数据
            cursor.execute(query, tuple(values))
            rows = cursor.fetchall()
    
            # 将结果转换为字典形式，并返回
            result = [dict(row) for row in rows]
    
            # 关闭数据库连接
            conn.close()
    
            return result
    
        except Exception as e:
            conn.close()
            raise ValueError(f"fetch_data_by_field:{str(e)}") from e
        
        
    def fetch_batch_insert(self, table, column_list, data):
        """
        批量插入数据到指定表格，自动识别固定字段与动态数据。
        :param conn: 数据库连接
        :param table: 表格名称
        :param column_list: 表格的列名列表
        :param data: 包含固定字段和动态数据的输入（根据输入结构动态解析）
        """
        try:
            # 打开数据库连接
            conn = sqlite3.connect(self.database_name, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 设置行工厂为 sqlite3.Row
            cursor = conn.cursor()
            # 启用 WAL 模式
            cursor.execute('PRAGMA journal_mode=WAL;')
            # 确保data和column_list长度一致
            if len(data) != len(column_list):
                raise ValueError(f"Column list length ({len(column_list)}) does not match data length ({len(data)})")

            row_count = None  # 用于存储数组的行数

            # 遍历data，检查每个元素是否是数组
            for item in data:
                if isinstance(item, list):  # 如果是数组
                    # 如果row_count还没有赋值，给它赋值为当前数组的长度
                    if row_count is None:
                        row_count = len(item)
                    # 如果已经有值，检查是否与当前数组长度一致
                    elif row_count != len(item):
                        raise ValueError(f"数组的长度不一致，预期长度为 {row_count}，但发现长度为 {len(item)}。")
            insert_sql = f"INSERT INTO {table} ({','.join(column_list)}) VALUES ({','.join(['?'] * len(column_list))})"
        
            # 构造插入数据
            final_data = []
            for i in range(row_count):
                row = []
                for item in data:
                    if isinstance(item, list):
                        row.append(item[i])  # 从每个数组中取出第i个元素
                    else:
                        row.append(item)  # 直接添加非数组类型的元素
                final_data.append(row)
            cursor.executemany(insert_sql, final_data)
            # 获取插入的行数
            inserted_rows = cursor.rowcount
            # 提交事务
            conn.commit()
            # 返回成功插入的行数
            return inserted_rows
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Error during batch insert: {e}")
        finally:
            # 确保连接被关闭
            conn.close()

import sqlite3


class SQLiteDB:
    def __init__(self, db_name):
        """
        初始化数据库连接
        :param db_name: 数据库名称（文件名）
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)  # 打开数据库连接
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        创建表
        :param table_name: 表名称
        :param columns: 字段及类型的字典，例如 {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"}
        """
        columns_definition = ", ".join(f"{col} {dtype}" for col, dtype in columns.items())
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
        self.cursor.execute(create_table_sql)
        print(f"表 '{table_name}' 创建成功。")

    def insert_record(self, table_name, record):
        """
        插入记录
        :param table_name: 表名称
        :param record: 插入的记录（字典形式，例如 {"name": "Alice", "age": 25}）
        """
        columns = ", ".join(record.keys())
        placeholders = ", ".join("?" for _ in record)
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(insert_sql, tuple(record.values()))
        self.conn.commit()
        print(f"插入记录到表 '{table_name}': {record}")

    def upsert_record(self, table_name, record, conditions=None):
        """
        更新插入（Upsert）：根据条件判断是否存在记录，存在则更新，不存在则插入。
        :param table_name: 表名称
        :param record: 要插入或更新的记录（字典格式，例如 {"name": "Alice", "age": 25}）
        :param conditions: 用于判断记录是否存在的字段（列表格式，例如 ["name", "age"]）。
                           如果不传，则默认比对 record 中的所有字段。
        """
        if conditions is None:
            conditions = list(record.keys())

        condition_values = {key: record[key] for key in conditions}
        where_clause = " AND ".join(f"{col} = ?" for col in condition_values.keys())
        query_sql = f"SELECT COUNT(*) FROM {table_name} WHERE {where_clause}"
        self.cursor.execute(query_sql, tuple(condition_values.values()))
        count = self.cursor.fetchone()[0]

        if count > 0:
            set_clause = ", ".join(f"{col} = ?" for col in record.keys())
            update_sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(update_sql, tuple(record.values()) + tuple(condition_values.values()))
            action = "更新"
        else:
            columns = ", ".join(record.keys())
            placeholders = ", ".join("?" for _ in record)
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(insert_sql, tuple(record.values()))
            action = "插入"

        self.conn.commit()
        print(f"{action}记录到表 '{table_name}': {record}")

    def delete_record(self, table_name, conditions):
        """
        删除记录
        :param table_name: 表名称
        :param conditions: 条件字段和值（字典形式，例如 {"name": "Alice"}）
        """
        where_clause = " AND ".join(f"{col} = ?" for col in conditions.keys())
        delete_sql = f"DELETE FROM {table_name} WHERE {where_clause}"
        self.cursor.execute(delete_sql, tuple(conditions.values()))
        self.conn.commit()
        print(f"删除表 '{table_name}' 中符合条件的记录: {conditions}")

    def query_records(self, table_name, conditions=None):
        """
        查询记录
        :param table_name: 表名称
        :param conditions: 条件字段和值（字典形式，例如 {"age": 25}），可选
        :return: 查询结果列表
        """
        where_clause = ""
        params = ()
        if conditions:
            where_clause = "WHERE " + " AND ".join(f"{col} = ?" for col in conditions.keys())
            params = tuple(conditions.values())
        query_sql = f"SELECT * FROM {table_name} {where_clause}"
        self.cursor.execute(query_sql, params)
        return self.cursor.fetchall()

    def close(self):
        """关闭数据库连接"""
        self.conn.close()
        print("数据库连接已关闭。")


# 示例代码
if __name__ == "__main__":
    db = SQLiteDB("example.db")

    # 创建表
    db.create_table("locations", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "time": "TEXT NOT NULL",
        "region": "TEXT NOT NULL",
        "address": "TEXT NOT NULL",
        "name": "TEXT NOT NULL",
        "phone": "TEXT NOT NULL",
        "is_added": "BOOLEAN NOT NULL"
    })

    db.upsert_record("locations", {
        "time": "2024-12-07 11:00:00",  # 更新时间
        "region": "河南洛阳A",
        "address": "洛阳市新安县老城河南88号",
        "name": "进一家",
        "phone": "15037999587",
        "is_added": False  # 修改状态
    }, conditions=["phone"])

    # 删除符合条件的记录
    db.delete_record("locations", {"phone": "15037995595871"})

    # 查询表中记录
    records = db.query_records("locations")
    print("当前表 'locations' 中的记录：")
    for record in records:
        print(record)

    # 关闭连接
    db.close()

from lljz_tools.client.db_client import MySQLConnectionPool


def test_mysql():
    with MySQLConnectionPool('mysql://root:Hosonsoft2020@192.168.1.220:3307/jmg') as pool:
        with pool.connect() as db:
            db.insert('insert into t (name) values (?)', ('张三', ))
            db.insert_many('insert into t (name) values (?)', [('李四', ), ('王五', )])
            db.commit()
            print(db.select('select * from t limit 10'))
            print(db.select_one('select * from t where id = ?', (1, )))
            print(db.select_all('select * from t'))
            db.update('update t set name = ? where id = ?', ('张三三', 1))
            print(db.select('select * from t limit 10'))
            db.delete('delete from t where id = ?', (2, ))
            print(db.select('select * from t limit 10'))
            db.commit()

if __name__ == '__main__':
    test_mysql()

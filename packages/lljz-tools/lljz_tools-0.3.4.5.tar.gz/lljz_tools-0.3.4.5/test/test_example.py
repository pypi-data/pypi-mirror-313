# coding=utf-8

"""
@fileName       :   test.py
@data           :   2024/9/4
@author         :   jiangmenggui@hosonsoft.com
"""
from lljz_tools.client.db_client import MySQLConnectionPool
from lljz_tools.console_table import ConsoleTable
from lljz_tools.excel import ExcelReader


def test_csv_reader():
    excel = ExcelReader('工作簿1.csv')
    data = excel.read(max_row=3)
    print(data)
    for row in data:
        print(row)


def test_excel_reader():
    excel = ExcelReader('data.xlsx')
    data = excel.read(min_row=2)
    print(data)
    result = list(data)
    for row in result:
        print(row)
    table = ConsoleTable(result)
    print(table)
    img = table.to_image()
    img.save('./data.png')


def test_mysql_connection():
    with MySQLConnectionPool('mysql://root:Hosonsoft2020@192.168.1.220:3307/jmg', show_sql=True) as pool:
        with pool.connect() as db:
            data = db.select('select * from order_count where id = ?', [1])
            # db.show_sql(db.conn.cursor(), 'select * from order_count where id = %s', [1])
            print(data)


def test_dateutil():
    from dateutil import parser
    import datetime
    date = parser.parse('2023-5-10')
    print(date)
    v = datetime.datetime.combine(date.date(), datetime.datetime.min.time())
    print(v)


def test_excel_template():
    from lljz_tools.excel_template import columns, ExcelTemplate, ExcelConfig

    class OrderImportTemplate(ExcelTemplate):
        config = ExcelConfig(allow_empty_template=True)

        orderNo = columns.StringColumn('订单号', required=True)
        sellerRemark = columns.StringColumn('卖家备注', required=False)
        orderType = columns.SequenceColumn('订单类型', {1: "手工订单", 2: "电商订单", 3: "补发订单"})

    data = OrderImportTemplate.read_excel('data.xlsx')
    print(data)
    OrderImportTemplate.create_excel_template('template2.xlsx')


if __name__ == '__main__':
    # table = ConsoleTable(
    #     ExcelReader(r"C:\Users\BJB20\Downloads\产品价格报表 (5).xlsx").read(),
    #     caption='产品价格表',
    # )
    # print(table)
    # img = table.to_image(font_size=16)
    # img.save('./test.png')
    ...

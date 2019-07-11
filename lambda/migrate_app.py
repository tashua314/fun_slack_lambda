import sys
from datetime import datetime

from models.scrap import Scrap
from models.sequence import Sequence


class MigrateApp():
    """ テーブルへのMigrateApp処理クラス """

    tables = [Scrap, Sequence]

    @classmethod
    def create_tables(cls):
        """ テーブル作成 """
        for table in cls.tables:
            cls.__create_table(table)

    @classmethod
    def __create_table(cls, table):
        if not table.exists():
            print('creating {} table...'.format(table.__name__))
            table.create_table(
                wait=True,
                read_capacity_units=1,
                write_capacity_units=1
            )
            print('done.')
        else:
            print('{} created already.'.format(table.__name__))

    @classmethod
    def delete_tables(cls):
        """ テーブル削除 """
        for table in cls.tables:
            cls.__delete_table(table)

    @classmethod
    def __delete_table(cls, table):
        if table.exists():
            print('deleting {} table...'.format(table.__name__))
            table.delete_table()
            print('done.')
        else:
            print('{} deleted already.'.format(table.__name__))

    # pylint: disable=too-many-arguments
    @classmethod
    def insert(cls, scrap_url, title, redirect_url, released_at):
        """ レコード作成 """
        record = Scrap(
            scrap_url,
            text=title,
            redirect_url=redirect_url,
            released_at=released_at
        )
        record.save()
        print(record)

    @classmethod
    def dumps(cls, target_class):
        """ ダンプファイル取得 """
        print(target_class.dumps())

    @classmethod
    def describe_tables(cls):
        """ モデルの詳細を取得 """
        for table in cls.tables:
            print(table.describe_table())
            print('---------------')


if __name__ == '__main__':
    ARGS = sys.argv

    if len(ARGS) == 1 or ARGS[1] == 'create_tables':
        MigrateApp.create_tables()
    elif ARGS[1] == 'delete_tables':
        MigrateApp.delete_tables()
    elif ARGS[1] == 'insert':
        MigrateApp.insert(
            'scrap_url1',
            'text1',
            'redirect_url1',
            datetime.now()
        )
    elif ARGS[1] == 'dumps':
        MigrateApp.dumps(Scrap)
        MigrateApp.dumps(Sequence)
    elif ARGS[1] == 'describe_tables':
        MigrateApp.describe_tables()
    else:
        print('unknown command.')

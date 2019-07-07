# coding: UTF-8

from os import environ
from os.path import dirname, join

from dotenv import load_dotenv

from pynamodb.attributes import NumberAttribute
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

DOTENV_PATH = join(dirname(__file__), '.env')
load_dotenv(DOTENV_PATH)


class Sequence(Model):
    """
    シーケンスモデル
    各モデルのインクリメントidを管理する
    """
    class Meta:
        table_name = 'sequence'

        region = 'ap-northeast-1'
        aws_access_key_id = environ.get("AWS_ACCESS_KEY")
        aws_secret_access_key = environ.get("AWS_SECRETE_KEY")

    # スクレイピング対象のURL
    target_name = UnicodeAttribute(hash_key=True, null=False)
    current_id = NumberAttribute(null=False)

    @classmethod
    def next_sequence(cls, class_name):
        record = cls.create_or_increment(class_name)
        return record.current_id

    @classmethod
    def create_or_increment(cls, class_name):
        """ 対象のクラスのレコード数(id)を登録 """
        try:
            # 既に1レコード以上ある場合
            record = cls.get(class_name)
            record.update(actions=[
                cls.current_id.set(record.current_id + 1)
            ])
            return record
        except cls.DoesNotExist:
            # レコードが無い場合
            record = cls(class_name, current_id=1)
            record.save()
            return record

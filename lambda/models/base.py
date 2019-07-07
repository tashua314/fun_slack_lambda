# coding: UTF-8

from datetime import datetime
from os import environ
from os.path import dirname, join

from dotenv import load_dotenv

from pynamodb.attributes import NumberAttribute
from pynamodb.attributes import UTCDateTimeAttribute
from pynamodb.models import Model

from .sequence import Sequence

DOTENV_PATH = join(dirname(__file__), '.env')
load_dotenv(DOTENV_PATH)


class Base(Model):
    """
    ベースモデル
    このモデルを継承してモデルを作成する
    """
    class Meta:
        # 各モデルで設定
        table_name = ''

        region = 'ap-northeast-1'
        aws_access_key_id = environ.get("AWS_ACCESS_KEY")
        aws_secret_access_key = environ.get("AWS_SECRETE_KEY")

    id = NumberAttribute(null=False)
    # レコード作成日時
    created_at = UTCDateTimeAttribute(
        default=datetime.now()
    )

    def __init__(
            self, hash_key=None, range_key=None,
            _user_instantiated=True, **attributes
    ):
        class_name = self.__class__.__name__
        if class_name == 'Sequence':
            return

        # idをインクリメント
        __id = Sequence.next_sequence(class_name)
        attributes.update({'id': __id})

        super().__init__(
            hash_key=hash_key,
            range_key=range_key,
            _user_instantiated=_user_instantiated,
            **attributes
        )

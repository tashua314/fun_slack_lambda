# coding: UTF-8

from pynamodb.attributes import NumberAttribute
from pynamodb.attributes import UnicodeAttribute

from .base import Base
from .sequence import Sequence


class Scrap(Base):
    """
    スクラップモデル
    スクレイピングデータを扱う
    """
    class Meta:
        table_name = 'scrap'

    # スクレイピング対象のURL
    scrap_url = UnicodeAttribute(hash_key=True, null=False)
    # スクレイピング対象毎の連番
    unit_id = NumberAttribute(range_key=True, null=False)
    # 取得したテキスト
    text = UnicodeAttribute(null=False)
    # リンク先のURL
    redirect_url = UnicodeAttribute()
    # 公開日時
    released_at = UnicodeAttribute(null=False)

    def __init__(
            self, hash_key=None, range_key=None,
            _user_instantiated=True, **attributes
    ):
        # idをインクリメント
        unit_id = Sequence.next_sequence('Scrap_'+hash_key)

        super().__init__(
            hash_key=hash_key,
            range_key=unit_id,
            _user_instantiated=_user_instantiated,
            **attributes
        )

    @classmethod
    def get_latest(cls, scrap_url):
        """ 最新データ取得 """
        latest_unit_id = cls.__get_latest_unit_id(scrap_url)
        if latest_unit_id is None:
            return None

        try:
            return cls.get(scrap_url, latest_unit_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def __get_latest_unit_id(cls, scrap_url):
        try:
            return Sequence.get(
                cls.__target_sequence_name(scrap_url)
            ).current_id
        except Sequence.DoesNotExist:
            return None

    @classmethod
    def __target_sequence_name(cls, scrap_url):
        return "{}_{}".format(__class__.__name__, scrap_url)

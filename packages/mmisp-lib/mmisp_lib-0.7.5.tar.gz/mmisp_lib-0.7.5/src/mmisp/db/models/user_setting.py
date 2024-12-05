from enum import Enum
from time import time

from sqlalchemy import ForeignKey, Integer, String, Text

from mmisp.db.database import Base
from mmisp.db.mypy import Mapped, mapped_column

from .user import User


class SettingName(Enum):
    PUBLISH_ALERT_FILTER = "publish_alert_filter"
    DASHBOARD_ACCESS = "dashboard_access"
    DASHBOARD = "dashboard"
    HOMEPAGE = "homepage"
    DEFAULT_RESTSEARCH_PARAMETERS = "default_restsearch_parameters"
    TAG_NUMERICAL_VALUE_OVERRIDE = "tag_numerical_value_override"
    EVENT_INDEX_HIDE_COLUMNS = "event_index_hide_columns"
    PERIODIC_NOTIFICATION_FILTERS = "periodic_notification_filters"
    USER_NAME = "user_name"
    VISUAL_SETTING = "visual_setting"


class UserSetting(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    setting: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, index=True)
    timestamp: Mapped[int] = mapped_column(Integer, default=time, onupdate=time, nullable=False, index=True)

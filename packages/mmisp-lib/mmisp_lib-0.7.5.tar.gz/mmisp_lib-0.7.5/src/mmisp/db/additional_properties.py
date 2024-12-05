from sqlalchemy import func, select
from sqlalchemy.orm import column_property

from mmisp.db.models.organisation import Organisation
from mmisp.db.models.user import User

Organisation.user_count = column_property(
    select(func.count(User.id)).where(User.org_id == Organisation.id).correlate_except(User).scalar_subquery(),
    deferred=False,
)

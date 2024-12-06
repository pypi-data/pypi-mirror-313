from sqlmodel import Session

from mtmai.crud import curd
from mtmai.models.models import Item, ItemCreate
from mtmai.tests.utils.user import create_random_user
from mtmai.tests.utils.utils import random_lower_string


def create_random_post(db: Session) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    return curd.create_item(session=db, item_in=item_in, owner_id=owner_id)

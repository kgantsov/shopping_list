from app.db import db
from app.schemas.shopping_list import Unit


class ShoppingListModel(db.Model):
    __tablename__ = 'shopping_list'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    description = db.Column(db.Unicode())

    user_id = db.Column(None, db.ForeignKey('user.id'))


class ShoppingItemModel(db.Model):
    __tablename__ = 'shopping_item'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    quantity = db.Column(db.Integer())
    unit = db.Column(db.Enum(Unit), nullable=False, default=Unit.kg)
    done = db.Column(db.Boolean(), default=False)

    user_id = db.Column(None, db.ForeignKey('user.id'))
    shopping_list_id = db.Column(None, db.ForeignKey('shopping_list.id'))

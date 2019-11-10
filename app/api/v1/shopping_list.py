from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.db import db

from app.auth import get_current_active_user
from app.models.auth import UserModel

from app.schemas.shopping_list import ShoppingListSchema
from app.schemas.shopping_list import ShoppingItemSchema
from app.schemas.shopping_list import ShoppingItemsSchema
from app.models.shopping_list import ShoppingListModel
from app.models.shopping_list import ShoppingItemModel


router = APIRouter()


@router.post("/lists/", response_model=ShoppingListSchema)
async def add_shopping_list(
        shopping_list_schema: ShoppingListSchema,
        user: UserModel = Depends(get_current_active_user)
):
    shopping_list = await ShoppingListModel.create(
        name=shopping_list_schema.name,
        description=shopping_list_schema.description,
        user_id=user.id
    )
    return ShoppingListSchema.parse_obj(shopping_list.to_dict())


@router.get("/lists/{list_id}/", response_model=ShoppingListSchema)
async def get_shopping_list(list_id: int, user: UserModel = Depends(get_current_active_user)):
    shopping_list = await ShoppingListModel.query.where(
        db.and_(
            ShoppingListModel.user_id == user.id,
            ShoppingListModel.id == list_id,
        )
    ).gino.first()

    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    return ShoppingListSchema.parse_obj(shopping_list.to_dict())


@router.put("/lists/{list_id}/", response_model=ShoppingListSchema)
async def edit_shopping_list(
        list_id: int,
        shopping_list_schema: ShoppingListSchema,
        user: UserModel = Depends(get_current_active_user)
):
    shopping_list = await ShoppingListModel.query.where(
        db.and_(
            ShoppingListModel.user_id == user.id,
            ShoppingListModel.id == list_id,
        )
    ).gino.first()

    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    await shopping_list.update(
        name=shopping_list_schema.name,
        description=shopping_list_schema.description,
    ).apply()

    return ShoppingListSchema.parse_obj(shopping_list.to_dict())


@router.delete("/lists/{list_id}/")
async def delete_shopping_list(
        list_id: int,
        user: UserModel = Depends(get_current_active_user)
):
    shopping_list = await ShoppingListModel.query.where(
        db.and_(
            ShoppingListModel.user_id == user.id,
            ShoppingListModel.id == list_id,
        )
    ).gino.first()

    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    await shopping_list.delete()

    return {}, 204


@router.post("/lists/{list_id}/items/", response_model=ShoppingItemSchema)
async def add_shopping_item(
        list_id: int,
        shopping_item_schema: ShoppingItemSchema,
        user: UserModel = Depends(get_current_active_user)
):
    shopping_list = await ShoppingItemModel.create(
        name=shopping_item_schema.name,
        quantity=shopping_item_schema.quantity,
        unit=shopping_item_schema.unit,
        done=shopping_item_schema.done,
        shopping_list_id=list_id,
        user_id=user.id,
    )
    return ShoppingItemSchema.parse_obj(shopping_list.to_dict())


@router.get("/lists/{list_id}/items/", response_model=ShoppingItemsSchema)
async def get_shopping_list_items(
        list_id: int,
        user: UserModel = Depends(get_current_active_user)
):
    shopping_list = await ShoppingListModel.query.where(
        db.and_(
            ShoppingListModel.user_id == user.id,
            ShoppingListModel.id == list_id,
        )
    ).gino.first()

    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    shopping_list_items = await ShoppingItemModel.query.where(
        db.and_(
            ShoppingItemModel.user_id == user.id,
            ShoppingItemModel.shopping_list_id == list_id,
        )
    ).limit(200).gino.all()

    return ShoppingItemsSchema.parse_obj({
        'shopping_list': shopping_list.to_dict(),
        'objects': [x.to_dict() for x in shopping_list_items],
    })


@router.get("/lists/{list_id}/items/{item_id}/", response_model=ShoppingItemsSchema)
async def get_shopping_list_item(
        list_id: int,
        item_id: int,
        user: UserModel = Depends(get_current_active_user)
):
    shopping_list = await ShoppingListModel.query.where(
        db.and_(
            ShoppingListModel.user_id == user.id,
            ShoppingListModel.id == list_id,
        )
    ).gino.first()

    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    shopping_list_item = await ShoppingItemModel.query.where(
        db.and_(
            ShoppingItemModel.user_id == user.id,
            ShoppingItemModel.shopping_list_id == list_id,
        )
    ).gino.first()

    if not shopping_list_item:
        raise HTTPException(status_code=404, detail="Shopping list item not found")

    return ShoppingItemSchema.parse_obj(shopping_list_item.to_dict())


@router.delete("/lists/{list_id}/items/{item_id}/", response_model=ShoppingItemsSchema)
async def delete_shopping_list_item(
        list_id: int,
        item_id: int,
        user: UserModel = Depends(get_current_active_user)
):
    shopping_list = await ShoppingListModel.query.where(
        db.and_(
            ShoppingListModel.user_id == user.id,
            ShoppingListModel.id == list_id,
        )
    ).gino.first()

    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    shopping_list_item = await ShoppingItemModel.query.where(
        db.and_(
            ShoppingItemModel.user_id == user.id,
            ShoppingItemModel.shopping_list_id == list_id,
        )
    ).gino.first()

    if not shopping_list_item:
        raise HTTPException(status_code=404, detail="Shopping list item not found")

    await shopping_list_item.delete()

    return {}, 204

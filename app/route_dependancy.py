# # routes.py
# from fastapi import APIRouter, Depends, Request, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from app import crud, schemas, database
#
# router = APIRouter()
#
# @router.post("/items/", response_model=schemas.ItemResponse)
# async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(database.get_tenant_db)):
#     return await crud.create_item(db=db, item=item)
#
# @router.get("/items/", response_model=list[schemas.ItemResponse])
# async def read_items(db: AsyncSession = Depends(database.get_tenant_db)):
#     return await crud.get_items(db=db)
#
# @router.get("/items/{item_id}", response_model=schemas.ItemResponse)
# async def read_item(item_id: int, db: AsyncSession = Depends(database.get_tenant_db)):
#     item = await crud.get_item(db=db, item_id=item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item
#
# @router.put("/items/{item_id}", response_model=schemas.ItemResponse)
# async def update_item(item_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(database.get_tenant_db)):
#     updated_item = await crud.update_item(db=db, item_id=item_id, item=item)
#     if updated_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return updated_item
#
# @router.delete("/items/{item_id}", response_model=schemas.ItemResponse)
# async def delete_item(item_id: int, db: AsyncSession = Depends(database.get_tenant_db)):
#     deleted_item = await crud.delete_item(db=db, item_id=item_id)
#     if deleted_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return deleted_item
#
# @router.get("/some-endpoint")
# async def some_endpoint(request: Request, session: AsyncSession = Depends(database.get_tenant_db)):
#     host = request.headers.get("host")
#     subdomain = host.split(".")[0] if host else None
#
#     if not subdomain:
#         raise HTTPException(status_code=400, detail="Invalid subdomain")
#
#     return {"message": "Success", "tenant": subdomain}

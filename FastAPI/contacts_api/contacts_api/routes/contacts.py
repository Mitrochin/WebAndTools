from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from contacts_api.database import get_db
from contacts_api import schemas
from contacts_api.repository import contacts as contact_repository

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: schemas.ContactCreate, db: AsyncSession = Depends(get_db)):
    new_contact = await contact_repository.create_contact(contact, db)
    return new_contact


@router.get("/", response_model=list[schemas.ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    contacts = await contact_repository.get_contacts(limit=limit, offset=skip, db=db)
    return contacts


@router.get("/{contact_id}", response_model=schemas.ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await contact_repository.get_contact(contact_id=contact_id, db=db)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=schemas.ContactResponse)
async def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: AsyncSession = Depends(get_db)):
    updated_contact = await contact_repository.update_contact(contact_id=contact_id, contact=contact, db=db)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await contact_repository.delete_contact(contact_id=contact_id, db=db)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.get("/search", response_model=list[schemas.ContactResponse])
async def search_contacts(
        first_name: Optional[str] = Query(None, min_length=1),
        last_name: Optional[str] = Query(None, min_length=1),
        email: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db)
):
    contacts = await contact_repository.search_contacts(db=db, first_name=first_name, last_name=last_name, email=email)
    if not contacts:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return contacts


@router.get("/upcoming_birthdays", response_model=list[dict])
async def upcoming_birthdays(days: int = 7, db: AsyncSession = Depends(get_db)):
    contacts = await contact_repository.get_upcoming_birthdays(db=db, days=days)
    return contacts


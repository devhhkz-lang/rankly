from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import Any
from models import Number
from demo_auth.views import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)


contacts_of_users = [

]


@app.get('/')
async def main() -> dict[str, Any]:
    return {
        'status' : 'ok',
        'code' : 200
    }

@app.get('/contacts')
async def get_contacts() -> dict:
    return {
        i+1: v.number for i, v in enumerate(contacts_of_users)
    }

@app.get('/contacts/{number}')
async def get_contact(number: int) -> dict:
    for contact in contacts_of_users:
        if number == contact.number:
            return {
                "number" : number
            }
    raise HTTPException(
        status_code=404,
        detail="Number not found"
    )

@app.post('/contacts')
async def post_contact(contact: Number) -> dict:
    if any(
        contact.number == i.number
        for i in contacts_of_users
    ):
        raise HTTPException(
            status_code=409,
            detail="Number is already exists"
        )
    contacts_of_users.append(contact)
    return {
        'contact' : contact.number,
        'added' : True
    }
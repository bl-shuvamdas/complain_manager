from typing import Optional

import asyncclick as click
from pydantic import EmailStr

from db import database
from manager import UserManager
from models import RollType


@click.command()
@click.option("-e", "--email", type=EmailStr, required=True)
@click.option("-p", "--password", type=str, required=True)
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-ph", "--phone", type=str, required=True)
async def create_user(email: EmailStr,
                      password: str,
                      first_name: Optional[str] = None,
                      last_name: Optional[str] = None,
                      iban: Optional[str] = None,
                      phone: Optional[str] = None
                      ):
    user_data = {
        "email": email,
        "password": password,
        "role": RollType.admin,
        "first_name": first_name,
        "last_name": last_name,
        "iban": iban,
        "phone": phone
    }
    await database.connect()
    await UserManager.register(user_data=user_data)
    await database.disconnect()


if __name__ == "__main__":
    create_user(_anyio_backend="asyncio")

# export PYTHONPATH=./
# python commands/createsuperuser.py -e admin@email.com -p password -f shuvam -l das -i iban0012458741 -ph 1234567890

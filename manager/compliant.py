from db import database
from models import Complaint, RollType, State


class ComplainManager:
    @staticmethod
    async def get_complaints(user):
        q = Complaint.select()
        if user.roll == RollType.complainer:
            q = q.where(Complaint.c.complainer_id == user.id)
            print(q)
        elif user.roll == RollType.approver:
            q = q.where(Complaint.c.state == State.pending)
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(data, user):
        data['complainer_id'] = user.id
        id_ = await database.execute(Complaint.insert().values(**data))
        return await database.fetch_one(Complaint.select().where(Complaint.c.id == id_))

    @staticmethod
    async def delete_complaint(id_):
        return await database.fetch_one(Complaint.delete().where(Complaint.c.id == id_))

    @staticmethod
    async def approve(id_):
        return await database.execute(Complaint.update().where(Complaint.c.id == id_).values(status=State.approved))

    @staticmethod
    async def reject(id_):
        return await database.execute(Complaint.update().where(Complaint.c.id == id_).values(status=State.rejected))

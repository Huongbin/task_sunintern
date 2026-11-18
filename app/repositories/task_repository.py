from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Task]:
        result = await self.session.execute(select(Task).order_by(Task.id))
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def create(self, title: str, description: str | None) -> Task:
        task = Task(title=title, description=description)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update(self, task: Task, title: str, description: str | None) -> Task:
        task.title = title
        task.description = description
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.commit()

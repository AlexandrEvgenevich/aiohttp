from aiohttp import web
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

d_base = 'postgresql+asyncpg://postgres:postgres@localhost:5432/rat_data_base'
engine = create_async_engine(d_base)

Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Notifications(Base):
    __tablename__ = 'Notes'

    noti_id = Column(Integer, primary_key=True)
    header = Column(String)
    description = Column(String)
    creation_date = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


async def rat_page(request):
    return web.json_response({'rat': 'rat'})


class Notis(web.View):

    async def get(self):

        async with engine.begin() as dat_base_connect:
            await dat_base_connect.run_sync(Base.metadata.create_all)
            await dat_base_connect.commit()

        Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with Session() as session:
            noti_id = self.request.match_info['noti_id']
            responce = await session.get(Notifications(noti_id=noti_id), int(noti_id))
        return web.json_response({'sucsess': responce})

    async def post(self):

        async with engine.begin() as dat_base_connect:
            await dat_base_connect.run_sync(Base.metadata.create_all)
            await dat_base_connect.commit()

        Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        data = await self.request.json()
        async with Session() as session:
            session.add(Notifications(header=data['header'], description=data['description'], owner=data['owner']))
            await session.commit()

        return web.json_response({'sucsses': 'note added'})

    async def patch(self):
        async with engine.begin() as dat_base_connect:
            await dat_base_connect.run_sync(Base.metadata.create_all)
            await dat_base_connect.commit()

        Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        noti_id = self.request.match_info['noti_id']
        data = await self.request.json()
        async with Session() as session:
            session.patch(Notifications(header=data['header'], description=data['description'], owner=data['owner']))
            await session.commit()

        return web.json_response({'sucsses': 'note pathed'})

    async def delete(self):
        return web.json_response()


app = web.Application()
app.router.add_get('', rat_page)
app.router.add_post('/notifications', Notis)
app.router.add_get('/notifications/{noti_id:\d+}', Notis)
app.router.add_patch('/notifications/{noti_id:\d+}', Notis)
app.router.add_delete('/notifications/{noti_id:\d+}', Notis)

if __name__ == '__main__':
    web.run_app(app)

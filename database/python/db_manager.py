import aiosqlite
from datetime import datetime


class DBManager():

    async def startup():
        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                with open("./database/sql/booker_schema.sql") as sql:
                    schema = sql.read()

                async with db.cursor() as cursor:
                    await cursor.executescript(schema)

                await db.commit()

        except Exception as e:
            print(e)

    async def add_room(id: int, room_number: str, room_name: str):
        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                await db.execute("PRAGMA foreign_keys = ON")
                async with db.cursor() as cursor:
                    await cursor.execute(f"INSERT INTO Room VALUES({id},'{room_number}','{room_name}')")

                await db.commit()

        except Exception as e:
            print(e)

    async def add_booking(start_date: str, end_date: str, user_id: str, name: str, room_id: int):
        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                await db.execute("PRAGMA foreign_keys = ON")
                async with db.cursor() as cursor:
                    await cursor.execute(
                        f"INSERT INTO Booking VALUES('{start_date}','{end_date}','{user_id}','{name}',{room_id})"
                    )

                await db.commit()

        except Exception as e:
            print(e)

    async def find_todays_bookings():
        rows = None

        today = datetime.now().strftime("%Y-%m-%d")

        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f"SELECT * FROM Booking WHERE B_StartDate LIKE '{today}%'")
                    rows = await cursor.fetchall()

                await db.commit()

        except Exception as e:
            print(e)

        return rows

    async def find_todays_bookings_time():
        rows = None

        today = datetime.now().strftime("%Y-%m-%d")

        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f"SELECT B_StartDate, B_EndDate FROM Booking WHERE B_StartDate LIKE '{today}%'")
                    rows = await cursor.fetchall()

                await db.commit()

        except Exception as e:
            print(e)

        return rows

    async def find_my_bookings(user_id: str):
        rows = None
        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f"SELECT * FROM Booking WHERE B_UserID = {user_id}")
                    rows = await cursor.fetchall()

                await db.commit()

        except Exception as e:
            print(e)

        return rows

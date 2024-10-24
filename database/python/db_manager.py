import aiosqlite
from datetime import datetime, timedelta

from classes.datetime_manager import DTManager as dtm


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
                    query = "INSERT INTO Room(R_ID, R_RoomNumber, R_Name) VALUES(?,?,?)"
                    await cursor.execute(query, (id, room_number, room_name))

                await db.commit()

        except Exception as e:
            print(e)

    async def add_booking(start_date: str, end_date: str, user_id: str, name: str, room_id: int):
        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                await db.execute("PRAGMA foreign_keys = ON")
                async with db.cursor() as cursor:
                    query = "INSERT INTO Booking(B_StartDate, B_EndDate, B_UserID, B_Name, B_RoomID) Values(?,?,?,?,?)"
                    await cursor.execute(query, (start_date, end_date, user_id, name, room_id))

                await db.commit()

        except Exception as e:
            print(e)

    async def find_bookings(date: str = "today", offset: int = 0, expanded: bool = True) -> list:
        rows = None

        interval_dt = dtm.get_interval_utc(date, offset)

        start_str: str = dtm.datetime_to_string(interval_dt[0])
        end_str: str = dtm.datetime_to_string(interval_dt[1])
        expanded_str: str = "*" if expanded else "B_StartDate, B_EndDate"

        try:
            async with aiosqlite.connect("./database/booker_db.sqlite") as db:
                async with db.cursor() as cursor:
                    query = f"""
                        SELECT {expanded_str}
                        FROM Booking
                        WHERE B_StartDate >= ? AND B_StartDate < ?
                    """
                    await cursor.execute(query, (start_str, end_str))
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

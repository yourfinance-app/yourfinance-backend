import asyncio


async def main():
    from yfa.database.utils import create_user_database
    print(await create_user_database("yfa_1001"))


if __name__ == "__main__":
    asyncio.run(main())

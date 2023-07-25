import asyncio

from src.extensions.DBWorkerExtension import DataBase


async def main():
    db = DataBase("GamesHeadless.db")
    await db.connect()

    """ Информация о профиле пользователя
    ProfileID INTEGER   - уникальный id человека
    BankAccount REAL    - счёт внутренней валюты человека
    """
    await db.run_que(
        "CREATE TABLE IF NOT EXISTS UserProfiles "
        "(ProfileID INTEGER, BankAccount REAL)"
    )

    """ Информация о созданном контейнере + сервере
    ContainerOwner INTEGER  - id хозяина контейнера
    ContainerSettings TEXT  - json настроек контейнера
    ServerSettings TEXT     - json настроек сервера игры
    """
    await db.run_que(
        "CREATE TABLE IF NOT EXISTS CreatedServers "
        "(HostIP TEXT, ContainerOwner INTEGER, ContainerSettings TEXT, ServerSettings TEXT)"
    )

    await db.close()


if __name__ == "__main__":
    asyncio.run(main())

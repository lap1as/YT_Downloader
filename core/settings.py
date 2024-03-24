from dataclasses import dataclass
from environs import Env


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    parse_mode: str


@dataclass
class Database:
    uri: str


@dataclass
class Settings:
    bots: Bots
    db: Database


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("BOT_TOKEN"),
            admin_id=int(env.str("ADMIN_ID")),
            parse_mode="HTML"
        ),
        db=Database(
            uri=env.str("MONGODB_URI")
        )
    )


settings = get_settings('.env')

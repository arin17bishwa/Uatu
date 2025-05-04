from config import export_db_config
from sqlalchemy import URL, create_engine
import sqlacodegen


def func():
    db_config = export_db_config()
    db_url = URL(
        drivername="oracle+oracledb",
        username=db_config["DB_USER"],
        host=db_config["DB_HOST"],
        port=db_config["DB_PORT"],
        password=db_config["DB_PASSWORD"],
        database=None,
        query={"service_name": db_config["DB_NAME"]},
    )
    api_db_engine = create_engine(url=db_url, echo=False, thick_mode=True)

    print(db_url.render_as_string(hide_password=False))


def main():
    func()


if __name__ == "__main__":
    main()

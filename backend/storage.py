from sqlalchemy import create_engine

engine = create_engine("sqlite:///market.db")


def persist(df, table="market_data"):
    df.to_sql(table, engine, if_exists="append", index=False)

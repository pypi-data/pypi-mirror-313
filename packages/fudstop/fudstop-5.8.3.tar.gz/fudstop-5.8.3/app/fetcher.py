import asyncpg


async def fetch_rsi_status_data():
    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT insertion_timestamp, timespan, ticker, rsi, status FROM rsi_status ORDER BY insertion_timestamp DESC"
    )
    await conn.close()
    return rows


async def fetch_td9():
    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT ticker, timespan, td9_state, insertion_timestamp FROM market_data ORDER BY insertion_timestamp DESC"
    )
    await conn.close()
    return rows


async def fetch_sec_filings():
    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT ticker, link, title, insertion_timestamp FROM sec_filings ORDER BY insertion_timestamp DESC;"
    )
    await conn.close()
    return rows


async def fetch_reg_sho():
    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT ticker, date, time, code FROM reg_sho ORDER BY date, time DESC;"
    )
    await conn.close()
    return rows


async def fetch_conditions():
    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch( 
        "SELECT ticker, strike, call_put, expiry, size, price, conditions, timestamp FROM conditions ORDER BY timestamp DESC;"
    )
    await conn.close()
    return rows

async def fetch_dark_pools():
    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT ticker,price,notional_value,sector,time FROM dark_pools ORDER BY time DESC;"
    )
    await conn.close()
    return rows


async def fetch_flow():
    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT flow_type, ticker, strike, call_put, expiry, dte, volume, oi, iv, sentiment, timestamp FROM flow ORDER BY timestamp DESC;"
    )
    await conn.close()
    return rows



async def fetch_reddit_posts():

    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT subreddit, title, context, insertion_timestamp FROM reddit_posts ORDER BY insertion_timestamp DESC;"
    )
    await conn.close()
    return rows

async def fetch_momentum_scalps():

    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT ticker, timeframe, move, insertion_timestamp FROM momentum_scalps ORDER BY insertion_timestamp DESC;"
    )
    await conn.close()
    return rows


async def fetch_messages():

    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT username, message, timestamp FROM messages ORDER BY timestamp DESC;"
    )
    await conn.close()
    return rows

async def fetch_crypto():

    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT ticker, dollar_cost, side, timestamp FROM crypto ORDER BY timestamp DESC;"
    )
    await conn.close()
    return rows

async def fetch_option_trades():

    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT size_type, ticker, strike, call_put, expiry, size, dollar_cost, timestamp FROM option_trades ORDER BY timestamp DESC;"
    )
    await conn.close()
    return rows



async def fetch_articles():

    conn = await asyncpg.connect("postgresql://chuck:fud@localhost:5432/fudstop")
    rows = await conn.fetch(
        "SELECT title, summary, publisher_name, article_url FROM articles ORDER BY published_utc DESC;"
    )
    await conn.close()
    return rows
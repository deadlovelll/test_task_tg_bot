import aiohttp

AVITO_ITEMS_URL = "https://api.avito.ru/core/v1/items"
AVITO_CALL_STATS_URL = "https://api.avito.ru/core/v1/accounts/{user_id}/calls/stats/"

async def get_avito_items(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(AVITO_ITEMS_URL, headers=headers) as response:
            return await response.json()

async def get_call_stats(token, user_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = AVITO_CALL_STATS_URL.format(user_id=user_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

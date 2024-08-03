import asyncio
from asyncio.log import logger
import aiohttp


async def fetch_json(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        return None


async def get_author_name(session, book_data):
    author_key = book_data.get("authors", [{}])[0].get("key")
    if not author_key:
        return "Unknown"
    url = f"https://openlibrary.org{author_key}.json"
    author_data = await fetch_json(session, url)
    return author_data.get("name", "Unknown") if author_data else "Unknown"


async def get_description(session, book_data):
    work_key = book_data.get("works", [{}])[0].get("key")
    if not work_key:
        return "Unknown"
    url = f"https://openlibrary.org{work_key}.json"
    works_data = await fetch_json(session, url)
    return works_data.get("description", "Unknown") if works_data else "Unknown"


async def async_handler(event, context):
    isbn = event.get("isbn")
    if not isbn:
        logger.error("ISBN is required")
        return {"statusCode": 400, "body": {"error": "ISBN is required"}}

    try:
        async with aiohttp.ClientSession() as session:
            book_url = f"https://openlibrary.org/isbn/{isbn}.json"
            book_data = await fetch_json(session, book_url)

            if not book_data:
                return {"statusCode": 404, "body": {"error": "Book not found"}}

            author_name, description = await asyncio.gather(
                get_author_name(session, book_data), get_description(session, book_data)
            )

            book_info = {
                "title": book_data.get("title", "Unknown"),
                "author": author_name,
                "publish_date": book_data.get("publish_date", "Unknown"),
                "description": description,
            }

            return {
                "statusCode": 200,
                "body": book_info,
            }

    except Exception as e:
        return {"statusCode": 500, "body": {"error": str(e)}}


def handler(event, context):
    return asyncio.run(async_handler(event, context))

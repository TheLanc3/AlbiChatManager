import json
import aiofiles

from user_records import UserRecords

async def update_user(userId: int, userData: UserRecords):
    async with aiofiles.open(f"users_records/{userId}.json", "w") as data:
        j_data = json.dumps(userData.__dict__, indent=4)
        await data.write(j_data)
import aiohttp

class cybralist:
    def __init__(self, client, token):
        self.client = client
        self.token = token

    async def serverCountPost(self):
        async with aiohttp.ClientSession() as session:
            payload = {'serverCount': str(len(self.client.guilds))}
            headers = {'Authorization': str(self.token), 'Content-Type': 'application/json'}
            async with session.post(url="https://api.cybralist.com/post/stats", json=payload, headers=headers) as res:
                print("Server count posted.")
                return await res.json()

    async def hasVoted(self, id):
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': str(self.token)}
            async with session.get(f"https://api.cybralist.com/vote/check/{id}", headers=headers) as res:
                return await res.json()

    async def search(self, id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.cybralist.com/bots/{id}") as res:
                return await res.json()

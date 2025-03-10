import asyncio
from colorama import init, Style
import httpx
import concurrent.futures
from agent import gr_ua
from deeplchain import log, countdown_timer, mrh, bru, pth, hju, kng, _clear, _banner, read_config

init(autoreset=True)

class Grows:
    def __init__(self, token_file):
        self.config = read_config()
        with open(token_file, "r") as file:
            self.access_tokens = [line.strip() for line in file if line.strip()]
        self.api_url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
        self.countdown_before_start = self.config.get('countdown_before_start', False)
        self.countdown_loop = self.config.get('countdown_loop', 60)
        self.api_key = "AIzaSyDipzN0VRfTPnMGhQ5PSzO27Cxm3DohJGY"
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'User-Agent': gr_ua()
        }

    async def start(self, url, method, payload_data=None, retries=3, delay=3, timeout=20):
        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.request(method, url, headers=self.headers, json=payload_data)
                    if response.status_code != 200:
                        raise Exception(f'HTTP error! Status: {response.status_code}')
                    return response.json()
            except Exception as e:
                log(mrh + f"Failed: Retrying {attempt + 1} {str(e)}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    raise

    async def refresh_access_token(self, refresh_token):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'https://securetoken.googleapis.com/v1/token?key={self.api_key}',
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=f'grant_type=refresh_token&refresh_token={refresh_token}'
            )
            if response.status_code != 200:
                raise Exception(mrh + f"Failed to refresh access token!")
            return response.json().get('access_token')

    async def grow_and_garden(self, refresh_token):
        new_access_token = await self.refresh_access_token(refresh_token)
        self.headers['authorization'] = f'Bearer {new_access_token}'

        info_query = {
            "query": "query CurrentUser { currentUser { id sub name iconPath depositCount totalPoint evmAddress { userId address } inviter { id name } } }",
            "operationName": "CurrentUser"
        }
        info = await self.start(self.api_url, 'POST', info_query)

        balance = info['data']['currentUser']['totalPoint']
        deposit = info['data']['currentUser']['depositCount']

        bet_query = {
            "query": "query GetGardenForCurrentUser { getGardenForCurrentUser { id inviteCode gardenDepositCount gardenStatus { id activeEpoch growActionCount gardenRewardActionCount } gardenMilestoneRewardInfo { id gardenDepositCountWhenLastCalculated lastAcquiredAt createdAt } gardenMembers { id sub name iconPath depositCount } } }",
            "operationName": "GetGardenForCurrentUser"
        }
        profile = await self.start(self.api_url, 'POST', bet_query)

        grow = profile['data']['getGardenForCurrentUser']['gardenStatus']['growActionCount']
        garden = profile['data']['getGardenForCurrentUser']['gardenStatus']['gardenRewardActionCount']
        print(hju + f"Points: {pth}{balance} {hju}| Grow : {pth}{grow} {hju}| Garden : {pth}{garden} {hju}| Deposit : {pth}{deposit} ")

        while garden <= 10:
            log(kng + f"You dont have enough garden to open!")
            break

        while garden >= 10:
            garden_action_query = {
                "query": "mutation executeGardenRewardAction($limit: Int!) { executeGardenRewardAction(limit: $limit) { data { cardId group } isNew } }",
                "variables": {"limit": 10},
                "operationName": "executeGardenRewardAction"
            }
            mine_garden = await self.start(self.api_url, 'POST', garden_action_query)
            card_ids = [item['data']['cardId'] for item in mine_garden['data']['executeGardenRewardAction']]
            log(hju + f"Garden Opened: {pth}{card_ids}")
            garden -= 10

    def process_token(self, refresh_token):
        asyncio.run(self.grow_and_garden(refresh_token))

    def main(self):
        _clear()
        _banner()
        log(hju + f"Preparing your garden data!")
        countdown_timer(self.countdown_before_start)
        while True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(self.process_token, token) for token in self.access_tokens]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        log(mrh + f"Error processing token: {str(e)}")

            log(bru + f"Cooling down for {self.countdown_loop} seconds...")
            countdown_timer(self.countdown_loop)

if __name__ == '__main__':
    try:
        grows = Grows("tokens.txt")
        grows.main()
    except KeyboardInterrupt:
        log(mrh + f"Keyboard interrupted by user!")

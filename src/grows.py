import asyncio
import aiohttp
from agent import gr_ua
from deeplchain import log, countdown_timer, mrh, bru, pth, hju, kng, htm, _clear, _banner, read_config, log_error

class Grows:
    def __init__(self, token_file):
        self.cfg = read_config()
        with open(token_file, "r") as file:
            self.tokens = [line.strip() for line in file if line.strip()]
        self.api_url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
        self.delay = self.cfg.get('account_delay', 5) 
        self.countdown_before_start = self.cfg.get('countdown_before_start', 5)
        self.cooldown = self.cfg.get('countdown_loop', 3800)
        self.api_key = "AIzaSyDipzN0VRfTPnMGhQ5PSzO27Cxm3DohJGY"
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'User-Agent': gr_ua()
        }

    async def req(self, session, url, method, payload=None):
        """Handle API requests."""
        async with session.request(method, url, headers=self.headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"HTTP Error: {response.status}")
            return await response.json()

    async def refresh_token(self, session, token):
        """Refresh and set authorization token once per session."""
        url = f'https://securetoken.googleapis.com/v1/token?key={self.api_key}'
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = f'grant_type=refresh_token&refresh_token={token}'
        async with session.post(url, headers=headers, data=payload) as response:
            if response.status != 200:
                raise Exception(mrh + f"Failed to refresh token")
            data = await response.json()
            return data.get('access_token')

    async def grow(self, session):
        """Perform the grow action and return reward."""
        query = {
            "query": """
                mutation executeGrowAction {
                    executeGrowAction(withAll: true) {
                        totalValue
                        multiplyRate
                    }
                    executeSnsShare(actionType: GROW, snsType: X) {
                        bonus
                    }
                }
            """,
            "operationName": "executeGrowAction"
        }
        res = await self.req(session, self.api_url, 'POST', query)
        if res and 'data' in res and 'executeGrowAction' in res['data']:
            return res['data']['executeGrowAction']['totalValue']
        else:
            log(mrh + f"Error: Unexpected response: {res}")
            return 0

    async def get_user_info(self, session, token):
        """Retrieve user information and log basic details."""
        auth_token = await self.refresh_token(session, token)
        self.headers['authorization'] = f'Bearer {auth_token}'

        query = {
            "query": """
                query GetGardenForCurrentUser {
                getGardenForCurrentUser {
                    id
                    inviteCode
                    gardenDepositCount
                    gardenStatus {
                    id
                    growActionCount
                    gardenRewardActionCount
                    }
                    gardenMilestoneRewardInfo {
                    id
                    gardenDepositCountWhenLastCalculated
                    lastAcquiredAt
                    createdAt
                    }
                    gardenMembers {
                    id
                    sub
                    name
                    iconPath
                    depositCount
                    }
                }
                }
            """,
            "operationName": "GetGardenForCurrentUser"
        }
        info = await self.req(session, self.api_url, 'POST', query)
        user_id = info['data']['getGardenForCurrentUser']['id']
        invite_code = info['data']['getGardenForCurrentUser']['inviteCode']
        log(hju + f"User ID: {pth}{user_id} {hju}| Invite Code: {pth}{invite_code}")

    async def process_account(self, session, token):
        """Process grow action and handle rewards."""
        auth_token = await self.refresh_token(session, token)
        self.headers['authorization'] = f'Bearer {auth_token}'

        query = {
            "query": "query getCurrentUser { "
                      "currentUser { id totalPoint depositCount } "
                      "getGardenForCurrentUser { "
                      "gardenStatus { growActionCount gardenRewardActionCount } "
                      "} "
                      "} ",
            "operationName": "getCurrentUser"
        }
        info = await self.req(session, self.api_url, 'POST', query)
        balance = info['data']['currentUser']['totalPoint']
        grow = info['data']['getGardenForCurrentUser']['gardenStatus']['growActionCount']
        garden = info['data']['getGardenForCurrentUser']['gardenStatus']['gardenRewardActionCount']
        log(hju + f"Grow: {pth}{grow} {hju}| Garden: {pth}{garden} {hju}| Balance: {pth}{balance}")

        if grow < 10:
            log(hju + "Not enough grow actions to claim!")

        if grow > 0:
            reward = await self.grow(session)
            if reward:
                balance += reward
                log(hju + f"Grow actions: {pth}{0} {hju}| Balance: {pth}{balance} {hju}| Rewards: {pth}{reward}")

    async def main(self):
        log(hju + f"Waiting for {pth}{self.countdown_before_start} seconds {hju}before start!")
        log("~" * 38)
        try:
            async with aiohttp.ClientSession() as session:
                total_accounts = len(self.tokens)
                account_number = 1

                for token in self.tokens:
                    countdown_timer(self.countdown_before_start)
                    log(hju + f"Processing account {pth}{account_number}/{total_accounts}")
                    await self.get_user_info(session, token)
                    await self.process_account(session, token)
                    log("~" * 38)
                    countdown_timer(self.delay)

                    account_number += 1

                countdown_timer(self.cooldown)
                account_number = 1

        except Exception as e:
            log(mrh + "An error occurred, check last.log")
            log_error(f"{e}")

if __name__ == '__main__':
    _clear()
    _banner()
    while True:
        try:
            grows = Grows("tokens.txt")
            asyncio.run(grows.main())
        except KeyboardInterrupt:
            log("Keyboard interrupted by user!")
            exit(0)

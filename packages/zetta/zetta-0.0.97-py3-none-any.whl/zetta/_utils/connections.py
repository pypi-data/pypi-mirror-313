# Copyright ZettaBlock Labs 2024
import requests

ai_network_endpoints = {
    'devnet': 'https://ai-network.stag-vxzy.zettablock.com',
    'testnet': 'https://testnet.prod.zettablock.com',
    'mainnet': 'https://mainnet.prod.zettablock.com'
}

def check_api_status(env):
    url = ai_network_endpoints.get(env)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return {"status": f"{env} API is up and running"}
        else:
            return {"status": f"{env} API is down", "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"status": f"{env} API is down", "error": str(e)}


# 安装依赖：pip install web3 goplus requests
import json
import time
from web3 import Web3
from goplus.token import Token
import requests

INFURA_URL = 'https://mainnet.infura.io/v3/你的infura_key' #你的infura_key
UNISWAP_V3_FACTORY_ADDRESS = '0x1F98431c8aD98523631AE4a59f267346ea31F984'
UNISWAP_V2_FACTORY_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
WETH_ADDRESS = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
DISCORD_WEBHOOK_URL = '你的discord_webhook_url' #你的discord_webhook_url
ETH_THRESHOLD = 1 #只有池子大于1ETH时才会发送消息，可以按需修改

with open('uniswap_v2_factory_abi.json', 'r') as abi_file:
    UNISWAP_V2_FACTORY_ABI = json.load(abi_file)

with open('uniswap_v3_factory_abi.json', 'r') as abi_file:
    UNISWAP_V3_FACTORY_ABI = json.load(abi_file)

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]

WETH_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
weth_contract = web3.eth.contract(address=WETH_ADDRESS, abi=WETH_ABI)
uniswap_v3_factory = web3.eth.contract(address=UNISWAP_V3_FACTORY_ADDRESS, abi=UNISWAP_V3_FACTORY_ABI)
uniswap_v2_factory = web3.eth.contract(address=UNISWAP_V2_FACTORY_ADDRESS, abi=UNISWAP_V2_FACTORY_ABI)

def get_token_symbol(token_address):
    try:
        token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
        symbol = token_contract.functions.symbol().call()
        return symbol
    except Exception as e:
        print(f"获取代币符号失败: {e}")
        return token_address

def get_token_security(token_address):
    try:
        data = Token(access_token=None).token_security(
            chain_id="1",
            addresses=[token_address]
        )
        
        if hasattr(data, 'result') and token_address.lower() in data.result:
            result = data.result[token_address.lower()]
            
            token_security = {
                "is_open_source": result.is_open_source if hasattr(result, 'is_open_source') else 'N/A',#是否开源
                "is_proxy": result.is_proxy if hasattr(result, 'is_proxy') else 'N/A',#是否代理合约
                "is_blacklisted": result.is_blacklisted if hasattr(result, 'is_blacklisted') else 'N/A',#是否有黑名单功能
                "is_honeypot": result.is_honeypot if hasattr(result, 'is_honeypot') else 'N/A',#是否蜜罐合约
                "transfer_pausable": result.transfer_pausable if hasattr(result, 'transfer_pausable') else 'N/A',#是否有暂停转账的功能
                "owner_control": result.owner_control if hasattr(result, 'owner_control') else 'N/A',
                "buy_tax": result.buy_tax if hasattr(result, 'buy_tax') else 'N/A',#买入税
                "sell_tax": result.sell_tax if hasattr(result, 'sell_tax') else 'N/A',#卖出税
                "is_paused": result.is_paused if hasattr(result, 'is_paused') else 'N/A',
                "is_malicious_contract": result.is_malicious_contract if hasattr(result, 'is_malicious_contract') else 'N/A',
                "creator_address": result.creator_address if hasattr(result, 'creator_address') else 'N/A',#合约的创建者地址
                "creator_percent": result.creator_percent if hasattr(result, 'creator_percent') else 'N/A',#创建者持有的代币占总供应量的比例
                "total_supply": result.total_supply if hasattr(result, 'total_supply') else 'N/A',#代币名称总量
                "dex_liquidity": result.dex if hasattr(result, 'dex') else [],#是否在去中心化交易所（DEX）上市
                "is_mintable": result.is_mintable if hasattr(result, 'is_mintable') else 'N/A',#是否可以铸币/增发
                "anti_whale_modifiable": result.anti_whale_modifiable if hasattr(result, 'anti_whale_modifiable') else 'N/A',#是否具有修改最大交易金额或最大代币持仓量的功能
                "can_take_back_ownership": result.can_take_back_ownership if hasattr(result, 'can_take_back_ownership') else 'N/A',
                "cannot_buy": result.cannot_buy if hasattr(result, 'cannot_buy') else 'N/A',#是否可以正常买入
                "cannot_sell_all": result.cannot_sell_all if hasattr(result, 'cannot_sell_all') else 'N/A',#是否限制全部出售
                "external_call": result.external_call if hasattr(result, 'external_call') else 'N/A',#是否调用外部合约
                "fake_token": result.fake_token if hasattr(result, 'fake_token') else 'N/A',#是否伪造代币
                "hidden_owner": result.hidden_owner if hasattr(result, 'hidden_owner') else 'N/A',#是否有隐藏的所有者
                "holder_count": result.holder_count if hasattr(result, 'holder_count') else 'N/A',#持有者数量
                "holders": result.holders if hasattr(result, 'holders') else [],#持有者
                "honeypot_with_same_creator": result.honeypot_with_same_creator if hasattr(result, 'honeypot_with_same_creator') else 'N/A',#创建者是否参与过蜜罐骗局的记录
                "is_airdrop_scam": result.is_airdrop_scam if hasattr(result, 'is_airdrop_scam') else 'N/A',#是否空投骗局
                "is_anti_whale": result.is_anti_whale if hasattr(result, 'is_anti_whale') else 'N/A',#是否反鲸鱼机制
                "is_in_dex": result.is_in_dex if hasattr(result, 'is_in_dex') else 'N/A',#是否在 DEX 上市
                "is_true_token": result.is_true_token if hasattr(result, 'is_true_token') else 'N/A',#是否真实代币
                "is_whitelisted": result.is_whitelisted if hasattr(result, 'is_whitelisted') else 'N/A',#是否白名单机制
                "lp_holder_count": result.lp_holder_count if hasattr(result, 'lp_holder_count') else 'N/A',#流动性提供者数量
                "lp_holders": result.lp_holders if hasattr(result, 'lp_holders') else [],#流动性提供者
                "lp_total_supply": result.lp_total_supply if hasattr(result, 'lp_total_supply') else 'N/A',#流动性总量
                "note": result.note if hasattr(result, 'note') else 'N/A',#没有特别的附注或说明
                "other_potential_risks": result.other_potential_risks if hasattr(result, 'other_potential_risks') else 'N/A',#其他潜在风险
                "owner_address": result.owner_address if hasattr(result, 'owner_address') else 'N/A',#所有者地址
                "owner_balance": result.owner_balance if hasattr(result, 'owner_balance') else 'N/A',#所有者余额
                "owner_change_balance": result.owner_change_balance if hasattr(result, 'owner_change_balance') else 'N/A',#所有者余额变化
                "owner_percent": result.owner_percent if hasattr(result, 'owner_percent') else 'N/A',#所有者持有代币比例
                "personal_slippage_modifiable": result.personal_slippage_modifiable if hasattr(result, 'personal_slippage_modifiable') else 'N/A',#是否允许修改个人滑点（交易税率）
                "selfdestruct": result.selfdestruct if hasattr(result, 'selfdestruct') else 'N/A',#是否有自毁功能
                "slippage_modifiable": result.slippage_modifiable if hasattr(result, 'slippage_modifiable') else 'N/A',#是否可以修改交易滑点（买卖税）
                "trading_cooldown": result.trading_cooldown if hasattr(result, 'trading_cooldown') else 'N/A',#是否有交易冷却机制
                "trust_list": result.trust_list if hasattr(result, 'trust_list') else 'N/A'
            }

            return token_security
        else:
            print(f"GoPlus API 请求失败或结果为空: {data}")
            return None
    except Exception as e:
        print(f"获取代币安全信息失败: {e}")
        return None

def get_icon(value):
    if value == '1':
        return "🟡是"
    elif value == '0':
        return "🟢否"
    else:
        return "❔️未知"
def get_is_open_icon(value):
    if value == '1':
        return "🟢是"
    elif value == '0':
        return "🔴否"
    else:
        return "❔️未知"

def send_discord_message(token0_symbol, token1_symbol, token0_address, token1_address, pair_address, pool_amount):
    if token0_address == WETH_ADDRESS:
        token_address = token1_address
        token_symbol = token1_symbol
    else:
        token_address = token0_address
        token_symbol = token0_symbol
    
    token_security = get_token_security(token_address)
    
    #if token_security and token_security['is_open_source'] == '1':
    if token_security:
        risk_params = [
            token_security['anti_whale_modifiable'],
            token_security['can_take_back_ownership'],
            token_security['cannot_sell_all'],
            token_security['external_call'],
            token_security['fake_token'],
            token_security['hidden_owner'],
            token_security['honeypot_with_same_creator'],
            token_security['is_airdrop_scam'],
            token_security['is_blacklisted'],
            token_security['is_honeypot'],
            token_security['is_mintable'],
            token_security['is_proxy'],
            token_security['personal_slippage_modifiable'],
            token_security['selfdestruct'],
            token_security['slippage_modifiable'],
            token_security['transfer_pausable']
        ]

        if all(param != '1' for param in risk_params):
            anti_whale_icon = get_icon(token_security['is_anti_whale'])
            trading_cooldown_icon = get_icon(token_security['trading_cooldown'])
            is_open_icon = get_is_open_icon(token_security['is_open_source'])

            buy_tax = token_security['buy_tax']
            sell_tax = token_security['sell_tax']
            creator_percent = token_security['creator_percent']
            owner_percent = token_security['owner_percent']
            buy_tax = f"{float(buy_tax) * 100}%" if buy_tax not in [None, '', 'N/A'] else 'N/A'
            sell_tax = f"{float(sell_tax) * 100}%" if sell_tax not in [None, '', 'N/A'] else 'N/A'
            creator_percent = f"{float(creator_percent) * 100}%" if creator_percent not in [None, '', 'N/A'] else 'N/A'
            owner_percent = f"{float(owner_percent) * 100}%" if owner_percent not in [None, '', 'N/A'] else 'N/A'

            lp_holders = token_security['lp_holders']
            lp_addresses = ', '.join(holder['address'] for holder in lp_holders) if lp_holders else '无'

            security_info = (
                f"- 是否开源: {is_open_icon}\n"
                f"- 是否反鲸鱼: {anti_whale_icon}\n"
                f"- 是否有交易冷却机制: {trading_cooldown_icon}\n"
                f"- 买/卖税率: {buy_tax}/{sell_tax}\n"
                f"- 合约创建者: {token_security['creator_address']}\n"
                f"- 合约所有者: {token_security['owner_address']}\n"
                f"- 合约创建者持有比例: {creator_percent}\n"
                f"- 合约所有者持有比例: {owner_percent}\n"
                f"- LP 持有者地址: {lp_addresses}\n"
                f"- 其他潜在风险: {token_security['other_potential_risks']}\n"
                
                
            )
            
            message = {
                "content": (
                    f"代币名称：{token_symbol}\n"
                    f"代币合约地址：{token_address}\n"
                    f"资金池数量：{pool_amount} ETH\n"
                    f"{security_info}"
                    f"[DEXTools](https://www.dextools.io/app/en/ether/pair-explorer/{pair_address}) - [GoPlus](https://gopluslabs.io/token-security/1/{token_address})\n"
                    "-----------------------------------------\n"
                    "-----------------------------------------"
                )
            }

            response = requests.post(DISCORD_WEBHOOK_URL, json=message)
            if response.status_code == 204:
                print(f"成功发送 Discord 消息: {token0_symbol}/{token1_symbol}")
            else:
                print(f"发送 Discord 消息失败: {response.status_code}, {response.text}")
        else:
            print(f"未发送消息，因合约存在风险: {token_address}")
    else:
        print(f"未发送消息，因合约未开源或获取代币安全信息失败: {token_address}")


def monitor_uniswap_v3_new_pairs():
    print("开始监控 Uniswap V3 新 Pairs...")
    
    new_pool_event_filter = uniswap_v3_factory.events.PoolCreated().create_filter(
        from_block='latest'
    )

    while True:
        try:
            events = new_pool_event_filter.get_new_entries()
            print(f"检测到 {len(events)} 个 Uniswap V3 新事件")
            for event in events:
                token0_address = event['args']['token0']
                token1_address = event['args']['token1']
                pool_address = event['args']['pool']
                token0_symbol = get_token_symbol(token0_address)
                token1_symbol = get_token_symbol(token1_address)
                weth_balance = weth_contract.functions.balanceOf(pool_address).call()
                weth_balance_in_ether = Web3.from_wei(weth_balance, 'ether')
                print(f"V3 资金池地址: {pool_address}, WETH 数量: {weth_balance_in_ether}")

                if weth_balance_in_ether >= ETH_THRESHOLD:
                    send_discord_message(token0_symbol, token1_symbol, token0_address, token1_address, pool_address, weth_balance_in_ether)

            time.sleep(10)

        except Exception as e:
            print(f"V3 监控错误: {e}")
            time.sleep(10)

def monitor_uniswap_v2_new_pairs():
    print("开始监控 Uniswap V2 新 Pairs...")
    new_pool_event_filter = uniswap_v2_factory.events.PairCreated().create_filter(
        from_block='latest'
    )

    while True:
        try:
            events = new_pool_event_filter.get_new_entries()
            print(f"检测到 {len(events)} 个 Uniswap V2 新事件")
            for event in events:
                token0_address = event['args']['token0']
                token1_address = event['args']['token1']
                pair_address = event['args']['pair']
                token0_symbol = get_token_symbol(token0_address)
                token1_symbol = get_token_symbol(token1_address)
                weth_balance = weth_contract.functions.balanceOf(pair_address).call()
                weth_balance_in_ether = Web3.from_wei(weth_balance, 'ether')
                print(f"V2 资金池地址: {pair_address}, 资金池余额:{weth_balance}, WETH 数量: {weth_balance_in_ether}")

                if weth_balance_in_ether >= ETH_THRESHOLD:
                    send_discord_message(token0_symbol, token1_symbol, token0_address, token1_address, pair_address, weth_balance_in_ether)

            time.sleep(10)

        except Exception as e:
            print(f"V2 监控错误: {e}")
            time.sleep(10)

if __name__ == '__main__':
    from threading import Thread
    
    v2_thread = Thread(target=monitor_uniswap_v2_new_pairs)
    v3_thread = Thread(target=monitor_uniswap_v3_new_pairs)
    
    v2_thread.start()
    v3_thread.start()
    
    v2_thread.join()
    v3_thread.join()

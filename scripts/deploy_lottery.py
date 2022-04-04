from brownie import Lottery, config, network, Lottery
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(get_contract("eth_usd_price_feed").address, 
    get_contract("vrf_coordinator").address, 
    get_contract("link_token").address,
    config["networks"][network.show_active()]["fee"], 
    config["networks"][network.show_active()]["key_hash"],
    {"from": account},
    publish_source = config["networks"][network.show_active()].get("verify", False))
    return lottery
 

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]   # picking up latest Lottery contract
    lottery.startLottery({"from": account})

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000     # adding some value above the entrance fee to enter the lottery
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the Lottery!!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract with LINK
    # end lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_lottery = lottery.endLottery()
    ending_lottery.wait(1)
    print("Lottery ended!!")
    time.sleep(180)
    print(f"The winner is {lottery.recentWinner()}")
    



def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
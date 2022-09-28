from os import access
from scripts.helpful_scripts import encode_function_data, get_account
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract

def test_proxy_delegate_calls():
    account = get_account()
    box = Box.deploy({"from" : account})
    proxy_admin = ProxyAdmin.deploy({"from" : account})
    box_encoded_initializer_funcitons = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
            box.address,
            proxy_admin.address,
            box_encoded_initializer_funcitons,
            {"from" : account}
        )
    proxy_box = Contract.from_abi("BoxV1", proxy.address, box.abi)
    assert proxy_box.retrive() == 0
    proxy_box.store(1, {"from" : account})
    assert proxy_box.retrive() == 1

from brownie import (
    Box,
    BoxV2,
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    network,
    config
)

from scripts.helpful_scripts import encode_function_data, get_account, upgrade


# Implement contract
def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(box.retrive())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # Encode initializer contract
    # initializer = box.store, 1
    box_encoded_initializer_func = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_func,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deploy to {proxy}, you can now upgrade to v2")

    proxy_box = Contract.from_abi(
        "Box", proxy.address, Box.abi
    )  # This proxy have the Box abi, and delegate all the calls to Box class
    proxy_box.store(1, {"from": account})

    # Upgrade
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from" : account})
    print(
        f"After upgrade: {proxy_box.retrive()}"
    )  # How we can see, the value has been saved after upgrade

    # Can see in the goeli testnet the proxy and the call to the box functions

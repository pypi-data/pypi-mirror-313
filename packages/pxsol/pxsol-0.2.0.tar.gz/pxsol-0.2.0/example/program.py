import argparse
import base64
import pathlib
import pxsol

# Publish a hello solana program, call it to show "Hello, Solana!". Then we update the program and call it again, and
# finally it will be explicit "Hello, Update!".

parser = argparse.ArgumentParser()
parser.add_argument('--action', type=str, choices=['call', 'deploy', 'update'])
parser.add_argument('--addr', type=str, help='addr')
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
args = parser.parse_args()

if args.net == 'develop':
    pxsol.config.current = pxsol.config.develop
if args.net == 'mainnet':
    pxsol.config.current = pxsol.config.mainnet
if args.net == 'testnet':
    pxsol.config.current = pxsol.config.testnet

user = pxsol.wallet.Wallet(pxsol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32))))

if args.action == 'deploy':
    data = bytearray(pathlib.Path('res/hello_solana_program.so').read_bytes())
    pubkey = user.program_deploy(data)
    print('Program ID:', pubkey)

if args.action == 'call':
    tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
    tx.message.account_keys.append(user.pubkey)
    tx.message.account_keys.append(pxsol.core.PubKey.base58_decode(args.addr))
    tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash()['blockhash'])
    tx.message.instructions.append(pxsol.core.Instruction(1, [], bytearray()))
    tx.signatures.append(user.prikey.sign(tx.message.serialize()))
    hash = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {
        'encoding': 'base64'
    })
    pxsol.rpc.wait(hash)
    r = pxsol.rpc.get_transaction(hash)
    for e in r['meta']['logMessages']:
        print(e)

if args.action == 'update':
    data = bytearray(pathlib.Path('res/hello_update_program.so').read_bytes())
    pubkey = pxsol.core.PubKey.base58_decode(args.addr)
    user.program_update(data, pubkey)
    print('Program ID:', pubkey)

# PoW
to find the right value, miners must have large times of hash caculate, algorithms make sure that no one can cheat on this, so running hash is is the proof of work

basiclly the algorithm is find the `x` that makes the below expression happen
```
SHA256(SHA256(version + prev_hash + merkle_root + ntime + nbits + x )) < TARGET
```

# PoS
Proof of Stake PoS is a consensus algorithm, unlike PoW it dose not use hash functions to caculate proof, instead the `cryptocurrency` is used to select which node can validate blocks.

Pors:
- resource less no need more GPUs and ASICS than PoW
- effective, transactions are faster compared to PoW based system.

different consensus algorithms/protocols:
- Honeybadger
- Ouroboros 
- Tezos
- Casper
- Tendermint


## implement of PoS
most implements of PoS is chain-based PoS and BFT-based(Byzantine Fault Tolerant) PoS.

Tendermint is BFT-based, Casper the Friendly Ghost is chain-based, and Casper the Friendly Finality Gadget is a hybrid of the two.

Tendermint [spec](https://github.com/tendermint/tendermint/tree/master/docs/spec)

details https://blog.cosmos.network/consensus-compare-casper-vs-tendermint-6df154ad56ae
 

# loom 

Dapp is an App base on BlockChain

Loom is a framework help dev use Solidity(so it is base on Ehtereum) develop apps. and it is base on PlasmaChain(DPoS), a side chain of Ehtereum

---
title:  "The simplest crowdsale contract"
description: "Creating smart contracts for crowdsale is easier than you think"
modified: 2018-02-03T12:39:00-03:00
tags:
  - solidity
  - blockchain
  - ethereum
  - ICO  
---

If we start to speak about 2017, I’ll say “That year was about cryptocurrency. Even my mom knows about Bitcoin”. Also that year stand in the people’s memory like age of ICO.

## A bit of theory

What is `ICO`? It’s `Initial Coin Offering`. Simple explanation is about making new cryptocurrency on the base of Ethereum blockchain. I won’t tell you details about working process of that blockchain, because we are here because of code.
What is smart contract? That is a piece of code uploaded to the blockchain and working there. For writing them is used 
`Solidity` language. In the example below you can watch the simplest smart contract.

```javascript
pragma solidity ^0.4.18;

contract HelloWorld {
    
    function getData() public constant returns (string) {
        return "Hello, world!";
    }    
}
```

`Contract` keyword has the same meaning like `class` word in every OOP language. So, there is a class with one method returning ‘Hello, world!’. `constant` signature means that we read data from blockchain and not changing its state. If change state of the variables we spend `gas` for it. `gas` is special resource metrics used for measuring your impact on Ethereum
(because when you change the variable, it’ll change on every Ethereum’s node). You pay for gas in ether.
If you want to make ICO, you need two contracts (to tell the truth the real ICO contains a huge amount of them, but technically you need only two)

## Token

In a few words, `token` is crypto coin which working on the base of Ethereum blockchain. In other two words you make your own cryptocurrency.
Token contract should implement <a href="https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20-token-standard.md">ERC20</a>  standard. Without this implementation wallets would’t recognize your token.
But you should be happy, there are a few of tools that can help you with its implementation. First one is <a href="https://github.com/OpenZeppelin/zeppelin-solidity">zeppelin-solidity</a>, it’s the open source framework which contains great recipes and templates for writing your own code. You can install it with NPM package-manager. 
The second one is flexible deploy tool called <a href="https://github.com/trufflesuite/truffle">truffle</a>.
So, the simplest token can be created with the simplest code. 

```javascript
pragma solidity ^0.4.17;

import "zeppelin-solidity/contracts/token/MintableToken.sol";

contract TheSimplestToken is MintableToken {
    string public constant name = " TheSimplestToken ";
    string public constant symbol = "TST";
    uint32 public constant decimals = 18;
}
```

This is `mintable` token, it means that you can mint new tokens without any problems.

## Crowdsale

`Crowdsale` contract is needed for the token sale. That contract takes ether and give tokens. 

```javascript
contract TheSimplestCrowdsale {
    address owner;
    TheSimplestToken  public token = new TheSimplestToken();
    uint start = 1516713344;
    uint period = 20;

    function TheSimplestCrowdsale() {
        owner = msg.sender;
    }

    function() external payable {
        require(now > start && now < start + period*24*60*60);
        owner.transfer(msg.value);
        token.mint(msg.sender, msg.value);
    }
}
```

Those few lines describe one of the easiest crowdsale contract ever. When people send you money, `fallback` function (name for the function without name and with payable modificator) will raise and send them tokens.

## Conclusion

Now you are ready for the your first ICO. I strongly recommend you to use truffle for deploying contracts. The tool can be installed by NPM and can make your deploying life much better.

That’s all, thank you for you attention!

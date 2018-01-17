---
title:  "The simplest ethereum smart contract"
description: "Creating smart contracts is easier than you think"
modified: 2018-01-17T12:20:00-03:00
tags:
  - solidity
  - blockchain
  - ethereum
---
Hi everyone! Today I want to speak about writign the simplest smart contract for ethereum blockchain.

Currently I'm working as a developer at the <a href="http://bonumchain.com/">Bonum</a> company.
The most interesting thing I did there was writing a bunch of code for the ICO process. If you don't believe me,
you can check <a href="https://github.com/Bonumchain/ico">some code</a>. I'm not a liar :)

So, idea of this article is about writing the simplest possible smart contract.

## A bit of theory

I won't talk too much about theory, you only need to know, that `Ethereum` is a global distributed virtual machine and you can run some code on it.

## A bit of code
So, why don't we write a simple `Hello World` program?

```solidity
pragma solidity ^0.4.19;
 
contract HelloWorld {
    
    function sayHello() public view returns (string) {
        return "Hello, world!";
    }
    
}
```

We've done. That's all. `contract` is some kind of classes for `Ethereum` (It's not the absolute truth, but for the first step that explanation is ok).

## A bit of code #2
For the second example we'll create a contract with changing it's state.

```solidity
pragma solidity ^0.4.19;

contract Speaker {    
    string phrase;

    function sayPhrase() public view returns (string) {
        return phrase;
    }
    
    function setName(string newPhrase) public {
        phrase = newPhrase;
    }
}
```
Here is it. In that contract we set `phrase` and can ask the contract to say it.
If we make phrase `public`, we will be able to read it's state without `getter`.
But we still need the `setter`, because of `Ethereum` realisation's features.

## Conclusion

That's all. I'll be happy, If this article helps you
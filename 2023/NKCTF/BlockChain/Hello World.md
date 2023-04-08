HelloWorld

学习智能合约第三步 自己写一个Hello World！！！

合约:
```solidity
contract HelloWorld {
    string greeting;
    constructor(string memory _greeting) public {
        greeting = _greeting;
}
    function greet() public view returns (string memory) {
        return greeting;
}
function setGreeting(string memory _greeting) public {
        greeting = _greeting;
}
function isSolved() public view returns (bool) {
        string memory expected = "Hello,NKCTF2023";
        return keccak256(abi.encodePacked(expected)) == keccak256(abi.encodePacked(greeting));
    }
}
```
NKCasino

学习智能合约最后一步 搞钱！！！

```Solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.7;

contract NKCasino{
    mapping (address=>uint) public balances;
    mapping (address=>bool) public isWin;

    constructor() payable {    }

    function playGuessGame(uint _guessNum,address _player) external payable {
        uint256 size;
        assembly {  size := extcodesize(_player) }
        require(size == 0, "Only EOA can play this game.");
        require(msg.value == 0.1 ether,"The game only need 0.1 eth");

        uint random = uint(keccak256(abi.encodePacked(block.difficulty, block.timestamp, msg.sender))) % 2;
        if (random == _guessNum) {
            balances[_player] += 0.2 ether;
            isWin[_player] = true;
        }else if (!isWin[_player]) {
            uint temp = balances[_player];
            balances[_player] = 0;
            address(this).call{value: temp}("");
        }
    }

    function gotPrize(address _player) public {
        require(isWin[_player], "You got the prize or not play or lose the game.");
        _player.call{value: balances[_player]}("");
        isWin[_player] = false;
    }

    function isSolved() public view returns(bool) {
        return address(this).balance == 0 ether;
    }

    receive() external payable {    }

}
```
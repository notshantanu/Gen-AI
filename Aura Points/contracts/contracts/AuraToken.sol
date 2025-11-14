// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title AuraToken
 * @dev ERC-20 token for the Aura Points platform
 * Admin can mint/burn tokens for MVP
 */
contract AuraToken is ERC20, Ownable {
    constructor(address initialOwner) ERC20("Aura Token", "AURA") Ownable(initialOwner) {
        // Initial supply: 1,000,000 AURA tokens
        _mint(initialOwner, 1_000_000 * 10**decimals());
    }

    /**
     * @dev Mint new tokens (admin only)
     * @param to Address to mint tokens to
     * @param amount Amount of tokens to mint
     */
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    /**
     * @dev Burn tokens (admin only)
     * @param from Address to burn tokens from
     * @param amount Amount of tokens to burn
     */
    function burn(address from, uint256 amount) public onlyOwner {
        _burn(from, amount);
    }
}


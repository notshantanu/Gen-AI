// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title AuraMarket
 * @dev Market contract for buying/selling aura shares
 * Uses internal mapping for share balances
 * Simple deterministic pricing formula
 */
contract AuraMarket is Ownable {
    IERC20 public auraToken;
    
    // Mapping: personalityId => user => shares
    mapping(uint256 => mapping(address => uint256)) public shares;
    
    // Mapping: personalityId => total shares
    mapping(uint256 => uint256) public totalShares;
    
    // Mapping: personalityId => current score (stored as uint256, scaled by 1e8)
    mapping(uint256 => uint256) public currentScores;
    
    // Base values for pricing
    uint256 public constant BASE_SCORE = 100 * 1e8; // 100.0 scaled by 1e8
    uint256 public constant BASE_PRICE = 1 * 1e18; // 1.0 AURA token per share
    uint256 public constant SCORE_MULTIPLIER = 5 * 1e7; // 0.5 scaled by 1e8
    
    event Trade(
        address indexed user,
        uint256 indexed personalityId,
        bool isBuy,
        uint256 shares,
        uint256 pricePerShare,
        uint256 totalCost,
        uint256 timestamp
    );
    
    event ScoreUpdated(uint256 indexed personalityId, uint256 newScore, uint256 timestamp);
    
    constructor(address _auraToken, address initialOwner) Ownable(initialOwner) {
        auraToken = IERC20(_auraToken);
    }
    
    /**
     * @dev Calculate price per share based on current score
     * Formula: price = base_price * (1 + score_multiplier * (current_score / base_score - 1))
     */
    function calculatePrice(uint256 personalityId) public view returns (uint256) {
        uint256 score = currentScores[personalityId];
        if (score == 0) {
            score = BASE_SCORE; // Default to base score
        }
        
        // price = BASE_PRICE * (1 + SCORE_MULTIPLIER * (score / BASE_SCORE - 1))
        // All calculations done with 1e18 precision
        uint256 scoreRatio = (score * 1e18) / BASE_SCORE;
        uint256 multiplier = (SCORE_MULTIPLIER * (scoreRatio - 1e18)) / 1e8;
        uint256 price = BASE_PRICE + (BASE_PRICE * multiplier) / 1e18;
        
        // Minimum price floor: 0.01 AURA
        uint256 minPrice = 1e16; // 0.01 * 1e18
        return price < minPrice ? minPrice : price;
    }
    
    /**
     * @dev Buy shares for a personality
     * @param personalityId ID of the personality
     * @param sharesAmount Amount of shares to buy
     */
    function buyShares(uint256 personalityId, uint256 sharesAmount) external {
        require(sharesAmount > 0, "Shares amount must be greater than 0");
        
        uint256 pricePerShare = calculatePrice(personalityId);
        uint256 totalCost = (pricePerShare * sharesAmount) / 1e18;
        
        require(
            auraToken.transferFrom(msg.sender, address(this), totalCost),
            "Token transfer failed"
        );
        
        shares[personalityId][msg.sender] += sharesAmount;
        totalShares[personalityId] += sharesAmount;
        
        emit Trade(
            msg.sender,
            personalityId,
            true,
            sharesAmount,
            pricePerShare,
            totalCost,
            block.timestamp
        );
    }
    
    /**
     * @dev Sell shares for a personality
     * @param personalityId ID of the personality
     * @param sharesAmount Amount of shares to sell
     */
    function sellShares(uint256 personalityId, uint256 sharesAmount) external {
        require(sharesAmount > 0, "Shares amount must be greater than 0");
        require(
            shares[personalityId][msg.sender] >= sharesAmount,
            "Insufficient shares"
        );
        
        uint256 pricePerShare = calculatePrice(personalityId);
        uint256 totalCost = (pricePerShare * sharesAmount) / 1e18;
        
        shares[personalityId][msg.sender] -= sharesAmount;
        totalShares[personalityId] -= sharesAmount;
        
        require(
            auraToken.transfer(msg.sender, totalCost),
            "Token transfer failed"
        );
        
        emit Trade(
            msg.sender,
            personalityId,
            false,
            sharesAmount,
            pricePerShare,
            totalCost,
            block.timestamp
        );
    }
    
    /**
     * @dev Update aura score for a personality (admin only)
     * @param personalityId ID of the personality
     * @param newScore New score (scaled by 1e8, e.g., 100.5 = 10050000000)
     */
    function updateScore(uint256 personalityId, uint256 newScore) external onlyOwner {
        require(newScore > 0, "Score must be greater than 0");
        currentScores[personalityId] = newScore;
        emit ScoreUpdated(personalityId, newScore, block.timestamp);
    }
    
    /**
     * @dev Get user's share balance for a personality
     */
    function getShares(uint256 personalityId, address user) external view returns (uint256) {
        return shares[personalityId][user];
    }
}


// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title ParlayContract
 * @dev Contract for managing multi-leg parlays
 * Resolution triggered by off-chain oracle/admin
 */
contract ParlayContract is Ownable {
    IERC20 public auraToken;
    
    struct ParlayLeg {
        uint256 personalityId;
        bool direction; // true = up, false = down
        uint256 threshold; // Score threshold (scaled by 1e8)
    }
    
    struct Parlay {
        uint256 id;
        address user;
        string name;
        ParlayLeg[] legs;
        uint256 stake;
        uint256 potentialPayout;
        uint256 status; // 0 = pending, 1 = active, 2 = won, 3 = lost, 4 = cancelled
        uint256 createdAt;
        uint256 resolvedAt;
    }
    
    mapping(uint256 => Parlay) public parlays;
    mapping(uint256 => mapping(uint256 => bool)) public legResults; // parlayId => legIndex => result
    uint256 public nextParlayId;
    
    event ParlayCreated(
        uint256 indexed parlayId,
        address indexed user,
        string name,
        uint256 stake,
        uint256 potentialPayout,
        uint256 timestamp
    );
    
    event ParlayResolved(
        uint256 indexed parlayId,
        uint256 status,
        uint256 timestamp
    );
    
    constructor(address _auraToken, address initialOwner) Ownable(initialOwner) {
        auraToken = IERC20(_auraToken);
        nextParlayId = 1;
    }
    
    /**
     * @dev Create a new parlay
     * @param name Name of the parlay
     * @param personalityIds Array of personality IDs
     * @param directions Array of directions (true = up, false = down)
     * @param thresholds Array of score thresholds
     * @param stake Amount of AURA tokens to stake
     */
    function createParlay(
        string memory name,
        uint256[] memory personalityIds,
        bool[] memory directions,
        uint256[] memory thresholds,
        uint256 stake
    ) external returns (uint256) {
        require(personalityIds.length >= 2, "Parlay must have at least 2 legs");
        require(
            personalityIds.length == directions.length &&
            personalityIds.length == thresholds.length,
            "Arrays length mismatch"
        );
        require(stake > 0, "Stake must be greater than 0");
        
        require(
            auraToken.transferFrom(msg.sender, address(this), stake),
            "Token transfer failed"
        );
        
        uint256 parlayId = nextParlayId++;
        Parlay storage parlay = parlays[parlayId];
        parlay.id = parlayId;
        parlay.user = msg.sender;
        parlay.name = name;
        parlay.stake = stake;
        parlay.potentialPayout = calculatePayout(stake, personalityIds.length);
        parlay.status = 1; // active
        parlay.createdAt = block.timestamp;
        
        for (uint256 i = 0; i < personalityIds.length; i++) {
            parlay.legs.push(ParlayLeg({
                personalityId: personalityIds[i],
                direction: directions[i],
                threshold: thresholds[i]
            }));
        }
        
        emit ParlayCreated(
            parlayId,
            msg.sender,
            name,
            stake,
            parlay.potentialPayout,
            block.timestamp
        );
        
        return parlayId;
    }
    
    /**
     * @dev Calculate potential payout based on stake and number of legs
     * Formula: payout = stake * (2 ^ numLegs)
     */
    function calculatePayout(uint256 stake, uint256 numLegs) public pure returns (uint256) {
        uint256 multiplier = 2 ** numLegs;
        return stake * multiplier;
    }
    
    /**
     * @dev Resolve a parlay (admin only)
     * @param parlayId ID of the parlay to resolve
     * @param results Array of results for each leg (true = won, false = lost)
     */
    function resolveParlay(uint256 parlayId, bool[] memory results) external onlyOwner {
        Parlay storage parlay = parlays[parlayId];
        require(parlay.status == 1, "Parlay not active");
        require(results.length == parlay.legs.length, "Results length mismatch");
        
        // Store leg results
        for (uint256 i = 0; i < results.length; i++) {
            legResults[parlayId][i] = results[i];
        }
        
        // Check if all legs won
        bool allWon = true;
        for (uint256 i = 0; i < results.length; i++) {
            if (!results[i]) {
                allWon = false;
                break;
            }
        }
        
        if (allWon) {
            parlay.status = 2; // won
            require(
                auraToken.transfer(parlay.user, parlay.potentialPayout),
                "Payout transfer failed"
            );
        } else {
            parlay.status = 3; // lost
            // Stake is already locked in contract
        }
        
        parlay.resolvedAt = block.timestamp;
        
        emit ParlayResolved(parlayId, parlay.status, block.timestamp);
    }
    
    /**
     * @dev Cancel a parlay (admin only, for edge cases)
     */
    function cancelParlay(uint256 parlayId) external onlyOwner {
        Parlay storage parlay = parlays[parlayId];
        require(parlay.status == 1, "Parlay not active");
        
        parlay.status = 4; // cancelled
        parlay.resolvedAt = block.timestamp;
        
        // Refund stake
        require(
            auraToken.transfer(parlay.user, parlay.stake),
            "Refund transfer failed"
        );
        
        emit ParlayResolved(parlayId, parlay.status, block.timestamp);
    }
    
    /**
     * @dev Get parlay details
     */
    function getParlay(uint256 parlayId) external view returns (
        uint256 id,
        address user,
        string memory name,
        uint256 stake,
        uint256 potentialPayout,
        uint256 status,
        uint256 createdAt,
        uint256 resolvedAt
    ) {
        Parlay storage parlay = parlays[parlayId];
        return (
            parlay.id,
            parlay.user,
            parlay.name,
            parlay.stake,
            parlay.potentialPayout,
            parlay.status,
            parlay.createdAt,
            parlay.resolvedAt
        );
    }
    
    /**
     * @dev Get number of legs in a parlay
     */
    function getParlayLegsCount(uint256 parlayId) external view returns (uint256) {
        return parlays[parlayId].legs.length;
    }
}


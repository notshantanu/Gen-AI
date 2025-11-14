const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AuraMarket", function () {
  let auraToken;
  let auraMarket;
  let owner;
  let addr1;
  let addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    
    const AuraToken = await ethers.getContractFactory("AuraToken");
    auraToken = await AuraToken.deploy(owner.address);
    await auraToken.waitForDeployment();
    
    const AuraMarket = await ethers.getContractFactory("AuraMarket");
    auraMarket = await AuraMarket.deploy(await auraToken.getAddress(), owner.address);
    await auraMarket.waitForDeployment();
    
    // Give addr1 some tokens
    await auraToken.mint(addr1.address, ethers.parseEther("1000"));
    await auraToken.connect(addr1).approve(await auraMarket.getAddress(), ethers.parseEther("1000"));
  });

  describe("Price Calculation", function () {
    it("Should calculate base price correctly", async function () {
      const personalityId = 1;
      const price = await auraMarket.calculatePrice(personalityId);
      // Base price should be around 1 AURA (1e18)
      expect(price).to.be.closeTo(ethers.parseEther("1"), ethers.parseEther("0.1"));
    });

    it("Should update price when score changes", async function () {
      const personalityId = 1;
      const newScore = 150 * 1e8; // 150.0 scaled
      await auraMarket.updateScore(personalityId, newScore);
      const price = await auraMarket.calculatePrice(personalityId);
      // Price should be higher than base
      expect(price).to.be.gt(ethers.parseEther("1"));
    });
  });

  describe("Trading", function () {
    it("Should allow buying shares", async function () {
      const personalityId = 1;
      const sharesAmount = ethers.parseEther("10");
      
      await expect(
        auraMarket.connect(addr1).buyShares(personalityId, sharesAmount)
      ).to.emit(auraMarket, "Trade");
      
      const shares = await auraMarket.getShares(personalityId, addr1.address);
      expect(shares).to.equal(sharesAmount);
    });

    it("Should allow selling shares", async function () {
      const personalityId = 1;
      const sharesAmount = ethers.parseEther("10");
      
      // Buy first
      await auraMarket.connect(addr1).buyShares(personalityId, sharesAmount);
      
      // Approve for selling (needed for transferFrom in sell)
      await auraToken.connect(addr1).approve(await auraMarket.getAddress(), ethers.MaxUint256);
      
      // Sell
      await expect(
        auraMarket.connect(addr1).sellShares(personalityId, sharesAmount)
      ).to.emit(auraMarket, "Trade");
      
      const shares = await auraMarket.getShares(personalityId, addr1.address);
      expect(shares).to.equal(0);
    });

    it("Should not allow selling more shares than owned", async function () {
      const personalityId = 1;
      const sharesAmount = ethers.parseEther("10");
      
      await expect(
        auraMarket.connect(addr1).sellShares(personalityId, sharesAmount)
      ).to.be.revertedWith("Insufficient shares");
    });
  });
});


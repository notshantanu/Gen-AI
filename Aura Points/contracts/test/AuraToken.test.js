const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AuraToken", function () {
  let auraToken;
  let owner;
  let addr1;
  let addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    
    const AuraToken = await ethers.getContractFactory("AuraToken");
    auraToken = await AuraToken.deploy(owner.address);
    await auraToken.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await auraToken.owner()).to.equal(owner.address);
    });

    it("Should mint initial supply to owner", async function () {
      const ownerBalance = await auraToken.balanceOf(owner.address);
      expect(ownerBalance).to.equal(ethers.parseEther("1000000"));
    });
  });

  describe("Minting", function () {
    it("Should allow owner to mint tokens", async function () {
      await auraToken.mint(addr1.address, ethers.parseEther("100"));
      const balance = await auraToken.balanceOf(addr1.address);
      expect(balance).to.equal(ethers.parseEther("100"));
    });

    it("Should not allow non-owner to mint", async function () {
      await expect(
        auraToken.connect(addr1).mint(addr2.address, ethers.parseEther("100"))
      ).to.be.revertedWithCustomError(auraToken, "OwnableUnauthorizedAccount");
    });
  });

  describe("Burning", function () {
    it("Should allow owner to burn tokens", async function () {
      await auraToken.burn(owner.address, ethers.parseEther("100"));
      const balance = await auraToken.balanceOf(owner.address);
      expect(balance).to.equal(ethers.parseEther("999900"));
    });
  });
});


const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString());

  // Deploy AuraToken
  const AuraToken = await hre.ethers.getContractFactory("AuraToken");
  const auraToken = await AuraToken.deploy(deployer.address);
  await auraToken.waitForDeployment();
  const auraTokenAddress = await auraToken.getAddress();
  console.log("AuraToken deployed to:", auraTokenAddress);

  // Deploy AuraMarket
  const AuraMarket = await hre.ethers.getContractFactory("AuraMarket");
  const auraMarket = await AuraMarket.deploy(auraTokenAddress, deployer.address);
  await auraMarket.waitForDeployment();
  const auraMarketAddress = await auraMarket.getAddress();
  console.log("AuraMarket deployed to:", auraMarketAddress);

  // Deploy ParlayContract
  const ParlayContract = await hre.ethers.getContractFactory("ParlayContract");
  const parlayContract = await ParlayContract.deploy(auraTokenAddress, deployer.address);
  await parlayContract.waitForDeployment();
  const parlayContractAddress = await parlayContract.getAddress();
  console.log("ParlayContract deployed to:", parlayContractAddress);

  console.log("\n=== Deployment Summary ===");
  console.log("AuraToken:", auraTokenAddress);
  console.log("AuraMarket:", auraMarketAddress);
  console.log("ParlayContract:", parlayContractAddress);
  
  // Save addresses to a file for easy reference
  const fs = require("fs");
  const addresses = {
    AuraToken: auraTokenAddress,
    AuraMarket: auraMarketAddress,
    ParlayContract: parlayContractAddress,
    network: hre.network.name,
    deployer: deployer.address
  };
  
  fs.writeFileSync(
    "./deployment-addresses.json",
    JSON.stringify(addresses, null, 2)
  );
  console.log("\nAddresses saved to deployment-addresses.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });


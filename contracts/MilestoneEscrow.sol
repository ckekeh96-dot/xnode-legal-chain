// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice DEMO ONLY. Not audited. Do not fund or deploy for real assets.
/// @dev Client deposits native currency. Client may release to provider.
/// After expiry client may refund. Disputes are not arbitrated by this contract.
contract MilestoneEscrow {
    address payable public immutable client;
    address payable public immutable provider;
    uint64 public immutable deadline;
    bool public settled;
    bool private locked;
    event Deposited(address indexed client, uint256 amount);
    event Released(address indexed provider, uint256 amount);
    event Refunded(address indexed client, uint256 amount);
    modifier nonReentrant() { require(!locked, "Reentrant"); locked = true; _; locked = false; }
    constructor(address payable _client, address payable _provider, uint64 _deadline) {
        require(_client != address(0) && _provider != address(0), "Zero address");
        require(_client != _provider, "Same party");
        require(_deadline > block.timestamp, "Past deadline");
        client = _client; provider = _provider; deadline = _deadline;
    }
    receive() external payable {
        require(msg.sender == client, "Client only");
        require(!settled && block.timestamp < deadline, "Closed");
        require(msg.value > 0, "Zero deposit");
        emit Deposited(msg.sender, msg.value);
    }
    function release() external nonReentrant {
        require(msg.sender == client, "Client only");
        require(!settled, "Settled");
        uint256 amount = address(this).balance;
        require(amount > 0, "No funds");
        settled = true;
        (bool ok,) = provider.call{value: amount}("");
        require(ok, "Transfer failed");
        emit Released(provider, amount);
    }
    function refund() external nonReentrant {
        require(msg.sender == client, "Client only");
        require(block.timestamp >= deadline, "Too early");
        require(!settled, "Settled");
        uint256 amount = address(this).balance;
        require(amount > 0, "No funds");
        settled = true;
        (bool ok,) = client.call{value: amount}("");
        require(ok, "Transfer failed");
        emit Refunded(client, amount);
    }
}

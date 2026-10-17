// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Demonstration registry of document hashes, not legal enforceability.
contract AgreementRegistry {
    struct Agreement { address owner; bytes32 documentHash; uint64 createdAt; bool revoked; }
    mapping(bytes32 => Agreement) public agreements;
    event Registered(bytes32 indexed agreementId, address indexed owner, bytes32 documentHash);
    event Revoked(bytes32 indexed agreementId);
    function register(bytes32 agreementId, bytes32 documentHash) external {
        require(agreementId != bytes32(0) && documentHash != bytes32(0), "Empty identifier");
        require(agreements[agreementId].owner == address(0), "Already registered");
        agreements[agreementId] = Agreement(msg.sender, documentHash, uint64(block.timestamp), false);
        emit Registered(agreementId, msg.sender, documentHash);
    }
    function revoke(bytes32 agreementId) external {
        Agreement storage a = agreements[agreementId];
        require(a.owner == msg.sender, "Not agreement owner");
        require(!a.revoked, "Already revoked");
        a.revoked = true;
        emit Revoked(agreementId);
    }
    function verify(bytes32 agreementId, bytes32 documentHash) external view returns (bool) {
        Agreement storage a = agreements[agreementId];
        return a.owner != address(0) && !a.revoked && a.documentHash == documentHash;
    }
}

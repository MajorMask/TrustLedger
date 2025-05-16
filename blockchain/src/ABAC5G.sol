// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/**
 * @title ABAC5G
 * @dev Attribute-Based Access Control model for 5G blockchain applications.
 */
contract ABAC5G {
    struct Attributes {
        string region;
        string deviceType;
    }

    mapping(address => Attributes) public attributes;
    address public admin;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }

    function setAttributes(address _account, string memory _region, string memory _deviceType) external onlyAdmin {
        attributes[_account] = Attributes(_region, _deviceType);
    }

    function accessByRegion(string memory region) external view returns (string memory) {
        require(
            keccak256(bytes(attributes[msg.sender].region)) == keccak256(bytes(region)),
            "Region mismatch"
        );
        return "Region-based access granted.";
    }
}

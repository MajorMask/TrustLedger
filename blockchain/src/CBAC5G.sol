// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/**
 * @title CBAC5G
 * @dev Capability-Based Access Control model for 5G blockchain applications.
 */
contract CBAC5G {
    struct Capability {
        string resource;
        string action;
        bool granted;
    }

    mapping(address => mapping(string => Capability)) public capabilities;
    address public admin;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }

    function grantCapability(address _account, string memory _resource, string memory _action) external onlyAdmin {
        capabilities[_account][_resource] = Capability(_resource, _action, true);
    }

    function revokeCapability(address _account, string memory _resource) external onlyAdmin {
        capabilities[_account][_resource].granted = false;
    }

    function hasCapability(address _account, string memory _resource, string memory _action) public view returns (bool) {
        Capability memory cap = capabilities[_account][_resource];
        return (cap.granted && keccak256(bytes(cap.action)) == keccak256(bytes(_action)));
    }

    function accessResource(string memory _resource, string memory _action) external view returns (string memory) {
        require(hasCapability(msg.sender, _resource, _action), "Access denied");
        return "Capability-based access granted.";
    }
}


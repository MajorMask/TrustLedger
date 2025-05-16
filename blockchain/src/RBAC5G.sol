// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/**
 * @title RBAC5G
   * @dev Role-Based Access Control model for 5G blockchain applications.
   */
contract RBAC5G {
    enum Role { None, Admin, User, Device }

    mapping(address => Role) public roles;
    address public owner;

    constructor() {
        owner = msg.sender;
        roles[owner] = Role.Admin;
    }

    modifier onlyAdmin() {
        require(roles[msg.sender] == Role.Admin, "Only Admin allowed");
        _;
    }

    modifier onlyRole(Role _role) {
        require(roles[msg.sender] == _role, "Unauthorized role");
        _;
    }

    function assignRole(address _account, Role _role) external onlyAdmin {
        roles[_account] = _role;
    }

    function revokeRole(address _account) external onlyAdmin {
        roles[_account] = Role.None;
    }

    function accessUserResource() external onlyRole(Role.User) view returns (string memory) {
        return "Access granted to user resource.";
    }

    function accessAdminResource() external onlyAdmin view returns (string memory) {
        return "Admin-only access.";
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import {RBAC5G} from "../src/RBAC5G.sol";
import {ABAC5G} from "../src/ABAC5G.sol";
import {CBAC5G} from "../src/CBAC5G.sol";

contract AccessControl5GTest is Test {
    RBAC5G rbac;
    ABAC5G abac;
    CBAC5G cbac;

    address admin = address(1);
    address user = address(2);
    address device = address(3);

    function setUp() public {
        vm.startPrank(admin);
        rbac = new RBAC5G();
        abac = new ABAC5G();
        cbac = new CBAC5G();
        vm.stopPrank();
    }

    function testRBACUserAccess() public {
        vm.startPrank(admin);
        rbac.assignRole(user, RBAC5G.Role.User);
        vm.stopPrank();

        vm.prank(user);
        string memory result = rbac.accessUserResource();
        assertEq(result, "Access granted to user resource.");
    }

    function testRBACAdminAccess() public {
        vm.prank(admin);
        string memory result = rbac.accessAdminResource();
        assertEq(result, "Admin-only access.");
    }

    function testABACRegionAccess() public {
        vm.startPrank(admin);
        abac.setAttributes(user, "RegionA", "Sensor");
        vm.stopPrank();

        vm.prank(user);
        string memory result = abac.accessByRegion("RegionA");
        assertEq(result, "Region-based access granted.");
    }

    function testCBACCapabilityAccess() public {
        vm.startPrank(admin);
        cbac.grantCapability(user, "SliceX", "read");
        vm.stopPrank();

        vm.prank(user);
        string memory result = cbac.accessResource("SliceX", "read");
        assertEq(result, "Capability-based access granted.");
    }
}

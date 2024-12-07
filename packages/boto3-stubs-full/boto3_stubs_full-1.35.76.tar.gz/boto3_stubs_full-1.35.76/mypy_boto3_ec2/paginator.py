"""
Type annotations for ec2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ec2.client import EC2Client
    from mypy_boto3_ec2.paginator import (
        DescribeAddressTransfersPaginator,
        DescribeAddressesAttributePaginator,
        DescribeAwsNetworkPerformanceMetricSubscriptionsPaginator,
        DescribeByoipCidrsPaginator,
        DescribeCapacityBlockExtensionHistoryPaginator,
        DescribeCapacityBlockExtensionOfferingsPaginator,
        DescribeCapacityBlockOfferingsPaginator,
        DescribeCapacityReservationBillingRequestsPaginator,
        DescribeCapacityReservationFleetsPaginator,
        DescribeCapacityReservationsPaginator,
        DescribeCarrierGatewaysPaginator,
        DescribeClassicLinkInstancesPaginator,
        DescribeClientVpnAuthorizationRulesPaginator,
        DescribeClientVpnConnectionsPaginator,
        DescribeClientVpnEndpointsPaginator,
        DescribeClientVpnRoutesPaginator,
        DescribeClientVpnTargetNetworksPaginator,
        DescribeCoipPoolsPaginator,
        DescribeDhcpOptionsPaginator,
        DescribeEgressOnlyInternetGatewaysPaginator,
        DescribeExportImageTasksPaginator,
        DescribeFastLaunchImagesPaginator,
        DescribeFastSnapshotRestoresPaginator,
        DescribeFleetsPaginator,
        DescribeFlowLogsPaginator,
        DescribeFpgaImagesPaginator,
        DescribeHostReservationOfferingsPaginator,
        DescribeHostReservationsPaginator,
        DescribeHostsPaginator,
        DescribeIamInstanceProfileAssociationsPaginator,
        DescribeImagesPaginator,
        DescribeImportImageTasksPaginator,
        DescribeImportSnapshotTasksPaginator,
        DescribeInstanceConnectEndpointsPaginator,
        DescribeInstanceCreditSpecificationsPaginator,
        DescribeInstanceEventWindowsPaginator,
        DescribeInstanceImageMetadataPaginator,
        DescribeInstanceStatusPaginator,
        DescribeInstanceTopologyPaginator,
        DescribeInstanceTypeOfferingsPaginator,
        DescribeInstanceTypesPaginator,
        DescribeInstancesPaginator,
        DescribeInternetGatewaysPaginator,
        DescribeIpamPoolsPaginator,
        DescribeIpamResourceDiscoveriesPaginator,
        DescribeIpamResourceDiscoveryAssociationsPaginator,
        DescribeIpamScopesPaginator,
        DescribeIpamsPaginator,
        DescribeIpv6PoolsPaginator,
        DescribeLaunchTemplateVersionsPaginator,
        DescribeLaunchTemplatesPaginator,
        DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginator,
        DescribeLocalGatewayRouteTableVpcAssociationsPaginator,
        DescribeLocalGatewayRouteTablesPaginator,
        DescribeLocalGatewayVirtualInterfaceGroupsPaginator,
        DescribeLocalGatewayVirtualInterfacesPaginator,
        DescribeLocalGatewaysPaginator,
        DescribeMacHostsPaginator,
        DescribeManagedPrefixListsPaginator,
        DescribeMovingAddressesPaginator,
        DescribeNatGatewaysPaginator,
        DescribeNetworkAclsPaginator,
        DescribeNetworkInsightsAccessScopeAnalysesPaginator,
        DescribeNetworkInsightsAccessScopesPaginator,
        DescribeNetworkInsightsAnalysesPaginator,
        DescribeNetworkInsightsPathsPaginator,
        DescribeNetworkInterfacePermissionsPaginator,
        DescribeNetworkInterfacesPaginator,
        DescribePrefixListsPaginator,
        DescribePrincipalIdFormatPaginator,
        DescribePublicIpv4PoolsPaginator,
        DescribeReplaceRootVolumeTasksPaginator,
        DescribeReservedInstancesModificationsPaginator,
        DescribeReservedInstancesOfferingsPaginator,
        DescribeRouteTablesPaginator,
        DescribeScheduledInstanceAvailabilityPaginator,
        DescribeScheduledInstancesPaginator,
        DescribeSecurityGroupRulesPaginator,
        DescribeSecurityGroupVpcAssociationsPaginator,
        DescribeSecurityGroupsPaginator,
        DescribeSnapshotTierStatusPaginator,
        DescribeSnapshotsPaginator,
        DescribeSpotFleetInstancesPaginator,
        DescribeSpotFleetRequestsPaginator,
        DescribeSpotInstanceRequestsPaginator,
        DescribeSpotPriceHistoryPaginator,
        DescribeStaleSecurityGroupsPaginator,
        DescribeStoreImageTasksPaginator,
        DescribeSubnetsPaginator,
        DescribeTagsPaginator,
        DescribeTrafficMirrorFiltersPaginator,
        DescribeTrafficMirrorSessionsPaginator,
        DescribeTrafficMirrorTargetsPaginator,
        DescribeTransitGatewayAttachmentsPaginator,
        DescribeTransitGatewayConnectPeersPaginator,
        DescribeTransitGatewayConnectsPaginator,
        DescribeTransitGatewayMulticastDomainsPaginator,
        DescribeTransitGatewayPeeringAttachmentsPaginator,
        DescribeTransitGatewayPolicyTablesPaginator,
        DescribeTransitGatewayRouteTableAnnouncementsPaginator,
        DescribeTransitGatewayRouteTablesPaginator,
        DescribeTransitGatewayVpcAttachmentsPaginator,
        DescribeTransitGatewaysPaginator,
        DescribeTrunkInterfaceAssociationsPaginator,
        DescribeVerifiedAccessEndpointsPaginator,
        DescribeVerifiedAccessGroupsPaginator,
        DescribeVerifiedAccessInstanceLoggingConfigurationsPaginator,
        DescribeVerifiedAccessInstancesPaginator,
        DescribeVerifiedAccessTrustProvidersPaginator,
        DescribeVolumeStatusPaginator,
        DescribeVolumesModificationsPaginator,
        DescribeVolumesPaginator,
        DescribeVpcClassicLinkDnsSupportPaginator,
        DescribeVpcEndpointConnectionNotificationsPaginator,
        DescribeVpcEndpointConnectionsPaginator,
        DescribeVpcEndpointServiceConfigurationsPaginator,
        DescribeVpcEndpointServicePermissionsPaginator,
        DescribeVpcEndpointServicesPaginator,
        DescribeVpcEndpointsPaginator,
        DescribeVpcPeeringConnectionsPaginator,
        DescribeVpcsPaginator,
        GetAssociatedIpv6PoolCidrsPaginator,
        GetAwsNetworkPerformanceDataPaginator,
        GetGroupsForCapacityReservationPaginator,
        GetInstanceTypesFromInstanceRequirementsPaginator,
        GetIpamAddressHistoryPaginator,
        GetIpamDiscoveredAccountsPaginator,
        GetIpamDiscoveredResourceCidrsPaginator,
        GetIpamPoolAllocationsPaginator,
        GetIpamPoolCidrsPaginator,
        GetIpamResourceCidrsPaginator,
        GetManagedPrefixListAssociationsPaginator,
        GetManagedPrefixListEntriesPaginator,
        GetNetworkInsightsAccessScopeAnalysisFindingsPaginator,
        GetSecurityGroupsForVpcPaginator,
        GetSpotPlacementScoresPaginator,
        GetTransitGatewayAttachmentPropagationsPaginator,
        GetTransitGatewayMulticastDomainAssociationsPaginator,
        GetTransitGatewayPolicyTableAssociationsPaginator,
        GetTransitGatewayPrefixListReferencesPaginator,
        GetTransitGatewayRouteTableAssociationsPaginator,
        GetTransitGatewayRouteTablePropagationsPaginator,
        GetVpnConnectionDeviceTypesPaginator,
        ListImagesInRecycleBinPaginator,
        ListSnapshotsInRecycleBinPaginator,
        SearchLocalGatewayRoutesPaginator,
        SearchTransitGatewayMulticastGroupsPaginator,
    )

    session = Session()
    client: EC2Client = session.client("ec2")

    describe_address_transfers_paginator: DescribeAddressTransfersPaginator = client.get_paginator("describe_address_transfers")
    describe_addresses_attribute_paginator: DescribeAddressesAttributePaginator = client.get_paginator("describe_addresses_attribute")
    describe_aws_network_performance_metric_subscriptions_paginator: DescribeAwsNetworkPerformanceMetricSubscriptionsPaginator = client.get_paginator("describe_aws_network_performance_metric_subscriptions")
    describe_byoip_cidrs_paginator: DescribeByoipCidrsPaginator = client.get_paginator("describe_byoip_cidrs")
    describe_capacity_block_extension_history_paginator: DescribeCapacityBlockExtensionHistoryPaginator = client.get_paginator("describe_capacity_block_extension_history")
    describe_capacity_block_extension_offerings_paginator: DescribeCapacityBlockExtensionOfferingsPaginator = client.get_paginator("describe_capacity_block_extension_offerings")
    describe_capacity_block_offerings_paginator: DescribeCapacityBlockOfferingsPaginator = client.get_paginator("describe_capacity_block_offerings")
    describe_capacity_reservation_billing_requests_paginator: DescribeCapacityReservationBillingRequestsPaginator = client.get_paginator("describe_capacity_reservation_billing_requests")
    describe_capacity_reservation_fleets_paginator: DescribeCapacityReservationFleetsPaginator = client.get_paginator("describe_capacity_reservation_fleets")
    describe_capacity_reservations_paginator: DescribeCapacityReservationsPaginator = client.get_paginator("describe_capacity_reservations")
    describe_carrier_gateways_paginator: DescribeCarrierGatewaysPaginator = client.get_paginator("describe_carrier_gateways")
    describe_classic_link_instances_paginator: DescribeClassicLinkInstancesPaginator = client.get_paginator("describe_classic_link_instances")
    describe_client_vpn_authorization_rules_paginator: DescribeClientVpnAuthorizationRulesPaginator = client.get_paginator("describe_client_vpn_authorization_rules")
    describe_client_vpn_connections_paginator: DescribeClientVpnConnectionsPaginator = client.get_paginator("describe_client_vpn_connections")
    describe_client_vpn_endpoints_paginator: DescribeClientVpnEndpointsPaginator = client.get_paginator("describe_client_vpn_endpoints")
    describe_client_vpn_routes_paginator: DescribeClientVpnRoutesPaginator = client.get_paginator("describe_client_vpn_routes")
    describe_client_vpn_target_networks_paginator: DescribeClientVpnTargetNetworksPaginator = client.get_paginator("describe_client_vpn_target_networks")
    describe_coip_pools_paginator: DescribeCoipPoolsPaginator = client.get_paginator("describe_coip_pools")
    describe_dhcp_options_paginator: DescribeDhcpOptionsPaginator = client.get_paginator("describe_dhcp_options")
    describe_egress_only_internet_gateways_paginator: DescribeEgressOnlyInternetGatewaysPaginator = client.get_paginator("describe_egress_only_internet_gateways")
    describe_export_image_tasks_paginator: DescribeExportImageTasksPaginator = client.get_paginator("describe_export_image_tasks")
    describe_fast_launch_images_paginator: DescribeFastLaunchImagesPaginator = client.get_paginator("describe_fast_launch_images")
    describe_fast_snapshot_restores_paginator: DescribeFastSnapshotRestoresPaginator = client.get_paginator("describe_fast_snapshot_restores")
    describe_fleets_paginator: DescribeFleetsPaginator = client.get_paginator("describe_fleets")
    describe_flow_logs_paginator: DescribeFlowLogsPaginator = client.get_paginator("describe_flow_logs")
    describe_fpga_images_paginator: DescribeFpgaImagesPaginator = client.get_paginator("describe_fpga_images")
    describe_host_reservation_offerings_paginator: DescribeHostReservationOfferingsPaginator = client.get_paginator("describe_host_reservation_offerings")
    describe_host_reservations_paginator: DescribeHostReservationsPaginator = client.get_paginator("describe_host_reservations")
    describe_hosts_paginator: DescribeHostsPaginator = client.get_paginator("describe_hosts")
    describe_iam_instance_profile_associations_paginator: DescribeIamInstanceProfileAssociationsPaginator = client.get_paginator("describe_iam_instance_profile_associations")
    describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
    describe_import_image_tasks_paginator: DescribeImportImageTasksPaginator = client.get_paginator("describe_import_image_tasks")
    describe_import_snapshot_tasks_paginator: DescribeImportSnapshotTasksPaginator = client.get_paginator("describe_import_snapshot_tasks")
    describe_instance_connect_endpoints_paginator: DescribeInstanceConnectEndpointsPaginator = client.get_paginator("describe_instance_connect_endpoints")
    describe_instance_credit_specifications_paginator: DescribeInstanceCreditSpecificationsPaginator = client.get_paginator("describe_instance_credit_specifications")
    describe_instance_event_windows_paginator: DescribeInstanceEventWindowsPaginator = client.get_paginator("describe_instance_event_windows")
    describe_instance_image_metadata_paginator: DescribeInstanceImageMetadataPaginator = client.get_paginator("describe_instance_image_metadata")
    describe_instance_status_paginator: DescribeInstanceStatusPaginator = client.get_paginator("describe_instance_status")
    describe_instance_topology_paginator: DescribeInstanceTopologyPaginator = client.get_paginator("describe_instance_topology")
    describe_instance_type_offerings_paginator: DescribeInstanceTypeOfferingsPaginator = client.get_paginator("describe_instance_type_offerings")
    describe_instance_types_paginator: DescribeInstanceTypesPaginator = client.get_paginator("describe_instance_types")
    describe_instances_paginator: DescribeInstancesPaginator = client.get_paginator("describe_instances")
    describe_internet_gateways_paginator: DescribeInternetGatewaysPaginator = client.get_paginator("describe_internet_gateways")
    describe_ipam_pools_paginator: DescribeIpamPoolsPaginator = client.get_paginator("describe_ipam_pools")
    describe_ipam_resource_discoveries_paginator: DescribeIpamResourceDiscoveriesPaginator = client.get_paginator("describe_ipam_resource_discoveries")
    describe_ipam_resource_discovery_associations_paginator: DescribeIpamResourceDiscoveryAssociationsPaginator = client.get_paginator("describe_ipam_resource_discovery_associations")
    describe_ipam_scopes_paginator: DescribeIpamScopesPaginator = client.get_paginator("describe_ipam_scopes")
    describe_ipams_paginator: DescribeIpamsPaginator = client.get_paginator("describe_ipams")
    describe_ipv6_pools_paginator: DescribeIpv6PoolsPaginator = client.get_paginator("describe_ipv6_pools")
    describe_launch_template_versions_paginator: DescribeLaunchTemplateVersionsPaginator = client.get_paginator("describe_launch_template_versions")
    describe_launch_templates_paginator: DescribeLaunchTemplatesPaginator = client.get_paginator("describe_launch_templates")
    describe_local_gateway_route_table_virtual_interface_group_associations_paginator: DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginator = client.get_paginator("describe_local_gateway_route_table_virtual_interface_group_associations")
    describe_local_gateway_route_table_vpc_associations_paginator: DescribeLocalGatewayRouteTableVpcAssociationsPaginator = client.get_paginator("describe_local_gateway_route_table_vpc_associations")
    describe_local_gateway_route_tables_paginator: DescribeLocalGatewayRouteTablesPaginator = client.get_paginator("describe_local_gateway_route_tables")
    describe_local_gateway_virtual_interface_groups_paginator: DescribeLocalGatewayVirtualInterfaceGroupsPaginator = client.get_paginator("describe_local_gateway_virtual_interface_groups")
    describe_local_gateway_virtual_interfaces_paginator: DescribeLocalGatewayVirtualInterfacesPaginator = client.get_paginator("describe_local_gateway_virtual_interfaces")
    describe_local_gateways_paginator: DescribeLocalGatewaysPaginator = client.get_paginator("describe_local_gateways")
    describe_mac_hosts_paginator: DescribeMacHostsPaginator = client.get_paginator("describe_mac_hosts")
    describe_managed_prefix_lists_paginator: DescribeManagedPrefixListsPaginator = client.get_paginator("describe_managed_prefix_lists")
    describe_moving_addresses_paginator: DescribeMovingAddressesPaginator = client.get_paginator("describe_moving_addresses")
    describe_nat_gateways_paginator: DescribeNatGatewaysPaginator = client.get_paginator("describe_nat_gateways")
    describe_network_acls_paginator: DescribeNetworkAclsPaginator = client.get_paginator("describe_network_acls")
    describe_network_insights_access_scope_analyses_paginator: DescribeNetworkInsightsAccessScopeAnalysesPaginator = client.get_paginator("describe_network_insights_access_scope_analyses")
    describe_network_insights_access_scopes_paginator: DescribeNetworkInsightsAccessScopesPaginator = client.get_paginator("describe_network_insights_access_scopes")
    describe_network_insights_analyses_paginator: DescribeNetworkInsightsAnalysesPaginator = client.get_paginator("describe_network_insights_analyses")
    describe_network_insights_paths_paginator: DescribeNetworkInsightsPathsPaginator = client.get_paginator("describe_network_insights_paths")
    describe_network_interface_permissions_paginator: DescribeNetworkInterfacePermissionsPaginator = client.get_paginator("describe_network_interface_permissions")
    describe_network_interfaces_paginator: DescribeNetworkInterfacesPaginator = client.get_paginator("describe_network_interfaces")
    describe_prefix_lists_paginator: DescribePrefixListsPaginator = client.get_paginator("describe_prefix_lists")
    describe_principal_id_format_paginator: DescribePrincipalIdFormatPaginator = client.get_paginator("describe_principal_id_format")
    describe_public_ipv4_pools_paginator: DescribePublicIpv4PoolsPaginator = client.get_paginator("describe_public_ipv4_pools")
    describe_replace_root_volume_tasks_paginator: DescribeReplaceRootVolumeTasksPaginator = client.get_paginator("describe_replace_root_volume_tasks")
    describe_reserved_instances_modifications_paginator: DescribeReservedInstancesModificationsPaginator = client.get_paginator("describe_reserved_instances_modifications")
    describe_reserved_instances_offerings_paginator: DescribeReservedInstancesOfferingsPaginator = client.get_paginator("describe_reserved_instances_offerings")
    describe_route_tables_paginator: DescribeRouteTablesPaginator = client.get_paginator("describe_route_tables")
    describe_scheduled_instance_availability_paginator: DescribeScheduledInstanceAvailabilityPaginator = client.get_paginator("describe_scheduled_instance_availability")
    describe_scheduled_instances_paginator: DescribeScheduledInstancesPaginator = client.get_paginator("describe_scheduled_instances")
    describe_security_group_rules_paginator: DescribeSecurityGroupRulesPaginator = client.get_paginator("describe_security_group_rules")
    describe_security_group_vpc_associations_paginator: DescribeSecurityGroupVpcAssociationsPaginator = client.get_paginator("describe_security_group_vpc_associations")
    describe_security_groups_paginator: DescribeSecurityGroupsPaginator = client.get_paginator("describe_security_groups")
    describe_snapshot_tier_status_paginator: DescribeSnapshotTierStatusPaginator = client.get_paginator("describe_snapshot_tier_status")
    describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
    describe_spot_fleet_instances_paginator: DescribeSpotFleetInstancesPaginator = client.get_paginator("describe_spot_fleet_instances")
    describe_spot_fleet_requests_paginator: DescribeSpotFleetRequestsPaginator = client.get_paginator("describe_spot_fleet_requests")
    describe_spot_instance_requests_paginator: DescribeSpotInstanceRequestsPaginator = client.get_paginator("describe_spot_instance_requests")
    describe_spot_price_history_paginator: DescribeSpotPriceHistoryPaginator = client.get_paginator("describe_spot_price_history")
    describe_stale_security_groups_paginator: DescribeStaleSecurityGroupsPaginator = client.get_paginator("describe_stale_security_groups")
    describe_store_image_tasks_paginator: DescribeStoreImageTasksPaginator = client.get_paginator("describe_store_image_tasks")
    describe_subnets_paginator: DescribeSubnetsPaginator = client.get_paginator("describe_subnets")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    describe_traffic_mirror_filters_paginator: DescribeTrafficMirrorFiltersPaginator = client.get_paginator("describe_traffic_mirror_filters")
    describe_traffic_mirror_sessions_paginator: DescribeTrafficMirrorSessionsPaginator = client.get_paginator("describe_traffic_mirror_sessions")
    describe_traffic_mirror_targets_paginator: DescribeTrafficMirrorTargetsPaginator = client.get_paginator("describe_traffic_mirror_targets")
    describe_transit_gateway_attachments_paginator: DescribeTransitGatewayAttachmentsPaginator = client.get_paginator("describe_transit_gateway_attachments")
    describe_transit_gateway_connect_peers_paginator: DescribeTransitGatewayConnectPeersPaginator = client.get_paginator("describe_transit_gateway_connect_peers")
    describe_transit_gateway_connects_paginator: DescribeTransitGatewayConnectsPaginator = client.get_paginator("describe_transit_gateway_connects")
    describe_transit_gateway_multicast_domains_paginator: DescribeTransitGatewayMulticastDomainsPaginator = client.get_paginator("describe_transit_gateway_multicast_domains")
    describe_transit_gateway_peering_attachments_paginator: DescribeTransitGatewayPeeringAttachmentsPaginator = client.get_paginator("describe_transit_gateway_peering_attachments")
    describe_transit_gateway_policy_tables_paginator: DescribeTransitGatewayPolicyTablesPaginator = client.get_paginator("describe_transit_gateway_policy_tables")
    describe_transit_gateway_route_table_announcements_paginator: DescribeTransitGatewayRouteTableAnnouncementsPaginator = client.get_paginator("describe_transit_gateway_route_table_announcements")
    describe_transit_gateway_route_tables_paginator: DescribeTransitGatewayRouteTablesPaginator = client.get_paginator("describe_transit_gateway_route_tables")
    describe_transit_gateway_vpc_attachments_paginator: DescribeTransitGatewayVpcAttachmentsPaginator = client.get_paginator("describe_transit_gateway_vpc_attachments")
    describe_transit_gateways_paginator: DescribeTransitGatewaysPaginator = client.get_paginator("describe_transit_gateways")
    describe_trunk_interface_associations_paginator: DescribeTrunkInterfaceAssociationsPaginator = client.get_paginator("describe_trunk_interface_associations")
    describe_verified_access_endpoints_paginator: DescribeVerifiedAccessEndpointsPaginator = client.get_paginator("describe_verified_access_endpoints")
    describe_verified_access_groups_paginator: DescribeVerifiedAccessGroupsPaginator = client.get_paginator("describe_verified_access_groups")
    describe_verified_access_instance_logging_configurations_paginator: DescribeVerifiedAccessInstanceLoggingConfigurationsPaginator = client.get_paginator("describe_verified_access_instance_logging_configurations")
    describe_verified_access_instances_paginator: DescribeVerifiedAccessInstancesPaginator = client.get_paginator("describe_verified_access_instances")
    describe_verified_access_trust_providers_paginator: DescribeVerifiedAccessTrustProvidersPaginator = client.get_paginator("describe_verified_access_trust_providers")
    describe_volume_status_paginator: DescribeVolumeStatusPaginator = client.get_paginator("describe_volume_status")
    describe_volumes_modifications_paginator: DescribeVolumesModificationsPaginator = client.get_paginator("describe_volumes_modifications")
    describe_volumes_paginator: DescribeVolumesPaginator = client.get_paginator("describe_volumes")
    describe_vpc_classic_link_dns_support_paginator: DescribeVpcClassicLinkDnsSupportPaginator = client.get_paginator("describe_vpc_classic_link_dns_support")
    describe_vpc_endpoint_connection_notifications_paginator: DescribeVpcEndpointConnectionNotificationsPaginator = client.get_paginator("describe_vpc_endpoint_connection_notifications")
    describe_vpc_endpoint_connections_paginator: DescribeVpcEndpointConnectionsPaginator = client.get_paginator("describe_vpc_endpoint_connections")
    describe_vpc_endpoint_service_configurations_paginator: DescribeVpcEndpointServiceConfigurationsPaginator = client.get_paginator("describe_vpc_endpoint_service_configurations")
    describe_vpc_endpoint_service_permissions_paginator: DescribeVpcEndpointServicePermissionsPaginator = client.get_paginator("describe_vpc_endpoint_service_permissions")
    describe_vpc_endpoint_services_paginator: DescribeVpcEndpointServicesPaginator = client.get_paginator("describe_vpc_endpoint_services")
    describe_vpc_endpoints_paginator: DescribeVpcEndpointsPaginator = client.get_paginator("describe_vpc_endpoints")
    describe_vpc_peering_connections_paginator: DescribeVpcPeeringConnectionsPaginator = client.get_paginator("describe_vpc_peering_connections")
    describe_vpcs_paginator: DescribeVpcsPaginator = client.get_paginator("describe_vpcs")
    get_associated_ipv6_pool_cidrs_paginator: GetAssociatedIpv6PoolCidrsPaginator = client.get_paginator("get_associated_ipv6_pool_cidrs")
    get_aws_network_performance_data_paginator: GetAwsNetworkPerformanceDataPaginator = client.get_paginator("get_aws_network_performance_data")
    get_groups_for_capacity_reservation_paginator: GetGroupsForCapacityReservationPaginator = client.get_paginator("get_groups_for_capacity_reservation")
    get_instance_types_from_instance_requirements_paginator: GetInstanceTypesFromInstanceRequirementsPaginator = client.get_paginator("get_instance_types_from_instance_requirements")
    get_ipam_address_history_paginator: GetIpamAddressHistoryPaginator = client.get_paginator("get_ipam_address_history")
    get_ipam_discovered_accounts_paginator: GetIpamDiscoveredAccountsPaginator = client.get_paginator("get_ipam_discovered_accounts")
    get_ipam_discovered_resource_cidrs_paginator: GetIpamDiscoveredResourceCidrsPaginator = client.get_paginator("get_ipam_discovered_resource_cidrs")
    get_ipam_pool_allocations_paginator: GetIpamPoolAllocationsPaginator = client.get_paginator("get_ipam_pool_allocations")
    get_ipam_pool_cidrs_paginator: GetIpamPoolCidrsPaginator = client.get_paginator("get_ipam_pool_cidrs")
    get_ipam_resource_cidrs_paginator: GetIpamResourceCidrsPaginator = client.get_paginator("get_ipam_resource_cidrs")
    get_managed_prefix_list_associations_paginator: GetManagedPrefixListAssociationsPaginator = client.get_paginator("get_managed_prefix_list_associations")
    get_managed_prefix_list_entries_paginator: GetManagedPrefixListEntriesPaginator = client.get_paginator("get_managed_prefix_list_entries")
    get_network_insights_access_scope_analysis_findings_paginator: GetNetworkInsightsAccessScopeAnalysisFindingsPaginator = client.get_paginator("get_network_insights_access_scope_analysis_findings")
    get_security_groups_for_vpc_paginator: GetSecurityGroupsForVpcPaginator = client.get_paginator("get_security_groups_for_vpc")
    get_spot_placement_scores_paginator: GetSpotPlacementScoresPaginator = client.get_paginator("get_spot_placement_scores")
    get_transit_gateway_attachment_propagations_paginator: GetTransitGatewayAttachmentPropagationsPaginator = client.get_paginator("get_transit_gateway_attachment_propagations")
    get_transit_gateway_multicast_domain_associations_paginator: GetTransitGatewayMulticastDomainAssociationsPaginator = client.get_paginator("get_transit_gateway_multicast_domain_associations")
    get_transit_gateway_policy_table_associations_paginator: GetTransitGatewayPolicyTableAssociationsPaginator = client.get_paginator("get_transit_gateway_policy_table_associations")
    get_transit_gateway_prefix_list_references_paginator: GetTransitGatewayPrefixListReferencesPaginator = client.get_paginator("get_transit_gateway_prefix_list_references")
    get_transit_gateway_route_table_associations_paginator: GetTransitGatewayRouteTableAssociationsPaginator = client.get_paginator("get_transit_gateway_route_table_associations")
    get_transit_gateway_route_table_propagations_paginator: GetTransitGatewayRouteTablePropagationsPaginator = client.get_paginator("get_transit_gateway_route_table_propagations")
    get_vpn_connection_device_types_paginator: GetVpnConnectionDeviceTypesPaginator = client.get_paginator("get_vpn_connection_device_types")
    list_images_in_recycle_bin_paginator: ListImagesInRecycleBinPaginator = client.get_paginator("list_images_in_recycle_bin")
    list_snapshots_in_recycle_bin_paginator: ListSnapshotsInRecycleBinPaginator = client.get_paginator("list_snapshots_in_recycle_bin")
    search_local_gateway_routes_paginator: SearchLocalGatewayRoutesPaginator = client.get_paginator("search_local_gateway_routes")
    search_transit_gateway_multicast_groups_paginator: SearchTransitGatewayMulticastGroupsPaginator = client.get_paginator("search_transit_gateway_multicast_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAddressesAttributeRequestDescribeAddressesAttributePaginateTypeDef,
    DescribeAddressesAttributeResultTypeDef,
    DescribeAddressTransfersRequestDescribeAddressTransfersPaginateTypeDef,
    DescribeAddressTransfersResultTypeDef,
    DescribeAwsNetworkPerformanceMetricSubscriptionsRequestDescribeAwsNetworkPerformanceMetricSubscriptionsPaginateTypeDef,
    DescribeAwsNetworkPerformanceMetricSubscriptionsResultTypeDef,
    DescribeByoipCidrsRequestDescribeByoipCidrsPaginateTypeDef,
    DescribeByoipCidrsResultTypeDef,
    DescribeCapacityBlockExtensionHistoryRequestDescribeCapacityBlockExtensionHistoryPaginateTypeDef,
    DescribeCapacityBlockExtensionHistoryResultTypeDef,
    DescribeCapacityBlockExtensionOfferingsRequestDescribeCapacityBlockExtensionOfferingsPaginateTypeDef,
    DescribeCapacityBlockExtensionOfferingsResultTypeDef,
    DescribeCapacityBlockOfferingsRequestDescribeCapacityBlockOfferingsPaginateTypeDef,
    DescribeCapacityBlockOfferingsResultTypeDef,
    DescribeCapacityReservationBillingRequestsRequestDescribeCapacityReservationBillingRequestsPaginateTypeDef,
    DescribeCapacityReservationBillingRequestsResultTypeDef,
    DescribeCapacityReservationFleetsRequestDescribeCapacityReservationFleetsPaginateTypeDef,
    DescribeCapacityReservationFleetsResultTypeDef,
    DescribeCapacityReservationsRequestDescribeCapacityReservationsPaginateTypeDef,
    DescribeCapacityReservationsResultTypeDef,
    DescribeCarrierGatewaysRequestDescribeCarrierGatewaysPaginateTypeDef,
    DescribeCarrierGatewaysResultTypeDef,
    DescribeClassicLinkInstancesRequestDescribeClassicLinkInstancesPaginateTypeDef,
    DescribeClassicLinkInstancesResultTypeDef,
    DescribeClientVpnAuthorizationRulesRequestDescribeClientVpnAuthorizationRulesPaginateTypeDef,
    DescribeClientVpnAuthorizationRulesResultTypeDef,
    DescribeClientVpnConnectionsRequestDescribeClientVpnConnectionsPaginateTypeDef,
    DescribeClientVpnConnectionsResultTypeDef,
    DescribeClientVpnEndpointsRequestDescribeClientVpnEndpointsPaginateTypeDef,
    DescribeClientVpnEndpointsResultTypeDef,
    DescribeClientVpnRoutesRequestDescribeClientVpnRoutesPaginateTypeDef,
    DescribeClientVpnRoutesResultTypeDef,
    DescribeClientVpnTargetNetworksRequestDescribeClientVpnTargetNetworksPaginateTypeDef,
    DescribeClientVpnTargetNetworksResultTypeDef,
    DescribeCoipPoolsRequestDescribeCoipPoolsPaginateTypeDef,
    DescribeCoipPoolsResultTypeDef,
    DescribeDhcpOptionsRequestDescribeDhcpOptionsPaginateTypeDef,
    DescribeDhcpOptionsResultTypeDef,
    DescribeEgressOnlyInternetGatewaysRequestDescribeEgressOnlyInternetGatewaysPaginateTypeDef,
    DescribeEgressOnlyInternetGatewaysResultTypeDef,
    DescribeExportImageTasksRequestDescribeExportImageTasksPaginateTypeDef,
    DescribeExportImageTasksResultTypeDef,
    DescribeFastLaunchImagesRequestDescribeFastLaunchImagesPaginateTypeDef,
    DescribeFastLaunchImagesResultTypeDef,
    DescribeFastSnapshotRestoresRequestDescribeFastSnapshotRestoresPaginateTypeDef,
    DescribeFastSnapshotRestoresResultTypeDef,
    DescribeFleetsRequestDescribeFleetsPaginateTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeFlowLogsRequestDescribeFlowLogsPaginateTypeDef,
    DescribeFlowLogsResultTypeDef,
    DescribeFpgaImagesRequestDescribeFpgaImagesPaginateTypeDef,
    DescribeFpgaImagesResultTypeDef,
    DescribeHostReservationOfferingsRequestDescribeHostReservationOfferingsPaginateTypeDef,
    DescribeHostReservationOfferingsResultTypeDef,
    DescribeHostReservationsRequestDescribeHostReservationsPaginateTypeDef,
    DescribeHostReservationsResultTypeDef,
    DescribeHostsRequestDescribeHostsPaginateTypeDef,
    DescribeHostsResultTypeDef,
    DescribeIamInstanceProfileAssociationsRequestDescribeIamInstanceProfileAssociationsPaginateTypeDef,
    DescribeIamInstanceProfileAssociationsResultTypeDef,
    DescribeImagesRequestDescribeImagesPaginateTypeDef,
    DescribeImagesResultTypeDef,
    DescribeImportImageTasksRequestDescribeImportImageTasksPaginateTypeDef,
    DescribeImportImageTasksResultTypeDef,
    DescribeImportSnapshotTasksRequestDescribeImportSnapshotTasksPaginateTypeDef,
    DescribeImportSnapshotTasksResultTypeDef,
    DescribeInstanceConnectEndpointsRequestDescribeInstanceConnectEndpointsPaginateTypeDef,
    DescribeInstanceConnectEndpointsResultTypeDef,
    DescribeInstanceCreditSpecificationsRequestDescribeInstanceCreditSpecificationsPaginateTypeDef,
    DescribeInstanceCreditSpecificationsResultTypeDef,
    DescribeInstanceEventWindowsRequestDescribeInstanceEventWindowsPaginateTypeDef,
    DescribeInstanceEventWindowsResultTypeDef,
    DescribeInstanceImageMetadataRequestDescribeInstanceImageMetadataPaginateTypeDef,
    DescribeInstanceImageMetadataResultTypeDef,
    DescribeInstancesRequestDescribeInstancesPaginateTypeDef,
    DescribeInstancesResultTypeDef,
    DescribeInstanceStatusRequestDescribeInstanceStatusPaginateTypeDef,
    DescribeInstanceStatusResultTypeDef,
    DescribeInstanceTopologyRequestDescribeInstanceTopologyPaginateTypeDef,
    DescribeInstanceTopologyResultTypeDef,
    DescribeInstanceTypeOfferingsRequestDescribeInstanceTypeOfferingsPaginateTypeDef,
    DescribeInstanceTypeOfferingsResultTypeDef,
    DescribeInstanceTypesRequestDescribeInstanceTypesPaginateTypeDef,
    DescribeInstanceTypesResultTypeDef,
    DescribeInternetGatewaysRequestDescribeInternetGatewaysPaginateTypeDef,
    DescribeInternetGatewaysResultTypeDef,
    DescribeIpamPoolsRequestDescribeIpamPoolsPaginateTypeDef,
    DescribeIpamPoolsResultTypeDef,
    DescribeIpamResourceDiscoveriesRequestDescribeIpamResourceDiscoveriesPaginateTypeDef,
    DescribeIpamResourceDiscoveriesResultTypeDef,
    DescribeIpamResourceDiscoveryAssociationsRequestDescribeIpamResourceDiscoveryAssociationsPaginateTypeDef,
    DescribeIpamResourceDiscoveryAssociationsResultTypeDef,
    DescribeIpamScopesRequestDescribeIpamScopesPaginateTypeDef,
    DescribeIpamScopesResultTypeDef,
    DescribeIpamsRequestDescribeIpamsPaginateTypeDef,
    DescribeIpamsResultTypeDef,
    DescribeIpv6PoolsRequestDescribeIpv6PoolsPaginateTypeDef,
    DescribeIpv6PoolsResultTypeDef,
    DescribeLaunchTemplatesRequestDescribeLaunchTemplatesPaginateTypeDef,
    DescribeLaunchTemplatesResultTypeDef,
    DescribeLaunchTemplateVersionsRequestDescribeLaunchTemplateVersionsPaginateTypeDef,
    DescribeLaunchTemplateVersionsResultTypeDef,
    DescribeLocalGatewayRouteTablesRequestDescribeLocalGatewayRouteTablesPaginateTypeDef,
    DescribeLocalGatewayRouteTablesResultTypeDef,
    DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestDescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginateTypeDef,
    DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsResultTypeDef,
    DescribeLocalGatewayRouteTableVpcAssociationsRequestDescribeLocalGatewayRouteTableVpcAssociationsPaginateTypeDef,
    DescribeLocalGatewayRouteTableVpcAssociationsResultTypeDef,
    DescribeLocalGatewaysRequestDescribeLocalGatewaysPaginateTypeDef,
    DescribeLocalGatewaysResultTypeDef,
    DescribeLocalGatewayVirtualInterfaceGroupsRequestDescribeLocalGatewayVirtualInterfaceGroupsPaginateTypeDef,
    DescribeLocalGatewayVirtualInterfaceGroupsResultTypeDef,
    DescribeLocalGatewayVirtualInterfacesRequestDescribeLocalGatewayVirtualInterfacesPaginateTypeDef,
    DescribeLocalGatewayVirtualInterfacesResultTypeDef,
    DescribeMacHostsRequestDescribeMacHostsPaginateTypeDef,
    DescribeMacHostsResultTypeDef,
    DescribeManagedPrefixListsRequestDescribeManagedPrefixListsPaginateTypeDef,
    DescribeManagedPrefixListsResultTypeDef,
    DescribeMovingAddressesRequestDescribeMovingAddressesPaginateTypeDef,
    DescribeMovingAddressesResultTypeDef,
    DescribeNatGatewaysRequestDescribeNatGatewaysPaginateTypeDef,
    DescribeNatGatewaysResultTypeDef,
    DescribeNetworkAclsRequestDescribeNetworkAclsPaginateTypeDef,
    DescribeNetworkAclsResultTypeDef,
    DescribeNetworkInsightsAccessScopeAnalysesRequestDescribeNetworkInsightsAccessScopeAnalysesPaginateTypeDef,
    DescribeNetworkInsightsAccessScopeAnalysesResultTypeDef,
    DescribeNetworkInsightsAccessScopesRequestDescribeNetworkInsightsAccessScopesPaginateTypeDef,
    DescribeNetworkInsightsAccessScopesResultTypeDef,
    DescribeNetworkInsightsAnalysesRequestDescribeNetworkInsightsAnalysesPaginateTypeDef,
    DescribeNetworkInsightsAnalysesResultTypeDef,
    DescribeNetworkInsightsPathsRequestDescribeNetworkInsightsPathsPaginateTypeDef,
    DescribeNetworkInsightsPathsResultTypeDef,
    DescribeNetworkInterfacePermissionsRequestDescribeNetworkInterfacePermissionsPaginateTypeDef,
    DescribeNetworkInterfacePermissionsResultTypeDef,
    DescribeNetworkInterfacesRequestDescribeNetworkInterfacesPaginateTypeDef,
    DescribeNetworkInterfacesResultTypeDef,
    DescribePrefixListsRequestDescribePrefixListsPaginateTypeDef,
    DescribePrefixListsResultTypeDef,
    DescribePrincipalIdFormatRequestDescribePrincipalIdFormatPaginateTypeDef,
    DescribePrincipalIdFormatResultTypeDef,
    DescribePublicIpv4PoolsRequestDescribePublicIpv4PoolsPaginateTypeDef,
    DescribePublicIpv4PoolsResultTypeDef,
    DescribeReplaceRootVolumeTasksRequestDescribeReplaceRootVolumeTasksPaginateTypeDef,
    DescribeReplaceRootVolumeTasksResultTypeDef,
    DescribeReservedInstancesModificationsRequestDescribeReservedInstancesModificationsPaginateTypeDef,
    DescribeReservedInstancesModificationsResultTypeDef,
    DescribeReservedInstancesOfferingsRequestDescribeReservedInstancesOfferingsPaginateTypeDef,
    DescribeReservedInstancesOfferingsResultTypeDef,
    DescribeRouteTablesRequestDescribeRouteTablesPaginateTypeDef,
    DescribeRouteTablesResultTypeDef,
    DescribeScheduledInstanceAvailabilityRequestDescribeScheduledInstanceAvailabilityPaginateTypeDef,
    DescribeScheduledInstanceAvailabilityResultTypeDef,
    DescribeScheduledInstancesRequestDescribeScheduledInstancesPaginateTypeDef,
    DescribeScheduledInstancesResultTypeDef,
    DescribeSecurityGroupRulesRequestDescribeSecurityGroupRulesPaginateTypeDef,
    DescribeSecurityGroupRulesResultTypeDef,
    DescribeSecurityGroupsRequestDescribeSecurityGroupsPaginateTypeDef,
    DescribeSecurityGroupsResultTypeDef,
    DescribeSecurityGroupVpcAssociationsRequestDescribeSecurityGroupVpcAssociationsPaginateTypeDef,
    DescribeSecurityGroupVpcAssociationsResultTypeDef,
    DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef,
    DescribeSnapshotsResultTypeDef,
    DescribeSnapshotTierStatusRequestDescribeSnapshotTierStatusPaginateTypeDef,
    DescribeSnapshotTierStatusResultTypeDef,
    DescribeSpotFleetInstancesRequestDescribeSpotFleetInstancesPaginateTypeDef,
    DescribeSpotFleetInstancesResponseTypeDef,
    DescribeSpotFleetRequestsRequestDescribeSpotFleetRequestsPaginateTypeDef,
    DescribeSpotFleetRequestsResponseTypeDef,
    DescribeSpotInstanceRequestsRequestDescribeSpotInstanceRequestsPaginateTypeDef,
    DescribeSpotInstanceRequestsResultTypeDef,
    DescribeSpotPriceHistoryRequestDescribeSpotPriceHistoryPaginateTypeDef,
    DescribeSpotPriceHistoryResultTypeDef,
    DescribeStaleSecurityGroupsRequestDescribeStaleSecurityGroupsPaginateTypeDef,
    DescribeStaleSecurityGroupsResultTypeDef,
    DescribeStoreImageTasksRequestDescribeStoreImageTasksPaginateTypeDef,
    DescribeStoreImageTasksResultTypeDef,
    DescribeSubnetsRequestDescribeSubnetsPaginateTypeDef,
    DescribeSubnetsResultTypeDef,
    DescribeTagsRequestDescribeTagsPaginateTypeDef,
    DescribeTagsResultTypeDef,
    DescribeTrafficMirrorFiltersRequestDescribeTrafficMirrorFiltersPaginateTypeDef,
    DescribeTrafficMirrorFiltersResultTypeDef,
    DescribeTrafficMirrorSessionsRequestDescribeTrafficMirrorSessionsPaginateTypeDef,
    DescribeTrafficMirrorSessionsResultTypeDef,
    DescribeTrafficMirrorTargetsRequestDescribeTrafficMirrorTargetsPaginateTypeDef,
    DescribeTrafficMirrorTargetsResultTypeDef,
    DescribeTransitGatewayAttachmentsRequestDescribeTransitGatewayAttachmentsPaginateTypeDef,
    DescribeTransitGatewayAttachmentsResultTypeDef,
    DescribeTransitGatewayConnectPeersRequestDescribeTransitGatewayConnectPeersPaginateTypeDef,
    DescribeTransitGatewayConnectPeersResultTypeDef,
    DescribeTransitGatewayConnectsRequestDescribeTransitGatewayConnectsPaginateTypeDef,
    DescribeTransitGatewayConnectsResultTypeDef,
    DescribeTransitGatewayMulticastDomainsRequestDescribeTransitGatewayMulticastDomainsPaginateTypeDef,
    DescribeTransitGatewayMulticastDomainsResultTypeDef,
    DescribeTransitGatewayPeeringAttachmentsRequestDescribeTransitGatewayPeeringAttachmentsPaginateTypeDef,
    DescribeTransitGatewayPeeringAttachmentsResultTypeDef,
    DescribeTransitGatewayPolicyTablesRequestDescribeTransitGatewayPolicyTablesPaginateTypeDef,
    DescribeTransitGatewayPolicyTablesResultTypeDef,
    DescribeTransitGatewayRouteTableAnnouncementsRequestDescribeTransitGatewayRouteTableAnnouncementsPaginateTypeDef,
    DescribeTransitGatewayRouteTableAnnouncementsResultTypeDef,
    DescribeTransitGatewayRouteTablesRequestDescribeTransitGatewayRouteTablesPaginateTypeDef,
    DescribeTransitGatewayRouteTablesResultTypeDef,
    DescribeTransitGatewaysRequestDescribeTransitGatewaysPaginateTypeDef,
    DescribeTransitGatewaysResultTypeDef,
    DescribeTransitGatewayVpcAttachmentsRequestDescribeTransitGatewayVpcAttachmentsPaginateTypeDef,
    DescribeTransitGatewayVpcAttachmentsResultTypeDef,
    DescribeTrunkInterfaceAssociationsRequestDescribeTrunkInterfaceAssociationsPaginateTypeDef,
    DescribeTrunkInterfaceAssociationsResultTypeDef,
    DescribeVerifiedAccessEndpointsRequestDescribeVerifiedAccessEndpointsPaginateTypeDef,
    DescribeVerifiedAccessEndpointsResultTypeDef,
    DescribeVerifiedAccessGroupsRequestDescribeVerifiedAccessGroupsPaginateTypeDef,
    DescribeVerifiedAccessGroupsResultTypeDef,
    DescribeVerifiedAccessInstanceLoggingConfigurationsRequestDescribeVerifiedAccessInstanceLoggingConfigurationsPaginateTypeDef,
    DescribeVerifiedAccessInstanceLoggingConfigurationsResultTypeDef,
    DescribeVerifiedAccessInstancesRequestDescribeVerifiedAccessInstancesPaginateTypeDef,
    DescribeVerifiedAccessInstancesResultTypeDef,
    DescribeVerifiedAccessTrustProvidersRequestDescribeVerifiedAccessTrustProvidersPaginateTypeDef,
    DescribeVerifiedAccessTrustProvidersResultTypeDef,
    DescribeVolumesModificationsRequestDescribeVolumesModificationsPaginateTypeDef,
    DescribeVolumesModificationsResultTypeDef,
    DescribeVolumesRequestDescribeVolumesPaginateTypeDef,
    DescribeVolumesResultTypeDef,
    DescribeVolumeStatusRequestDescribeVolumeStatusPaginateTypeDef,
    DescribeVolumeStatusResultTypeDef,
    DescribeVpcClassicLinkDnsSupportRequestDescribeVpcClassicLinkDnsSupportPaginateTypeDef,
    DescribeVpcClassicLinkDnsSupportResultTypeDef,
    DescribeVpcEndpointConnectionNotificationsRequestDescribeVpcEndpointConnectionNotificationsPaginateTypeDef,
    DescribeVpcEndpointConnectionNotificationsResultTypeDef,
    DescribeVpcEndpointConnectionsRequestDescribeVpcEndpointConnectionsPaginateTypeDef,
    DescribeVpcEndpointConnectionsResultTypeDef,
    DescribeVpcEndpointServiceConfigurationsRequestDescribeVpcEndpointServiceConfigurationsPaginateTypeDef,
    DescribeVpcEndpointServiceConfigurationsResultTypeDef,
    DescribeVpcEndpointServicePermissionsRequestDescribeVpcEndpointServicePermissionsPaginateTypeDef,
    DescribeVpcEndpointServicePermissionsResultTypeDef,
    DescribeVpcEndpointServicesRequestDescribeVpcEndpointServicesPaginateTypeDef,
    DescribeVpcEndpointServicesResultTypeDef,
    DescribeVpcEndpointsRequestDescribeVpcEndpointsPaginateTypeDef,
    DescribeVpcEndpointsResultTypeDef,
    DescribeVpcPeeringConnectionsRequestDescribeVpcPeeringConnectionsPaginateTypeDef,
    DescribeVpcPeeringConnectionsResultTypeDef,
    DescribeVpcsRequestDescribeVpcsPaginateTypeDef,
    DescribeVpcsResultTypeDef,
    GetAssociatedIpv6PoolCidrsRequestGetAssociatedIpv6PoolCidrsPaginateTypeDef,
    GetAssociatedIpv6PoolCidrsResultTypeDef,
    GetAwsNetworkPerformanceDataRequestGetAwsNetworkPerformanceDataPaginateTypeDef,
    GetAwsNetworkPerformanceDataResultTypeDef,
    GetGroupsForCapacityReservationRequestGetGroupsForCapacityReservationPaginateTypeDef,
    GetGroupsForCapacityReservationResultTypeDef,
    GetInstanceTypesFromInstanceRequirementsRequestGetInstanceTypesFromInstanceRequirementsPaginateTypeDef,
    GetInstanceTypesFromInstanceRequirementsResultTypeDef,
    GetIpamAddressHistoryRequestGetIpamAddressHistoryPaginateTypeDef,
    GetIpamAddressHistoryResultTypeDef,
    GetIpamDiscoveredAccountsRequestGetIpamDiscoveredAccountsPaginateTypeDef,
    GetIpamDiscoveredAccountsResultTypeDef,
    GetIpamDiscoveredResourceCidrsRequestGetIpamDiscoveredResourceCidrsPaginateTypeDef,
    GetIpamDiscoveredResourceCidrsResultTypeDef,
    GetIpamPoolAllocationsRequestGetIpamPoolAllocationsPaginateTypeDef,
    GetIpamPoolAllocationsResultTypeDef,
    GetIpamPoolCidrsRequestGetIpamPoolCidrsPaginateTypeDef,
    GetIpamPoolCidrsResultTypeDef,
    GetIpamResourceCidrsRequestGetIpamResourceCidrsPaginateTypeDef,
    GetIpamResourceCidrsResultTypeDef,
    GetManagedPrefixListAssociationsRequestGetManagedPrefixListAssociationsPaginateTypeDef,
    GetManagedPrefixListAssociationsResultTypeDef,
    GetManagedPrefixListEntriesRequestGetManagedPrefixListEntriesPaginateTypeDef,
    GetManagedPrefixListEntriesResultTypeDef,
    GetNetworkInsightsAccessScopeAnalysisFindingsRequestGetNetworkInsightsAccessScopeAnalysisFindingsPaginateTypeDef,
    GetNetworkInsightsAccessScopeAnalysisFindingsResultTypeDef,
    GetSecurityGroupsForVpcRequestGetSecurityGroupsForVpcPaginateTypeDef,
    GetSecurityGroupsForVpcResultTypeDef,
    GetSpotPlacementScoresRequestGetSpotPlacementScoresPaginateTypeDef,
    GetSpotPlacementScoresResultTypeDef,
    GetTransitGatewayAttachmentPropagationsRequestGetTransitGatewayAttachmentPropagationsPaginateTypeDef,
    GetTransitGatewayAttachmentPropagationsResultTypeDef,
    GetTransitGatewayMulticastDomainAssociationsRequestGetTransitGatewayMulticastDomainAssociationsPaginateTypeDef,
    GetTransitGatewayMulticastDomainAssociationsResultTypeDef,
    GetTransitGatewayPolicyTableAssociationsRequestGetTransitGatewayPolicyTableAssociationsPaginateTypeDef,
    GetTransitGatewayPolicyTableAssociationsResultTypeDef,
    GetTransitGatewayPrefixListReferencesRequestGetTransitGatewayPrefixListReferencesPaginateTypeDef,
    GetTransitGatewayPrefixListReferencesResultTypeDef,
    GetTransitGatewayRouteTableAssociationsRequestGetTransitGatewayRouteTableAssociationsPaginateTypeDef,
    GetTransitGatewayRouteTableAssociationsResultTypeDef,
    GetTransitGatewayRouteTablePropagationsRequestGetTransitGatewayRouteTablePropagationsPaginateTypeDef,
    GetTransitGatewayRouteTablePropagationsResultTypeDef,
    GetVpnConnectionDeviceTypesRequestGetVpnConnectionDeviceTypesPaginateTypeDef,
    GetVpnConnectionDeviceTypesResultTypeDef,
    ListImagesInRecycleBinRequestListImagesInRecycleBinPaginateTypeDef,
    ListImagesInRecycleBinResultTypeDef,
    ListSnapshotsInRecycleBinRequestListSnapshotsInRecycleBinPaginateTypeDef,
    ListSnapshotsInRecycleBinResultTypeDef,
    SearchLocalGatewayRoutesRequestSearchLocalGatewayRoutesPaginateTypeDef,
    SearchLocalGatewayRoutesResultTypeDef,
    SearchTransitGatewayMulticastGroupsRequestSearchTransitGatewayMulticastGroupsPaginateTypeDef,
    SearchTransitGatewayMulticastGroupsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAddressTransfersPaginator",
    "DescribeAddressesAttributePaginator",
    "DescribeAwsNetworkPerformanceMetricSubscriptionsPaginator",
    "DescribeByoipCidrsPaginator",
    "DescribeCapacityBlockExtensionHistoryPaginator",
    "DescribeCapacityBlockExtensionOfferingsPaginator",
    "DescribeCapacityBlockOfferingsPaginator",
    "DescribeCapacityReservationBillingRequestsPaginator",
    "DescribeCapacityReservationFleetsPaginator",
    "DescribeCapacityReservationsPaginator",
    "DescribeCarrierGatewaysPaginator",
    "DescribeClassicLinkInstancesPaginator",
    "DescribeClientVpnAuthorizationRulesPaginator",
    "DescribeClientVpnConnectionsPaginator",
    "DescribeClientVpnEndpointsPaginator",
    "DescribeClientVpnRoutesPaginator",
    "DescribeClientVpnTargetNetworksPaginator",
    "DescribeCoipPoolsPaginator",
    "DescribeDhcpOptionsPaginator",
    "DescribeEgressOnlyInternetGatewaysPaginator",
    "DescribeExportImageTasksPaginator",
    "DescribeFastLaunchImagesPaginator",
    "DescribeFastSnapshotRestoresPaginator",
    "DescribeFleetsPaginator",
    "DescribeFlowLogsPaginator",
    "DescribeFpgaImagesPaginator",
    "DescribeHostReservationOfferingsPaginator",
    "DescribeHostReservationsPaginator",
    "DescribeHostsPaginator",
    "DescribeIamInstanceProfileAssociationsPaginator",
    "DescribeImagesPaginator",
    "DescribeImportImageTasksPaginator",
    "DescribeImportSnapshotTasksPaginator",
    "DescribeInstanceConnectEndpointsPaginator",
    "DescribeInstanceCreditSpecificationsPaginator",
    "DescribeInstanceEventWindowsPaginator",
    "DescribeInstanceImageMetadataPaginator",
    "DescribeInstanceStatusPaginator",
    "DescribeInstanceTopologyPaginator",
    "DescribeInstanceTypeOfferingsPaginator",
    "DescribeInstanceTypesPaginator",
    "DescribeInstancesPaginator",
    "DescribeInternetGatewaysPaginator",
    "DescribeIpamPoolsPaginator",
    "DescribeIpamResourceDiscoveriesPaginator",
    "DescribeIpamResourceDiscoveryAssociationsPaginator",
    "DescribeIpamScopesPaginator",
    "DescribeIpamsPaginator",
    "DescribeIpv6PoolsPaginator",
    "DescribeLaunchTemplateVersionsPaginator",
    "DescribeLaunchTemplatesPaginator",
    "DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginator",
    "DescribeLocalGatewayRouteTableVpcAssociationsPaginator",
    "DescribeLocalGatewayRouteTablesPaginator",
    "DescribeLocalGatewayVirtualInterfaceGroupsPaginator",
    "DescribeLocalGatewayVirtualInterfacesPaginator",
    "DescribeLocalGatewaysPaginator",
    "DescribeMacHostsPaginator",
    "DescribeManagedPrefixListsPaginator",
    "DescribeMovingAddressesPaginator",
    "DescribeNatGatewaysPaginator",
    "DescribeNetworkAclsPaginator",
    "DescribeNetworkInsightsAccessScopeAnalysesPaginator",
    "DescribeNetworkInsightsAccessScopesPaginator",
    "DescribeNetworkInsightsAnalysesPaginator",
    "DescribeNetworkInsightsPathsPaginator",
    "DescribeNetworkInterfacePermissionsPaginator",
    "DescribeNetworkInterfacesPaginator",
    "DescribePrefixListsPaginator",
    "DescribePrincipalIdFormatPaginator",
    "DescribePublicIpv4PoolsPaginator",
    "DescribeReplaceRootVolumeTasksPaginator",
    "DescribeReservedInstancesModificationsPaginator",
    "DescribeReservedInstancesOfferingsPaginator",
    "DescribeRouteTablesPaginator",
    "DescribeScheduledInstanceAvailabilityPaginator",
    "DescribeScheduledInstancesPaginator",
    "DescribeSecurityGroupRulesPaginator",
    "DescribeSecurityGroupVpcAssociationsPaginator",
    "DescribeSecurityGroupsPaginator",
    "DescribeSnapshotTierStatusPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeSpotFleetInstancesPaginator",
    "DescribeSpotFleetRequestsPaginator",
    "DescribeSpotInstanceRequestsPaginator",
    "DescribeSpotPriceHistoryPaginator",
    "DescribeStaleSecurityGroupsPaginator",
    "DescribeStoreImageTasksPaginator",
    "DescribeSubnetsPaginator",
    "DescribeTagsPaginator",
    "DescribeTrafficMirrorFiltersPaginator",
    "DescribeTrafficMirrorSessionsPaginator",
    "DescribeTrafficMirrorTargetsPaginator",
    "DescribeTransitGatewayAttachmentsPaginator",
    "DescribeTransitGatewayConnectPeersPaginator",
    "DescribeTransitGatewayConnectsPaginator",
    "DescribeTransitGatewayMulticastDomainsPaginator",
    "DescribeTransitGatewayPeeringAttachmentsPaginator",
    "DescribeTransitGatewayPolicyTablesPaginator",
    "DescribeTransitGatewayRouteTableAnnouncementsPaginator",
    "DescribeTransitGatewayRouteTablesPaginator",
    "DescribeTransitGatewayVpcAttachmentsPaginator",
    "DescribeTransitGatewaysPaginator",
    "DescribeTrunkInterfaceAssociationsPaginator",
    "DescribeVerifiedAccessEndpointsPaginator",
    "DescribeVerifiedAccessGroupsPaginator",
    "DescribeVerifiedAccessInstanceLoggingConfigurationsPaginator",
    "DescribeVerifiedAccessInstancesPaginator",
    "DescribeVerifiedAccessTrustProvidersPaginator",
    "DescribeVolumeStatusPaginator",
    "DescribeVolumesModificationsPaginator",
    "DescribeVolumesPaginator",
    "DescribeVpcClassicLinkDnsSupportPaginator",
    "DescribeVpcEndpointConnectionNotificationsPaginator",
    "DescribeVpcEndpointConnectionsPaginator",
    "DescribeVpcEndpointServiceConfigurationsPaginator",
    "DescribeVpcEndpointServicePermissionsPaginator",
    "DescribeVpcEndpointServicesPaginator",
    "DescribeVpcEndpointsPaginator",
    "DescribeVpcPeeringConnectionsPaginator",
    "DescribeVpcsPaginator",
    "GetAssociatedIpv6PoolCidrsPaginator",
    "GetAwsNetworkPerformanceDataPaginator",
    "GetGroupsForCapacityReservationPaginator",
    "GetInstanceTypesFromInstanceRequirementsPaginator",
    "GetIpamAddressHistoryPaginator",
    "GetIpamDiscoveredAccountsPaginator",
    "GetIpamDiscoveredResourceCidrsPaginator",
    "GetIpamPoolAllocationsPaginator",
    "GetIpamPoolCidrsPaginator",
    "GetIpamResourceCidrsPaginator",
    "GetManagedPrefixListAssociationsPaginator",
    "GetManagedPrefixListEntriesPaginator",
    "GetNetworkInsightsAccessScopeAnalysisFindingsPaginator",
    "GetSecurityGroupsForVpcPaginator",
    "GetSpotPlacementScoresPaginator",
    "GetTransitGatewayAttachmentPropagationsPaginator",
    "GetTransitGatewayMulticastDomainAssociationsPaginator",
    "GetTransitGatewayPolicyTableAssociationsPaginator",
    "GetTransitGatewayPrefixListReferencesPaginator",
    "GetTransitGatewayRouteTableAssociationsPaginator",
    "GetTransitGatewayRouteTablePropagationsPaginator",
    "GetVpnConnectionDeviceTypesPaginator",
    "ListImagesInRecycleBinPaginator",
    "ListSnapshotsInRecycleBinPaginator",
    "SearchLocalGatewayRoutesPaginator",
    "SearchTransitGatewayMulticastGroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAddressTransfersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeAddressTransfers.html#EC2.Paginator.DescribeAddressTransfers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeaddresstransferspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeAddressTransfersRequestDescribeAddressTransfersPaginateTypeDef],
    ) -> _PageIterator[DescribeAddressTransfersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeAddressTransfers.html#EC2.Paginator.DescribeAddressTransfers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeaddresstransferspaginator)
        """


class DescribeAddressesAttributePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeAddressesAttribute.html#EC2.Paginator.DescribeAddressesAttribute)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeaddressesattributepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAddressesAttributeRequestDescribeAddressesAttributePaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAddressesAttributeResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeAddressesAttribute.html#EC2.Paginator.DescribeAddressesAttribute.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeaddressesattributepaginator)
        """


class DescribeAwsNetworkPerformanceMetricSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeAwsNetworkPerformanceMetricSubscriptions.html#EC2.Paginator.DescribeAwsNetworkPerformanceMetricSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeawsnetworkperformancemetricsubscriptionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAwsNetworkPerformanceMetricSubscriptionsRequestDescribeAwsNetworkPerformanceMetricSubscriptionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAwsNetworkPerformanceMetricSubscriptionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeAwsNetworkPerformanceMetricSubscriptions.html#EC2.Paginator.DescribeAwsNetworkPerformanceMetricSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeawsnetworkperformancemetricsubscriptionspaginator)
        """


class DescribeByoipCidrsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeByoipCidrs.html#EC2.Paginator.DescribeByoipCidrs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describebyoipcidrspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeByoipCidrsRequestDescribeByoipCidrsPaginateTypeDef]
    ) -> _PageIterator[DescribeByoipCidrsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeByoipCidrs.html#EC2.Paginator.DescribeByoipCidrs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describebyoipcidrspaginator)
        """


class DescribeCapacityBlockExtensionHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityBlockExtensionHistory.html#EC2.Paginator.DescribeCapacityBlockExtensionHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityblockextensionhistorypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCapacityBlockExtensionHistoryRequestDescribeCapacityBlockExtensionHistoryPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeCapacityBlockExtensionHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityBlockExtensionHistory.html#EC2.Paginator.DescribeCapacityBlockExtensionHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityblockextensionhistorypaginator)
        """


class DescribeCapacityBlockExtensionOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityBlockExtensionOfferings.html#EC2.Paginator.DescribeCapacityBlockExtensionOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityblockextensionofferingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCapacityBlockExtensionOfferingsRequestDescribeCapacityBlockExtensionOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeCapacityBlockExtensionOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityBlockExtensionOfferings.html#EC2.Paginator.DescribeCapacityBlockExtensionOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityblockextensionofferingspaginator)
        """


class DescribeCapacityBlockOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityBlockOfferings.html#EC2.Paginator.DescribeCapacityBlockOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityblockofferingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCapacityBlockOfferingsRequestDescribeCapacityBlockOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeCapacityBlockOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityBlockOfferings.html#EC2.Paginator.DescribeCapacityBlockOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityblockofferingspaginator)
        """


class DescribeCapacityReservationBillingRequestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityReservationBillingRequests.html#EC2.Paginator.DescribeCapacityReservationBillingRequests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityreservationbillingrequestspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCapacityReservationBillingRequestsRequestDescribeCapacityReservationBillingRequestsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeCapacityReservationBillingRequestsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityReservationBillingRequests.html#EC2.Paginator.DescribeCapacityReservationBillingRequests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityreservationbillingrequestspaginator)
        """


class DescribeCapacityReservationFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityReservationFleets.html#EC2.Paginator.DescribeCapacityReservationFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityreservationfleetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCapacityReservationFleetsRequestDescribeCapacityReservationFleetsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeCapacityReservationFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityReservationFleets.html#EC2.Paginator.DescribeCapacityReservationFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityreservationfleetspaginator)
        """


class DescribeCapacityReservationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityReservations.html#EC2.Paginator.DescribeCapacityReservations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityreservationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCapacityReservationsRequestDescribeCapacityReservationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeCapacityReservationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCapacityReservations.html#EC2.Paginator.DescribeCapacityReservations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecapacityreservationspaginator)
        """


class DescribeCarrierGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCarrierGateways.html#EC2.Paginator.DescribeCarrierGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecarriergatewayspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeCarrierGatewaysRequestDescribeCarrierGatewaysPaginateTypeDef]
    ) -> _PageIterator[DescribeCarrierGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCarrierGateways.html#EC2.Paginator.DescribeCarrierGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecarriergatewayspaginator)
        """


class DescribeClassicLinkInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClassicLinkInstances.html#EC2.Paginator.DescribeClassicLinkInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclassiclinkinstancespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClassicLinkInstancesRequestDescribeClassicLinkInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeClassicLinkInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClassicLinkInstances.html#EC2.Paginator.DescribeClassicLinkInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclassiclinkinstancespaginator)
        """


class DescribeClientVpnAuthorizationRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnAuthorizationRules.html#EC2.Paginator.DescribeClientVpnAuthorizationRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnauthorizationrulespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClientVpnAuthorizationRulesRequestDescribeClientVpnAuthorizationRulesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeClientVpnAuthorizationRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnAuthorizationRules.html#EC2.Paginator.DescribeClientVpnAuthorizationRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnauthorizationrulespaginator)
        """


class DescribeClientVpnConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnConnections.html#EC2.Paginator.DescribeClientVpnConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnconnectionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClientVpnConnectionsRequestDescribeClientVpnConnectionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeClientVpnConnectionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnConnections.html#EC2.Paginator.DescribeClientVpnConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnconnectionspaginator)
        """


class DescribeClientVpnEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnEndpoints.html#EC2.Paginator.DescribeClientVpnEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnendpointspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClientVpnEndpointsRequestDescribeClientVpnEndpointsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeClientVpnEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnEndpoints.html#EC2.Paginator.DescribeClientVpnEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnendpointspaginator)
        """


class DescribeClientVpnRoutesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnRoutes.html#EC2.Paginator.DescribeClientVpnRoutes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnroutespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeClientVpnRoutesRequestDescribeClientVpnRoutesPaginateTypeDef]
    ) -> _PageIterator[DescribeClientVpnRoutesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnRoutes.html#EC2.Paginator.DescribeClientVpnRoutes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpnroutespaginator)
        """


class DescribeClientVpnTargetNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnTargetNetworks.html#EC2.Paginator.DescribeClientVpnTargetNetworks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpntargetnetworkspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClientVpnTargetNetworksRequestDescribeClientVpnTargetNetworksPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeClientVpnTargetNetworksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeClientVpnTargetNetworks.html#EC2.Paginator.DescribeClientVpnTargetNetworks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeclientvpntargetnetworkspaginator)
        """


class DescribeCoipPoolsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCoipPools.html#EC2.Paginator.DescribeCoipPools)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecoippoolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeCoipPoolsRequestDescribeCoipPoolsPaginateTypeDef]
    ) -> _PageIterator[DescribeCoipPoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeCoipPools.html#EC2.Paginator.DescribeCoipPools.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describecoippoolspaginator)
        """


class DescribeDhcpOptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeDhcpOptions.html#EC2.Paginator.DescribeDhcpOptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describedhcpoptionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeDhcpOptionsRequestDescribeDhcpOptionsPaginateTypeDef]
    ) -> _PageIterator[DescribeDhcpOptionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeDhcpOptions.html#EC2.Paginator.DescribeDhcpOptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describedhcpoptionspaginator)
        """


class DescribeEgressOnlyInternetGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeEgressOnlyInternetGateways.html#EC2.Paginator.DescribeEgressOnlyInternetGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeegressonlyinternetgatewayspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEgressOnlyInternetGatewaysRequestDescribeEgressOnlyInternetGatewaysPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeEgressOnlyInternetGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeEgressOnlyInternetGateways.html#EC2.Paginator.DescribeEgressOnlyInternetGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeegressonlyinternetgatewayspaginator)
        """


class DescribeExportImageTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeExportImageTasks.html#EC2.Paginator.DescribeExportImageTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeexportimagetaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeExportImageTasksRequestDescribeExportImageTasksPaginateTypeDef],
    ) -> _PageIterator[DescribeExportImageTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeExportImageTasks.html#EC2.Paginator.DescribeExportImageTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeexportimagetaskspaginator)
        """


class DescribeFastLaunchImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFastLaunchImages.html#EC2.Paginator.DescribeFastLaunchImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefastlaunchimagespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeFastLaunchImagesRequestDescribeFastLaunchImagesPaginateTypeDef],
    ) -> _PageIterator[DescribeFastLaunchImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFastLaunchImages.html#EC2.Paginator.DescribeFastLaunchImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefastlaunchimagespaginator)
        """


class DescribeFastSnapshotRestoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFastSnapshotRestores.html#EC2.Paginator.DescribeFastSnapshotRestores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefastsnapshotrestorespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeFastSnapshotRestoresRequestDescribeFastSnapshotRestoresPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeFastSnapshotRestoresResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFastSnapshotRestores.html#EC2.Paginator.DescribeFastSnapshotRestores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefastsnapshotrestorespaginator)
        """


class DescribeFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFleets.html#EC2.Paginator.DescribeFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFleetsRequestDescribeFleetsPaginateTypeDef]
    ) -> _PageIterator[DescribeFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFleets.html#EC2.Paginator.DescribeFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefleetspaginator)
        """


class DescribeFlowLogsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFlowLogs.html#EC2.Paginator.DescribeFlowLogs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeflowlogspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFlowLogsRequestDescribeFlowLogsPaginateTypeDef]
    ) -> _PageIterator[DescribeFlowLogsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFlowLogs.html#EC2.Paginator.DescribeFlowLogs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeflowlogspaginator)
        """


class DescribeFpgaImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFpgaImages.html#EC2.Paginator.DescribeFpgaImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefpgaimagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFpgaImagesRequestDescribeFpgaImagesPaginateTypeDef]
    ) -> _PageIterator[DescribeFpgaImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeFpgaImages.html#EC2.Paginator.DescribeFpgaImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describefpgaimagespaginator)
        """


class DescribeHostReservationOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeHostReservationOfferings.html#EC2.Paginator.DescribeHostReservationOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describehostreservationofferingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeHostReservationOfferingsRequestDescribeHostReservationOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeHostReservationOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeHostReservationOfferings.html#EC2.Paginator.DescribeHostReservationOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describehostreservationofferingspaginator)
        """


class DescribeHostReservationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeHostReservations.html#EC2.Paginator.DescribeHostReservations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describehostreservationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeHostReservationsRequestDescribeHostReservationsPaginateTypeDef],
    ) -> _PageIterator[DescribeHostReservationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeHostReservations.html#EC2.Paginator.DescribeHostReservations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describehostreservationspaginator)
        """


class DescribeHostsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeHosts.html#EC2.Paginator.DescribeHosts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describehostspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeHostsRequestDescribeHostsPaginateTypeDef]
    ) -> _PageIterator[DescribeHostsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeHosts.html#EC2.Paginator.DescribeHosts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describehostspaginator)
        """


class DescribeIamInstanceProfileAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIamInstanceProfileAssociations.html#EC2.Paginator.DescribeIamInstanceProfileAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeiaminstanceprofileassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeIamInstanceProfileAssociationsRequestDescribeIamInstanceProfileAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeIamInstanceProfileAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIamInstanceProfileAssociations.html#EC2.Paginator.DescribeIamInstanceProfileAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeiaminstanceprofileassociationspaginator)
        """


class DescribeImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeImages.html#EC2.Paginator.DescribeImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeimagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeImagesRequestDescribeImagesPaginateTypeDef]
    ) -> _PageIterator[DescribeImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeImages.html#EC2.Paginator.DescribeImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeimagespaginator)
        """


class DescribeImportImageTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeImportImageTasks.html#EC2.Paginator.DescribeImportImageTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeimportimagetaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeImportImageTasksRequestDescribeImportImageTasksPaginateTypeDef],
    ) -> _PageIterator[DescribeImportImageTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeImportImageTasks.html#EC2.Paginator.DescribeImportImageTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeimportimagetaskspaginator)
        """


class DescribeImportSnapshotTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeImportSnapshotTasks.html#EC2.Paginator.DescribeImportSnapshotTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeimportsnapshottaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeImportSnapshotTasksRequestDescribeImportSnapshotTasksPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeImportSnapshotTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeImportSnapshotTasks.html#EC2.Paginator.DescribeImportSnapshotTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeimportsnapshottaskspaginator)
        """


class DescribeInstanceConnectEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceConnectEndpoints.html#EC2.Paginator.DescribeInstanceConnectEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstanceconnectendpointspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceConnectEndpointsRequestDescribeInstanceConnectEndpointsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstanceConnectEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceConnectEndpoints.html#EC2.Paginator.DescribeInstanceConnectEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstanceconnectendpointspaginator)
        """


class DescribeInstanceCreditSpecificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceCreditSpecifications.html#EC2.Paginator.DescribeInstanceCreditSpecifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancecreditspecificationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceCreditSpecificationsRequestDescribeInstanceCreditSpecificationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstanceCreditSpecificationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceCreditSpecifications.html#EC2.Paginator.DescribeInstanceCreditSpecifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancecreditspecificationspaginator)
        """


class DescribeInstanceEventWindowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceEventWindows.html#EC2.Paginator.DescribeInstanceEventWindows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstanceeventwindowspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceEventWindowsRequestDescribeInstanceEventWindowsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstanceEventWindowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceEventWindows.html#EC2.Paginator.DescribeInstanceEventWindows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstanceeventwindowspaginator)
        """


class DescribeInstanceImageMetadataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceImageMetadata.html#EC2.Paginator.DescribeInstanceImageMetadata)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstanceimagemetadatapaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceImageMetadataRequestDescribeInstanceImageMetadataPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstanceImageMetadataResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceImageMetadata.html#EC2.Paginator.DescribeInstanceImageMetadata.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstanceimagemetadatapaginator)
        """


class DescribeInstanceStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceStatus.html#EC2.Paginator.DescribeInstanceStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancestatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeInstanceStatusRequestDescribeInstanceStatusPaginateTypeDef]
    ) -> _PageIterator[DescribeInstanceStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceStatus.html#EC2.Paginator.DescribeInstanceStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancestatuspaginator)
        """


class DescribeInstanceTopologyPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceTopology.html#EC2.Paginator.DescribeInstanceTopology)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancetopologypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeInstanceTopologyRequestDescribeInstanceTopologyPaginateTypeDef],
    ) -> _PageIterator[DescribeInstanceTopologyResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceTopology.html#EC2.Paginator.DescribeInstanceTopology.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancetopologypaginator)
        """


class DescribeInstanceTypeOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceTypeOfferings.html#EC2.Paginator.DescribeInstanceTypeOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancetypeofferingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceTypeOfferingsRequestDescribeInstanceTypeOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstanceTypeOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceTypeOfferings.html#EC2.Paginator.DescribeInstanceTypeOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancetypeofferingspaginator)
        """


class DescribeInstanceTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceTypes.html#EC2.Paginator.DescribeInstanceTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancetypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeInstanceTypesRequestDescribeInstanceTypesPaginateTypeDef]
    ) -> _PageIterator[DescribeInstanceTypesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstanceTypes.html#EC2.Paginator.DescribeInstanceTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancetypespaginator)
        """


class DescribeInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstances.html#EC2.Paginator.DescribeInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeInstancesRequestDescribeInstancesPaginateTypeDef]
    ) -> _PageIterator[DescribeInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstances.html#EC2.Paginator.DescribeInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinstancespaginator)
        """


class DescribeInternetGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInternetGateways.html#EC2.Paginator.DescribeInternetGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinternetgatewayspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeInternetGatewaysRequestDescribeInternetGatewaysPaginateTypeDef],
    ) -> _PageIterator[DescribeInternetGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInternetGateways.html#EC2.Paginator.DescribeInternetGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeinternetgatewayspaginator)
        """


class DescribeIpamPoolsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamPools.html#EC2.Paginator.DescribeIpamPools)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipampoolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeIpamPoolsRequestDescribeIpamPoolsPaginateTypeDef]
    ) -> _PageIterator[DescribeIpamPoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamPools.html#EC2.Paginator.DescribeIpamPools.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipampoolspaginator)
        """


class DescribeIpamResourceDiscoveriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamResourceDiscoveries.html#EC2.Paginator.DescribeIpamResourceDiscoveries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamresourcediscoveriespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeIpamResourceDiscoveriesRequestDescribeIpamResourceDiscoveriesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeIpamResourceDiscoveriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamResourceDiscoveries.html#EC2.Paginator.DescribeIpamResourceDiscoveries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamresourcediscoveriespaginator)
        """


class DescribeIpamResourceDiscoveryAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamResourceDiscoveryAssociations.html#EC2.Paginator.DescribeIpamResourceDiscoveryAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamresourcediscoveryassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeIpamResourceDiscoveryAssociationsRequestDescribeIpamResourceDiscoveryAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeIpamResourceDiscoveryAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamResourceDiscoveryAssociations.html#EC2.Paginator.DescribeIpamResourceDiscoveryAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamresourcediscoveryassociationspaginator)
        """


class DescribeIpamScopesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamScopes.html#EC2.Paginator.DescribeIpamScopes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamscopespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeIpamScopesRequestDescribeIpamScopesPaginateTypeDef]
    ) -> _PageIterator[DescribeIpamScopesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpamScopes.html#EC2.Paginator.DescribeIpamScopes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamscopespaginator)
        """


class DescribeIpamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpams.html#EC2.Paginator.DescribeIpams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeIpamsRequestDescribeIpamsPaginateTypeDef]
    ) -> _PageIterator[DescribeIpamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpams.html#EC2.Paginator.DescribeIpams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipamspaginator)
        """


class DescribeIpv6PoolsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpv6Pools.html#EC2.Paginator.DescribeIpv6Pools)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipv6poolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeIpv6PoolsRequestDescribeIpv6PoolsPaginateTypeDef]
    ) -> _PageIterator[DescribeIpv6PoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeIpv6Pools.html#EC2.Paginator.DescribeIpv6Pools.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeipv6poolspaginator)
        """


class DescribeLaunchTemplateVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLaunchTemplateVersions.html#EC2.Paginator.DescribeLaunchTemplateVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelaunchtemplateversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLaunchTemplateVersionsRequestDescribeLaunchTemplateVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLaunchTemplateVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLaunchTemplateVersions.html#EC2.Paginator.DescribeLaunchTemplateVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelaunchtemplateversionspaginator)
        """


class DescribeLaunchTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLaunchTemplates.html#EC2.Paginator.DescribeLaunchTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelaunchtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeLaunchTemplatesRequestDescribeLaunchTemplatesPaginateTypeDef]
    ) -> _PageIterator[DescribeLaunchTemplatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLaunchTemplates.html#EC2.Paginator.DescribeLaunchTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelaunchtemplatespaginator)
        """


class DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociations.html#EC2.Paginator.DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayroutetablevirtualinterfacegroupassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestDescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[
        DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsResultTypeDef
    ]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociations.html#EC2.Paginator.DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayroutetablevirtualinterfacegroupassociationspaginator)
        """


class DescribeLocalGatewayRouteTableVpcAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayRouteTableVpcAssociations.html#EC2.Paginator.DescribeLocalGatewayRouteTableVpcAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayroutetablevpcassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLocalGatewayRouteTableVpcAssociationsRequestDescribeLocalGatewayRouteTableVpcAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLocalGatewayRouteTableVpcAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayRouteTableVpcAssociations.html#EC2.Paginator.DescribeLocalGatewayRouteTableVpcAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayroutetablevpcassociationspaginator)
        """


class DescribeLocalGatewayRouteTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayRouteTables.html#EC2.Paginator.DescribeLocalGatewayRouteTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayroutetablespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLocalGatewayRouteTablesRequestDescribeLocalGatewayRouteTablesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLocalGatewayRouteTablesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayRouteTables.html#EC2.Paginator.DescribeLocalGatewayRouteTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayroutetablespaginator)
        """


class DescribeLocalGatewayVirtualInterfaceGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayVirtualInterfaceGroups.html#EC2.Paginator.DescribeLocalGatewayVirtualInterfaceGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayvirtualinterfacegroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLocalGatewayVirtualInterfaceGroupsRequestDescribeLocalGatewayVirtualInterfaceGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLocalGatewayVirtualInterfaceGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayVirtualInterfaceGroups.html#EC2.Paginator.DescribeLocalGatewayVirtualInterfaceGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayvirtualinterfacegroupspaginator)
        """


class DescribeLocalGatewayVirtualInterfacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayVirtualInterfaces.html#EC2.Paginator.DescribeLocalGatewayVirtualInterfaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayvirtualinterfacespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLocalGatewayVirtualInterfacesRequestDescribeLocalGatewayVirtualInterfacesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLocalGatewayVirtualInterfacesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGatewayVirtualInterfaces.html#EC2.Paginator.DescribeLocalGatewayVirtualInterfaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayvirtualinterfacespaginator)
        """


class DescribeLocalGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGateways.html#EC2.Paginator.DescribeLocalGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeLocalGatewaysRequestDescribeLocalGatewaysPaginateTypeDef]
    ) -> _PageIterator[DescribeLocalGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeLocalGateways.html#EC2.Paginator.DescribeLocalGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describelocalgatewayspaginator)
        """


class DescribeMacHostsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeMacHosts.html#EC2.Paginator.DescribeMacHosts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describemachostspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeMacHostsRequestDescribeMacHostsPaginateTypeDef]
    ) -> _PageIterator[DescribeMacHostsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeMacHosts.html#EC2.Paginator.DescribeMacHosts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describemachostspaginator)
        """


class DescribeManagedPrefixListsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeManagedPrefixLists.html#EC2.Paginator.DescribeManagedPrefixLists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describemanagedprefixlistspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeManagedPrefixListsRequestDescribeManagedPrefixListsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeManagedPrefixListsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeManagedPrefixLists.html#EC2.Paginator.DescribeManagedPrefixLists.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describemanagedprefixlistspaginator)
        """


class DescribeMovingAddressesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeMovingAddresses.html#EC2.Paginator.DescribeMovingAddresses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describemovingaddressespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeMovingAddressesRequestDescribeMovingAddressesPaginateTypeDef]
    ) -> _PageIterator[DescribeMovingAddressesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeMovingAddresses.html#EC2.Paginator.DescribeMovingAddresses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describemovingaddressespaginator)
        """


class DescribeNatGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNatGateways.html#EC2.Paginator.DescribeNatGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenatgatewayspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeNatGatewaysRequestDescribeNatGatewaysPaginateTypeDef]
    ) -> _PageIterator[DescribeNatGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNatGateways.html#EC2.Paginator.DescribeNatGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenatgatewayspaginator)
        """


class DescribeNetworkAclsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkAcls.html#EC2.Paginator.DescribeNetworkAcls)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkaclspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeNetworkAclsRequestDescribeNetworkAclsPaginateTypeDef]
    ) -> _PageIterator[DescribeNetworkAclsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkAcls.html#EC2.Paginator.DescribeNetworkAcls.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkaclspaginator)
        """


class DescribeNetworkInsightsAccessScopeAnalysesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsAccessScopeAnalyses.html#EC2.Paginator.DescribeNetworkInsightsAccessScopeAnalyses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightsaccessscopeanalysespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNetworkInsightsAccessScopeAnalysesRequestDescribeNetworkInsightsAccessScopeAnalysesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeNetworkInsightsAccessScopeAnalysesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsAccessScopeAnalyses.html#EC2.Paginator.DescribeNetworkInsightsAccessScopeAnalyses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightsaccessscopeanalysespaginator)
        """


class DescribeNetworkInsightsAccessScopesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsAccessScopes.html#EC2.Paginator.DescribeNetworkInsightsAccessScopes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightsaccessscopespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNetworkInsightsAccessScopesRequestDescribeNetworkInsightsAccessScopesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeNetworkInsightsAccessScopesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsAccessScopes.html#EC2.Paginator.DescribeNetworkInsightsAccessScopes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightsaccessscopespaginator)
        """


class DescribeNetworkInsightsAnalysesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsAnalyses.html#EC2.Paginator.DescribeNetworkInsightsAnalyses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightsanalysespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNetworkInsightsAnalysesRequestDescribeNetworkInsightsAnalysesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeNetworkInsightsAnalysesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsAnalyses.html#EC2.Paginator.DescribeNetworkInsightsAnalyses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightsanalysespaginator)
        """


class DescribeNetworkInsightsPathsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsPaths.html#EC2.Paginator.DescribeNetworkInsightsPaths)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightspathspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNetworkInsightsPathsRequestDescribeNetworkInsightsPathsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeNetworkInsightsPathsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInsightsPaths.html#EC2.Paginator.DescribeNetworkInsightsPaths.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinsightspathspaginator)
        """


class DescribeNetworkInterfacePermissionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInterfacePermissions.html#EC2.Paginator.DescribeNetworkInterfacePermissions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinterfacepermissionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNetworkInterfacePermissionsRequestDescribeNetworkInterfacePermissionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeNetworkInterfacePermissionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInterfacePermissions.html#EC2.Paginator.DescribeNetworkInterfacePermissions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinterfacepermissionspaginator)
        """


class DescribeNetworkInterfacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInterfaces.html#EC2.Paginator.DescribeNetworkInterfaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinterfacespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeNetworkInterfacesRequestDescribeNetworkInterfacesPaginateTypeDef],
    ) -> _PageIterator[DescribeNetworkInterfacesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeNetworkInterfaces.html#EC2.Paginator.DescribeNetworkInterfaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describenetworkinterfacespaginator)
        """


class DescribePrefixListsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribePrefixLists.html#EC2.Paginator.DescribePrefixLists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeprefixlistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePrefixListsRequestDescribePrefixListsPaginateTypeDef]
    ) -> _PageIterator[DescribePrefixListsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribePrefixLists.html#EC2.Paginator.DescribePrefixLists.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeprefixlistspaginator)
        """


class DescribePrincipalIdFormatPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribePrincipalIdFormat.html#EC2.Paginator.DescribePrincipalIdFormat)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeprincipalidformatpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribePrincipalIdFormatRequestDescribePrincipalIdFormatPaginateTypeDef],
    ) -> _PageIterator[DescribePrincipalIdFormatResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribePrincipalIdFormat.html#EC2.Paginator.DescribePrincipalIdFormat.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeprincipalidformatpaginator)
        """


class DescribePublicIpv4PoolsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribePublicIpv4Pools.html#EC2.Paginator.DescribePublicIpv4Pools)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describepublicipv4poolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePublicIpv4PoolsRequestDescribePublicIpv4PoolsPaginateTypeDef]
    ) -> _PageIterator[DescribePublicIpv4PoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribePublicIpv4Pools.html#EC2.Paginator.DescribePublicIpv4Pools.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describepublicipv4poolspaginator)
        """


class DescribeReplaceRootVolumeTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeReplaceRootVolumeTasks.html#EC2.Paginator.DescribeReplaceRootVolumeTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describereplacerootvolumetaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplaceRootVolumeTasksRequestDescribeReplaceRootVolumeTasksPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReplaceRootVolumeTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeReplaceRootVolumeTasks.html#EC2.Paginator.DescribeReplaceRootVolumeTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describereplacerootvolumetaskspaginator)
        """


class DescribeReservedInstancesModificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeReservedInstancesModifications.html#EC2.Paginator.DescribeReservedInstancesModifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describereservedinstancesmodificationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedInstancesModificationsRequestDescribeReservedInstancesModificationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReservedInstancesModificationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeReservedInstancesModifications.html#EC2.Paginator.DescribeReservedInstancesModifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describereservedinstancesmodificationspaginator)
        """


class DescribeReservedInstancesOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeReservedInstancesOfferings.html#EC2.Paginator.DescribeReservedInstancesOfferings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describereservedinstancesofferingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedInstancesOfferingsRequestDescribeReservedInstancesOfferingsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReservedInstancesOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeReservedInstancesOfferings.html#EC2.Paginator.DescribeReservedInstancesOfferings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describereservedinstancesofferingspaginator)
        """


class DescribeRouteTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeRouteTables.html#EC2.Paginator.DescribeRouteTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeroutetablespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeRouteTablesRequestDescribeRouteTablesPaginateTypeDef]
    ) -> _PageIterator[DescribeRouteTablesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeRouteTables.html#EC2.Paginator.DescribeRouteTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeroutetablespaginator)
        """


class DescribeScheduledInstanceAvailabilityPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeScheduledInstanceAvailability.html#EC2.Paginator.DescribeScheduledInstanceAvailability)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describescheduledinstanceavailabilitypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeScheduledInstanceAvailabilityRequestDescribeScheduledInstanceAvailabilityPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeScheduledInstanceAvailabilityResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeScheduledInstanceAvailability.html#EC2.Paginator.DescribeScheduledInstanceAvailability.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describescheduledinstanceavailabilitypaginator)
        """


class DescribeScheduledInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeScheduledInstances.html#EC2.Paginator.DescribeScheduledInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describescheduledinstancespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeScheduledInstancesRequestDescribeScheduledInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeScheduledInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeScheduledInstances.html#EC2.Paginator.DescribeScheduledInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describescheduledinstancespaginator)
        """


class DescribeSecurityGroupRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroupRules.html#EC2.Paginator.DescribeSecurityGroupRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesecuritygrouprulespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSecurityGroupRulesRequestDescribeSecurityGroupRulesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSecurityGroupRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroupRules.html#EC2.Paginator.DescribeSecurityGroupRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesecuritygrouprulespaginator)
        """


class DescribeSecurityGroupVpcAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroupVpcAssociations.html#EC2.Paginator.DescribeSecurityGroupVpcAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesecuritygroupvpcassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSecurityGroupVpcAssociationsRequestDescribeSecurityGroupVpcAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSecurityGroupVpcAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroupVpcAssociations.html#EC2.Paginator.DescribeSecurityGroupVpcAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesecuritygroupvpcassociationspaginator)
        """


class DescribeSecurityGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroups.html#EC2.Paginator.DescribeSecurityGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesecuritygroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSecurityGroupsRequestDescribeSecurityGroupsPaginateTypeDef]
    ) -> _PageIterator[DescribeSecurityGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroups.html#EC2.Paginator.DescribeSecurityGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesecuritygroupspaginator)
        """


class DescribeSnapshotTierStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSnapshotTierStatus.html#EC2.Paginator.DescribeSnapshotTierStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesnapshottierstatuspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSnapshotTierStatusRequestDescribeSnapshotTierStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSnapshotTierStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSnapshotTierStatus.html#EC2.Paginator.DescribeSnapshotTierStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesnapshottierstatuspaginator)
        """


class DescribeSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSnapshots.html#EC2.Paginator.DescribeSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesnapshotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef]
    ) -> _PageIterator[DescribeSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSnapshots.html#EC2.Paginator.DescribeSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesnapshotspaginator)
        """


class DescribeSpotFleetInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotFleetInstances.html#EC2.Paginator.DescribeSpotFleetInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotfleetinstancespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSpotFleetInstancesRequestDescribeSpotFleetInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSpotFleetInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotFleetInstances.html#EC2.Paginator.DescribeSpotFleetInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotfleetinstancespaginator)
        """


class DescribeSpotFleetRequestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotFleetRequests.html#EC2.Paginator.DescribeSpotFleetRequests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotfleetrequestspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeSpotFleetRequestsRequestDescribeSpotFleetRequestsPaginateTypeDef],
    ) -> _PageIterator[DescribeSpotFleetRequestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotFleetRequests.html#EC2.Paginator.DescribeSpotFleetRequests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotfleetrequestspaginator)
        """


class DescribeSpotInstanceRequestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotInstanceRequests.html#EC2.Paginator.DescribeSpotInstanceRequests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotinstancerequestspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSpotInstanceRequestsRequestDescribeSpotInstanceRequestsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeSpotInstanceRequestsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotInstanceRequests.html#EC2.Paginator.DescribeSpotInstanceRequests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotinstancerequestspaginator)
        """


class DescribeSpotPriceHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotPriceHistory.html#EC2.Paginator.DescribeSpotPriceHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotpricehistorypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeSpotPriceHistoryRequestDescribeSpotPriceHistoryPaginateTypeDef],
    ) -> _PageIterator[DescribeSpotPriceHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSpotPriceHistory.html#EC2.Paginator.DescribeSpotPriceHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describespotpricehistorypaginator)
        """


class DescribeStaleSecurityGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeStaleSecurityGroups.html#EC2.Paginator.DescribeStaleSecurityGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describestalesecuritygroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeStaleSecurityGroupsRequestDescribeStaleSecurityGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeStaleSecurityGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeStaleSecurityGroups.html#EC2.Paginator.DescribeStaleSecurityGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describestalesecuritygroupspaginator)
        """


class DescribeStoreImageTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeStoreImageTasks.html#EC2.Paginator.DescribeStoreImageTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describestoreimagetaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStoreImageTasksRequestDescribeStoreImageTasksPaginateTypeDef]
    ) -> _PageIterator[DescribeStoreImageTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeStoreImageTasks.html#EC2.Paginator.DescribeStoreImageTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describestoreimagetaskspaginator)
        """


class DescribeSubnetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSubnets.html#EC2.Paginator.DescribeSubnets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesubnetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSubnetsRequestDescribeSubnetsPaginateTypeDef]
    ) -> _PageIterator[DescribeSubnetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSubnets.html#EC2.Paginator.DescribeSubnets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describesubnetspaginator)
        """


class DescribeTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTags.html#EC2.Paginator.DescribeTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeTagsRequestDescribeTagsPaginateTypeDef]
    ) -> _PageIterator[DescribeTagsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTags.html#EC2.Paginator.DescribeTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetagspaginator)
        """


class DescribeTrafficMirrorFiltersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrafficMirrorFilters.html#EC2.Paginator.DescribeTrafficMirrorFilters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrafficmirrorfilterspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTrafficMirrorFiltersRequestDescribeTrafficMirrorFiltersPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTrafficMirrorFiltersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrafficMirrorFilters.html#EC2.Paginator.DescribeTrafficMirrorFilters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrafficmirrorfilterspaginator)
        """


class DescribeTrafficMirrorSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrafficMirrorSessions.html#EC2.Paginator.DescribeTrafficMirrorSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrafficmirrorsessionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTrafficMirrorSessionsRequestDescribeTrafficMirrorSessionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTrafficMirrorSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrafficMirrorSessions.html#EC2.Paginator.DescribeTrafficMirrorSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrafficmirrorsessionspaginator)
        """


class DescribeTrafficMirrorTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrafficMirrorTargets.html#EC2.Paginator.DescribeTrafficMirrorTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrafficmirrortargetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTrafficMirrorTargetsRequestDescribeTrafficMirrorTargetsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTrafficMirrorTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrafficMirrorTargets.html#EC2.Paginator.DescribeTrafficMirrorTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrafficmirrortargetspaginator)
        """


class DescribeTransitGatewayAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayAttachments.html#EC2.Paginator.DescribeTransitGatewayAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayattachmentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayAttachmentsRequestDescribeTransitGatewayAttachmentsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayAttachments.html#EC2.Paginator.DescribeTransitGatewayAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayattachmentspaginator)
        """


class DescribeTransitGatewayConnectPeersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayConnectPeers.html#EC2.Paginator.DescribeTransitGatewayConnectPeers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayconnectpeerspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayConnectPeersRequestDescribeTransitGatewayConnectPeersPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayConnectPeersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayConnectPeers.html#EC2.Paginator.DescribeTransitGatewayConnectPeers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayconnectpeerspaginator)
        """


class DescribeTransitGatewayConnectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayConnects.html#EC2.Paginator.DescribeTransitGatewayConnects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayconnectspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayConnectsRequestDescribeTransitGatewayConnectsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayConnectsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayConnects.html#EC2.Paginator.DescribeTransitGatewayConnects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayconnectspaginator)
        """


class DescribeTransitGatewayMulticastDomainsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayMulticastDomains.html#EC2.Paginator.DescribeTransitGatewayMulticastDomains)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewaymulticastdomainspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayMulticastDomainsRequestDescribeTransitGatewayMulticastDomainsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayMulticastDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayMulticastDomains.html#EC2.Paginator.DescribeTransitGatewayMulticastDomains.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewaymulticastdomainspaginator)
        """


class DescribeTransitGatewayPeeringAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayPeeringAttachments.html#EC2.Paginator.DescribeTransitGatewayPeeringAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewaypeeringattachmentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayPeeringAttachmentsRequestDescribeTransitGatewayPeeringAttachmentsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayPeeringAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayPeeringAttachments.html#EC2.Paginator.DescribeTransitGatewayPeeringAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewaypeeringattachmentspaginator)
        """


class DescribeTransitGatewayPolicyTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayPolicyTables.html#EC2.Paginator.DescribeTransitGatewayPolicyTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewaypolicytablespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayPolicyTablesRequestDescribeTransitGatewayPolicyTablesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayPolicyTablesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayPolicyTables.html#EC2.Paginator.DescribeTransitGatewayPolicyTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewaypolicytablespaginator)
        """


class DescribeTransitGatewayRouteTableAnnouncementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayRouteTableAnnouncements.html#EC2.Paginator.DescribeTransitGatewayRouteTableAnnouncements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayroutetableannouncementspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayRouteTableAnnouncementsRequestDescribeTransitGatewayRouteTableAnnouncementsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayRouteTableAnnouncementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayRouteTableAnnouncements.html#EC2.Paginator.DescribeTransitGatewayRouteTableAnnouncements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayroutetableannouncementspaginator)
        """


class DescribeTransitGatewayRouteTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayRouteTables.html#EC2.Paginator.DescribeTransitGatewayRouteTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayroutetablespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayRouteTablesRequestDescribeTransitGatewayRouteTablesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayRouteTablesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayRouteTables.html#EC2.Paginator.DescribeTransitGatewayRouteTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayroutetablespaginator)
        """


class DescribeTransitGatewayVpcAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayVpcAttachments.html#EC2.Paginator.DescribeTransitGatewayVpcAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayvpcattachmentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTransitGatewayVpcAttachmentsRequestDescribeTransitGatewayVpcAttachmentsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTransitGatewayVpcAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayVpcAttachments.html#EC2.Paginator.DescribeTransitGatewayVpcAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayvpcattachmentspaginator)
        """


class DescribeTransitGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGateways.html#EC2.Paginator.DescribeTransitGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeTransitGatewaysRequestDescribeTransitGatewaysPaginateTypeDef]
    ) -> _PageIterator[DescribeTransitGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGateways.html#EC2.Paginator.DescribeTransitGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetransitgatewayspaginator)
        """


class DescribeTrunkInterfaceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrunkInterfaceAssociations.html#EC2.Paginator.DescribeTrunkInterfaceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrunkinterfaceassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTrunkInterfaceAssociationsRequestDescribeTrunkInterfaceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeTrunkInterfaceAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTrunkInterfaceAssociations.html#EC2.Paginator.DescribeTrunkInterfaceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describetrunkinterfaceassociationspaginator)
        """


class DescribeVerifiedAccessEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessEndpoints.html#EC2.Paginator.DescribeVerifiedAccessEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessendpointspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVerifiedAccessEndpointsRequestDescribeVerifiedAccessEndpointsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVerifiedAccessEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessEndpoints.html#EC2.Paginator.DescribeVerifiedAccessEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessendpointspaginator)
        """


class DescribeVerifiedAccessGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessGroups.html#EC2.Paginator.DescribeVerifiedAccessGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessgroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVerifiedAccessGroupsRequestDescribeVerifiedAccessGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVerifiedAccessGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessGroups.html#EC2.Paginator.DescribeVerifiedAccessGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessgroupspaginator)
        """


class DescribeVerifiedAccessInstanceLoggingConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessInstanceLoggingConfigurations.html#EC2.Paginator.DescribeVerifiedAccessInstanceLoggingConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessinstanceloggingconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVerifiedAccessInstanceLoggingConfigurationsRequestDescribeVerifiedAccessInstanceLoggingConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVerifiedAccessInstanceLoggingConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessInstanceLoggingConfigurations.html#EC2.Paginator.DescribeVerifiedAccessInstanceLoggingConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessinstanceloggingconfigurationspaginator)
        """


class DescribeVerifiedAccessInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessInstances.html#EC2.Paginator.DescribeVerifiedAccessInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessinstancespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVerifiedAccessInstancesRequestDescribeVerifiedAccessInstancesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVerifiedAccessInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessInstances.html#EC2.Paginator.DescribeVerifiedAccessInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccessinstancespaginator)
        """


class DescribeVerifiedAccessTrustProvidersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessTrustProviders.html#EC2.Paginator.DescribeVerifiedAccessTrustProviders)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccesstrustproviderspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVerifiedAccessTrustProvidersRequestDescribeVerifiedAccessTrustProvidersPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVerifiedAccessTrustProvidersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVerifiedAccessTrustProviders.html#EC2.Paginator.DescribeVerifiedAccessTrustProviders.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describeverifiedaccesstrustproviderspaginator)
        """


class DescribeVolumeStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVolumeStatus.html#EC2.Paginator.DescribeVolumeStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevolumestatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeVolumeStatusRequestDescribeVolumeStatusPaginateTypeDef]
    ) -> _PageIterator[DescribeVolumeStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVolumeStatus.html#EC2.Paginator.DescribeVolumeStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevolumestatuspaginator)
        """


class DescribeVolumesModificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVolumesModifications.html#EC2.Paginator.DescribeVolumesModifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevolumesmodificationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVolumesModificationsRequestDescribeVolumesModificationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVolumesModificationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVolumesModifications.html#EC2.Paginator.DescribeVolumesModifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevolumesmodificationspaginator)
        """


class DescribeVolumesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVolumes.html#EC2.Paginator.DescribeVolumes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevolumespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeVolumesRequestDescribeVolumesPaginateTypeDef]
    ) -> _PageIterator[DescribeVolumesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVolumes.html#EC2.Paginator.DescribeVolumes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevolumespaginator)
        """


class DescribeVpcClassicLinkDnsSupportPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcClassicLinkDnsSupport.html#EC2.Paginator.DescribeVpcClassicLinkDnsSupport)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcclassiclinkdnssupportpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVpcClassicLinkDnsSupportRequestDescribeVpcClassicLinkDnsSupportPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVpcClassicLinkDnsSupportResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcClassicLinkDnsSupport.html#EC2.Paginator.DescribeVpcClassicLinkDnsSupport.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcclassiclinkdnssupportpaginator)
        """


class DescribeVpcEndpointConnectionNotificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointConnectionNotifications.html#EC2.Paginator.DescribeVpcEndpointConnectionNotifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointconnectionnotificationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVpcEndpointConnectionNotificationsRequestDescribeVpcEndpointConnectionNotificationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVpcEndpointConnectionNotificationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointConnectionNotifications.html#EC2.Paginator.DescribeVpcEndpointConnectionNotifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointconnectionnotificationspaginator)
        """


class DescribeVpcEndpointConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointConnections.html#EC2.Paginator.DescribeVpcEndpointConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointconnectionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVpcEndpointConnectionsRequestDescribeVpcEndpointConnectionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVpcEndpointConnectionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointConnections.html#EC2.Paginator.DescribeVpcEndpointConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointconnectionspaginator)
        """


class DescribeVpcEndpointServiceConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointServiceConfigurations.html#EC2.Paginator.DescribeVpcEndpointServiceConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointserviceconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVpcEndpointServiceConfigurationsRequestDescribeVpcEndpointServiceConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVpcEndpointServiceConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointServiceConfigurations.html#EC2.Paginator.DescribeVpcEndpointServiceConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointserviceconfigurationspaginator)
        """


class DescribeVpcEndpointServicePermissionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointServicePermissions.html#EC2.Paginator.DescribeVpcEndpointServicePermissions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointservicepermissionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVpcEndpointServicePermissionsRequestDescribeVpcEndpointServicePermissionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVpcEndpointServicePermissionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointServicePermissions.html#EC2.Paginator.DescribeVpcEndpointServicePermissions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointservicepermissionspaginator)
        """


class DescribeVpcEndpointServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointServices.html#EC2.Paginator.DescribeVpcEndpointServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointservicespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVpcEndpointServicesRequestDescribeVpcEndpointServicesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVpcEndpointServicesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpointServices.html#EC2.Paginator.DescribeVpcEndpointServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointservicespaginator)
        """


class DescribeVpcEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpoints.html#EC2.Paginator.DescribeVpcEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeVpcEndpointsRequestDescribeVpcEndpointsPaginateTypeDef]
    ) -> _PageIterator[DescribeVpcEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcEndpoints.html#EC2.Paginator.DescribeVpcEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcendpointspaginator)
        """


class DescribeVpcPeeringConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcPeeringConnections.html#EC2.Paginator.DescribeVpcPeeringConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcpeeringconnectionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVpcPeeringConnectionsRequestDescribeVpcPeeringConnectionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVpcPeeringConnectionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcPeeringConnections.html#EC2.Paginator.DescribeVpcPeeringConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcpeeringconnectionspaginator)
        """


class DescribeVpcsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcs.html#EC2.Paginator.DescribeVpcs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeVpcsRequestDescribeVpcsPaginateTypeDef]
    ) -> _PageIterator[DescribeVpcsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeVpcs.html#EC2.Paginator.DescribeVpcs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#describevpcspaginator)
        """


class GetAssociatedIpv6PoolCidrsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetAssociatedIpv6PoolCidrs.html#EC2.Paginator.GetAssociatedIpv6PoolCidrs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getassociatedipv6poolcidrspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetAssociatedIpv6PoolCidrsRequestGetAssociatedIpv6PoolCidrsPaginateTypeDef
        ],
    ) -> _PageIterator[GetAssociatedIpv6PoolCidrsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetAssociatedIpv6PoolCidrs.html#EC2.Paginator.GetAssociatedIpv6PoolCidrs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getassociatedipv6poolcidrspaginator)
        """


class GetAwsNetworkPerformanceDataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetAwsNetworkPerformanceData.html#EC2.Paginator.GetAwsNetworkPerformanceData)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getawsnetworkperformancedatapaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetAwsNetworkPerformanceDataRequestGetAwsNetworkPerformanceDataPaginateTypeDef
        ],
    ) -> _PageIterator[GetAwsNetworkPerformanceDataResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetAwsNetworkPerformanceData.html#EC2.Paginator.GetAwsNetworkPerformanceData.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getawsnetworkperformancedatapaginator)
        """


class GetGroupsForCapacityReservationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetGroupsForCapacityReservation.html#EC2.Paginator.GetGroupsForCapacityReservation)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getgroupsforcapacityreservationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetGroupsForCapacityReservationRequestGetGroupsForCapacityReservationPaginateTypeDef
        ],
    ) -> _PageIterator[GetGroupsForCapacityReservationResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetGroupsForCapacityReservation.html#EC2.Paginator.GetGroupsForCapacityReservation.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getgroupsforcapacityreservationpaginator)
        """


class GetInstanceTypesFromInstanceRequirementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetInstanceTypesFromInstanceRequirements.html#EC2.Paginator.GetInstanceTypesFromInstanceRequirements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getinstancetypesfrominstancerequirementspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetInstanceTypesFromInstanceRequirementsRequestGetInstanceTypesFromInstanceRequirementsPaginateTypeDef
        ],
    ) -> _PageIterator[GetInstanceTypesFromInstanceRequirementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetInstanceTypesFromInstanceRequirements.html#EC2.Paginator.GetInstanceTypesFromInstanceRequirements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getinstancetypesfrominstancerequirementspaginator)
        """


class GetIpamAddressHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamAddressHistory.html#EC2.Paginator.GetIpamAddressHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamaddresshistorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetIpamAddressHistoryRequestGetIpamAddressHistoryPaginateTypeDef]
    ) -> _PageIterator[GetIpamAddressHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamAddressHistory.html#EC2.Paginator.GetIpamAddressHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamaddresshistorypaginator)
        """


class GetIpamDiscoveredAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamDiscoveredAccounts.html#EC2.Paginator.GetIpamDiscoveredAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamdiscoveredaccountspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetIpamDiscoveredAccountsRequestGetIpamDiscoveredAccountsPaginateTypeDef],
    ) -> _PageIterator[GetIpamDiscoveredAccountsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamDiscoveredAccounts.html#EC2.Paginator.GetIpamDiscoveredAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamdiscoveredaccountspaginator)
        """


class GetIpamDiscoveredResourceCidrsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamDiscoveredResourceCidrs.html#EC2.Paginator.GetIpamDiscoveredResourceCidrs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamdiscoveredresourcecidrspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetIpamDiscoveredResourceCidrsRequestGetIpamDiscoveredResourceCidrsPaginateTypeDef
        ],
    ) -> _PageIterator[GetIpamDiscoveredResourceCidrsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamDiscoveredResourceCidrs.html#EC2.Paginator.GetIpamDiscoveredResourceCidrs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamdiscoveredresourcecidrspaginator)
        """


class GetIpamPoolAllocationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamPoolAllocations.html#EC2.Paginator.GetIpamPoolAllocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipampoolallocationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetIpamPoolAllocationsRequestGetIpamPoolAllocationsPaginateTypeDef]
    ) -> _PageIterator[GetIpamPoolAllocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamPoolAllocations.html#EC2.Paginator.GetIpamPoolAllocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipampoolallocationspaginator)
        """


class GetIpamPoolCidrsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamPoolCidrs.html#EC2.Paginator.GetIpamPoolCidrs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipampoolcidrspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetIpamPoolCidrsRequestGetIpamPoolCidrsPaginateTypeDef]
    ) -> _PageIterator[GetIpamPoolCidrsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamPoolCidrs.html#EC2.Paginator.GetIpamPoolCidrs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipampoolcidrspaginator)
        """


class GetIpamResourceCidrsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamResourceCidrs.html#EC2.Paginator.GetIpamResourceCidrs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamresourcecidrspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetIpamResourceCidrsRequestGetIpamResourceCidrsPaginateTypeDef]
    ) -> _PageIterator[GetIpamResourceCidrsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetIpamResourceCidrs.html#EC2.Paginator.GetIpamResourceCidrs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getipamresourcecidrspaginator)
        """


class GetManagedPrefixListAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetManagedPrefixListAssociations.html#EC2.Paginator.GetManagedPrefixListAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getmanagedprefixlistassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetManagedPrefixListAssociationsRequestGetManagedPrefixListAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetManagedPrefixListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetManagedPrefixListAssociations.html#EC2.Paginator.GetManagedPrefixListAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getmanagedprefixlistassociationspaginator)
        """


class GetManagedPrefixListEntriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetManagedPrefixListEntries.html#EC2.Paginator.GetManagedPrefixListEntries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getmanagedprefixlistentriespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetManagedPrefixListEntriesRequestGetManagedPrefixListEntriesPaginateTypeDef
        ],
    ) -> _PageIterator[GetManagedPrefixListEntriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetManagedPrefixListEntries.html#EC2.Paginator.GetManagedPrefixListEntries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getmanagedprefixlistentriespaginator)
        """


class GetNetworkInsightsAccessScopeAnalysisFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetNetworkInsightsAccessScopeAnalysisFindings.html#EC2.Paginator.GetNetworkInsightsAccessScopeAnalysisFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getnetworkinsightsaccessscopeanalysisfindingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetNetworkInsightsAccessScopeAnalysisFindingsRequestGetNetworkInsightsAccessScopeAnalysisFindingsPaginateTypeDef
        ],
    ) -> _PageIterator[GetNetworkInsightsAccessScopeAnalysisFindingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetNetworkInsightsAccessScopeAnalysisFindings.html#EC2.Paginator.GetNetworkInsightsAccessScopeAnalysisFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getnetworkinsightsaccessscopeanalysisfindingspaginator)
        """


class GetSecurityGroupsForVpcPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetSecurityGroupsForVpc.html#EC2.Paginator.GetSecurityGroupsForVpc)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getsecuritygroupsforvpcpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetSecurityGroupsForVpcRequestGetSecurityGroupsForVpcPaginateTypeDef]
    ) -> _PageIterator[GetSecurityGroupsForVpcResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetSecurityGroupsForVpc.html#EC2.Paginator.GetSecurityGroupsForVpc.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getsecuritygroupsforvpcpaginator)
        """


class GetSpotPlacementScoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetSpotPlacementScores.html#EC2.Paginator.GetSpotPlacementScores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getspotplacementscorespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetSpotPlacementScoresRequestGetSpotPlacementScoresPaginateTypeDef]
    ) -> _PageIterator[GetSpotPlacementScoresResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetSpotPlacementScores.html#EC2.Paginator.GetSpotPlacementScores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getspotplacementscorespaginator)
        """


class GetTransitGatewayAttachmentPropagationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayAttachmentPropagations.html#EC2.Paginator.GetTransitGatewayAttachmentPropagations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayattachmentpropagationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayAttachmentPropagationsRequestGetTransitGatewayAttachmentPropagationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayAttachmentPropagationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayAttachmentPropagations.html#EC2.Paginator.GetTransitGatewayAttachmentPropagations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayattachmentpropagationspaginator)
        """


class GetTransitGatewayMulticastDomainAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayMulticastDomainAssociations.html#EC2.Paginator.GetTransitGatewayMulticastDomainAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewaymulticastdomainassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayMulticastDomainAssociationsRequestGetTransitGatewayMulticastDomainAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayMulticastDomainAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayMulticastDomainAssociations.html#EC2.Paginator.GetTransitGatewayMulticastDomainAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewaymulticastdomainassociationspaginator)
        """


class GetTransitGatewayPolicyTableAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayPolicyTableAssociations.html#EC2.Paginator.GetTransitGatewayPolicyTableAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewaypolicytableassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayPolicyTableAssociationsRequestGetTransitGatewayPolicyTableAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayPolicyTableAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayPolicyTableAssociations.html#EC2.Paginator.GetTransitGatewayPolicyTableAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewaypolicytableassociationspaginator)
        """


class GetTransitGatewayPrefixListReferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayPrefixListReferences.html#EC2.Paginator.GetTransitGatewayPrefixListReferences)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayprefixlistreferencespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayPrefixListReferencesRequestGetTransitGatewayPrefixListReferencesPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayPrefixListReferencesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayPrefixListReferences.html#EC2.Paginator.GetTransitGatewayPrefixListReferences.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayprefixlistreferencespaginator)
        """


class GetTransitGatewayRouteTableAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayRouteTableAssociations.html#EC2.Paginator.GetTransitGatewayRouteTableAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayroutetableassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayRouteTableAssociationsRequestGetTransitGatewayRouteTableAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayRouteTableAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayRouteTableAssociations.html#EC2.Paginator.GetTransitGatewayRouteTableAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayroutetableassociationspaginator)
        """


class GetTransitGatewayRouteTablePropagationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayRouteTablePropagations.html#EC2.Paginator.GetTransitGatewayRouteTablePropagations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayroutetablepropagationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetTransitGatewayRouteTablePropagationsRequestGetTransitGatewayRouteTablePropagationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetTransitGatewayRouteTablePropagationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayRouteTablePropagations.html#EC2.Paginator.GetTransitGatewayRouteTablePropagations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#gettransitgatewayroutetablepropagationspaginator)
        """


class GetVpnConnectionDeviceTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetVpnConnectionDeviceTypes.html#EC2.Paginator.GetVpnConnectionDeviceTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getvpnconnectiondevicetypespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetVpnConnectionDeviceTypesRequestGetVpnConnectionDeviceTypesPaginateTypeDef
        ],
    ) -> _PageIterator[GetVpnConnectionDeviceTypesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetVpnConnectionDeviceTypes.html#EC2.Paginator.GetVpnConnectionDeviceTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#getvpnconnectiondevicetypespaginator)
        """


class ListImagesInRecycleBinPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/ListImagesInRecycleBin.html#EC2.Paginator.ListImagesInRecycleBin)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#listimagesinrecyclebinpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImagesInRecycleBinRequestListImagesInRecycleBinPaginateTypeDef]
    ) -> _PageIterator[ListImagesInRecycleBinResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/ListImagesInRecycleBin.html#EC2.Paginator.ListImagesInRecycleBin.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#listimagesinrecyclebinpaginator)
        """


class ListSnapshotsInRecycleBinPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/ListSnapshotsInRecycleBin.html#EC2.Paginator.ListSnapshotsInRecycleBin)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#listsnapshotsinrecyclebinpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSnapshotsInRecycleBinRequestListSnapshotsInRecycleBinPaginateTypeDef],
    ) -> _PageIterator[ListSnapshotsInRecycleBinResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/ListSnapshotsInRecycleBin.html#EC2.Paginator.ListSnapshotsInRecycleBin.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#listsnapshotsinrecyclebinpaginator)
        """


class SearchLocalGatewayRoutesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/SearchLocalGatewayRoutes.html#EC2.Paginator.SearchLocalGatewayRoutes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#searchlocalgatewayroutespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[SearchLocalGatewayRoutesRequestSearchLocalGatewayRoutesPaginateTypeDef],
    ) -> _PageIterator[SearchLocalGatewayRoutesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/SearchLocalGatewayRoutes.html#EC2.Paginator.SearchLocalGatewayRoutes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#searchlocalgatewayroutespaginator)
        """


class SearchTransitGatewayMulticastGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/SearchTransitGatewayMulticastGroups.html#EC2.Paginator.SearchTransitGatewayMulticastGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#searchtransitgatewaymulticastgroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            SearchTransitGatewayMulticastGroupsRequestSearchTransitGatewayMulticastGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[SearchTransitGatewayMulticastGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/SearchTransitGatewayMulticastGroups.html#EC2.Paginator.SearchTransitGatewayMulticastGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/paginators/#searchtransitgatewaymulticastgroupspaginator)
        """

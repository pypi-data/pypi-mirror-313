import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-digitalocean",
    "version": "11.11.0",
    "description": "Prebuilt digitalocean Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-digitalocean.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-digitalocean.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_digitalocean",
        "cdktf_cdktf_provider_digitalocean._jsii",
        "cdktf_cdktf_provider_digitalocean.app",
        "cdktf_cdktf_provider_digitalocean.cdn",
        "cdktf_cdktf_provider_digitalocean.certificate",
        "cdktf_cdktf_provider_digitalocean.container_registry",
        "cdktf_cdktf_provider_digitalocean.container_registry_docker_credentials",
        "cdktf_cdktf_provider_digitalocean.custom_image",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_account",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_app",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_certificate",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_container_registry",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_database_ca",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_database_cluster",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_database_connection_pool",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_database_replica",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_database_user",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_domain",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_domains",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_droplet",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_droplet_snapshot",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_droplets",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_firewall",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_floating_ip",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_image",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_images",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_kubernetes_cluster",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_kubernetes_versions",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_loadbalancer",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_project",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_projects",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_record",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_records",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_region",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_regions",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_reserved_ip",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_sizes",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_spaces_bucket",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_spaces_bucket_object",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_spaces_bucket_objects",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_spaces_buckets",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_ssh_key",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_ssh_keys",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_tag",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_tags",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_volume",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_volume_snapshot",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_vpc",
        "cdktf_cdktf_provider_digitalocean.data_digitalocean_vpc_peering",
        "cdktf_cdktf_provider_digitalocean.database_cluster",
        "cdktf_cdktf_provider_digitalocean.database_connection_pool",
        "cdktf_cdktf_provider_digitalocean.database_db",
        "cdktf_cdktf_provider_digitalocean.database_firewall",
        "cdktf_cdktf_provider_digitalocean.database_kafka_config",
        "cdktf_cdktf_provider_digitalocean.database_kafka_topic",
        "cdktf_cdktf_provider_digitalocean.database_mongodb_config",
        "cdktf_cdktf_provider_digitalocean.database_mysql_config",
        "cdktf_cdktf_provider_digitalocean.database_opensearch_config",
        "cdktf_cdktf_provider_digitalocean.database_postgresql_config",
        "cdktf_cdktf_provider_digitalocean.database_redis_config",
        "cdktf_cdktf_provider_digitalocean.database_replica",
        "cdktf_cdktf_provider_digitalocean.database_user",
        "cdktf_cdktf_provider_digitalocean.domain",
        "cdktf_cdktf_provider_digitalocean.droplet",
        "cdktf_cdktf_provider_digitalocean.droplet_snapshot",
        "cdktf_cdktf_provider_digitalocean.firewall",
        "cdktf_cdktf_provider_digitalocean.floating_ip",
        "cdktf_cdktf_provider_digitalocean.floating_ip_assignment",
        "cdktf_cdktf_provider_digitalocean.kubernetes_cluster",
        "cdktf_cdktf_provider_digitalocean.kubernetes_node_pool",
        "cdktf_cdktf_provider_digitalocean.loadbalancer",
        "cdktf_cdktf_provider_digitalocean.monitor_alert",
        "cdktf_cdktf_provider_digitalocean.project",
        "cdktf_cdktf_provider_digitalocean.project_resources",
        "cdktf_cdktf_provider_digitalocean.provider",
        "cdktf_cdktf_provider_digitalocean.record",
        "cdktf_cdktf_provider_digitalocean.reserved_ip",
        "cdktf_cdktf_provider_digitalocean.reserved_ip_assignment",
        "cdktf_cdktf_provider_digitalocean.spaces_bucket",
        "cdktf_cdktf_provider_digitalocean.spaces_bucket_cors_configuration",
        "cdktf_cdktf_provider_digitalocean.spaces_bucket_object",
        "cdktf_cdktf_provider_digitalocean.spaces_bucket_policy",
        "cdktf_cdktf_provider_digitalocean.ssh_key",
        "cdktf_cdktf_provider_digitalocean.tag",
        "cdktf_cdktf_provider_digitalocean.uptime_alert",
        "cdktf_cdktf_provider_digitalocean.uptime_check",
        "cdktf_cdktf_provider_digitalocean.volume",
        "cdktf_cdktf_provider_digitalocean.volume_attachment",
        "cdktf_cdktf_provider_digitalocean.volume_snapshot",
        "cdktf_cdktf_provider_digitalocean.vpc",
        "cdktf_cdktf_provider_digitalocean.vpc_peering"
    ],
    "package_data": {
        "cdktf_cdktf_provider_digitalocean._jsii": [
            "provider-digitalocean@11.11.0.jsii.tgz"
        ],
        "cdktf_cdktf_provider_digitalocean": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf>=0.20.0, <0.21.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.105.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)

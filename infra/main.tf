# Terraform provider setup
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-azure-poc"
  location = "East US 2"
}

# VNet and Subnets
module "network" {
  source              = "Azure/network/azurerm"
  resource_group_name = azurerm_resource_group.rg.name
  vnet_name           = "poc-vnet"
  address_space       = "10.0.0.0/16"
  subnet_prefixes     = ["10.0.1.0/24", "10.0.2.0/24"]
  subnet_names        = ["public-subnet", "private-subnet"]
  use_for_each        = true
}

# Add delegation to the private subnet (index 1)
resource "azurerm_subnet" "delegated_private_subnet" {
  name                 = "private-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = module.network.vnet_name
  address_prefixes     = ["10.0.2.0/24"]

  delegation {
    name = "mysqlDelegation"
    service_delegation {
      name    = "Microsoft.DBforMySQL/flexibleServers"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }

  depends_on = [module.network]
}

# MySQL Flexible Server
resource "azurerm_mysql_flexible_server" "mysql" {
  name                   = "mysql-poc-server"
  location               = azurerm_resource_group.rg.location
  resource_group_name    = azurerm_resource_group.rg.name
  administrator_login    = "mysqladmin"
  administrator_password = "ChangeThisPassword123!"
  version                = "8.0.21"
  sku_name               = "B_Standard_B1ms"
  zone                   = "1"

  delegated_subnet_id = azurerm_subnet.delegated_private_subnet.id

  storage {
    size_gb = 32
  }

  high_availability {
    mode = "ZoneRedundant"
  }

  depends_on = [azurerm_subnet.delegated_private_subnet]
}

# Key Vault
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = "pockeyvault123"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  purge_protection_enabled    = true
  soft_delete_retention_days  = 7
}

# MySQL Connection Secret in Key Vault
resource "azurerm_key_vault_secret" "mysql_password" {
  name         = "mysql-password"
  value        = azurerm_mysql_flexible_server.mysql.administrator_password
  key_vault_id = azurerm_key_vault.kv.id
}

# Private DNS Zone for MySQL
resource "azurerm_private_dns_zone" "mysql" {
  name                = "privatelink.mysql.database.azure.com"
  resource_group_name = azurerm_resource_group.rg.name
}

# Private Endpoint for MySQL
resource "azurerm_private_endpoint" "mysql" {
  name                = "mysql-private-endpoint"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.delegated_private_subnet.id

  private_service_connection {
    name                           = "mysql-service-connection"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_mysql_flexible_server.mysql.id
    subresource_names              = ["mysqlServer"]
  }
}

# Output MySQL connection information
output "mysql_fqdn" {
  value = azurerm_mysql_flexible_server.mysql.fqdn
}

output "mysql_password" {
  value     = azurerm_key_vault_secret.mysql_password.value
  sensitive = true
}

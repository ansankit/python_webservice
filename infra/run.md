terraform init
terrafrom validate
terraform plan -out=tfplan 
terraform import azurerm_resource_group.rg /subscriptions/1f1f121f-4446-4ab6-933a-eefc118be151/resourceGroups/rg-azure-poc
terraform apply tfplan
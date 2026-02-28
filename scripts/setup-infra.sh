#!/bin/bash
set -e

echo "=== Infrastructure Setup Script ==="

TERRAFORM_DIR="infrastructure/terraform"

cd "$TERRAFORM_DIR" || exit 1

if [ ! -f ".terraform.lock.hcl" ]; then
    echo "Initializing Terraform..."
    terraform init
fi

echo "Validating Terraform configuration..."
terraform validate

echo "Planning infrastructure changes..."
terraform plan -var-file="terraform.tfvars" -out=tfplan

echo "Applying infrastructure..."
terraform apply tfplan

echo "Infrastructure setup complete!"
terraform output

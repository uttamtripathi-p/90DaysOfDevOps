# Day 63 — Variables, Outputs, Data Sources & Locals

---

## 1. variables.tf — All Variable Types

```hcl
variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "subnet_cidr" {
  type    = string
  default = "10.0.1.0/24"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "project_name" {
  type = string
  # No default — Terraform will prompt for this
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "allowed_ports" {
  type    = list(number)
  default = [22, 80, 443]
}

variable "extra_tags" {
  type    = map(string)
  default = {}
}
```

---

## 2. Variable Files

**terraform.tfvars** (loaded automatically):
```hcl
project_name  = "terraweek"
environment   = "dev"
instance_type = "t2.micro"
```

**prod.tfvars** (loaded with `-var-file="prod.tfvars"`):
```hcl
project_name  = "terraweek"
environment   = "prod"
instance_type = "t3.small"
vpc_cidr      = "10.1.0.0/16"
subnet_cidr   = "10.1.1.0/24"
```

---

## 3. Outputs After `terraform apply`

```
Outputs:

vpc_id               = "vpc-0abc123def456"
subnet_id            = "subnet-0def456abc789"
instance_id          = "i-0a1b2c3d4e5f6"
instance_public_ip   = "13.233.xx.xx"
instance_public_dns  = "ec2-13-233-xx-xx.ap-south-1.compute.amazonaws.com"
security_group_id    = "sg-0123456789abcdef"
```

> Run `terraform output instance_public_ip` to fetch a specific value.
> Run `terraform output -json` for script-friendly JSON format.

---

## 4. Variable Precedence — Lowest to Highest

| Priority | Source | Example |
|---|---|---|
| 1 (lowest) | Default in `variables.tf` | `default = "t2.micro"` |
| 2 | `terraform.tfvars` | Auto-loaded by Terraform |
| 3 | `*.auto.tfvars` | Any file ending in `.auto.tfvars` |
| 4 | `-var-file` flag | `terraform plan -var-file="prod.tfvars"` |
| 5 | `-var` flag | `terraform plan -var="instance_type=t2.nano"` |
| 6 (highest) | `TF_VAR_*` env var | `export TF_VAR_environment="staging"` |

**In plain terms:** CLI flags beat `.tfvars` files, which beat defaults. Environment variables sit above defaults but below explicit file/flag overrides.

---

## 5. Five Most Useful Built-in Functions

### `merge(map1, map2)`
Combines two maps into one. Last key wins on conflict.
```hcl
tags = merge(local.common_tags, { Name = "my-server" })
```
Best for applying common tags across all resources without repeating them.

### `cidrsubnet(prefix, newbits, netnum)`
Calculates a subnet CIDR from a parent block.
```hcl
cidrsubnet("10.0.0.0/16", 8, 1) # → "10.0.1.0/24"
```
Eliminates manual subnet math — pair with `count` to auto-generate multiple subnets.

### `lookup(map, key, default)`
Fetches a value from a map by key, with a safe fallback.
```hcl
lookup({ dev = "t2.micro", prod = "t3.small" }, var.environment, "t2.micro")
```
Cleaner than long conditional chains when mapping environments to values.

### `toset(list)`
Converts a list to a set, removing duplicates.
```hcl
toset(["ap-south-1a", "ap-south-1b", "ap-south-1a"]) # → {"ap-south-1a", "ap-south-1b"}
```
Required when using `for_each`, which only accepts sets or maps — not lists.

### `templatefile(path, vars)`
Reads an external file and interpolates variables into it.
```hcl
user_data = templatefile("scripts/setup.sh.tpl", {
  environment = var.environment
  db_host     = aws_db_instance.main.address
})
```
Keeps large scripts out of `.tf` files while keeping them dynamic.

---

## 6. Variable vs Local vs Output vs Data

### `variable`
An **input** to your configuration — provided by the user at runtime via `.tfvars`, CLI flags, or env vars.
```hcl
variable "environment" {
  type    = string
  default = "dev"
}
```
> Think of it as a function parameter — it comes from outside.

---

### `local`
A **computed value** defined inside your config for reuse. Not exposed to the user.
```hcl
locals {
  name_prefix = "${var.project_name}-${var.environment}"
}
```
> Think of it as a local variable inside a function — internal use only.

---

### `output`
An **exported value** printed after `terraform apply` and accessible via `terraform output`. Used to pass values to other configs or scripts.
```hcl
output "instance_public_ip" {
  value = aws_instance.main.public_ip
}
```
> Think of it as a function's return value — it comes out of the config.

---

### `data`
A **read-only lookup** of existing infrastructure. Terraform fetches it but never creates, modifies, or destroys it.
```hcl
data "aws_ami" "main" {
  most_recent = true
  owners      = ["amazon"]
}
```
> Think of it as a query — you're asking AWS for information, not telling it to do anything.

---

| Concept | Direction | Owned by Terraform? | Use Case |
|---|---|---|---|
| `variable` | Into config | No | User-provided inputs |
| `local` | Internal | No | Reusable computed values |
| `output` | Out of config | No | Expose values after apply |
| `data` | Into config | No | Read existing infrastructure |

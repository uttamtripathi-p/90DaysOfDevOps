# How many resources does Terraform track?
## Terraform only tracks what it created. Anything you made manually in the AWS console is invisible to Terraform unless you explicitly import it with terraform import.
# What attributes does the state store for an EC2 instance? (hint: way more than what you defined)
## Terraform stores everything AWS returns about the resource, not just what you wrote in your config.

# Day 64 — Terraform State Management and Remote Backends

## Local vs Remote State

Local state lives on your laptop — one deleted file and Terraform forgets everything. Remote state on S3 is safe, shared, and locked.

```
Local → terraform.tfstate on laptop (risky)
Remote → S3 bucket + DynamoDB locking (production-ready)
```

---

## Remote Backend Setup

```hcl
terraform {
  backend "s3" {
    bucket         = "terraweek-state-uttam"
    key            = "dev/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraweek-state-lock"
    encrypt        = true
  }
}
```

`terraform init` migrated local state to S3. State file visible at `terraweek-state-uttam/dev/terraform.tfstate` (28.3 KB).

<!-- Screenshot: state file in S3 console -->

---

## State Locking

Running `terraform plan` in Terminal 2 while Terminal 1 had an active apply showed:

```
Error: Error acquiring the state lock
Lock Info:
  ID:        97953684-3a0c-837b-ec00-da544df0b67e
  Operation: OperationTypeApply
  Who:       dell-2004@Uttam-Pc
```

<!-- Screenshot: lock error -->

DynamoDB prevents two operations from writing state simultaneously. Release a stale lock with `terraform force-unlock <ID>`.

---

## Terraform Import

Manually created `terraweek-import-test-uttam` in AWS console, then:

```bash
terraform import aws_s3_bucket.logs_bucket terraweek-import-test-uttam
terraform plan  # No changes — import matched config perfectly
```

Import brings existing AWS resources under Terraform management without recreating them.

---

## State Surgery

```bash
terraform state mv aws_s3_bucket.imported aws_s3_bucket.logs_bucket  # rename
terraform state rm aws_s3_bucket.logs_bucket                          # stop tracking
terraform import aws_s3_bucket.logs_bucket terraweek-import-test-uttam # re-import
```

Use `state mv` when refactoring resource names. Use `state rm` when handing a resource to another team.

---

## Drift Simulation

Manually removed the `day` tag from EC2 in AWS console. `terraform plan` detected:

```
~ tags = {
  - "day" = "64" -> null
}
Plan: 0 to add, 1 to change, 0 to destroy.
```

<!-- Screenshot: drift plan output -->

`terraform apply` restored the tag. **No changes** on next plan.

---

## Command Reference

| Command | Purpose |
|---|---|
| `terraform state list` | List all tracked resources |
| `terraform state mv` | Rename resource in state |
| `terraform state rm` | Remove from state (keeps AWS resource) |
| `terraform import` | Import existing resource into state |
| `terraform force-unlock` | Release stuck lock |
| `terraform apply -refresh-only` | Sync state to reality without changes |

---

*#90DaysOfDevOps #TerraWeek #TrainWithShubham*

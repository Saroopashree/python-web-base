locals {
  cluster_name = "todo-application"
}

module "vpc" {
  source = "git::https://git@github.com/reactiveops/terraform-vpc.git?ref=v5.0.1"

  aws_region = "us-east-1"
  az_count   = 2
  aws_azs    = "us-east-1a, us-east-1b"

  global_tags = {
    "purpose"       = "eks"
    "resource_name" = "${local.cluster_name}"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"

  cluster_name = local.cluster_name

  cluster_endpoint_public_access = true

  vpc_id     = module.vpc.aws_vpc_id
  subnet_ids = module.vpc.aws_subnet_private_prod_ids

  eks_managed_node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 2
      min_capaicty     = 2

      instance_type = "t3.medium"
    }
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  name_regex  = "al2023-.*-x86_64"
}

resource "aws_instance" "sandbox_compute" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnet_ids[0]

  vpc_security_group_ids = [aws_security_group.compute_sg.id]

  key_name = "sandbox-key"

  tags = {
    Name        = "${var.environment}-compute"
    Environment = var.environment
    Project     = "infrastructure"
  }
}

resource "aws_key_pair" "sandbox_key" {
  key_name   = "sandbox-key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC placeholder-key-for-sandbox"
}

provider "aws" {
    region = "us-east-1" #  Specifies the AWS region where all resources will be created. Here, "us-east-1" is selected.
}

# Creation of ec2 instance
resource "aws_instance" "parsenimbus_instance" { 
    ami ="ami-0866a3c8686eaeeba" # Amazon Machine Image of Ubuntu to launch ec2 instance.
    instance_type = "t2.micro"  # Selecting t2.micro as the instance type, it is free-tier eligible.
    key_name = "ec2_parsenimbus_KP" # The key pair name used to securely ssh into the ec2 instance.
    vpc_security_group_ids = ["sg-058d2104aa47f4ad3"] # The security group to control traffic for the ec2 instance
    tags = {
      Name = "ParseNimbus" # Tags the EC2 instance with a name for easier identification, here 'ParseNimbus'
    }
}

# Creation of s3 bucket
resource "aws_s3_bucket" "parsenimbus_s3_bucket" { 
  bucket = "parsenimbus-s3-bucket-2184" # Defines the S3 bucket name to store data and documents. The name must be unique globally, here 'parsenimbus-s3-bucket-2184'
}

resource "aws_secretsmanager_secret" "api_credentials" {
  name        = "api_credentials_2184" #Specifies a unique name for the secret to store sensitive data like API credentials.
  description = "API credentials for document processing." # Describes the purpose of this secret for better understanding and use of it.
}

resource "aws_sqs_queue" "document_queue" {
  name = "document-processing-queue_2184" ## Defines the name for the SQS queue to handle messages related to document processing.
}
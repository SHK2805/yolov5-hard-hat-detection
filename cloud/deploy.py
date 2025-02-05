import subprocess
import boto3

region = 'us-east-1'
stack_name = 'dev-stack'
sg_group_name = 'dev-sg-ec2'
bucket_name = 'dev-stack-cv-bucket-0123456789'

class CloudFormationManager:
    def __init__(self, region_name):
        self.cf_client = boto3.client('cloudformation', region_name=region_name)
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.logs_client = boto3.client('logs', region_name=region_name)
        self.ssm_client = boto3.client('ssm', region_name=region_name)
        self.ecr_client = boto3.client('ecr', region_name=region_name)
        self.stack_name = stack_name

    def get_default_vpc_id(self):
        response = self.ec2_client.describe_vpcs(
            Filters=[{'Name': 'isDefault', 'Values': ['true']}]
        )
        return response['Vpcs'][0]['VpcId'] if response['Vpcs'] else None

    def stack_exists(self):
        stacks = self.cf_client.list_stacks(
            StackStatusFilter=[
                'CREATE_IN_PROGRESS', 'CREATE_FAILED', 'CREATE_COMPLETE',
                'ROLLBACK_IN_PROGRESS', 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE',
                'DELETE_FAILED', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
                'UPDATE_COMPLETE', 'UPDATE_FAILED', 'UPDATE_ROLLBACK_IN_PROGRESS',
                'UPDATE_ROLLBACK_FAILED', 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
                'UPDATE_ROLLBACK_COMPLETE', 'REVIEW_IN_PROGRESS', 'IMPORT_IN_PROGRESS',
                'IMPORT_COMPLETE', 'IMPORT_ROLLBACK_IN_PROGRESS', 'IMPORT_ROLLBACK_FAILED',
                'IMPORT_ROLLBACK_COMPLETE'
            ]
        )
        for stack in stacks['StackSummaries']:
            if stack['StackName'] == self.stack_name:
                return True
        return False

    def create_stack(self, template_body, default_vpc_id):
        if self.stack_exists():
            print(f"Stack {self.stack_name} already exists. Skipping creation.")
            return

        print(f"Stack {self.stack_name} does NOT exist. Starting creation.")
        template_body = template_body.replace('!Ref DefaultVpcId', default_vpc_id)
        try:
            response = self.cf_client.create_stack(
                StackName=self.stack_name,
                TemplateBody=template_body,
                Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM']
            )
            print(f"Creating {self.stack_name} stack...")
            waiter = self.cf_client.get_waiter('stack_create_complete')
            waiter.wait(StackName=self.stack_name)
            print(f"Stack {self.stack_name} created successfully.")
            self.print_stack_outputs()
        except Exception as e:
            print(f"Error creating stack {self.stack_name}: {e}")

    def delete_stack(self):
        try:
            response = self.cf_client.delete_stack(StackName=self.stack_name)
            print(f"Deleting {self.stack_name} stack...")
            waiter = self.cf_client.get_waiter('stack_delete_complete')
            waiter.wait(StackName=self.stack_name)
            print(f"Stack {self.stack_name} deleted successfully.")
            self.delete_log_groups()
        except Exception as e:
            print(f"Error deleting stack: {e}")

    def delete_log_groups(self):
        try:
            log_groups = self.logs_client.describe_log_groups(
                logGroupNamePrefix=self.stack_name
            )
            for log_group in log_groups['logGroups']:
                log_group_name = log_group['logGroupName']
                self.logs_client.delete_log_group(logGroupName=log_group_name)
                print(f"Deleted log group: {log_group_name}")
        except Exception as e:
            print(f"Error deleting log groups: {e}")

    def print_stack_outputs(self):
        try:
            response = self.cf_client.describe_stacks(StackName=self.stack_name)
            stack = response['Stacks'][0]
            outputs = stack.get('Outputs', [])
            for output in outputs:
                print(f"{output['OutputKey']}: {output['OutputValue']}")
        except Exception as e:
            print(f"Error retrieving stack outputs: {e}")

    def upload_file(self, bucket_name, file_path, object_name):
        try:
            response = self.s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"File {file_path} uploaded to {bucket_name}/{object_name} successfully.")
        except Exception as e:
            print(f"Error uploading file to bucket: {e}")

    def execute_command_on_instance(self, instance_id, commands):
        try:
            response = self.ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName='AWS-RunShellScript',
                Parameters={'commands': commands}
            )
            command_id = response['Command']['CommandId']
            print(f"Executed command on instance {instance_id} with Command ID: {command_id}")
        except Exception as e:
            print(f"Error executing command on instance: {e}")

    def build_and_push_docker_image(self, image_name, ecr_repo_name):
        try:
            # Retrieve the ECR repository URI from CloudFormation stack outputs
            response = self.cf_client.describe_stacks(StackName=self.stack_name)
            ecr_repo_url = [output['OutputValue'] for output in response['Stacks'][0]['Outputs'] if output['OutputKey'] == 'MyECRRepositoryUri'][0]

            subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
            subprocess.run(["docker", "tag", f"{image_name}:latest", f"{ecr_repo_url}:latest"], check=True)
            subprocess.run(["aws", "ecr", "get-login-password", "--region", region], check=True)
            subprocess.run(["docker", "login", "--username", "AWS", "--password-stdin", ecr_repo_url], check=True)
            subprocess.run(["docker", "push", f"{ecr_repo_url}:latest"], check=True)
            print("Docker image built and pushed to ECR successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error building and pushing Docker image: {e}")

# Main function
def main():
    with open('cloudformation_template.yaml', 'r') as template_file:
        template_body = template_file.read()

    cf_manager = CloudFormationManager(region)
    default_vpc_id = cf_manager.get_default_vpc_id()

    if default_vpc_id:
        cf_manager.create_stack(template_body, default_vpc_id)
        # Docker build and push
        cf_manager.build_and_push_docker_image('your-image-name', 'your-ecr-repo')
        # Get the EC2 instance ID from the stack outputs
        response = cf_manager.cf_client.describe_stacks(StackName=stack_name)
        instance_id = [output['OutputValue'] for output in response['Stacks'][0]['Outputs'] if output['OutputKey'] == 'EC2InstanceId'][0]
        # Execute Docker run command on EC2 instance
        commands = [
            'sudo docker pull your-aws-account-id.dkr.ecr.us-east-1.amazonaws.com/your-ecr-repo:latest',
            'sudo docker-compose up -d'
        ]
        cf_manager.execute_command_on_instance(instance_id, commands)
        # Uncomment the line below to delete the stack
        # cf_manager.delete_stack()
    else:
        print("No default VPC found. Stack creation aborted.")

if __name__ == "__main__":
    main()

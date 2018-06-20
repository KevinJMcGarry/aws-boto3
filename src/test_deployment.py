# Script for creating a VPC
# works hand in hand with the vpc class in /src/ec2/vpc.py

from src.ec2.vpc import VPC  # importing the vpc class from the vpc file
from src.client_locator import EC2Client  # importing the ec2 client


def main():
    # Create a VPC
    # get ec2 client so that we can pass it into our vpc class
    ec2_client = EC2Client().get_client()
    # now get the vpc class and pass in the ec2_client
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc('10.221.0.0/16')  # creates a dictionary response

    print(f"VPC Created: {vpc_response}")

    # Add Name Tag to the VPC
    vpc_name = "Boto3-VPC"
    vpc_id = vpc_response['Vpc']['VpcId']  # extracting the vpcid value from the dict
    vpc.add_name_tag(vpc_id, vpc_name)

    print(f"Added {vpc_name} to {vpc_id}")

    # Create an IGW
    igw_response = vpc.create_internet_gateway()

    # need to get IGW ID to attach it to the VPC
    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    # now attach it to our VPC
    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    # create a public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.221.1.0/24')
    print(f"subnet created created for {vpc_id}: {public_subnet_response}")

    # Were going to use the default created VPC route table for the private subnet
    # and now create a new route table for the public subnet just created
    public_route_table_response = vpc.create_public_route_table(vpc_id)

    # to get the RouteTableID - see create_inernet_gateway boto3 documentation
    rtb_id = public_route_table_response['RouteTable']['RouteTableId']
    # to get SubnetId of the subnet created - see create_subnet boto3 documentation
    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    # add name tag to public subnet
    vpc.add_name_tag(public_subnet_id, "Boto3 Public Subnet")

    # adding the IGW to the public route table (the IGW has already been attached to the vpc)
    vpc.create_igw_route_for_public_route_table(rtb_id, igw_id)

    # associate subnet (public or private) with route table just created
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)

    # allow auto-assign of public ip addresses to instances in the public subnet
    vpc.allow_auto_assign_publicip_for_public_subnet(public_subnet_id)

    # create a private subnet
    # currently it will be associated with the default vpc route table which doesn't have the IGW as the default gateway
    private_subnet_response = vpc.create_subnet(vpc_id, '10.221.10.0/24')  # remember the boto3 client connection returns dicts
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']
    print(f"Created Private Subnet {private_subnet_id} for VPC {vpc_id}")

    # add name tag to private subnet
    # this uses the add_name_tag() method already defined
    vpc.add_name_tag(private_subnet_id, "Boto3 Private Subnet")




if __name__ == '__main__':
    main()



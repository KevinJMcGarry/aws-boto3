# VPC Class

class VPC:
    def __init__(self, client):  # get the boto3 client for our vpc
        self._client = client
        """ :type : pyboto3.ec2 """  # this enables auto-complete using pyboto3

    def create_vpc(self, cidr):  # create vpc method
        print('Creating a VPC...')
        return self._client.create_vpc(
            CidrBlock=cidr
        )

    def add_name_tag(self, resource_id, resource_name):  # tagging the vpc
        print(f"Adding {resource_name} tag to the resource {resource_id}")
        return self._client.create_tags(
            Resources=[resource_id],
            Tags=[{
                'Key': 'Name',
                'Value': resource_name
            }]
        )

    def create_internet_gateway(self):
        print('Creating an IGW...')
        return self._client.create_internet_gateway()


    def attach_igw_to_vpc(self, vpc_id, igw_id):
        print(f"Attaching IGW {igw_id} to the VPC {vpc_id}...")
        return self._client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )

    # method for creating a public or private subnet
    def create_subnet(self, vpc_id, cidr_block):
        print(f"Creating a VPC for {vpc_id} with CIDR Block of {cidr_block}")
        return self._client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block
        )

    # method to create a public route table
    def create_public_route_table(self, vpc_id):
        print(f"Creating Public Route Table for {vpc_id}")
        return self._client.create_route_table(VpcId=vpc_id)

    # method to create an IGW
    def create_igw_route_for_public_route_table(self, rtb_id, igw_id):
        print(f"Adding route for IGW {igw_id} to Route Table {rtb_id}")
        return self._client.create_route(
            RouteTableId=rtb_id,
            GatewayId=igw_id,
            DestinationCidrBlock='0.0.0.0/0'
        )

    # method to associate a particular subnet (pub or priv) to a particular route table
    def associate_subnet_with_route_table(self, subnet_id, rtb_id):
        print(f"Associating subnet {subnet_id} with Route Table {rtb_id}")
        return self._client.associate_route_table(
            SubnetId=subnet_id,
            RouteTableId=rtb_id
        )

    # method to allow auto-assign of public ip addresses to instances in the public subnets
    def allow_auto_assign_publicip_for_public_subnet(self, subnet_id):
        return self._client.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={'Value': True}
        )



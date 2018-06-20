# using the ec2 client as that is what all the vpc constructs are located under
# https://boto3.readthedocs.io/en/latest/reference/services/ec2.html

import boto3


class ClientLocator:
    def __init__(self, client):  # client is the argument that you can specify which allows you to work with various aws resources - ec2, iam, rds, s3 etc.
        self._client = boto3.client(client, region_name="us-east-2")

    def get_client(self):  # method to get and return the client we created above (that we set with the initializer method)
        return self._client


class EC2Client(ClientLocator):  # class to get the ec2 client. Notice the argument for this class is the class created above
    def __init__(self):  # this class will initialize itself with the boto3.client parameter above
        super().__init__('ec2')  # calling the super method and initializing it with the client we want to use (ec2)
        # this passes in the client we want to use (ec2) to the ClientLocator class
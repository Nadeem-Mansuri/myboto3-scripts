from botocore.exceptions import ClientError
import os
import boto3

vpc_client = boto3.client('ec2')
vpc_resource = boto3.resource('ec2')

def filter_vpcid():
    response = vpc_client.describe_vpcs(
        Filters=[{'Name':'cidr-block-association.cidr-block','Values': ['192.168.0.0/21', ]},])
    novpc = []
    desvpc = response['Vpcs']
    if desvpc == novpc:
        vpc = vpc_resource.create_vpc(
            CidrBlock='192.168.0.0/21',
            TagSpecifications=[ {'ResourceType': 'vpc','Tags': [ {'Key': 'Name','Value': 'My-VPC'},]},])
        vpc.wait_until_available(
            Filters=[{'Name': 'cidr-block-association.cidr-block','Values': ['192.168.0.0/21',]},],)
        print('New VPC My-VPC Created')

    else:
        print('VPC Exists: My-VPC')

def getvpcname():
    response = vpc_client.describe_vpcs(
        Filters=[{'Name': 'tag:Name','Values': ['My-VPC', ]},])
    for i in response['Vpcs']:
        for tag in i['Tags']:            
            vpcname = tag['Value']
    for i in response['Vpcs']:
        vpcid = i['VpcId']
    return vpcname, vpcid

def createsubnet1():
    try:
        vpcname, vpcid = getvpcname()

        response = vpc_client.describe_subnets(
            Filters=[{'Name':'cidr-block','Values': ['192.168.1.0/24', ]},])

        nosub1 = []
        dessub1 = response['Subnets']
        if dessub1 == nosub1:
            subnet1 = vpc_client.create_subnet(
                TagSpecifications=[{'ResourceType': 'subnet', 'Tags': [{'Key': 'Name','Value': 'Public-subnet1A'},]},],
                AvailabilityZone='us-east-1a',
                CidrBlock='192.168.1.0/24',
                VpcId= vpcid,
                )
            subnetid1 =  subnet1['Subnet']['SubnetId']
            print('Subnet Created: Private-subnet1A', subnetid1)

        else:
            for subnet in response['Subnets']:
                subnetid1 = subnet['SubnetId'] 
                print('Public-subnet1A is already exists :',subnetid1 )
    except Exception as e:
        print("There is a error in the client configuration: ", e)
    return subnetid1

def createsubnet2():
    try: 
        vpcname, vpcid = getvpcname()
        subnetid1 = createsubnet1()
        
        response = vpc_client.describe_subnets(
            Filters=[{'Name':'cidr-block','Values': ['192.168.2.0/24', ]},])        
        nosub2 = []
        dessub2 = response['Subnets']
        if dessub2 == nosub2:
            subnet2 = vpc_client.create_subnet(
                TagSpecifications=[{'ResourceType': 'subnet','Tags': [{'Key': 'Name','Value': 'Private-subnet1B'},]},],
                AvailabilityZone='us-east-1b',
                CidrBlock='192.168.2.0/24',
                VpcId= vpcid,
            )
            subnetid2 =  subnet2['Subnet']['SubnetId']

            print('Subnet Created: Private-subnet1B', subnetid2 )
        else:
            for subnet in response['Subnets']:
                subnetid2 = subnet['SubnetId'] 
                print('Private-subnet1B is already exists :',subnetid2 )

    except Exception as e:
        print("There is a error in the client configuration: ", e)

    vpc_client.modify_subnet_attribute(SubnetId=subnetid1, MapPublicIpOnLaunch={'Value': True},)
    return subnetid2

def createsubnet3():
    try:
        vpcname, vpcid = getvpcname()

        response = vpc_client.describe_subnets(
            Filters=[{'Name':'cidr-block','Values': ['192.168.3.0/24', ]},])
        nosub3 = []
        dessub3 = response['Subnets']
        if dessub3 == nosub3:
            subnet3 = vpc_client.create_subnet(
                TagSpecifications=[{'ResourceType': 'subnet','Tags': [ {'Key': 'Name','Value': 'Private-subnet2C' },]},],
                AvailabilityZone='us-east-1c',
                CidrBlock='192.168.3.0/24',
                VpcId= vpcid,
                DryRun=False
                )
            subnetid3 =  subnet3['Subnet']['SubnetId']
        else:
            for subnet in response['Subnets']:
                subnetid3 = subnet['SubnetId'] 
                print('Private-subnet2C is already exists :',subnetid3)

    except Exception as e:
        print("There is a error in the client configuration: ", e)
    return subnetid3

def createsubnet4():
    try:
        vpcname, vpcid = getvpcname()

        response = vpc_client.describe_subnets(
            Filters=[{'Name':'cidr-block','Values': ['192.168.4.0/24', ]},])
        nosub4 = []
        dessub4 = response['Subnets']
        if dessub4 == nosub4: 
            subnet4 = vpc_client.create_subnet(
                TagSpecifications=[{'ResourceType': 'subnet','Tags': [{'Key': 'Name','Value': 'Private-subnet3D' },]},],
                AvailabilityZone='us-east-1d',
                CidrBlock='192.168.4.0/24',
                VpcId= vpcid,
                DryRun=False
            )
            subnetid4 =  subnet4['Subnet']['SubnetId']
        else:
            for subnet in response['Subnets']:
                subnetid4 = subnet['SubnetId'] 
                print('Private-subnet3D is already exists :',subnetid4)
    except Exception as e:
        print("There is a error in the client configuration: ", e)
    return subnetid4 

def createinternetgw():
    try:     
        vpcname, vpcid = getvpcname()

        response = vpc_client.describe_internet_gateways(
            Filters=[{'Name': 'tag:Name','Values': ['My-IGW', ]},],)    
        NoIGW = []
        DescribeInternetGateway = response['InternetGateways']
        if DescribeInternetGateway == NoIGW:
            CreateInternetGateway = vpc_client.create_internet_gateway(
                TagSpecifications=[{'ResourceType': 'internet-gateway','Tags': [{'Key': 'Name','Value': 'My-IGW'},]},],)
            waiter = vpc_client.get_waiter('internet_gateway_exists')
            waiter.wait(
                Filters=[{'Name': 'tag:Name','Values': ['My-IGW',]},],)

            MYInternetGatewayID = CreateInternetGateway['InternetGateway']['InternetGatewayId']
        else:
            for i in response['InternetGateways']:
                MYInternetGatewayID = i['InternetGatewayId']
                print('Internet Gateway Already exists :',MYInternetGatewayID ) 
    except Exception as e:
        print("There is a error in the client configuration: ", e)
    return MYInternetGatewayID
  
def attachIGWVpc():
    try:
        vpcname, vpcid = getvpcname()
        response = vpc_client.describe_internet_gateways(
            Filters=[{ 'Name': 'tag:Name','Values': ['My-IGW',]},],)

        for i in response['InternetGateways']:
            MYInternetGatewayID=i['InternetGatewayId']
            vpc_client.attach_internet_gateway(
                InternetGatewayId=MYInternetGatewayID,
                VpcId=vpcid
                )
            print(f"{MYInternetGatewayID} is attached to {vpcname}")

    except Exception as e:
        if str(e).__contains__("Resource.AlreadyAssociated"):
            print(f"{MYInternetGatewayID} is already attached to the VPC: {vpcname}")

def createroute_table():
    vpcname, vpcid = getvpcname()
    subnetid1 = createsubnet1()
    MYInternetGatewayID = createinternetgw()
    response = vpc_client.describe_route_tables(
        Filters=[{'Name': 'tag:Name','Values': ['Public-RT',]},],)
    nort1 = []
    desrt1 = response['RouteTables']
    if desrt1 == nort1:
        route_table =  vpc_resource.create_route_table(
            VpcId=vpcid,
            TagSpecifications=[{'ResourceType': 'route-table','Tags': [{'Key': 'Name','Value': 'Public-RT'},]},])
        route = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=MYInternetGatewayID
        )
        route_table_association = route_table.associate_with_subnet(
            SubnetId=subnetid1
        )


        print(f"Public Route_Table Exists {route_table} and route added 0.0.0.0/0 to {MYInternetGatewayID}")

    else: 
        route_table = response['RouteTables'][0]['RouteTableId']
        print(f"Public Route_Table Exists {route_table} and route added 0.0.0.0/0 to {MYInternetGatewayID}")

def CreateEIP():
    try:
        response = vpc_client.describe_addresses(
            Filters=[{'Name': 'tag:Name', 'Values': ['MY-EIP',]},],)
        noeip = []
        desnoeip = response['Addresses']
        if desnoeip == noeip:
            CreateEipAddr = vpc_client.allocate_address(
                TagSpecifications=[ {'ResourceType': 'elastic-ip','Tags': [{'Key': 'Name','Value': 'MY-EIP'},]},])
            EIP_AllocId = CreateEipAddr['AllocationId']
            EIP_PublicIP = CreateEipAddr['PublicIp']
            print(f"EIP Created: {EIP_AllocId} {EIP_PublicIP}")
        else:
            for i in response['Addresses']:
                EIP_AllocId = i['AllocationId']
                EIP_PublicIP = i['PublicIp']
                print(f"Elastic IP Exists Allocation ID is {EIP_AllocId} & Public IP is {EIP_PublicIP}")
    except Exception as e:
        print("There is a error in the client configuration: ", e)
    return EIP_AllocId, EIP_PublicIP        

def CreateNGW():
    try: 
        EIP_AllocId, EIP_PublicIP = CreateEIP()
        subnetid1 = createsubnet1()
        ngwname = 'MY-NGW1'
        DescribeNATGateway = vpc_client.describe_nat_gateways(
            Filters=[ {'Name': 'tag:Name','Values': [ngwname,]},],)  

        CurrentState = DescribeNATGateway['NatGateways']
        NoNATGateway = []

        if CurrentState == NoNATGateway:            
            CreateNATGateway = vpc_client.create_nat_gateway(
                AllocationId = EIP_AllocId,
                SubnetId=subnetid1,
                TagSpecifications=[{'ResourceType': 'natgateway','Tags': [{'Key': 'Name','Value': ngwname},]},])
            print('Please wait!!! NGW creation is in progress' )
            waiter = vpc_client.get_waiter('nat_gateway_available')
            waiter.wait(
                Filters=[{'Name': 'tag:Name','Values': [ ngwname,]},],)
            NATGatewayId = CreateNATGateway['NatGateway']['NatGatewayId']
            print('NGW Created and it is avalable now')
        else:
            for i in DescribeNATGateway['NatGateways']:
                NATGatewayId = i['NatGatewayId']
            print(f"NATGateway is already Exists: {NATGatewayId} and State is Available")
    except Exception as e:
        print("There is a error in the client configuration: ", e)
    return NATGatewayId
        
def AddTagIn_MainRouteTable():
    try: 
        vpcname, vpcid = getvpcname()
        DescribeRouteTable = vpc_client.describe_route_tables(
           Filters=[{'Name': 'vpc-id','Values': [vpcid,]},],)

        for i in DescribeRouteTable['RouteTables']:
            for RTassociationid in i['Associations']:
                if RTassociationid['Main'] == True:
                   MainRouteTable_Id = RTassociationid['RouteTableId']

        DescribeRouteTable1 = vpc_client.describe_route_tables(
            Filters=[{'Name': 'route-table-id','Values': [MainRouteTable_Id,]},],)
        NoTags = DescribeRouteTable1['RouteTables'][0]['Tags']

        if NoTags == []:  
            route_table = vpc_resource.RouteTable(MainRouteTable_Id)
            CreateTag_MainRT = route_table.create_tags(
                Tags=[{'Key': 'Name','Value': 'MY-Main-RT'}])
            print('Name Tags added into Main Route-Table')
        else:
            for tags in DescribeRouteTable1['RouteTables']:
                existingtag = tags['Tags'][0]['Value']
                print(f"Name Tags already exists in {MainRouteTable_Id} which is {existingtag}")
    except Exception as e:
         print("There is a error in the client configuration: ", e)
         
    return MainRouteTable_Id

def AddPrivSubnet_in_MainRT():
    try:
        MainRouteTable_Id = AddTagIn_MainRouteTable()
        NATGatewayId = CreateNGW()
        subnetid1 = createsubnet1()
        subnetid2 = createsubnet2()
        subnetid3 = createsubnet3()
        subnetid4 = createsubnet4()

        response = vpc_client.describe_route_tables(
        Filters=[{'Name': 'route-table-id','Values': [MainRouteTable_Id,]},],)
        association =  response['RouteTables'][0]['Associations']
        exissub = []
        for routables in association:
            if routables['Main'] == False:
                exissub.append (routables['SubnetId'])    

        if subnetid2 not in exissub:
            response = vpc_client.associate_route_table(
            RouteTableId=MainRouteTable_Id,
            SubnetId = subnetid2
            )            
            print(f"{subnetid2} is added on {MainRouteTable_Id}")
        else:
            print(f"{subnetid2} is exists on {MainRouteTable_Id}")

        if subnetid3 not in exissub:
            response = vpc_client.associate_route_table(
            RouteTableId=MainRouteTable_Id,
            SubnetId = subnetid3
            )
            print(f"{subnetid3} is added on {MainRouteTable_Id}")
        else:
            print(f"{subnetid3} is exists on {MainRouteTable_Id}")
                    
        if subnetid4 not in exissub:
            response = vpc_client.associate_route_table(
            RouteTableId=MainRouteTable_Id,
            SubnetId = subnetid4
            )
            print(f"{subnetid4} is added on {MainRouteTable_Id}")
        else:
            print(f"{subnetid4} is exists on {MainRouteTable_Id}")

    except Exception as e:
         print("There is a error in the client configuration: ", e)

def AddNGW_in_mainRT():
    try:
        MainRouteTable_Id = AddTagIn_MainRouteTable()
        NATGatewayId = CreateNGW()

        route_table = vpc_resource.RouteTable(MainRouteTable_Id)
        route = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            NatGatewayId=NATGatewayId,
        )
    except Exception as e:
        if str(e).__contains__("RouteAlreadyExists"):
            print('Nat-Gateway is Already added as a route into a Main Route-Table' , MainRouteTable_Id)



try:
    vpc_client = boto3.client('ec2')
    vpc_resource =  boto3.resource('ec2')
    filter_vpcid()
    getvpcname()
    createsubnet1()
    createsubnet2()
    createsubnet3()
    createsubnet4()
    createinternetgw()
    attachIGWVpc()
    createroute_table()    
    CreateEIP()
    CreateNGW()
    AddTagIn_MainRouteTable()
    AddPrivSubnet_in_MainRT()
    AddNGW_in_mainRT()

except ClientError as e:
    print("There is a error in the client configuration: ", e)

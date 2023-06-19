import boto3
import sys
from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc)
today=today.strftime('%Y-%m-%d')
recordlist = []
#AWS_Profile = input( "Please enter the AWS Profile :")
#Hosted_Zone = input( "Please enter the HostedZoneName :")
AWS_Profile = 'default'
Hosted_Zone = 'nadeemlabs.com.'


sts_client = boto3.client('sts')
session = boto3.session.Session(profile_name=AWS_Profile)
r53_client = session.client('route53')

r53_filename = "Route53_Report_"+today+".csv"

def main():
    print("Fetching the records ...")
    get_record()
    print("Found {} records. Generating the report...".format(len(recordlist)))
    generate_report()
    print("Report Generated. Script Execution Completed !")

def get_record():
    response = r53_client.list_hosted_zones()

    for hostedzone in response['HostedZones']:
#        if hostedzone['Name'].lower() == Hosted_Zone.lower() :
        if Hosted_Zone.lower() in hostedzone['Name'].lower() :
            hostedzoneId = hostedzone['Id']
            record_response = r53_client.list_resource_record_sets(HostedZoneId=hostedzoneId)
            for record in record_response['ResourceRecordSets']:
                if 'AliasTarget' in record:
                    record_dict = {}
                    record_dict['HostedZoneName'] = hostedzone['Name']
                    record_dict['HostedZoneId'] = hostedzoneId.replace("/hostedzone/","")
                    record_dict['RecordName'] = record['Name']
                    try:
                        record_dict['RecordAlias'] = record['AliasTarget']['DNSName']
                    except:
                        record_dict['RecordAlias'] = ''
                    try:
                        record_dict['RecordType'] = record['Type']
                    except:
                        record_dict['RecordAlias'] = ''
                    record_dict['TTL'] = ''
                    record_dict['RecordValue'] = ''
                    recordlist.append(record_dict)
                else:
                    try:
                        for value in record['ResourceRecords']:
                            record_dict = {}
                            record_dict['HostedZoneName'] = hostedzone['Name']
                            record_dict['HostedZoneId'] = hostedzoneId.replace("/hostedzone/","")
                            record_dict['RecordName'] = record['Name']
                            record_dict['RecordType']=  record['Type']
                            record_dict['RecordAlias'] = ''
                            record_dict['TTL'] = record['TTL']
                            record_dict['RecordValue'] = value['Value']
                            recordlist.append(record_dict)
                    except:
                        pass
def generate_report():
    with open(r53_filename, 'w') as f:
        print("%s,%s,%s,%s,%s,%s,%s" % ("HostedZoneName","HostedZoneId","RecordName","RecordType","TTL","RecordValue","RecordAlias"),file=f)
        for records in recordlist:
            try:
                print("%s,%s,%s,%s,%s,%s,%s" % (records['HostedZoneName'],records['HostedZoneId'],records['RecordName'],records['RecordType'],records['TTL'],records['RecordValue'],records['RecordAlias']),file=f)
            except:
                err = PrintException()
                print(err)
                print(records)

main()


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    captureErr = "Line No. : " + str(lineno)  + " | ERROR: " + str(exc_obj)
    return captureErr
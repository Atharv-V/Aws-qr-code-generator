import json
import boto3
import qrcode
import io
import base64
import argparse
import argparse

parser = argparse.ArgumentParser(description="Generate QR code from URL")
parser.add_argument("url", help="The URL to convert to a QR code")
args = parser.parse_args()


print(args.url)

s3 = boto3.client('s3')
s3 = boto3.client('s3', 
                  aws_access_key_id='A******', 
                  aws_secret_access_key='u******************',
                  region_name='eu-north-1')

def lambda_handler(url):

    img = qrcode.make(url)
    img_bytes = io.BytesIO()
    img.save(img_bytes)
    img_bytes = img_bytes.getvalue()

    filename = url.split("://")[1].replace("/", "_") + '.png'

    s3.put_object(Bucket='qr-code-generator1', Key=filename, Body=img_bytes, ContentType='image/png', ACL='public-read')
    
    location = s3.get_bucket_location(Bucket='qr-code-generator1')['LocationConstraint']
    region = '' if location is None else f'{location}'
    qr_code_url = f"https://s3-{region}.amazonaws.com/{'qr-code-generator1'}/{filename}"
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'QR code generated and uploaded to S3 bucket successfully!', 'qr_code_url': qr_code_url})
    }

lambda_handler(args.url)
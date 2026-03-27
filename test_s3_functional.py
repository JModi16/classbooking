import os
import django
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import boto3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

print("=== AWS S3 FUNCTIONAL TEST ===\n")

try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    test_file = 'test_upload.txt'
    test_content = b'ClassBooking S3 Test - This file was uploaded from Django'
    print(f"Testing upload to bucket: {bucket}\n")
    # Test upload
    print(f"⏳ Uploading test file: {test_file}...")
    s3_client.put_object(
        Bucket=bucket,
        Key=test_file,
        Body=test_content,
        ContentType='text/plain'
    )
    print(f"✅ Upload successful!")
    # Test download/read
    print(f"\n⏳ Downloading test file...")
    response = s3_client.get_object(Bucket=bucket, Key=test_file)
    downloaded_content = response['Body'].read()
    print(f"✅ Download successful!")
    print(f"   Content: {downloaded_content.decode()}")
    # Verify content
    if downloaded_content == test_content:
        success_msg = (
            "\n✅ \nContent verification successful - "
            "S3 is working perfectly!"
        )
        print(success_msg)
    else:
        fail_msg = (
            "\n❌ Content verification failed - downloaded content "
            "does not match uploaded content."
        )
        print(fail_msg)
        raise ValueError(
            "S3 content verification failed: downloaded content "
            "does not match uploaded content."
        )
    # Clean up
    print(f"\n⏳ Cleaning up test file...")
    s3_client.delete_object(Bucket=bucket, Key=test_file)
    print(f"✅ Test file deleted")
    print(f"\n=== S3 DJANGO STORAGES CONFIG ===\n")
    print(f"STORAGES: {settings.STORAGES}")
    print(f"\nSTATIC_URL: {settings.STATIC_URL}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"\n✅ AWS S3 is READY for production!")
except Exception as e:
    print(f"❌ S3 Test Failed: {str(e)}")
    import traceback
    traceback.print_exc()
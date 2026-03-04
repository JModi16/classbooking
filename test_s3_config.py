import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

from django.conf import settings
import boto3

print("=== AWS S3 CONFIGURATION CHECK ===\n")

print(f"USE_AWS enabled: {'USE_AWS' in os.environ}")
print(f"AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME if 'USE_AWS' in os.environ else 'Not set'}")
print(f"AWS_S3_REGION_NAME: {settings.AWS_S3_REGION_NAME if 'USE_AWS' in os.environ else 'Not set'}")
print(f"AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN if 'USE_AWS' in os.environ else 'Not set'}")

print("\n=== TESTING S3 CONNECTION ===\n")

try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    # Test connection by listing buckets
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    
    print(f"✅ Connected to AWS S3 successfully!")
    print(f"   Available buckets: {', '.join(buckets)}")
    
    if settings.AWS_STORAGE_BUCKET_NAME in buckets:
        print(f"✅ Bucket '{settings.AWS_STORAGE_BUCKET_NAME}' found!")
    else:
        print(f"❌ Bucket '{settings.AWS_STORAGE_BUCKET_NAME}' not found in your account")
    
    print("\n=== STORAGES CONFIGURATION ===\n")
    print(f"Default Storage: {settings.STORAGES['default']['BACKEND']}")
    print(f"Static Files Storage: {settings.STORAGES['staticfiles']['BACKEND']}")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    
except Exception as e:
    print(f"❌ Error connecting to S3: {str(e)}")

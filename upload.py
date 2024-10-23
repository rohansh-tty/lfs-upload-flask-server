import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import boto3, botocore
from boto3.s3.transfer import TransferConfig

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)
def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    # large  file config 
    config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10,
                        multipart_chunksize=1024*25, use_threads=True) 
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            },
            config=config
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        import traceback
        print("Something Happened: ", traceback.format_exc())
        return e
    

    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename
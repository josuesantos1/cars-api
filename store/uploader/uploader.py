import boto3, os

class Uploader():
    def get_file(key):
        s3_client = boto3.client('s3')
        try:
           return s3_client.generate_presigned_url('get_object',
                            Params={'Bucket': str(os.getenv('BUCKET')),
                                    'Key': key},
                            ExpiresIn=3600)
        except:
            return None

import os
class S3Syncer:
    def load_to_s3(self,aws_key_url,folder):
        command=f'aws s3 sync {folder} {aws_key_url}'
        os.system(command)
    def load_from_s3(self,aws_key_url,folder):
        command=f'aws s3 sync {aws_key_url} {folder}'
        os.system(command)
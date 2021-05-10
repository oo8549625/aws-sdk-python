from flask import Flask, request
import boto3
import numpy as np
app = Flask(__name__)


@app.route('/object/copy', methods=['POST'])
def create_store():
    request_data = request.get_json()
    if 'source_accessKey' not in request_data:
        return {'message': "source_accessKey is required."}
    elif 'source_secretKey' not in request_data:
        return {'message': "source_secretKey is required."}
    elif 'source_bucket' not in request_data:
        return {'message': "source_bucket is required."}
    elif 'source_prefix' not in request_data:
        return {'message': "source_prefix is required."}
    elif 'dest_accessKey' not in request_data:
        return {'message': "dest_accessKey is required."}
    elif 'dest_secketKey' not in request_data:
        return {'message': "dest_secketKey is required."}
    elif 'dest_bucket' not in request_data:
        return {'message': "dest_bucket is required."}
    else:
        source = boto3.client(
            's3',
            aws_access_key_id=request_data['source_accessKey'],
            aws_secret_access_key=request_data['source_secretKey'],
            endpoint_url='https://cos.twcc.ai'
        )
        dest = boto3.client(
            's3',
            aws_access_key_id=request_data['dest_accessKey'],
            aws_secret_access_key=request_data['dest_secketKey'],
            endpoint_url='https://cos.twcc.ai'
        )
        try:
            objects = source.list_objects(
                Bucket=request_data['source_bucket'],
                Prefix=request_data['source_prefix']
            )
        except Exception as e:
            return {'message': e.response}
        else:
            objs = np.array(list(objects['Contents']))
            for object in objs:
                source_obj = source.get_object(
                    Bucket=request_data['source_bucket'],
                    Key=object['Key'],
                )
                try:
                    dest.put_object(
                        Bucket=request_data['dest_bucket'],
                        Key=object['Key'],
                        Body=source_obj['Body'].read()
                    )
                except Exception as e:
                    return {'message': e.response}
            return {'message': 'OK'}


if __name__ == "__main__":
    app.run(debug=True)

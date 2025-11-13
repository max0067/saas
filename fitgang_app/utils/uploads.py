"""File upload utilities."""
import os
import uuid
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer
import boto3
from botocore.exceptions import ClientError


def allowed_file(filename, file_type='image'):
    """Check if file extension is allowed."""
    if '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()

    if file_type == 'image':
        allowed = current_app.config['ALLOWED_IMAGE_EXTENSIONS']
    elif file_type == 'video':
        allowed = current_app.config['ALLOWED_VIDEO_EXTENSIONS']
    elif file_type == 'document':
        allowed = current_app.config['ALLOWED_DOCUMENT_EXTENSIONS']
    else:
        return False

    return ext in allowed


def generate_unique_filename(filename):
    """Generate unique filename."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_name = f"{uuid.uuid4().hex}"
    return f"{unique_name}.{ext}" if ext else unique_name


def save_uploaded_file(file, folder='uploads', file_type='image'):
    """
    Save uploaded file to local storage or S3.

    Args:
        file: FileStorage object
        folder: Folder name within uploads directory
        file_type: Type of file (image, video, document)

    Returns:
        tuple: (success, file_path or error_message)
    """
    if not file or file.filename == '':
        return False, 'No file provided'

    if not allowed_file(file.filename, file_type):
        return False, f'File type not allowed for {file_type}'

    # Generate unique filename
    original_filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(original_filename)

    # Use S3 if configured
    if current_app.config.get('USE_S3'):
        return upload_to_s3(file, unique_filename, folder)
    else:
        return save_to_local(file, unique_filename, folder)


def save_to_local(file, filename, folder):
    """Save file to local storage."""
    try:
        # Create upload directory
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_path, exist_ok=True)

        # Save file
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)

        # Return relative path for database storage
        relative_path = os.path.join(folder, filename)
        return True, relative_path

    except Exception as e:
        current_app.logger.error(f"Error saving file: {str(e)}")
        return False, str(e)


def upload_to_s3(file, filename, folder):
    """Upload file to AWS S3."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION']
        )

        bucket = current_app.config['AWS_BUCKET_NAME']
        s3_path = f"{folder}/{filename}"

        s3_client.upload_fileobj(
            file,
            bucket,
            s3_path,
            ExtraArgs={'ACL': 'private', 'ContentType': file.content_type}
        )

        return True, s3_path

    except ClientError as e:
        current_app.logger.error(f"Error uploading to S3: {str(e)}")
        return False, str(e)


def delete_file(file_path):
    """Delete file from local storage or S3."""
    if current_app.config.get('USE_S3'):
        return delete_from_s3(file_path)
    else:
        return delete_from_local(file_path)


def delete_from_local(file_path):
    """Delete file from local storage."""
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
        return True
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
        return False


def delete_from_s3(file_path):
    """Delete file from S3."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION']
        )

        bucket = current_app.config['AWS_BUCKET_NAME']
        s3_client.delete_object(Bucket=bucket, Key=file_path)
        return True

    except ClientError as e:
        current_app.logger.error(f"Error deleting from S3: {str(e)}")
        return False


def generate_signed_url(file_path, expiration=3600):
    """
    Generate signed URL for secure file downloads.

    Args:
        file_path: Path to the file
        expiration: URL expiration time in seconds (default: 1 hour)

    Returns:
        Signed URL string
    """
    if current_app.config.get('USE_S3'):
        return generate_s3_signed_url(file_path, expiration)
    else:
        return generate_local_signed_url(file_path, expiration)


def generate_s3_signed_url(file_path, expiration):
    """Generate S3 presigned URL."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION']
        )

        bucket = current_app.config['AWS_BUCKET_NAME']

        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': file_path},
            ExpiresIn=expiration
        )

        return url

    except ClientError as e:
        current_app.logger.error(f"Error generating S3 signed URL: {str(e)}")
        return None


def generate_local_signed_url(file_path, expiration):
    """Generate signed URL for local files."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(file_path, salt='download-file')

    # For local files, we'll use a route that verifies the token
    return url_for('main.download_file', token=token, _external=True)


def verify_signed_url_token(token, max_age=3600):
    """Verify signed URL token."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        file_path = serializer.loads(token, salt='download-file', max_age=max_age)
        return file_path
    except Exception as e:
        current_app.logger.error(f"Error verifying token: {str(e)}")
        return None


def get_file_url(file_path):
    """Get public URL for file."""
    if not file_path:
        return None

    if current_app.config.get('USE_S3'):
        bucket = current_app.config['AWS_BUCKET_NAME']
        region = current_app.config['AWS_REGION']
        return f"https://{bucket}.s3.{region}.amazonaws.com/{file_path}"
    else:
        return url_for('static', filename=f'../{current_app.config["UPLOAD_FOLDER"]}/{file_path}', _external=True)

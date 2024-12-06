import arrow
import json
import jwt
import logging
import os
import time


logger = logging.getLogger(__name__)


def get_access_token():
    home_dir = os.path.expanduser("~")
    credentials_path = os.path.join(home_dir, '.config', 'vinz', 'credentials.json')
    if os.path.exists(credentials_path):
        with open(credentials_path) as readfile:
            try:
                data = json.loads(readfile.read())
            except Exception:
                raise Exception(f'Invalid credentials file: {credentials_path}')
        if 'access_token' not in data:
            raise Exception('No access token found. Use:\n\nvinz-cli auth login')
        access_token = data['access_token']
        if not access_token:
            raise Exception('Invalid access token. Use:\n\nvinz-cli auth login')
        decoded_jwt = jwt.decode(access_token, options={"verify_signature": False})
        if decoded_jwt['exp'] < int(time.time()):
            raise Exception('Access token expired. Use:\n\nvinz-cli auth login')
        return access_token
    else:
        raise Exception(f"No credentials found at: {credentials_path}")


def write_access_token(access_token):
    home_dir = os.path.expanduser("~")
    credentials_folder = os.path.join(home_dir, '.config', 'vinz')
    credentials_path = os.path.join(credentials_folder, 'credentials.json')
    if os.path.exists(credentials_path):
        logger.info(f'Updating file: {credentials_path}')
        with open(credentials_path) as readfile:
            try:
                data = json.loads(readfile.read())
            except Exception:
                data = {}
        data['access_token'] = access_token
        data['time'] = arrow.utcnow().isoformat()
        with open(credentials_path, 'w') as writefile:
            json.dump(data, writefile, indent=4)
    else:
        os.makedirs(credentials_folder, exist_ok=True)
        logger.info(f'Creating new file: {credentials_path}')
        data = {'access_token': access_token, 'time': arrow.utcnow().isoformat()}
        with open(credentials_path, 'w') as writefile:
            writefile.write(json.dumps(data))


def write_config(config):
    home_dir = os.path.expanduser("~")
    config_folder = os.path.join(home_dir, '.config', 'vinz')
    config_path = os.path.join(config_folder, 'config.json')
    if os.path.exists(config_path):
        logger.info(f'Updating file: {config_path}')
        with open(config_path) as readfile:
            try:
                data = json.loads(readfile.read())
            except Exception:
                data = {}
        data.update(**config)
        data['update_time'] = arrow.utcnow().isoformat()
        with open(config_path, 'w') as writefile:
            json.dump(data, writefile, indent=4)
    else:
        os.makedirs(config_folder, exist_ok=True)
        logger.info(f'Creating new file: {config_folder}')
        data = {'update_time': arrow.utcnow().isoformat()}
        data.update(**config)
        with open(config_path, 'w') as writefile:
            writefile.write(json.dumps(data))


def get_config():
    result = {'output': 'yaml'}
    home_dir = os.path.expanduser("~")
    config_path = os.path.join(home_dir, '.config', 'vinz', 'config.json')
    if os.path.exists(config_path):
        with open(config_path) as readfile:
            try:
                data = json.loads(readfile.read())
            except Exception:
                raise Exception(f'Invalid config file: {config_path}')
        result = data
    return result

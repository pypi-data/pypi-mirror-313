import pytz
import OpenSSL
from datetime import datetime
from echobox.tool import file

def cert_expiry_datetime(cert_path):
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, file.file_get_contents(cert_path))
    expiry_datetime = cert.get_notAfter().decode('utf-8')
    expiry_datetime = datetime.strptime(expiry_datetime, '%Y%m%d%H%M%S%z')
    expiry_datetime = expiry_datetime.replace(tzinfo=pytz.utc)
    return [
        expiry_datetime,
        (expiry_datetime - datetime.now(pytz.utc)).days
    ]

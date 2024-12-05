import paramiko
import sys

from cmpparis.ses_utils import *

class FTP:
    def __init__(self, host, port=22):
        self.host = host
        self.port = port
        self.transport = paramiko.Transport((self.host, self.port))
        self.sftp = None

    def set_working_directory(self, directory):
        try:
            self.sftp.chdir(directory)
        except Exception as e:
            error_message = f"Error while setting working directory on SFTP server: {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    def login(self, username, passwd):
        try:
            self.transport.connect(username=username, password=passwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as e:
            error_message = f"Error while connecting to SFTP server: {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    def list_files(self):
        try:
            return self.sftp.listdir()
        except Exception as e:
            error_message = f"Error while listing files on SFTP server: {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    def upload_file(self, localfile, remotefile):
        try:
            self.sftp.put(localfile, remotefile)
        except Exception as e:
            error_message = f"Error while uploading file to SFTP server: {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    def download_file(self, remotefile, localfile):
        try:
            self.sftp.get(remotefile, localfile)
        except Exception as e:
            error_message = f"Error while downloading file from SFTP server: {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()

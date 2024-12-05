import io
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File as SharePointFile

class Sharepoint:
    def __init__(self, site_url, site_path, client_id, client_secret):
        self.site_url = site_url
        self.site_path = site_path
        self.client_id = client_id
        self.client_secret = client_secret
        self.ctx = ClientContext(f"{self.site_url}/{self.site_path}").with_credentials(ClientCredential(self.client_id, self.client_secret))

    def download_file(self, file_location, local_file_path):
        with open(local_file_path, 'wb') as local_file:
            self.ctx.web.get_file_by_server_relative_url(file_location).download(local_file).execute_query()

    def get_files(self, folder_path):
        folder = self.ctx.web.get_folder_by_server_relative_url(folder_path)
        files = folder.files
        self.ctx.load(files)
        self.ctx.execute_query()
        return files
    
    def read_file(self, file_location):
        response = SharePointFile.open_binary(self.ctx, file_location)

        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)

        return bytes_file_obj
    
    def upload_file(self, folder_path, filename):
        target_folder = self.ctx.web.get_folder_by_server_relative_url(folder_path)

        with open(filename, 'rb') as file_content:
            content = file_content.read()
            target_folder.upload_file(filename, content).execute_query()
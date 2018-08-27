import sys, uuid, os
import os.path
import ntpath
import zipfile

from azure.storage.blob import BlockBlobService, PublicAccess

from config import Config


# first submission uploads to 'uploaded-submissions' container by frontend part. Backend service watches uploaded
# container and validates. if it passes validation then submission file is moved to processed container and catalog in
# bots folder is updated with latest bot

class SubmissionManager:

    def __init__(self):
        self.config = Config()
        self.block_blob_service = BlockBlobService(account_name=self.config.account_name(), account_key=self.config.account_key())
        # not processed/verified submissions
        self.upload_container = 'uploaded-submissions'
        self.block_blob_service.create_container(self.upload_container)

        # processed submissions
        self.processed_submissions_container = 'processed-submissions'
        self.block_blob_service.create_container(self.processed_submissions_container)

        if not os.path.exists(self.config.bots_test_dir()):
            os.makedirs(self.config.bots_test_dir())

        if not os.path.exists(self.config.bots_dir()):
            os.makedirs(self.config.bots_dir())

    def get_uploaded_submissions(self):
        return self.block_blob_service.list_blobs(self.upload_container)

    # temp_full_path_filename will be deleted after uploading to blob container
    def upload_submission(self, temp_full_path_filename):
        print("upload "+temp_full_path_filename)
        self.block_blob_service.create_blob_from_path(self.upload_container, ntpath.basename(temp_full_path_filename),
                                                      temp_full_path_filename)
        os.remove(temp_full_path_filename)

    def downlaod_submission(self, file_name):
        print("download "+file_name)
        download_file = self.config.bots_test_dir()+'/'+file_name
        self.block_blob_service.get_blob_to_path(self.upload_container, file_name, download_file)

    def move_sumbmission_to_processed(self, file_name):
        blob_url = self.block_blob_service.make_blob_url(self.upload_container, file_name)
        print("move submission to valid submissions "+blob_url)
        self.block_blob_service.copy_blob(self.processed_submissions_container, file_name, blob_url)
        self.block_blob_service.delete_blob(self.upload_container, file_name)

    def validate_submission(self, file_name):
        full_path_to_file = os.path.join(self.config.bots_test_dir(), '/'+file_name)
        zip_ref = zipfile.ZipFile(full_path_to_file, 'r')
        zip_ref.extract(self.config.bots_test_dir()+'/'+os.path.basename(full_path_to_file))
        zip_ref.close()
        return True

    def get_processed_submissions(self):
        return self.block_blob_service.list_blobs(self.processed_submissions_container)


def create_test_file( test_file_name ):
    full_path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_file_name)
    # Write text to the file.
    file = open(full_path_to_file, 'w')
    file.write("Hello, World!")
    file.close()
    print("Temp file = " + full_path_to_file)
    return full_path_to_file


def uploadBots(submission_manager: SubmissionManager):
    # c:/bots/rashBot.zip
    submission_manager.upload_submission('c:/bots/rashBot.zip')
    # submissionManager.move_sumbmission_to_processed('rashBot.zip')


# Main method.
if __name__ == '__main__':
    submissionManager = SubmissionManager()
    # test_file = create_test_file('test.txt')
    submissionManager.upload_submission(temp_full_path_filename='c:/bots/rashBot.zip')

    print("new submissions")
    for submission in submissionManager.get_uploaded_submissions():
        print(submission.name)
        submissionManager.downlaod_submission(submission.name)
        if submissionManager.validate_submission(submission.name):
            submissionManager.move_sumbmission_to_processed(submission.name)

    print("processed submission")
    for submission in submissionManager.get_processed_submissions():
        print(submission.name)
        #submissionManager.downlaod_submission(submission.name)

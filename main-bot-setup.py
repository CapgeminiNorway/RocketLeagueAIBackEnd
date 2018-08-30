import time
import asyncio
from submission_manager import SubmissionManager
from validation_manager import ValidationManager


def process_bot(bot_file_name):
    print("processing " + submission.name)
    try:
        submissionManager.download_submission(bot_file_name)
        bot_full_path = submissionManager.extract_submission(bot_file_name)
        if validationManager.validate(bot_full_path):
            submissionManager.move_submission_to_processed(bot_file_name)
    except Exception as e:
        print("Unexpected Error in processing {}: {}".format(bot_file_name, str(e)))
        submissionManager.remove_uploaded_submission(bot_file_name)
        print("submission {} was deleted, due to processing error".format(bot_file_name))
        return


if __name__ == '__main__':
    submissionManager = SubmissionManager()
    validationManager = ValidationManager()
    print("starting bot tester and extractor")
    while True:
        for submission in submissionManager.get_uploaded_submissions():
            process_bot(submission.name)
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(process_bot(submission.name))
            # loop.close()
        time.sleep(5)

    print("finish process")

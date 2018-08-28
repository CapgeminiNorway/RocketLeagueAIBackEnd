import time
import asyncio
from submission_manager import SubmissionManager
from validation_manager import ValidationManager


async def processBot(bot_file_name):
    print("processing " + submission.name)
    submissionManager.download_submission(bot_file_name)
    bot_full_path = submissionManager.extract_submission(bot_file_name)
    if validationManager.validate(bot_full_path):
        submissionManager.move_submission_to_processed(bot_file_name)



if __name__ == '__main__':
    submissionManager = SubmissionManager()
    validationManager = ValidationManager()
    print("starting bot tester and extractor")
    while True:
        for submission in submissionManager.get_uploaded_submissions():
            loop = asyncio.get_event_loop()
            loop.run_until_complete(processBot(submission.name))
            loop.close()
        time.sleep(5)

    print("finish process")

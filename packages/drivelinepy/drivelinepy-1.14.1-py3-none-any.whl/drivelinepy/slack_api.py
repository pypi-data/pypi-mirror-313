#================================================================================
# Author: Garrett York
# Date: 2024/02/01
# Description: Class for Slack API
#================================================================================

from .base_api_wrapper import BaseAPIWrapper
import os
import mimetypes

class SlackAPI(BaseAPIWrapper):

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------

    def __init__(self, token, base_url="https://slack.com/api/"):
        super().__init__(base_url)
        self.token = token

    #---------------------------------------------------------------------------
    # Method - Post Message
    #---------------------------------------------------------------------------

    def post_message(self, channel, text, thread_timestamp=None):
        """
        Posts a message to a specified channel on Slack.

        :param channel: The channel ID where the message will be posted.
        :param text: The text of the message to post.
        :param thread_timestamp: The timestamp (string or float) of the parent message to post in a thread.
                                This should be a UNIX timestamp to 6 decimal places, typically obtained from
                                the response of a successful post.
        :return: The response from the Slack API as a JSON object.
        """
        self.logger.info("Entering post_message()")

        if not text:
            error_msg = "Text cannot be None or an empty string."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        endpoint = "chat.postMessage"
        payload = {
            'channel': channel,
            'text': text
        }
        if thread_timestamp:
            payload['thread_ts'] = thread_timestamp

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.post(endpoint, data=payload, headers=headers)

        if response is None:
            error_msg = "Failed to post message: No response received from Slack API. Please check the network connection and API endpoint."
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        try:
            response_json = response.json()
        except ValueError as e:
            error_msg = f"Failed to parse JSON response: {e}. Response content: {response.text}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

        if response.status_code != 200 or not response_json.get('ok', False):
            error_msg = (f"Failed to post message to channel {channel}. "
                        f"Status Code: {response.status_code}, Response: {response.text}")
            self.logger.error(error_msg)
            raise Exception(error_msg)

        self.logger.info(f"Message posted successfully to channel {channel}.")
        self.logger.info("Exiting post_message()")
        return response_json
    
    #---------------------------------------------------------------------------
    # Method - Post File + Message (optional)
    #---------------------------------------------------------------------------

    def upload_file(self, channel, file_absolute_path, text=None, thread_timestamp=None):
        """
        Uploads a file to a specified channel on Slack. Optionally posts the
        file in a thread.

        This method attempts to upload a file to the specified Slack channel. It first checks if the file exists at the given path and then determines its MIME type for proper uploading. The file is then uploaded with an optional initial comment.

        :param channel: str
            The channel ID where the file will be uploaded.
        :param file_absolute_path: str
            The absolute path to the file to upload.
        :param text: str, optional
            An initial comment to add when uploading the file. Defaults to None. The API documentation refers to this parameter is initial_comment
            but it is referred to as text in this method to match the parameter name in the post_message method.
        :param thread_timestamp: str, optional
            The timestamp of the parent message to post in a thread. Defaults to None.

        :return: dict
            A dictionary response from the Slack API indicating the success or failure of the file upload.
        """
        self.logger.info("Entering upload_file()")

        if not os.path.exists(file_absolute_path):
            error_msg = f"File not found: {file_absolute_path}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        endpoint = "files.upload"

        mime_type, _ = mimetypes.guess_type(file_absolute_path)
        mime_type = mime_type or 'application/octet-stream'

        try:
            with open(file_absolute_path, 'rb') as file_content:
                files = [('file', (os.path.basename(file_absolute_path), file_content, mime_type))]
                payload = {'channels': channel}
                if text:
                    payload['initial_comment'] = text
                if thread_timestamp:
                    payload['thread_ts'] = thread_timestamp
                headers = {'Authorization': f'Bearer {self.token}'}
                response = self.post(endpoint, headers=headers, data=payload, files=files)
                
                if response is None:
                    error_msg = "Failed to upload file: No response received from Slack API. Please check the network connection and API endpoint."
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                
                try:
                    response_json = response.json()
                except ValueError as e:
                    error_msg = f"Failed to parse JSON response: {e}. Response content: {response.text}"
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                
                if response.status_code != 200 or not response_json.get('ok', False):
                    error_msg = (f"Failed to upload file to channel {channel}. "
                                f"Status Code: {response.status_code}, Response: {response.text}")
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                
        except Exception as e:
            error_msg = f"Error uploading file: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

        self.logger.info("Exiting upload_file()")
        return response_json
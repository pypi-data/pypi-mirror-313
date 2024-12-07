from .base import Aws
from pathlib import Path
from .schemas import TextractResponse


class AwsTextract(Aws):

    def __init__(self, **kwargs):
        super(AwsTextract, self).__init__(**kwargs)

    def textract(self, *, filepath: str | Path) -> TextractResponse:
        """Perform a Tables + Forms + Queries on any given file

        see boto3.textract.detect_document_text response syntax on
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/detect_document_text.html
        """
        # Read document content
        with open(filepath, 'rb') as document:
            bytes_data = bytearray(document.read())

        # Amazon Textract client
        session = self.get_session()
        textract = session.client('textract')

        # Call Amazon Textract
        response = textract.detect_document_text(Document={'Bytes': bytes_data})

        # return a pydantic model
        return TextractResponse(**response)

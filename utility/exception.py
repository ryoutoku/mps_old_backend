from rest_framework.exceptions import APIException


class ResumeIDNotFoundException(APIException):
    status_code = 400
    default_detail = 'resume id is invalid'
    default_code = 'bad_request'


class QuestionIDNotFoundException(APIException):
    status_code = 400
    default_detail = 'question id is invalid'
    default_code = 'bad_request'

# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.


class ProjectException(Exception):
    status_code = 500
    error_msg = ''

    def __init__(self, status_code=None, error_msg=None):
        if status_code:
            self.status_code = status_code
        if error_msg:
            self.error_msg = error_msg
        self.content = {
            'code': self.status_code,
            'error_msg': self.error_msg,
            'result': '',
        }

    def __str__(self):
        return self.error_msg


class ProjectNotFoundException(ProjectException):
    status_code = 404
    error_msg = 'Project not found'

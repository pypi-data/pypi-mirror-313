# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.
from typing import Any


class User:
    def __init__(
        self,
        user_id: str = '',
        username: str = '',
        role: str = '',
        email: str = '',
        first_name: str = '',
        last_name: str = '',
        realm_roles: list[str] = None,
    ):
        self.id = user_id
        self.username = username
        self.role = role
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.realm_roles = realm_roles

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'realm_roles': self.realm_roles,
        }

    def __str__(self):
        return f'<User {self.username}>'

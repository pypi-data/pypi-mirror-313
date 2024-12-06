# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import faker
import pytest


class Faker(faker.Faker):
    def project_code(self) -> str:
        return self.pystr_format('?#' * 10).lower()

    def project_id(self) -> str:
        return self.uuid4()


@pytest.fixture(scope='session')
def fake() -> Faker:
    yield Faker()

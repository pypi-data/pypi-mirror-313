from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def load_dotenv():
    import dotenv

    dotenv.load_dotenv()

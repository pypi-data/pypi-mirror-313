import json
import os
from typing import Any, Union, Optional

import requests
from pydantic import BaseModel, Field
from .environment import Env

env = Env()

headers = {
    'X-API-Key': env.CHRONULUS_API_KEY
}


class Session(BaseModel):

    session_id: Union[str, None] = Field(default=None)
    name: str
    situation: str
    task: str

    def model_post_init(self, __context: Any) -> None:
        if self.session_id is None:
            self.create()

    def create(self):
        resp = requests.post(
            url=f"{env.API_URI}/sessions/create",
            headers=headers,
            json=self.model_dump()
        )
        response_json = resp.json()
        self.session_id = response_json['session_id']
        print(f"Session created with session_id: {response_json['session_id']}")

    @staticmethod
    def from_saved_session(session_id: str):
        resp = requests.post(
            url=f"{env.API_URI}/sessions/from-session-id",
            headers=headers,
            json={"session_id": session_id}
        )
        response_json = resp.json()

        try:
            return Session(**response_json)

        except:
            raise ValueError(response_json)



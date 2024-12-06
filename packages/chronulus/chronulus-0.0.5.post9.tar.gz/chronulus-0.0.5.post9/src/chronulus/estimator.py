from datetime import datetime
from typing import Tuple, TypeVar, Type
import pickle
import base64
import pandas as pd
import requests
from io import StringIO
from pydantic import BaseModel

from .session import Session
from .environment import Env

env = Env()
headers = {
    'X-API-Key': env.CHRONULUS_API_KEY
}

BaseModelSubclass = TypeVar('BaseModelSubclass', bound=BaseModel)


class Estimator:
    def __init__(self, session: Session, input_type: Type[BaseModelSubclass]):
        self.estimator_id = None
        self.session = session
        self.estimator_name = "EstimatorBase"
        self.input_type = input_type


class EstimatorCreationRequest(BaseModel):
    estimator_name: str
    session_id: str
    input_item_schema_b64: str


class NormalizedForecaster(Estimator):

    def __init__(self, session: Session, input_type: Type[BaseModelSubclass]):
        super().__init__(session, input_type)
        self.estimator_name = "NormalizedForecaster"
        self.create()

    def create(self):

        fields = pickle.dumps(self.input_type.model_fields)
        fields_b64 = base64.b64encode(fields).decode()

        request_data = EstimatorCreationRequest(
            estimator_name=self.estimator_name,
            session_id=self.session.session_id,
            input_item_schema_b64=fields_b64,
        )

        resp = requests.post(
            url=f"{env.API_URI}/estimators/create",
            headers=headers,
            json=request_data.model_dump()
        )

        response_json = resp.json()

        if 'estimator_id' in response_json:
            self.estimator_id = response_json['estimator_id']
            print(f"Estimator created with estimator_id: {response_json['estimator_id']}")
        else:
            raise ValueError("There was an error creating the estimator. Please try again.")

    def predict(self,
            item: BaseModelSubclass,
            start_dt: datetime = None,
            weeks: int = None,
            days: int = None,
            hours: int = None,
            note_length: Tuple[int, int] = (3, 5),
        ):

        if not isinstance(item, self.input_type):
            raise TypeError(f"Expect item to be an instance of {self.input_type}, but item has type {type(item)}")

        data = dict(
            estimator_id=self.estimator_id,
            item_data=item.model_dump(),
            start_dt=start_dt.timestamp(),
            weeks=weeks,
            days=days,
            hours=hours,
            note_length=note_length,
        )

        resp = requests.post(
            url=f"{env.API_URI}/estimators/predict",
            headers=headers,
            json=data,
        )

        response_json = resp.json()

        output = dict(
            notes=response_json['notes'],
            predictions=pd.read_json(StringIO(response_json['predictions']), orient='split'),
        )

        return output
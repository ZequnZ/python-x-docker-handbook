import json
import os
import pickle

import pandas as pd
import redis
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.tools import parse_obj_as

from data import venue_data_preprocessing
from model import Model

venue_data_columns = [
    "conversions_per_impression",
    "price_range",
    "rating",
    "popularity",
    "retention_rate",
]

app = FastAPI()

# Create the connection to Redis cache
r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=False,
)


def import_data_to_redis(data_path: str) -> None:
    """
       Put the venue data into Redis cache
       into the following key-value format:
        Key: venue_id(str)
        Values: a list with columns:
            ['conversions_per_impression', 'price_range',
            'rating', 'popularity', 'retention_rate']

    Args:
        data_path (str): path of the venue data file
    """

    # Read csv data as DataFrame
    venue_df = pd.read_csv(data_path)
    venue_df = venue_data_preprocessing(venue_df)

    # Use venue_id as key
    keys = venue_df.venue_id.values.tolist()
    # The rest columns as values
    values = venue_df.iloc[:, 1:].values.tolist()
    # Convert into key:value pairs & serialize the list
    data = {str(key): pickle.dumps(value) for key, value in zip(keys, values)}
    # Set the key:value pairs into Redis
    assert r.mset(data)


def get_data_from_redis(venue_ids: list) -> pd.DataFrame:
    """Given the list of venue ids, Get the venue data from Redis.

    Args:
        venue_ids (list): list of venue ids

    Returns:
        pd.DataFrame: venue data
    """
    data_lists = [pickle.loads(r.get(str(k))) for k in venue_ids]
    df = pd.DataFrame(data_lists, columns=venue_data_columns)
    df["venue_id"] = venue_ids
    return df


# Import venue data into Redis cache
import_data_to_redis("data/venues.csv")

# Initialize and load the model
model = Model()
model.model_loading(os.getenv("MODEL_DIRECTORY"))


class InputItem(BaseModel):
    """
    Define the data type of each input item
    """

    venue_id: int
    is_new_user: bool
    is_from_order_again: bool
    is_recommended: bool


class OutputItem(BaseModel):
    """
    Define the data type of each output item
    """

    venue_id: int
    score: float


class InputData(BaseModel):
    """
    Define the data type of input data - a list of input item
    """

    data: list[InputItem]

    class Config:
        arbitrary_types_allowed = True


class OutputData(BaseModel):
    """
    Define the data type of output data - a list of output item
    """

    data: list[OutputItem]


@app.get("/version/")
def return_model_version():
    """Simple route returning the model version

    Returns:
        JSON reponse:
            {
            'healtcheck': 'Everything OK!'
            }
    """
    return {"Model version": model.model_version}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
def healthcheck():
    """Simple route for healthcheck

    Returns:
        JSON reponse:
            {
            'healtcheck': 'Everything OK!'
            }
    """
    return {"healthcheck": "Everything OK!"}


@app.post("/prediction/")
async def prediction(data: InputData) -> OutputData:
    """Route for prediction given the input from request

    Args:
        data (InputData): request data consisting a user session

    Returns:
        OutputData: list of venue ids with corresponding scores
        JSON reponse:
            {
                "data":
                    [
                        {
                            "venue_id":1234, "score":0.333},
                            "venue_id":-4321, "score":0.777}
                    ]
            }
    """

    # input -> json
    input_json = jsonable_encoder(data)

    # json -> DataFrame
    df = pd.DataFrame(input_json["data"])

    # Get venue data from Redis
    venue_df = get_data_from_redis(df["venue_id"].values.tolist())

    # Merge data
    df = df.merge(venue_df, how="inner", on="venue_id")

    # Pop "venue_id" and turn it into a DataFrame for generating output
    res_df = df.pop("venue_id").to_frame()

    # Get prediction from the model
    res_df["score"] = model.model_prediction(df)

    # sort df based on score
    res_df.sort_values("score", ascending=False, inplace=True)

    # generate output_json
    output_json = (
        '{"data":' + res_df[["venue_id", "score"]].to_json(orient="records") + "}"
    )

    output = parse_obj_as(OutputData, json.loads(output_json))

    return output


if __name__ == "__main__":
    # Start the sever, set reload=True for testing
    uvicorn.run("main:app", host="0.0.0.0", port=8002, log_level="info", reload=False)

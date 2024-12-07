from pydantic import BaseModel

class AerialCorridorRead(BaseModel):
    "A class to read data from the Aerial Corridor table "
    
    url: str
    min_cell_level: int
    max_cell_level: int
    start_datetime: str
    end_datetime: str
    created_at: str
    updated_at: str

class AerialCorridorWrite(BaseModel):
    "A class to write data to the Aerial Corridor table "
    id: str
    url: str
    min_cell_level: int
    max_cell_level: int
    start_datetime: str
    end_datetime: str

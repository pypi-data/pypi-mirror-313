from pydantic import BaseModel, Field

class ImageGeneratorInput(BaseModel):
  query: str = Field(
      description="description of the image to generate."
  )
  language: str = Field(description="Language of the query. Default is 'it'", default="it")

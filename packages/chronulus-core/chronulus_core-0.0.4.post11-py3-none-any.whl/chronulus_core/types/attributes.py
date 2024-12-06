from typing import Any

from pydantic import BaseModel, Field
from PIL import Image


def get_pillow_image_type(ext: str):
    ext = "." + ext.lower().replace('.','')
    if ext in Image.registered_extensions():
        return Image.registered_extensions()[ext]
    else:
        return None


class ImageFromUrl(BaseModel):
    url: str
    type: str | None = Field(default=None)

    def model_post_init(self, __context: Any) -> None:
        if self.type is None:
            parts = self.url.split(".")
            if len(parts) == 1:
                raise ValueError(f"""Image type could not be determined for {self.url}. 
                Please add it in the `type` argument.""")
            else:
                ext = parts[-1]
                pillow_format = get_pillow_image_type(ext)
                if pillow_format is None:
                    raise ValueError(
                        f"""Image type was detected as '.{ext}' but this type is not supported.
                            If this is incorrect, please provide the correct type in the `type` argument.
                        """)
                else:
                    self.type = pillow_format

        else:
            pillow_format = get_pillow_image_type(self.type)
            if pillow_format is None:
                raise ValueError(
                    f"""Image type '{self.type}' was specified but this type is not supported.
                        If this is incorrect, please provide the correct type in the `type` argument.
                    """)
            else:
                self.type = pillow_format


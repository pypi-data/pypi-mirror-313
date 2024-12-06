import json
from typing import Optional

from bpkio_api.models.common import BaseResource, NamedModel


class TranscodingProfileId(BaseResource):
    pass


class TranscodingProfileIn(NamedModel):
    content: str
    tenantId: Optional[int]


class TranscodingProfile(TranscodingProfileIn, BaseResource):
    internalId: str
    
    @property
    def json_content(self):
        return json.loads(self.content)

    @property
    def layers(self):
        audio_layers = [a for a in self.json_content["audios"].keys() if a != "common"]
        video_layers = [v for v in self.json_content["videos"].keys() if v != "common"]
        return f"V:{len(video_layers)} A:{len(audio_layers)}"

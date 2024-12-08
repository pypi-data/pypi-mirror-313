from ...base_models.chatty_asset_model import ChattyAssetModel
from ...utils.types.identifier import StrObjectId

class FriendlyCodeForSource(ChattyAssetModel):
    """Used to map a code to a source for friendly urls"""
    friendly_code: str
    source_id: StrObjectId
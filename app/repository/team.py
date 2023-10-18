from app.model import Team
from app.repository.base import BaseRepository


class _TeamRepository(BaseRepository):
    ...

TeamRepository = _TeamRepository(model=Team)
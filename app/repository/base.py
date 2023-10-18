from fastapi.encoders import jsonable_encoder


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _query(self, session, *_, **kwargs):
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)

    def get(self, session, *_, **kwargs):
        return self._query(session, **kwargs).one_or_none()

    def get_many(self, session, *_, **kwargs):
        return self._query(session, **kwargs).all()
    
    def save(self, session, item, refresh=True):
        items = item if isinstance(item, list) else [item]
        session.add_all(items)
        session.commit()
        if refresh:
            for each in items:
                session.refresh(each)
        return item

    def create(self, session, obj_in):
        db_obj = self.model(**jsonable_encoder(obj_in))
        return self.save(session, db_obj)
    
    def update(self, session, db_obj, obj_in):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True, exclude={"id"})

        for field in update_data:
            if update_data[field] == getattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        return self.save(session, db_obj)
    
    def delete(self, session, db_obj):
        session.delete(db_obj)
        session.commit()
        return True

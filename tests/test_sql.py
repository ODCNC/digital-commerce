from odcnc.sql import *


class Brand(Model):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String)


def test_model():
    Brand.create_all()
    Brand(name='test').flush()
    assert Brand.get(1).name == 'test'

    Brand(name='test').flush()
    assert Brand.where(Brand.name == 'test').first().id == 1

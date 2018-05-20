from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:password@localhost/bili?charset=utf8')

Base = declarative_base()

Session = sessionmaker(bind=engine)

class Users(Base):
    """创建一个数据表：news"""
    __tablename__ = 'users_info'
    home_url = Column(String(200), nullable=False)
    mid = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    face_img = Column(String(200), nullable=True)
    curr_level = Column(Integer, nullable=True)
    sex = Column(String(20), nullable=True)
    regtime = Column(DateTime, nullable=True)
    follower = Column(Integer, nullable=True)
    following = Column(Integer, nullable=True)


class Insertitem(object):
    def __init__(self):
        self.session = Session()

    def add_item(self, new_item):
        """
        向数据表中插入一条数据
        :return:
        """

        self.session.add(new_item)
        try:
            self.session.commit()
        except:
            self.session.rollback()
        #print('成功插入一条用户信息！')


if __name__ == '__main__':
    #需要事先在mysql中创建好数据库bili
   Base.metadata.create_all(engine)  #用来创建数据表
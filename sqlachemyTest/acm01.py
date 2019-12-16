#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import easygui


engine = create_engine("mysql+pymysql://root:123456@10.0.0.20:3306/py13?charset=utf8",encoding="utf-8", max_overflow=5)

Base = declarative_base()

class Host(Base):
    __tablename__="Hosts"
    Host_id=Column(Integer,primary_key=True,autoincrement=True)
    Host_name=Column(String(50),unique=True)
    ip_attr=Column(String(15))
    group_id = Column(Integer, ForeignKey('groups.group_id'),default=1)
    group=relationship("group")
    def __repr__(self):
        print("%s-%s-%s"%(self.Host_id,self.Host_name,self.ip_attr))
class group(Base):
    __tablename__="groups"
    group_id=Column(Integer,primary_key=True,autoincrement=True)
    group_name=Column(String(50),unique=True)
    def __repr__(self):
        print("%s-%s"%(self.group_id,self.group_name))
'''
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
'''
SessionCls=sessionmaker(bind=engine)
session=SessionCls()
'''
b1=group(group_name="未分配组")
b2=group(group_name="proxy_group")
b3=group(group_name="lnmp_group")


h1=Host(Host_name='haporxy',ip_attr='172.16.1.10')
h2=Host(Host_name='lnmp',ip_attr='172.16.1.12',group_id=2)
h3=Host(Host_name='mysql',ip_attr='172.16.1.13',group_id=3)
h4=Host(Host_name='nfs',ip_attr='172.16.1.14')

session.add_all([b1,b2,b3,h1,h2,h3,h4])

'''
ret=session.query(Host).first()
ret.group
ret_dic={}
for i in ret:
    ret_dic.setdefault(i.Host_name,i.group.group_name)
print(ret_dic)
session.commit()
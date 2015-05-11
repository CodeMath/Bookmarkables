# -*- coding:utf-8 -*-
from apps import db
from datetime import datetime
class User(db.Model):
	id = db.Column(db.String(255), primary_key=True)
	date = db.Column(db.DateTime, default=datetime.utcnow())
	name = db.Column(db.String(200),default="북마커블")
	email = db.Column(db.String(255))
	# 비밀번호 입력 창
	master_key = db.Column(db.String(255), default="0")
	# 에디터로 선정된 사람들만 글작성
	editors = db.Column(db.String(20),default="0")
	# 추천사이트 등록 가능한 사람
	recommender = db.Column(db.String(20),default="0")

class develop(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_name = db.Column(db.String(255))
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('develops', cascade='all, delete-orphan'))

	complains = db.Column(db.Integer,default=0)

	# 해당 URL올리기
	subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	explain = db.Column(db.String(255))
	
	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())

class design(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_name = db.Column(db.String(255))
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('designs', cascade='all, delete-orphan'))

	complains = db.Column(db.Integer,default=0)

	# 해당 URL올리기
	subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	explain = db.Column(db.String(255))

	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())

class source(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_name = db.Column(db.String(255))
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('sources', cascade='all, delete-orphan'))

	complains = db.Column(db.Integer,default=0)

	# 해당 URL올리기
	subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	explain = db.Column(db.String(255))
	
	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())

class slideshare(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_name = db.Column(db.String(255))
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('slideshares', cascade='all, delete-orphan'))

	complains = db.Column(db.Integer,default=0)

	# 해당 URL올리기
	subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	explain = db.Column(db.String(255))
	
	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())	

class ppt(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_name = db.Column(db.String(255))
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('ppts', cascade='all, delete-orphan'))

	complains = db.Column(db.Integer,default=0)

	# 해당 URL올리기
	subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	explain = db.Column(db.String(255))
	
	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())	


class honey_news(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_name = db.Column(db.String(255))
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('honey_newss', cascade='all, delete-orphan'))

	complains = db.Column(db.Integer,default=0)

	# 해당 URL올리기
	subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	explain = db.Column(db.String(255))
	
	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())	


class recommend(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_name = db.Column(db.String(255))
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('recommends', cascade='all, delete-orphan'))

	complains = db.Column(db.Integer,default=0)

	# 해당 URL올리기
	subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	explain = db.Column(db.String(255))
	
	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())	
	
# 각 카테고리별 저장 정리
class saving(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# 각 유저의 아이디를 누적으로?
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('savings', cascade='all, delete-orphan'))
	
	user_name = db.Column(db.String(255),default="북마커블")
	
	re_subject = db.Column(db.String(255))
	urls = db.Column(db.String(255))
	re_explain = db.Column(db.String(255))

	category = db.Column(db.String(255),default="북마커블")

	comment = db.Column(db.String(255),default="북마크 저장!")

	tag1 = db.Column(db.String(255),default="")
	tag2 = db.Column(db.String(255),default="")

	date = db.Column(db.DateTime, default=datetime.utcnow())

class article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# 유저의 닉네임
	user_name = db.Column(db.String(255),default="북마커블")
	# 제목
	subject = db.Column(db.String(255))
	# 해당 내용
	val_text = db.Column(db.Text)
	# 카테고리
	category = db.Column(db.String(255))
	# 날짜
	date = db.Column(db.DateTime, default=datetime.utcnow())
	
# HTML 북마크 업로드 / 내보내기 전용.
class user_bookmark(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# 유저의 facebook 아이디 값(확인값)
	user_id = db.Column(db.String(255), db.ForeignKey(User.id))
	user = db.relationship('User', backref=db.backref('user_bookmarks', cascade='all, delete-orphan'))
	# 유저의 닉네임
	user_name = db.Column(db.String(255),default="북마커블")
	# 유저의 카테고리 등록
	category = db.Column(db.String(255),default="미 분류")
	# 제목
	subject = db.Column(db.String(255))
	# 링크 주소
	urls = db.Column(db.String(255))
	# 링크 설명 / 추후 수정가능?
	explain = db.Column(db.String(255),default="북마크 저장!")
	# 관련 링크 태그 / 추후 수정 가능하게끔
	tag1 = db.Column(db.String(255),default=" ")
	tag2 = db.Column(db.String(255),default=" ")
	# 저장한 북마크가 공개/비공개 인지 확인 값 (기본값은 0 으로 비공개 -> 공개로 바꾸면 "1" 로 바뀜)
	check_open = db.Column(db.String(10),default="0")
	# 시간 저장
	date = db.Column(db.DateTime, default=datetime.utcnow())




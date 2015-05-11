# -*- coding: utf-8 -*-
from datetime import datetime
# Flask 불러오기
from flask import Flask, url_for, render_template,redirect,session, jsonify, request, flash
# bs4를 이용해서 사용자들이 올린 HTMl 파일 읽기
from bs4 import BeautifulSoup
import urllib
# db와 facebook 로그인 정보 가져오기
from apps import app,db,facebook
# Model의 Table
from models import User, design, develop, slideshare, source, recommend, ppt, honey_news,\
saving, article, user_bookmark
# sqlalchemy 함수
from sqlalchemy import desc,func, or_
import codecs


# 메인화면
@app.route('/')
def main():
    main_data={}
    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 추천 사이트 받기
        row_recommend = recommend.query.count()
        main_data['recommend'] = recommend.query.filter_by( id = row_recommend )
        
        # 각각의 카테고리별 최신 데이터 받아오기 & 데이터 가져오기
        # 개발 부분
        row_develop=develop.query.count()
        main_data['develop'] = develop.query.filter_by( id = row_develop )
        
        # 디자인 부분
        row_design=design.query.count()
        main_data['design'] = design.query.filter_by( id = row_design )
        
        # 개발 소스 부분
        row_source=source.query.count()
        main_data['source'] = source.query.filter_by( id = row_source )
        
        # 슬라이드 쉐어 부분
        row_slideshare=slideshare.query.count()
        main_data['slideshare'] = slideshare.query.filter_by( id = row_slideshare )

        # 꿀뉴스 부분
        row_honey_news=honey_news.query.count()
        main_data['honey_news'] = honey_news.query.filter_by( id = row_honey_news )
        
        # PPT 부분
        row_ppt=ppt.query.count()
        main_data['ppt'] = ppt.query.filter_by( id = row_ppt )
        
        return render_template('main.html',
            year=datetime.now().year,
            data_send=data_send,
            main_data=main_data,
            row_recommend=row_recommend,
            row_develop=row_develop,
            row_design=row_design,
            row_source=row_source,
            row_slideshare=row_slideshare,
            row_honey_news=row_honey_news,
            row_ppt=row_ppt
            )

    # 추천 사이트 받기
    row_recommend = recommend.query.count()
    main_data['recommend'] = recommend.query.filter_by( id = row_recommend )
    
    # 각각의 카테고리별 최신 데이터 받아오기 & 데이터 가져오기
    # 개발 부분
    row_develop=develop.query.count()
    main_data['develop'] = develop.query.filter_by( id = row_develop )
    
    # 디자인 부분
    row_design=design.query.count()
    main_data['design'] = design.query.filter_by( id = row_design )
    
    # 개발 소스 부분
    row_source=source.query.count()
    main_data['source'] = source.query.filter_by( id = row_source )
    
    # 슬라이드 쉐어 부분
    row_slideshare=slideshare.query.count()
    main_data['slideshare'] = slideshare.query.filter_by( id = row_slideshare )

    # 꿀뉴스 부분
    row_honey_news=honey_news.query.count()
    main_data['honey_news'] = honey_news.query.filter_by( id = row_honey_news )
    
    # PPT 부분
    row_ppt=ppt.query.count()
    main_data['ppt'] = ppt.query.filter_by( id = row_ppt )
    
    return render_template('main.html',
        year=datetime.now().year,
        main_data=main_data,
        row_recommend=row_recommend,
        row_develop=row_develop,
        row_design=row_design,
        row_source=row_source,
        row_slideshare=row_slideshare,
        row_honey_news=row_honey_news,
        row_ppt=row_ppt
        )

# 북마커블 소개
@app.route('/intro')
def intro():
    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        return render_template('intro.html',year=datetime.now().year,data_send=data_send)

    return render_template('intro.html',year=datetime.now().year)

# 개발자 노트
@app.route('/develop_note')
def note():
    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        return render_template('dev_note.html',year=datetime.now().year,data_send=data_send)
    return render_template('dev_note.html',year=datetime.now().year)

# 각 사이트 리뷰 하는 게시판
@app.route('/note')
def write_note():
    dev_article={}

    if "facebook_session" in session:
        # 로그인 유저
        data_send=User.query.get(session['facebook_user_id'])
        
        # 글 가져오기
        dev_article['content']=article.query.order_by(desc(article.date))
    
        
        return render_template('note.html',
            year=datetime.now().year,
            data_send=data_send,
            dev_article=dev_article,
            )

    # 비로그인 유저
    # 글 가져오기
    dev_article['content']=article.query.order_by(desc(article.date))
    

    return render_template('note.html',
        year=datetime.now().year,
        dev_article=dev_article,
        )

# 사이트 리뷰 게시판에서 카테고리별로 보기
@app.route('/category/<cate>')
def category_note(cate):
    dev_article={}

    if "facebook_session" in session:
        # 로그인 유저
        data_send=User.query.get(session['facebook_user_id'])
        
        # 카테고리별 접근
        dev_article['content']=article.query.order_by(desc(article.date)).filter_by( category = cate)
        
        return render_template('note.html',
            year=datetime.now().year,
            data_send=data_send,
            dev_article=dev_article,
            )

    # 비로그인 유저
    # 카테고리별 접근
    dev_article['content']=article.query.order_by(desc(article.date)).filter_by( category = cate )

    return render_template('note.html',
        year=datetime.now().year,
        dev_article=dev_article,
        )


# 리뷰 게시판 보기/<cate>받기
@app.route('/reviews/<cate>')
def read_review(cate):
    dev_article={}
    number=cate
    if "facebook_session" in session:
        # 로그인 유저
        data_send=User.query.get(session['facebook_user_id'])
        
        # 해당 글 받아오기
        dev_article['now']=article.query.filter_by(id = cate )
        return render_template('article_note.html',year=datetime.now().year,data_send=data_send,dev_article=dev_article,number=number)

    # 비로그인 유저

    # 해당 글 받아오기
    dev_article['now']=article.query.filter_by(id = cate )
    return render_template('article_note.html',year=datetime.now().year,dev_article=dev_article,number=number)


# article 작성하는 섬머노트 에디터
@app.route('/write', methods=['GET','POST'])
def write():
    # 로그인한 사람만 접근
    if 'facebook_user_id' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 관리자만 접근 가능
        if data_send.id != '804911099582509' :
            flash(u"승인된 관리자만 글을 작성할 수 있습니다.")
            return redirect(url_for('main'))    
    
        data={}
        if request.method=='GET':
            set_tag1_design=set([designs.tag1 for designs in design.query.all()])
            set_tag2_design=set([designs.tag2 for designs in design.query.all()])
            set_tag1_develop=set([develops.tag1 for develops in develop.query.all()])
            set_tag2_develop=set([develops.tag2 for develops in develop.query.all()])
            set_tag1_source=set([sources.tag1 for sources in source.query.all()])
            set_tag2_source=set([sources.tag2 for sources in source.query.all()])
            set_tag1_slideshare=set([slideshares.tag1 for slideshares in slideshare.query.all()])
            set_tag2_slideshare=set([slideshares.tag2 for slideshares in slideshare.query.all()])
            set_tag1_ppt=set([ppts.tag1 for ppts in ppt.query.all()])
            set_tag2_ppt=set([ppts.tag2 for ppts in ppt.query.all()])
            set_tag1_honey_news=set([honey_newss.tag1 for honey_newss in honey_news.query.all()])
            set_tag2_honey_news=set([honey_newss.tag2 for honey_newss in honey_news.query.all()])
            # 중복 제외하고 tags에 테그 모음 담기
            data['tags']=set_tag1_design|set_tag2_design|set_tag1_develop|set_tag2_develop|set_tag1_source|set_tag2_source|set_tag1_slideshare|set_tag2_slideshare
        
            # 태그 1개 입력한 것 때문에 빈 칸 제거
            if "" in data['tags']:
                data['tags'].remove("")
            # summernote 부분
            return render_template('write_note.html',year=datetime.now().year,data_send=data_send,data=data)

        # 쓴 거 가져오는 부분
        subject=request.form['subject']
        val_text = request.form['text_val']
        # DB 업데이트
        update=article(
            user_name=data_send.name,
            subject=subject,
            val_text=val_text,
            category=request.form['iCheck']
            )


        db.session.add(update)
        db.session.commit()

        return redirect(url_for('write_note'))
    else:
        flash(u'정확하지 않은 접근입니다.')
        return redirect(url_for('main'))


# 제안하는 곳 및 항의하는 곳
@app.route('/contact')
def contact():
    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        return render_template('contact.html',year=datetime.now().year,data_send=data_send)
    return render_template('contact.html',year=datetime.now().year)

# 리스트 1단
@app.route('/list/<cate>')
def list(cate):
    if cate=="design":
        sections=1111
        content="design"
        rows=design.query.count()
        rows=rows-12
        data={}
        data['content']=design.query.order_by(desc(design.date)).filter(design.id>rows)
        # 테그 컬럼 가져오기
        set_tag1=set([designs.tag1 for designs in design.query.all()])
        set_tag2=set([designs.tag2 for designs in design.query.all()])
        # 테그 중복 제거 & 리스트화
        data['tags']=set_tag1|set_tag2
        if "" in data['tags']:
            data['tags'].remove("")
        
        

    elif cate=="develop":
        sections=2222
        content="develop"
        rows=develop.query.count()
        rows=rows-12
        data={}
        data['content']=develop.query.order_by(desc(develop.date)).filter(develop.id>rows)
        # 테그 컬럼 가져오기
        set_tag1=set([develops.tag1 for develops in develop.query.all()])
        set_tag2=set([develops.tag2 for develops in develop.query.all()])
        # 테그 중복 제거 & 리스트화
        data['tags']=set_tag1|set_tag2
        if "" in data['tags']:
            data['tags'].remove("")

    elif cate=="source":
        sections=3333
        content="source"
        rows=source.query.count()
        rows=rows-12
        data={}
        data['content']=source.query.order_by(desc(source.date)).filter(source.id>rows)
        # 테그 컬럼 가져오기
        set_tag1=set([sources.tag1 for sources in source.query.all()])
        set_tag2=set([sources.tag2 for sources in source.query.all()])
        # 테그 중복 제거 & 리스트화
        data['tags']=set_tag1|set_tag2
        if "" in data['tags']:
            data['tags'].remove("")
        

    elif cate=="slideshare":
        sections=4444
        content="slideshare"
        rows=slideshare.query.count()
        rows=rows-12
        data={}
        data['content']=slideshare.query.order_by(desc(slideshare.date)).filter(slideshare.id>rows)
        # 테그 컬럼 가져오기
        set_tag1=set([slideshares.tag1 for slideshares in slideshare.query.all()])
        set_tag2=set([slideshares.tag2 for slideshares in slideshare.query.all()])
        # 테그 중복 제거 & 리스트화
        data['tags']=set_tag1|set_tag2
        if "" in data['tags']:
            data['tags'].remove("")

        # 로그인 유저
        if "facebook_session" in session:
            data_send=User.query.get(session['facebook_user_id'])
            return render_template('lists.html',year=datetime.now().year,data=data,sections=sections,content=content,data_send=data_send)
        # 비로그인 유저
        return render_template('lists.html',year=datetime.now().year,data=data,sections=sections,content=content)

    
    elif cate=="ppt":
        sections=5555
        content="ppt"
        rows=ppt.query.count()
        rows=rows-12
        data={}
        data['content']=ppt.query.order_by(desc(ppt.date)).filter(ppt.id>rows)
        # 테그 컬럼 가져오기
        set_tag1=set([ppts.tag1 for ppts in ppt.query.all()])
        set_tag2=set([ppts.tag2 for ppts in ppt.query.all()])
        # 테그 중복 제거 & 리스트화
        data['tags']=set_tag1|set_tag2
        if "" in data['tags']:
            data['tags'].remove("")

    elif cate=="honey_news":
        sections=6666
        content="honey_news"
        rows=honey_news.query.count()
        rows=rows-12
        data={}
        data['content']=honey_news.query.order_by(desc(honey_news.date)).filter(honey_news.id>rows)
        # 테그 컬럼 가져오기
        set_tag1=set([honey_newss.tag1 for honey_newss in honey_news.query.all()])
        set_tag2=set([honey_newss.tag2 for honey_newss in honey_news.query.all()])
        # 테그 중복 제거 & 리스트화
        data['tags']=set_tag1|set_tag2
        if "" in data['tags']:
            data['tags'].remove("")

    elif cate=="recommend":
        sections=7777
        content="recommend"
        rows=recommend.query.count()
        rows=rows-12
        data={}
        data['content']=recommend.query.order_by(desc(recommend.date)).filter(recommend.id>rows)
        # 테그 컬럼 가져오기
        set_tag1=set([recommends.tag1 for recommends in recommend.query.all()])
        set_tag2=set([recommends.tag2 for recommends in recommend.query.all()])
        # 테그 중복 제거 & 리스트화
        data['tags']=set_tag1|set_tag2
        if "" in data['tags']:
            data['tags'].remove("")        

    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        return render_template('lists.html',year=datetime.now().year,data=data,sections=sections,content=content,data_send=data_send)    

    return render_template('lists.html',year=datetime.now().year,data=data,sections=sections,content=content)



# 각 메인 카테고리별 상세보기 페이지
# design 상세보기
@app.route('/design/<cate>')
def content_design(cate):
        
    sections=1111
    data_view={}    
    data_view['content']=design.query.filter_by(id = cate)
    if 'facebook_session' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 저장한지 체크
        check_saving=[]
        check_saving = saving.query.filter_by(user_id = session['facebook_user_id']).all()
        # 해당 부분의 url값 불러오기
        check_from_db = design.query.get(cate)
        for each in check_saving:
            if each.urls == check_from_db.urls:
                pre_ups="true"
                return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,pre_ups=pre_ups)
        # 없으면
        return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send)
    return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections)
    

# develop 상세보기
@app.route('/develop/<cate>')
def content_develop(cate):
    
    sections=2222
    data_view={}    
    data_view['content']=develop.query.filter_by(id = cate)
    if 'facebook_session' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 저장한지 체크
        check_saving=[]
        check_saving = saving.query.filter_by(user_id = session['facebook_user_id']).all()
        # 해당 부분의 url값 불러오기
        check_from_db = develop.query.get(cate)
        for each in check_saving:
            if each.urls == check_from_db.urls:
                pre_ups="true"
                return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,pre_ups=pre_ups)
        # 없으면
        return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send)
    return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections)

    
# source 상세보기
@app.route('/source/<cate>')
def content_source(cate):
    
    sections=3333
    data_view={}    
    data_view['content']=source.query.filter_by(id = cate)
    if 'facebook_session' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 저장한지 체크
        check_saving=[]
        check_saving = saving.query.filter_by(user_id = session['facebook_user_id']).all()
        # 해당 부분의 url값 불러오기
        check_from_db = source.query.get(cate)
        for each in check_saving:
            if each.urls == check_from_db.urls:
                pre_ups="true"
                return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,pre_ups=pre_ups)
        # 없으면
        return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send)
    
    return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections)

    
# slideshare 상세보기 /og:image이
@app.route('/slideshare/<cate>')
def content_slideshare(cate):
    
    sections=4444
    data_view={}    
    data_view['content']=slideshare.query.filter_by(id = cate)
    # 해당 이미지 가져오기
    query_slideshare = slideshare.query.get( cate )
    urls_slideshare = str(query_slideshare.urls)
    page_slideshare = urllib.urlopen( urls_slideshare ).read()
    soup_slideshare = BeautifulSoup(page_slideshare)
    imgs_slideshare = soup_slideshare.find('meta',{'property':'og:image'})['content']
    


    if 'facebook_session' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 저장한지 체크
        check_saving=[]
        check_saving = saving.query.filter_by(user_id = session['facebook_user_id']).all()
        # 해당 부분의 url값 불러오기
        check_from_db = slideshare.query.get(cate)
        for each in check_saving:
            if each.urls == check_from_db.urls:
                pre_ups="true"
                return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,imgs_slideshare=imgs_slideshare,pre_ups=pre_ups)
        # 없으면
        return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,imgs_slideshare=imgs_slideshare)
    
    return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,imgs_slideshare=imgs_slideshare)

    
# ppt 상세보기
@app.route('/ppt/<cate>')
def content_ppt(cate):
    
    sections=5555
    data_view={}    
    data_view['content']=ppt.query.filter_by(id = cate)
    if 'facebook_session' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 저장한지 체크
        check_saving=[]
        check_saving = saving.query.filter_by(user_id = session['facebook_user_id']).all()
        # 해당 부분의 url값 불러오기
        check_from_db = ppt.query.get(cate)
        for each in check_saving:
            if each.urls == check_from_db.urls:
                pre_ups="true"
                return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,pre_ups=pre_ups)
        # 없으면
        return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send)
    
    return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections)

    
# honey_news 상세보기
@app.route('/honey_news/<cate>')
def content_honey_news(cate):
    
    sections=6666
    data_view={}    
    data_view['content']=honey_news.query.filter_by(id = cate)
    if 'facebook_session' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 저장한지 체크
        check_saving=[]
        check_saving = saving.query.filter_by(user_id = session['facebook_user_id']).all()
        # 해당 부분의 url값 불러오기
        check_from_db = honey_news.query.get(cate)
        for each in check_saving:
            if each.urls == check_from_db.urls:
                pre_ups="true"
                return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,pre_ups=pre_ups)
        # 없으면
        return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send)
    
    return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections)

    
# recommend 상세보기
@app.route('/recommend/<cate>')
def content_recommend(cate):
    
    sections=7777
    data_view={}    
    data_view['content']=recommend.query.filter_by(id = cate)
    if 'facebook_session' in session:
        data_send=User.query.get(session['facebook_user_id'])
        # 저장한지 체크
        check_saving=[]
        check_saving = saving.query.filter_by(user_id = session['facebook_user_id']).all()
        # 해당 부분의 url값 불러오기
        check_from_db = recommend.query.get(cate)
        for each in check_saving:
            if each.urls == check_from_db.urls:
                pre_ups="true"
                return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send,pre_ups=pre_ups)
        # 없으면
        return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections,data_send=data_send)
    
    return render_template('contents.html',year=datetime.now().year,data_view=data_view,sections=sections)

    
# 제보하기 기능
@app.route('/sending', methods=['GET','POST'])
def sending():
    
    data={}
    
    if request.method=='GET':
        set_tag1_design=set([designs.tag1 for designs in design.query.all()])
        set_tag2_design=set([designs.tag2 for designs in design.query.all()])
        set_tag1_develop=set([develops.tag1 for develops in develop.query.all()])
        set_tag2_develop=set([develops.tag2 for develops in develop.query.all()])
        set_tag1_source=set([sources.tag1 for sources in source.query.all()])
        set_tag2_source=set([sources.tag2 for sources in source.query.all()])
        set_tag1_slideshare=set([slideshares.tag1 for slideshares in slideshare.query.all()])
        set_tag2_slideshare=set([slideshares.tag2 for slideshares in slideshare.query.all()])
        set_tag1_ppt=set([ppts.tag1 for ppts in ppt.query.all()])
        set_tag2_ppt=set([ppts.tag2 for ppts in ppt.query.all()])
        set_tag1_honey_news=set([honey_newss.tag1 for honey_newss in honey_news.query.all()])
        set_tag2_honey_news=set([honey_newss.tag2 for honey_newss in honey_news.query.all()])
        # 중복 제외하고 tags에 테그 모음 담기
        data['tags']=set_tag1_design|set_tag2_design|set_tag1_develop|set_tag2_develop|set_tag1_source|set_tag2_source|set_tag1_slideshare|set_tag2_slideshare|set_tag1_ppt|set_tag2_ppt|set_tag1_honey_news|set_tag2_honey_news
        
        # 태그 1개 입력한 것 때문에 빈 칸 제거
        if "" in data['tags']:
            data['tags'].remove("")

        if 'facebook_session' in session:
            data_send=User.query.get(session['facebook_user_id'])
            return render_template('sending.html',year=datetime.now().year,data=data,data_send=data_send)

        return render_template('sending.html',year=datetime.now().year,data=data)

    # validato
    if request.form['iCheck'] == None or request.form['subject'] == None or request.form['urls'] == None or request.form['explain'] == None :
            flash(u"빠진 곳이 없나 확인해주세요! 태그는 최소 1개 이상! 2개까지만 적용 가능해요!")
            return redirect(url_for('sending'))

    l_tag = request.form.getlist('tags')
    n = len(l_tag)
    tag=[]
    # 태그 리스트가 0개라면 다시.
    if (n == 0) or (n > 2):
        flash(u"태그를 입력해주세요! 1개~2개 까지!")
        return redirect(url_for('sending'))
    elif n == 1:
        tag.append(l_tag[0])
        tag.append("")
    else:
        tag.append(l_tag[0])
        tag.append(l_tag[1])
    
    # 사용자 확인 / Master 아이디
    user_log=User.query.get(session['facebook_user_id'])

    # 공개로 저장할 시, 바로 각 Table에 저장
    
    # 서버 업데이트 
    if request.form['iCheck']=="develop":
        if develop.query.filter_by( urls = request.form['urls'] ).count() > 0 :
            flash(u"Ops~! 이미 등록된 URL인가봐요 ㅠ 확인해볼까요?")
            return redirect(url_for('sending'))
        else:
            update=develop(
                    subject=request.form['subject'],
                    urls=request.form['urls'],
                    explain=request.form['explain'],
                    user_name=user_log.name,
                    user_id=session['facebook_user_id'],
                    tag1=tag[0],
                    tag2=tag[1]
                    )

    elif request.form['iCheck']=="design":
        if design.query.filter_by( urls = request.form['urls'] ).count() > 0 :
            flash(u"Ops~! 이미 등록된 URL인가봐요 ㅠ 확인해볼까요?")
            return redirect(url_for('sending'))
        else:
            update=design(
                    subject=request.form['subject'],
                    urls=request.form['urls'],
                    explain=request.form['explain'],
                    user_name=user_log.name,
                    user_id=session['facebook_user_id'],
                    tag1=tag[0],
                    tag2=tag[1]
                    )

    elif request.form['iCheck']=="slideshare":
        if slideshare.query.filter_by( urls = request.form['urls'] ).count() > 0 :
            flash(u"Ops~! 이미 등록된 URL인가봐요 ㅠ 확인해볼까요?")
            return redirect(url_for('sending'))
        else:
            update=slideshare(
                    subject=request.form['subject'],
                    urls=request.form['urls'],
                    explain=request.form['explain'],
                    user_name=user_log.name,
                    user_id=session['facebook_user_id'],
                    tag1=tag[0],
                    tag2=tag[1]
                    )

    elif request.form['iCheck']=="source":
        if source.query.filter_by( urls = request.form['urls'] ).count() > 0 :
            flash(u"Ops~! 이미 등록된 URL인가봐요 ㅠ 확인해볼까요?")
            return redirect(url_for('sending'))
        else:
            update=source(
                    subject=request.form['subject'],
                    urls=request.form['urls'],
                    explain=request.form['explain'],
                    user_name=user_log.name,
                    user_id=session['facebook_user_id'],
                    tag1=tag[0],
                    tag2=tag[1]
                    )

    elif request.form['iCheck']=="ppt":
        if ppt.query.filter_by( urls = request.form['urls'] ).count() > 0 :
            flash(u"Ops~! 이미 등록된 URL인가봐요 ㅠ 확인해볼까요?")
            return redirect(url_for('sending'))
        else:
            update=ppt(
                    subject=request.form['subject'],
                    urls=request.form['urls'],
                    explain=request.form['explain'],
                    user_name=user_log.name,
                    user_id=session['facebook_user_id'],
                    tag1=tag[0],
                    tag2=tag[1]
                    )

    elif request.form['iCheck']=="honey_news":
        if honey_news.query.filter_by( urls = request.form['urls'] ).count() > 0 :
            flash(u"Ops~! 이미 등록된 URL인가봐요 ㅠ 확인해볼까요?")
            return redirect(url_for('sending'))
        else:
            update=honey_news(
                    subject=request.form['subject'],
                    urls=request.form['urls'],
                    explain=request.form['explain'],
                    user_name=user_log.name,
                    user_id=session['facebook_user_id'],
                    tag1=tag[0],
                    tag2=tag[1]
                    )

    else:
        pass


    db.session.add(update)
    db.session.commit()
    flash(u"유용한 링크를 공유해주셔서 감사합니다!")

    return redirect(url_for('sending'))



# 해당링크 세이브 기능 (ajax)
@app.route('/saving',methods=['POST'])
def saving_data():
    # 데이터 받기
    urls = request.form.get('urls')
    subject = request.form.get('subject')
    explain = request.form.get('explain')
    comment = request.form.get('comment')
        
    category = request.form.get('category')

    user_name = request.form.get('user_name')
    tag1 = request.form.get('tag1')
    tag2 = request.form.get('tag2')

        

     # Table check & id 값으로 해당 쿼리 찾기
    update_saving=saving(
        user_id=session['facebook_user_id'],
        re_subject=subject,
        urls=urls,
        re_explain=explain,
        comment=comment,
        category=category,
        user_name=user_name,
        tag1=tag1,
        tag2=tag2
        )
    db.session.add(update_saving)
    db.session.commit()        
    
    upload=":"
    
    return jsonify(upload=upload)



# 마이페이지 관련
# 마이페이지의 북마크 저장한것 삭제하기. (ajax)
@app.route('/delete',methods=['POST'])
def delete_comment():
    # 삭제할 수 있는 해당 쿼리 부분 불러오기
    del_comment = request.form.get('del_id',0,type=int)
    # 해당 쿼리 부분 불러오는 부분
    del_query = saving.query.get(del_comment)

    # 삭제를 하기 위해서, 유저의 마스터 키 값과 비교
    data_send=User.query.get(session['facebook_user_id'])

    # 마스터키와 입력한 값이 같으면 삭제 성공.
    if request.form.get('passwords') == data_send.master_key:
        # 해당 쿼리 부분을 삭제
        db.session.delete(del_query)
        db.session.commit()
        # 삭제 완료
        dels="yes"
        return jsonify(dels=dels)
    else:
        dels="no"
        return jsonify(dels=dels)

    
# 마이페이지의 코멘트 수정하기 기능(ajax)
@app.route('/comment',methods=['POST'])
def re_comment():
    # 수정할 부분의 쿼리 부분을 불러옴.
    re_saving_comment = saving.query.get(request.form.get('re_id',0,type=int))

    # 수정해야할 부분의 쿼리부분의 comment부분을 불러와서 request로 교체
    re_saving_comment.comment = request.form.get('comment')
        
    # # 수정 완료 후, DB 업데이트 
    db.session.add(re_saving_comment)
    db.session.commit()        
        
    fixed="yes"

    return jsonify(fixed=fixed)


# 마이페이지
@app.route('/mypage/<cate>',methods=['GET','POST'])
def mypage(cate):
    # 미인증 확인용
    re_pass="미인증"
    # 마스터 확인용
    masters=cate
    # 현재 페이지 cate값의 User 테이블의 쿼리 값 확인용
    data_send=User.query.get(cate)
    name=data_send.name
    # 로그인 유저 체크
    if 'facebook_user_id' in session:
        # 로그인 유저 이면서 마스터 유저
        if masters == session['facebook_user_id']:
            # 저장된 북마크 불러옴
            list_data={}
            list_data['bookmark']=saving.query.order_by(desc(saving.date)).filter(saving.user_id == cate)
            
            # 에디터일 경우
            if (data_send.editors == "10") or (data_send.editors == "Master") :
                editors = "True"
                # 추천 사이트 제보가능한 사람
                if (data_send.recommender == "10") or (data_send.recommender == "Master") :
                    recommender = "True"
                    # 추천 사이트 제보 경우
                    return render_template('mypage.html',
                        year=datetime.now().year,
                        masters=masters,
                        data_send=data_send,
                        list_data=list_data,
                        editors=editors,
                        recommender=recommender,
                        name=name
                        )
                # 에디터인 경우
                return render_template('mypage.html',
                    year=datetime.now().year,
                    masters=masters,
                    data_send=data_send,
                    list_data=list_data,
                    editors=editors,
                    name=name
                    )
            # 일반 마스터 유저
            return render_template('mypage.html',
                year=datetime.now().year,
                masters=masters,
                data_send=data_send,
                list_data=list_data,
                name=name
                )
        # 로그인 유저 이지만, 마스터유저가 아닌 경우
        else:
            return render_template('mypage.html',year=datetime.now().year, re_pass=re_pass,data_send=data_send,name=name)    
    # 비로그인 유저
    else:
        return render_template('mypage.html',year=datetime.now().year, re_pass=re_pass, masters=masters,name=name)



# 개발 중인 부분
@app.route('/course')
def course():
    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        return render_template('course.html',year=datetime.now().year,data_send=data_send)
    return render_template('course.html',year=datetime.now().year)


@app.route('/course/<cate>')
def active_course(cate):
    course = cate
    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        return render_template('active_course.html',year=datetime.now().year
            ,data_send=data_send
            ,course=course
            )

    return render_template('active_course.html',year=datetime.now().year
        ,course=course
        )






# 추천 사용자 제보 화면[수정중]
@app.route('/recommender',methods=['GET','POST'])
def recommender():
    flash(u"수정중")
    return redirect(url_for('main'))

# 개인 북마크 화면
@app.route('/bookmarks/<ids>')
def bookmarks(ids):
    if "facebook_session" in session:
        data_send=User.query.get(session['facebook_user_id'])
        return render_template('bookmarks.html',year=datetime.now().year,data_send=data_send)

    return render_template('bookmarks.html',year=datetime.now().year)

# 개인 북마크 - 카테고리 생성하기
@app.route('/m_category')
def m_category():
    
    category = request.form['category']

    return jsonify(category=category)

# 업로드시, HTML파일인지 체크하기
app.config['ALLOWED_EXTENSIONS'] = set(['html'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# 브라우저의 북마크에서 HTML파일로 내보낸 것을 bs4로 파씽하기 
@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        if "facebook_session" in session:
            data_send=User.query.get(session['facebook_user_id'])
            return render_template('upload.html',year=datetime.now().year,data_send=data_send)
        else:
            flash(u"로그인 유저만 이용할 수 있습니다.")
            return redirect(url_for('main'))
    
    data_send=User.query.get(session['facebook_user_id'])
    
    # 공지 확인용 (bot제거)
    if request.form['iCheck'] != "yes":
        flash(u"공지를 확인하시고 '예'를 클릭해주세요!")
        return redirect(url_for('upload'))

    # 북마크를 불러들임. HTML 확장자인지 체크 함수 불러오
    lists = request.files['file']
    if lists and allowed_file(lists.filename):
    
        bookmarks = lists.stream.read()

        # soup형태로 만들기
        soup = BeautifulSoup(bookmarks)

    else:
        flash(u"HTMl 파일만 업로드해주세요!")
        return redirect(url_for('upload'))

    # 빈 리스트
    upload_bookmarks=[]
    
    # 트리 항해
    for link in soup.find_all('a'):
        # 유해사이트인지 검토하기
        if (link.get('href')[0:18] == "http://www.ilbe.com") : pass
        else:
            # 빈 리스트 만들기/for문이 돌 때 마다 빈 리스트 만들서어 0,1에 찍고 / append시키고 나서 다시 빈리스트....
            mic_data=[link.string,link.get('href')]
            upload_bookmarks.append(mic_data)
    
    # db 저장   
    for each in upload_bookmarks:
        upload_user_bookmark = user_bookmark(
            user_id=session['facebook_user_id'],
            user_name=session['facebook_name'],
            subject=each[0],
            urls=each[1]
            )
        # 이거보다 더 빠르게 할 수 없나? 생각해보기 [업그레이드 대상]
        db.session.add(upload_user_bookmark)
        
    db.session.commit()     

    flash(u"업로드 완료! 고생하셨어요. 마이페이지에서 확인해보세요!")
    return redirect(url_for('main'))

# 개발 중인 부분 끝



# Tag 검색기 부분
@app.route('/search',methods=['GET','POST'])
def searches():
    if "facebook_session" in session:

        data={}
        data_send=User.query.get(session['facebook_user_id'])
        # Tag 부분 보내기 / 검색하기 전
        if request.form == 'GET':
            set_tag1_design=set([designs.tag1 for designs in design.query.all()])
            set_tag2_design=set([designs.tag2 for designs in design.query.all()])
            set_tag1_develop=set([develops.tag1 for develops in develop.query.all()])
            set_tag2_develop=set([develops.tag2 for develops in develop.query.all()])
            set_tag1_source=set([sources.tag1 for sources in source.query.all()])
            set_tag2_source=set([sources.tag2 for sources in source.query.all()])
            set_tag1_slideshare=set([slideshares.tag1 for slideshares in slideshare.query.all()])
            set_tag2_slideshare=set([slideshares.tag2 for slideshares in slideshare.query.all()])
            set_tag1_ppt=set([ppts.tag1 for ppts in ppt.query.all()])
            set_tag2_ppt=set([ppts.tag2 for ppts in ppt.query.all()])
            set_tag1_honey_news=set([honey_newss.tag1 for honey_newss in honey_news.query.all()])
            set_tag2_honey_news=set([honey_newss.tag2 for honey_newss in honey_news.query.all()])
            set_tag1_recommend=set([recommends.tag1 for recommends in recommend.query.all()])
            set_tag2_recommend=set([recommends.tag2 for recommends in recommend.query.all()])
            # 중복 제외하고 tags에 테그 모음 담기
            data['tags']=set_tag1_design|set_tag2_design|set_tag1_develop|set_tag2_develop|set_tag1_source\
            |set_tag2_source|set_tag1_slideshare|set_tag2_slideshare|set_tag1_ppt|set_tag2_ppt\
            |set_tag1_honey_news|set_tag2_honey_news|set_tag1_recommend|set_tag2_recommend
        
            # 태그 1개 입력한 것 때문에 빈 칸 제거
            if "" in data['tags']:
                data['tags'].remove("")

            return render_template('search.html',year=datetime.now().year,data_send=data_send,data=data)
        # 검색하고 후,
        else:
            # 유저 Tag 검색 요청
            tags = request.form.getlist('tags')
            design_dict={}
            for each in tags:
                dic_1 = design.query.order_by(desc(design.date)).filter(design.tag1 == each)
                dic_2 = design.query.order_by(desc(design.date)).filter(design.tag2 == each)
                design_dict[each]=dic_1
                design_dict[each]=dic_2
            

            develop_dict={}
            for each in tags:
                dic_1=[]
                dic_2=[]
                dic_1=develop.query.order_by(desc(develop.date)).filter(develop.tag1 == each)
                dic_2=develop.query.order_by(desc(develop.date)).filter(develop.tag2 == each)
                develop_dict[each]=dic_1
                develop_dict[each]=dic_2
            
 
            source_dict={}
            for each in tags:
                dic_1=[]
                dic_2=[]
                dic_1=source.query.order_by(desc(source.date)).filter(source.tag1 == each)
                dic_2=source.query.order_by(desc(source.date)).filter(source.tag2 == each)
                source_dict[each]=dic_1 
                source_dict[each]=dic_2   
            
 
            slideshare_dict={}
            for each in tags:
                dic_1=[]
                dic_2=[]
                dic_1=slideshare.query.order_by(desc(slideshare.date)).filter(slideshare.tag1 == each)
                dic_2=slideshare.query.order_by(desc(slideshare.date)).filter(slideshare.tag2 == each)
                slideshare_dict[each]=dic_1
                slideshare_dict[each]=dic_2
            

            ppt_dict={}
            for each in tags:
                dic_1=[]
                dic_2=[]
                dic_1=ppt.query.order_by(desc(ppt.date)).filter(ppt.tag1 == each)
                dic_2=ppt.query.order_by(desc(ppt.date)).filter(ppt.tag2 == each)
                ppt_dict[each]=dic_1
                ppt_dict[each]=dic_2  
            

            honey_news_dict={}
            for each in tags:
                dic_1=[]
                dic_2=[]
                dic_1=honey_news.query.order_by(desc(honey_news.date)).filter(honey_news.tag1 == each)
                dic_2=honey_news.query.order_by(desc(honey_news.date)).filter(honey_news.tag2 == each)
                honey_news_dict[each]=dic_1
                honey_news_dict[each]=dic_2
            

            recommend_dict={}
            for each in tags:
                dic_1=[]
                dic_2=[]
                dic_1=recommend.query.order_by(desc(recommend.date)).filter(recommend.tag1 == each)
                dic_2=recommend.query.order_by(desc(recommend.date)).filter(recommend.tag2 == each)
                recommend_dict[each]=dic_1
                recommend_dict[each]=dic_2
            
                
            
            # Tag 검색기 부분 다시 전송
            set_tag1_design=set([designs.tag1 for designs in design.query.all()])
            set_tag2_design=set([designs.tag2 for designs in design.query.all()])
            set_tag1_develop=set([develops.tag1 for develops in develop.query.all()])
            set_tag2_develop=set([develops.tag2 for develops in develop.query.all()])
            set_tag1_source=set([sources.tag1 for sources in source.query.all()])
            set_tag2_source=set([sources.tag2 for sources in source.query.all()])
            set_tag1_slideshare=set([slideshares.tag1 for slideshares in slideshare.query.all()])
            set_tag2_slideshare=set([slideshares.tag2 for slideshares in slideshare.query.all()])
            set_tag1_ppt=set([ppts.tag1 for ppts in ppt.query.all()])
            set_tag2_ppt=set([ppts.tag2 for ppts in ppt.query.all()])
            set_tag1_honey_news=set([honey_newss.tag1 for honey_newss in honey_news.query.all()])
            set_tag2_honey_news=set([honey_newss.tag2 for honey_newss in honey_news.query.all()])
            set_tag1_recommend=set([recommends.tag1 for recommends in recommend.query.all()])
            set_tag2_recommend=set([recommends.tag2 for recommends in recommend.query.all()])

            # 중복 제외하고 tags에 테그 모음 담기
            data['tags']=set_tag1_design|set_tag2_design|set_tag1_develop|set_tag2_develop|set_tag1_source\
            |set_tag2_source|set_tag1_slideshare|set_tag2_slideshare|set_tag1_ppt|set_tag2_ppt|set_tag1_honey_news\
            |set_tag2_honey_news|set_tag1_recommend|set_tag2_recommend
        
            # 태그 1개 입력한 것 때문에 빈 칸 제거
            if "" in data['tags']:
                data['tags'].remove("")

            return render_template('search.html',
                year=datetime.now().year,
                data_send=data_send,
                data=data,
                recommend_dict=recommend_dict,
                honey_news_dict=honey_news_dict,
                ppt_dict=ppt_dict,
                design_dict=design_dict,
                develop_dict=develop_dict,
                source_dict=source_dict,
                slideshare_dict=slideshare_dict,
                tags=tags
                )

    # 비로그인 유저 불가
    flash(u'로그인 해주세요! (>3<)')
    return redirect(url_for('main'))


# 미인증 사용자 비밀번호 체크
@app.route('/checking',methods=['GET','POST'])
def checking():
    # 비밀번호 넣은 값
    intro_pass=request.form['var_pass']
    # 북마크 유저의 id값
    mypage_value=request.form['sections']
    # 북마크 유저의 id값을 통해 쿼리 불러옴
    data_send=User.query.get(mypage_value)
    # post방식일 때
    if request.method == 'POST':
        # 비번과 일치여부 확인
        if data_send.master_key == intro_pass:
            # 저장된 북마크 불러옴
            list_data={}
            list_data['bookmark']=saving.query.order_by(desc(saving.date)).filter( saving.user_id == mypage_value )

            return render_template('mypage.html',
                year=datetime.now().year,
                list_data=list_data,
                data_send=data_send
                )
        else:
            flash(u"접근 비밀번호가 틀렸습니다.")
            return redirect(url_for('main'))
    
    flash(u"Error 발생! 다시 접근해주세요!")
    return redirect(url_for('main'))

# 북마크 유저의 비밀번호 셋팅(ajax)
@app.route('/pass_setting',methods=['POST'])
def pass_setting():
    
    # 유저가 입력한 비밀번호
    user_pass = request.form.get('set_pass')
    # 해당 유저의 쿼리를 불러옴
    update_master_key = User.query.get(request.form.get('set_id'))
    # 업데이트하기
    update_master_key.master_key=user_pass

    db.session.add(update_master_key)
    db.session.commit()        
    pass_set="true"
    return jsonify(pass_set=pass_set)


# 닉네임 수정하기 (ajax)
@app.route('/nic_set',methods=['POST'])
def nic_set():
    # 유저가 설정한 닉네임값
    nic_set = request.form.get('nic_set')
    # 해당 유저의 쿼리를 불러옴
    update_nicname = User.query.get(request.form.get('set_id'))
    # 업데이트 실행
    update_nicname.name=nic_set

    db.session.add(update_nicname)
    db.session.commit()        
    nic_up="true"
    return jsonify(nic_up=nic_up)


# 리스트에 넘겨줄 것들(ajax)
# json으로 DB갯수 파악(다시 json형태로 전송)
@app.route('/rows')
def rows():
    if request.args.get('sections',0,type=int) == 1111:
        rows=design.query.count()
    elif request.args.get('sections',0,type=int) == 2222:
        rows=develop.query.count()
    elif request.args.get('sections',0,type=int) == 3333:
        rows=source.query.count()
    elif request.args.get('sections',0,type=int) == 4444:
        rows=slideshare.query.count()
    elif request.args.get('sections',0,type=int)== 5555:
        rows=ppt.query.count()
    elif request.args.get('sections',0,type=int)== 6666:
        rows=honey_news.query.count()
    elif request.args.get('sections',0,type=int)== 7777:
        rows=recommend.query.count()
    else:
        pass
    return jsonify(rows=rows)

# [앨범형]json으로 data 넘겨주기
@app.route('/more')
def getdata():
    number = request.args.get('number',0,type=int)
    id=""
    subject=""
    urls=""
    explain=""
    user_name=""
    user_id=""
    tag1=""
    tag2=""

    getdata={}
    if request.args.get('sections',0,type=int) == 1111:
        getdata['content']=design.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int) == 2222:
        getdata['content']=develop.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int) == 3333:
        getdata['content']=source.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 4444:
        getdata['content']=slideshare.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 5555:
        getdata['content']=ppt.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 6666:
        getdata['content']=honey_news.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 7777:
        getdata['content']=recommend.query.filter_by(id = number)
    else:
        pass

    for item in getdata.get('content'):
        id=item.id
        subject=item.subject
        explain=item.explain
        user_id=item.user_id
        user_name=item.user_name
        tag1=item.tag1
        tag2=item.tag2
        urls=item.urls
        break;

    if id=="":
        id=0

    return jsonify(
        id=id,
        subject=subject,
        urls=urls,
        explain=explain,
        user_id=user_id,
        user_name=user_name,
        tag1=tag1,
        tag2=tag2
        )

# 게시판형 데이터 넘겨주기
@app.route('/t_more')
def t_getdata():
    number = request.args.get('number',0,type=int)
    id=""
    subject=""
    urls=""
    explain=""
    user_name=""
    user_id=""
    tag1=""
    tag2=""

    getdata={}
    if request.args.get('sections',0,type=int) == 1111:
        getdata['content']=design.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int) == 2222:
        getdata['content']=develop.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int) == 3333:
        getdata['content']=source.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 4444:
        getdata['content']=slideshare.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 5555:
        getdata['content']=ppt.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 6666:
        getdata['content']=honey_news.query.filter_by(id = number)
    elif request.args.get('sections',0,type=int)== 7777:
        getdata['content']=recommend.query.filter_by(id = number)
    else:
        pass

    for item in getdata.get('content'):
        id=item.id
        subject=item.subject
        explain=item.explain
        user_id=item.user_id
        user_name=item.user_name
        tag1=item.tag1
        tag2=item.tag2
        break;

    # 글자 수 제한해서 json으로 넘겨주기
    # explain 부분 글자 제한해서 보여주기
    if len(explain) >= 26:
        ab_explain = explain[0:25]
        dummy = "..."
        explain = ab_explain+dummy

    if id=="":
        id=0

    return jsonify(
        id=id,
        subject=subject,
        urls=urls,
        explain=explain,
        user_id=user_id,
        user_name=user_name,
        tag1=tag1,
        tag2=tag2
        )


# 로그아웃
@app.route('/logout')
def logout():
    if "facebook_session" in session:
        session.clear()
        flash(u"로그아웃 되었습니다.")
    else:
        pass
    return redirect(url_for('main'))   

# 페이스북 로그인
@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',next=request.args.get('next') or request.referrer or None, _external=True))
# Authoreization [email/name/id 값]
@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        flash('Access denied: reason=%s error=%s' % ( request.args['error_reason'], request.args['error_description'] ))
        return redirect(url_for('index'))

    session['oauth_token']=(resp['access_token'],'')
    me=facebook.get('/me')
    session['facebook_session']=me.data['email']
    session['facebook_name']=me.data['name']
    session['facebook_user_id']=me.data['id']
    user = User.query.get( session['facebook_user_id'] )
    
    if user == None: # 회원가입 안되있다!
        user_db=User(
        email = session['facebook_session'],
        name = session['facebook_name'],
        id = session['facebook_user_id']
        )

        db.session.add(user_db)
        db.session.commit()

        #페북으로 회원가입됨

    else:
        return redirect(url_for('main'))
        #페북으로 로그인됨

    return redirect(url_for('main'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

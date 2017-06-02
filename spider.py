# -*- coding: utf-8 -*-
import requests
import json,codecs
import re
import simplejson
from DB import MyDB

def getLrc(id):
    print(id)
    lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(id) + '&lv=1&kv=1&tv=-1'
    lyric = requests.get(lrc_url)
    json_obj = lyric.text
    j = json.loads(json_obj)
    if 'lrc' in j:
        if 'lyric' in j['lrc']:
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc = lrc.strip()
            return lrc
    return None

def save_to_file(list, filename):
    with codecs.open(filename, 'a', encoding='utf-8') as f:
        f.writelines(list)

def searchSong(keyWord,offset=0,limit=20):
    result = []
    while True:
        url='http://music.163.com/api/search/pc'
        data={'s':keyWord,'offset':offset,'type':1,'limit':limit}
        r=requests.post(url,data=data)
        res= simplejson.loads(r.text)
        if  res['code'] == 200:
            if 'songs' not in res['result']:
                break
            songs=res['result']['songs']
            for song in songs:
                item={'id':'','name':'','artists':[]}
                item['id']=song['id']
                item['name']=song['name']
                artists=song['artists']
                for artist in artists:
                    ar={'id':'','name':''}
                    ar['id']=artist['id']
                    ar['name']=artist['name'].replace('<','').replace('>','').replace('/','')
                    item['artists'].append(ar)
                result.append(item)
            offset=offset+limit
        else:
            break
    return result

def songToDB(res):
    mydb = MyDB()
    for song in res:
        rs=mydb.getSong(song['id'])
        if not rs:
            mydb.insertSong(song['id'],song['name'])
            authors=song['artists']
            for artist in authors:
                auth=mydb.getAuthor(artist['id'])
                if not auth:
                    mydb.insertAuthor(artist['id'],artist['name'])
                mydb.insertRel(song['id'],artist['id'])
    mydb.db.commit()
    mydb.db.close()

if __name__=='__main__':
    # res=searchSong('民谣')
    # songToDB(res)
    mydb=MyDB()
    res=mydb.getAllSong()
    for id,name in res:
        lrc=getLrc(id)
        if lrc:
            file=r'lrc/'+name.replace('<','').replace('>','').replace('/','')+'.txt'
            save_to_file(lrc,file)
        mydb.updateSong(id,1)
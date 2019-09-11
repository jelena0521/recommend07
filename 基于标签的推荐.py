#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 14:16:15 2019

@author: liujun
"""

import math
import pandas as pd

class basetagrec:
    def __init__(self):
        self.user_file='user_artists.dat'
        self.user_dict=self.getuser()  #{userid:{artistid:weight}}
        self.tag_file='user_taggedartists.dat'
        self.tag_dict,self.user_tag_dict=self.getusertagnum() #{tagid:次数} {userid:{tagid:次数}}
        self.artist_tag_dict=self.getartisttagnum() #{artistid:{tagid:1}} 
        self.usertagpre=self.getusertagpre()
        self.artistsall = list(pd.read_table("artists.dat", delimiter="\t")["id"].values)
        
    def getuser(self):
        user_dict={}
        for line in open(self.user_file,'r').readlines():
            if not line.startswith('userID'):
                userid,artistid,weight=line.strip().split('\t')
                user_dict.setdefault(int(userid),{})
                user_dict[int(userid)][int(artistid)]=float(weight)/10000
        return user_dict
    
    def getusertagnum(self):
        tag_dict={}
        user_tag_dict={}
        for line in open(self.tag_file,'r').readlines():
            if not line.startswith('userID'):
                userid,artistid,tagid=line.strip().split('\t')[:3]
                if int(tagid) in user_tag_dict.keys():
                    user_tag_dict[int(tagid)]=user_tag_dict[int(tagid)]+1
                else:
                    user_tag_dict[int(tagid)]=1
                tag_dict.setdefault(int(userid),{})
                if int(tagid) in tag_dict[int(userid)].keys():
                    tag_dict[int(userid)][int(tagid)]=tag_dict[int(userid)][int(tagid)]+1
                else:
                    tag_dict[int(userid)][int(tagid)]=1
        return tag_dict,user_tag_dict
    
    def getartisttagnum(self):
        artist_tag_dict={}
        for line in open(self.tag_file,'r').readlines():
            if not line.startswith('userID'):
                userid,artistid,tagid=line.split('\t')[:3]
                artist_tag_dict.setdefault(int(artistid),{})
                artist_tag_dict[int(artistid)][int(tagid)]=1
        return artist_tag_dict
    
    def getusertagpre(self):
        usertagpre={}
        usertagcount={}
        num=len(open(self.tag_file,'r').readlines()) #用户打标总数
        for line in open(self.tag_file,'r').readlines():
            if not line.startswith('userID'):
                userid,artistid,tagid=line.split('\t')[:3]
                usertagpre.setdefault(int(userid),{})
                usertagcount.setdefault(int(userid),{})
                if int(artistid) in self.user_dict[int(userid)].keys():
                    rate_ui=self.user_dict[int(userid)][int(artistid)]
                else:
                    rate_ui=0
                if int(tagid) not in usertagpre[int(userid)].keys():
                    usertagpre[int(userid)][int(tagid)]=(rate_ui*self.artist_tag_dict[int(artistid)][int(tagid)])
                    usertagcount[int(userid)][int(tagid)]=1
                else:
                    usertagpre[int(userid)][int(tagid)]=usertagpre[int(userid)][int(tagid)]+(rate_ui*self.artist_tag_dict[int(artistid)][int(tagid)])
                    usertagcount[int(userid)][int(tagid)]=usertagcount[int(userid)][int(tagid)]+1
        for userid in usertagpre.keys():
            for tagid in usertagpre[userid].keys():
                tf_ut=self.tag_dict[int(userid)][int(tagid)]/sum(self.tag_dict[int(userid)].values())
                idf_ut=math.log(num*1/(self.user_tag_dict[int(tagid)]+1))
                usertagpre[userid][tagid]=usertagpre[userid][tagid]/usertagcount[userid][tagid]*tf_ut*idf_ut
        return usertagpre
    
    def recommend(self,user,k,flag=True):
        userartistpredict={}
        for artist in self.artistsall:
            if int(artist) in self.artist_tag_dict.keys():
                for tag in self.usertagpre[int(user)].keys():
                    rate_ut=self.usertagpre[int(user)][int(tag)]
                    if tag not in self.artist_tag_dict[int(artist)].keys():
                        rel_it=0
                    else:
                        rel_it=self.artist_tag_dict[int(artist)][tag]
                    if artist in userartistpredict.keys():
                        userartistpredict[int(artist)]=userartistpredict[int(artist)]+rate_ut*rel_it
                    else:
                        userartistpredict[int(artist)]=rate_ut*rel_it
        newuserartistpredict={}
        if flag:
            for artist in userartistpredict.keys():
                if artist not in self.user_dict[int(user)].keys():
                    newuserartistpredict[artist]=userartistpredict[int(artist)]
            return sorted(newuserartistpredict.items(),key=lambda x:x[1],reverse=True)[:k]
        else:
            return sorted(userartistpredict.items(),key=lambda x:x[1],reverse=True)[:k]
                    
                    
    def evaluate(self,user):
        k=len(self.user_dict[int(user)])
        recresult=self.recommend(user,k=k,flag=False)
        count=0
        for artist,pre in recresult:
            if artist in self.user_dict[int(user)]:
                count=count+1
        return count/k
    
if __name__=='__main__':
    rbt=basetagrec()
    print(rbt.recommend('2',k=20))
    print(rbt.evaluate('2'))

        
            
                    
            
                
                
                
                
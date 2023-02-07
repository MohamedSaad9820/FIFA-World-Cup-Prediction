#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
rf1 = RandomForestClassifier(max_depth=15, max_features=2, random_state=42)
rf2 = RandomForestClassifier(max_depth=15, max_features=2, random_state=42)
rf3 = RandomForestClassifier(max_depth=15, max_features=2, random_state=42)
rf4 = RandomForestClassifier(max_depth=15, max_features=2, random_state=42)
country=['Algeria','Angola','Argentina','Australia','Austria','BAH','BEN','BHR','Belgium','Bolivia','Brazil','Bulgaria','Cameroon','Canada','Chile','China PR','Colombia','Costa Rica','Croatia','Cuba','Czech Republic','Czechoslovakia',"Cï¿½te d'Ivoire",'Denmark','Dutch East Indies','ETH','Ecuador','Egypt','El Salvador','England','FIN','France','GAM','GUA','GUT','German DR','Germany','Germany FR','Ghana','Greece','HKG','Haiti','Honduras','Hungary','Iceland','Iran','Iraq','Israel','Italy','Jamaica','Japan','Korea DPR','Korea Republic','Kuwait','LBY','MLI','MRI','Mexico','Morocco','NIG','Netherlands','New Zealand','Nigeria','Northern Ireland','Norway','Panama','Paraguay','Peru','Poland','Portugal','QTR','Qatar','Romania','Russia','SEY','SIN','SYR','Saudi Arabia','Scotland','Senegal','Serbia','Slovakia','Slovenia','South Africa','Soviet Union','Spain','Sweden','Switzerland','THA','Togo','Tunisia','Turkey','USA','UZB','UZK','Ukraine','Uruguay','VEN','VNZ','Wales','Yugoslavia','ZMB','Zaire','rn">Bosnia and Herzegovina','rn">Republic of Ireland','rn">Serbia and Montenegro','rn">Trinidad and Tobago','rn">United Arab Emirates']


def get_data():
    df2=pd.read_csv("D:\Projects\FIFA World Cup Prediction\FIFA World Cup Data.csv",sep=",",encoding="utf-8")
    return df2


def coding(x):
    u=0
    while u<=107:
        if x==country[u]:
            code=country.index(country[u])
            break
        else:
            u+=1
    return code


def preprocess(df2):
    df2["Stage"]=df2["Stage"].replace({"Group 1","Group 2","Group 3","Group 4","Group 5","Group 6","Group A","Group B","Group C","Group D","Group E","Group F","Group G","Group H"},"Round of groups")
    df2["Stage"]=df2["Stage"].replace({"First round","Preliminary round"},"Round of 16")
    df2["Stage"]=df2["Stage"].replace({"Match for third place","Play-off for third place"},"Third place")
    df2["Attendance"]=df2["Attendance"].fillna(int(df2["Attendance"].mean())).astype(int)
    Winner=[]
    w=0
    while w<=963:
        if df2["Home Team Goals"][w]>df2["Away Team Goals"][w]:
            Winner.append(df2["Home Team Name"][w])
        elif df2["Home Team Goals"][w]<df2["Away Team Goals"][w]:
            Winner.append(df2["Away Team Name"][w])
        else:
            if df2["Win conditions"][w]==" ":
                Winner.append("tie_match")
            elif int(df2["Win conditions"][w][-7])>int(df2["Win conditions"][w][-3]):
                Winner.append(df2["Home Team Name"][w])
            else:
                Winner.append(df2["Away Team Name"][w])
        w+=1
    df2["Winner"]=Winner
    extratime=[]
    x=0
    while x<=963:
        if df2["Win conditions"][x]!=" ":
            if(df2["Win conditions"][x][-2]=="e" or df2["Win conditions"][x][-2]=="l"):
                extratime.append(1)
            else:
                extratime.append(0)
        else:
            extratime.append(0)
        x+=1
    df2["Extratime"]=extratime
    penalties=[]
    p=0
    while p<=963:
        if df2["Win conditions"][p]!=" ":
            if(df2["Win conditions"][p][-2]==")"):
                penalties.append(1)
            else:
                penalties.append(0)
        else:
            penalties.append(0)
        p+=1
    df2["Penalties"]=penalties
    df2=df2.drop(["Win conditions"],axis=1)
    df2["Home Team Name"]=df2["Home Team Name"].replace("IR Iran","Iran")
    df2["Away Team Name"]=df2["Away Team Name"].replace("IR Iran","Iran")
    df2["Home Team Name"]=df2["Home Team Name"].replace("South Korea","Korea Republic")
    df2["Away Team Name"]=df2["Away Team Name"].replace("South Korea","Korea Republic")
    list1=df2["Away Team Initials"].values
    nationality=[]
    n=0
    while n<=963:
        u=0
        while u<=963:
            if df2["Referee"][n][-4:-1]==list1[u]:
                nationality.append(df2["Away Team Name"][u])
                break
            else:
                u+=1
                if u==964:
                    nationality.append(df2["Referee"][n][-4:-1]) 
        n+=1
    df2["Referee Nationality"]=nationality
    homecode=[]
    h=0
    while h<=963:
        u=0
        while u<=107:
            if df2["Home Team Name"][h]==country[u]:
                homecode.append(country.index(country[u]))
                break
            else:
                u+=1
        h+=1
    df2["homecode"]=homecode
    awaycode=[]
    a=0
    while a<=963:
        u=0
        while u<=107:
            if df2["Away Team Name"][a]==country[u]:
                awaycode.append(country.index(country[u]))
                break
            else:
                u+=1
        a+=1
    df2["awaycode"]=awaycode
    df=df2
    return df


def totalmatch(df,t1,t2):
    m=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            m+=1
        i+=1
    return m

def groupmatch(df,t1,t2):
    g=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Stage"][i]=="Round of groups"):
                g+=1
        i+=1
    return g

def r16match(df,t1,t2):
    r16=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Stage"][i]=="Round of 16"):
                r16+=1
        i+=1
    return r16

def quartermatch(df,t1,t2):
    q=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Stage"][i]=="Quarter-finals"):
                q+=1
        i+=1
    return q


def semifinalmatch(df,t1,t2):
    sf=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Stage"][i]=="Semi-finals"):
                sf+=1
        i+=1
    return sf


def thirdmatch(df,t1,t2):
    th=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Stage"][i]=="Third place"):
                th+=1
        i+=1
    return th

def finalmatch(df,t1,t2):
    f=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Stage"][i]=="Final"):
                f+=1
        i+=1
    return f

def t1winmatch(df,t1,t2):
    w1=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Winner"][i]==t1):
                w1+=1
        i+=1
    return w1

def t2winmatch(df,t1,t2):
    w2=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Winner"][i]==t2):
                w2+=1
        i+=1
    return w2

def tiematch(df,t1,t2):
    t=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Winner"][i]=="tie_match"):
                t+=1
        i+=1
    return t

def exmatch(df,t1,t2):
    ex=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Extratime"][i]==1):
                ex+=1
        i+=1
    return ex

def penmatch(df,t1,t2):
    p=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            if (df["Penalties"][i]==1):
                p+=1
        i+=1
    return p

def totalgoal(df,t1,t2):
    gl=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            gl+=(df["Home Team Goals"][i]+df["Away Team Goals"][i])
        i+=1
    return int(gl)

def t1goal(df,t1,t2):
    g1=0
    for i in range(964):
        if df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2:
            g1+=df["Home Team Goals"][i]
        elif df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1:
            g1+=df["Away Team Goals"][i]
        i+=1
    return int(g1)

def t2goal(df,t1,t2):
    g2=0
    for i in range(964):
        if df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2:
            g2+=df["Away Team Goals"][i]
        elif df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1:
            g2+=df["Home Team Goals"][i]
        i+=1
    return int(g2)

def firsttotalgoal(df,t1,t2):
    fg=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            fg+=(df["Half-time Home Goals"][i]+df["Half-time Away Goals"][i])
        i+=1
    return int(fg)

def firstt1goal(df,t1,t2):
    fg1=0
    for i in range(964):
        if df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2:
            fg1+=df["Half-time Home Goals"][i]
        elif df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1:
            fg1+=df["Half-time Away Goals"][i]
        i+=1
    return int(fg1)

def firstt2goal(df,t1,t2):
    fg2=0
    for i in range(964):
        if df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2:
            fg2+=df["Half-time Away Goals"][i]
        elif df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1:
            fg2+=df["Half-time Home Goals"][i]
        i+=1
    return int(fg2)

def attendance(df,t1,t2):
    a=0
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            a+=df["Attendance"][i]
        i+=1
    return int(a)

def refnat(df,t1,t2):
    nat=[]
    for i in range(964):
        if (df["Home Team Name"][i]==t1 and df["Away Team Name"][i]==t2) or (df["Home Team Name"][i]==t2 and df["Away Team Name"][i]==t1):
            nat.append(df["Referee Nationality"][i])
        i+=1
    nat_count=pd.Series(nat).value_counts()
    return nat_count


def traing(x,df):
    x1_train,x1_test,y1_train,y1_test = train_test_split(x,df["Home Team Goals"],test_size=1/3,random_state=42)
    rf1.fit(x1_train,y1_train)
    return round(rf1.score(x1_train,y1_train)*100,2)
def trainx(x,df):
    x2_train,x2_test,y2_train,y2_test = train_test_split(x,df["Extratime"],test_size=1/3,random_state=42)
    rf2.fit(x2_train,y2_train)
    return round(rf2.score(x2_train,y2_train)*100,2)
def trainr(x,df):
    x3_train,x3_test,y3_train,y3_test = train_test_split(x,df["Referee Nationality"],test_size=1/3,random_state=42)
    rf3.fit(x3_train,y3_train)
    return round(rf3.score(x3_train,y3_train)*100,2)
def trainw(x,df):
    x4_train,x4_test,y4_train,y4_test = train_test_split(x,df["Winner"],test_size=1/3,random_state=42)
    rf4.fit(x4_train,y4_train)
    return round(rf4.score(x4_train,y4_train)*100,2)

def predictg(c1,c2):
    x1=[[c1,c2]]
    y1=rf1.predict(x1)[0]
    return int(y1)

def predictx(c1,c2):
    x2=[[c1,c2]]
    y2=rf2.predict(x2)[0]
    return int(y2)

def predictr(c1,c2):
    x3=[[c1,c2]]
    y3=rf3.predict(x3)[0]
    return y3

def predictw(c1,c2):
    x4=[[c1,c2]]
    y4=rf4.predict(x4)[0]
    return y4
    


# In[ ]:





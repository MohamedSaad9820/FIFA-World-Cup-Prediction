#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


df=pd.read_csv("D:\Projects\FIFA World Cup Prediction\FIFA World Cup Data.csv",sep=",",encoding="utf-8")


# In[3]:


df.head(-5)


# In[4]:


df.info()


# In[5]:


df["Year"].value_counts()


# In[6]:


df["Stage"].value_counts()


# In[7]:


df["Stage"]=df["Stage"].replace("Match for third place","Third place")


# In[8]:


df["Stage"].value_counts()


# In[9]:


df["Stage"]=df["Stage"].replace("Play-off for third place","Third place")


# In[10]:


df["Stage"].value_counts()


# In[11]:


df["Stage"]=df["Stage"].replace("First round","Round of 16")
df["Stage"]=df["Stage"].replace("Preliminary round","Round of 16")
df["Stage"].value_counts()


# In[12]:


df["Stage"]=df["Stage"].replace({"Group 1","Group 2","Group 3","Group 4","Group 5","Group 6","Group A","Group B","Group C","Group D","Group E","Group F","Group G","Group H"},"Round of groups")


# In[13]:


df["Stage"].value_counts()


# In[14]:


df.info()


# In[15]:


Winner=[]
i=0
while i<=963:
    if df["Home Team Goals"][i]>df["Away Team Goals"][i]:
        Winner.append(df["Home Team Name"][i])
    elif df["Home Team Goals"][i]<df["Away Team Goals"][i]:
        Winner.append(df["Away Team Name"][i])
    else:
        if df["Win conditions"][i]==" ":
            Winner.append("tie_match")
        elif int(df["Win conditions"][i][-7])>int(df["Win conditions"][i][-3]):
            Winner.append(df["Home Team Name"][i])
        else:
            Winner.append(df["Away Team Name"][i])
    i+=1


# In[16]:


df["Winner"]=Winner


# In[17]:


df["Winner"].value_counts()


# In[18]:


df["Attendance"]=df["Attendance"].fillna(int(df["Attendance"].mean())).astype(int)


# In[19]:


df.info()


# In[20]:


df["Win conditions"].value_counts()


# In[21]:


extratime=[]
i=0
while i<=963:
    if df["Win conditions"][i]!=" ":
        if(df["Win conditions"][i][-2]=="e" or df["Win conditions"][i][-2]=="l"):
            extratime.append(1)
        else:
            extratime.append(0)
    else:
        extratime.append(0)
    i+=1


# In[22]:


df["Extratime"]=extratime


# In[23]:


penalties=[]
i=0
while i<=963:
    if df["Win conditions"][i]!=" ":
        if(df["Win conditions"][i][-2]==")"):
            penalties.append(1)
        else:
            penalties.append(0)
    else:
        penalties.append(0)
    i+=1


# In[24]:


df["Penalties"]=penalties


# In[25]:


df.head()


# In[26]:


df=df.drop(["Win conditions"],axis=1)


# In[27]:


df.info()


# In[28]:


df["Home Team Name"].value_counts()


# In[29]:


df["Home Team Initials"].value_counts()


# In[30]:


df["Home Team Name"]=df["Home Team Name"].replace("IR Iran","Iran")
df["Home Team Name"]=df["Home Team Name"].replace("South Korea","Korea Republic")


# In[31]:


df["Home Team Name"].value_counts()


# In[32]:


df["Home Team Initials"].value_counts()


# In[33]:


df["Away Team Name"].value_counts()


# In[34]:


df["Away Team Initials"].value_counts()


# In[35]:


df["Away Team Name"]=df["Away Team Name"].replace("IR Iran","Iran")
df["Away Team Name"]=df["Away Team Name"].replace("South Korea","Korea Republic")


# In[36]:


df["Away Team Initials"].value_counts()


# In[37]:


list1 = df["Away Team Initials"].values
list1


# In[38]:


len(list1)


# In[39]:


nationality=[]
i=0
while i<=963:
    u=0
    while u<=963:
        if df["Referee"][i][-4:-1]==list1[u]:
            nationality.append(df["Away Team Name"][u])
            break
        else:
            u+=1
            if u==964:
                nationality.append(df["Referee"][i][-4:-1]) 
    i+=1


# In[40]:


df["Referee Nationality"]=nationality


# In[41]:


df.info()


# In[42]:


df.head()


# # INFORMATION

# In[43]:


df["Stage"].value_counts()


# In[44]:


def info(x1,x2):
    m=g=r16=q=sf=th=f=w1=w2=t=ex=p=gl=g1=g2=fg=fg1=fg2=a=0
    nat=[]
    for i in range(964):      #no.of all matches
        if (df["Home Team Name"][i]==x1 and df["Away Team Name"][i]==x2) or (df["Home Team Name"][i]==x2 and df["Away Team Name"][i]==x1):
            m+=1
            if df["Stage"][i]=="Round of groups":
                g+=1      #no. of group matches
            elif df["Stage"][i]=="Round of 16":
                r16+=1      #no. of l16 matches
            elif df["Stage"][i]=="Quarter-finals":
                q+=1      #no. of quarter matches
            elif df["Stage"][i]=="Semi-finals":
                sf+=1       #no. of semi final matches
            elif df["Stage"][i]=="Third place":
                th+=1       #no. of third position matches
            elif df["Stage"][i]=="Final":
                f+=1       #no.of final matches
            if df["Winner"][i]==x1:
                w1+=1
            elif df["Winner"][i]==x2:
                w2+=1
            elif df["Winner"][i]=="tie_match":
                t+=1
            if df["Extratime"][i]==1:
                ex+=1
            if df["Penalties"][i]==1:
                p+=1
            gl=gl+df["Home Team Goals"][i]+df["Away Team Goals"][i]
            if df["Home Team Name"][i]==x1 and df["Away Team Name"][i]==x2:
                g1=g1+df["Home Team Goals"][i]
                g2=g2+df["Away Team Goals"][i]
            elif df["Home Team Name"][i]==x2 and df["Away Team Name"][i]==x1:
                g2=g2+df["Home Team Goals"][i]
                g1=g1+df["Away Team Goals"][i]
            fg=fg+df["Half-time Home Goals"][i]+df["Half-time Away Goals"][i]
            if df["Home Team Name"][i]==x1 and df["Away Team Name"][i]==x2:
                fg1=fg1+df["Half-time Home Goals"][i]
                fg2=fg2+df["Half-time Away Goals"][i]
            elif df["Home Team Name"][i]==x2 and df["Away Team Name"][i]==x1:
                fg2=fg2+df["Half-time Home Goals"][i]
                fg1=fg1+df["Half-time Away Goals"][i]
            a=a+df["Attendance"][i]
            nat.append(df["Referee Nationality"][i])
        i+=1
    if m==0:
        avg=0
    else:
        avg=int(a/m)
    nat_count=pd.Series(nat).value_counts()
    print("The Result And Matches Information Between ",x1," And ",x2," In FIFA World Cup (from cup 1930 to 2022)")
    print("     (MATCHES)")
    print("no.of all matches= ",m)
    print("no.of group matches= ",g)
    print("no.of round 16 matches= ",r16)
    print("no.of quarter final matches= ",q)
    print("no.of semi_final matches= ",sf)
    print("no.of third place matches= ",th)
    print("no.of final matches= ",f)
    print("------------------------------------")
    print("     (RESULTS)")
    print(x1," win ",w1," matches")
    print(x2," win ",w2," matches")
    print("Tie_Matches= ",t," matches")
    print("Extra_Time Matches= ",ex)
    print("Penalties Matches= ",p)
    print("------------------------------------")
    print("     (GOALS)")
    print("The total goals= ",gl)
    print("The total goals of ",x1,"= ",g1)
    print("The total goals of ",x2,"= ",g2)
    print("The half_time goals= ",fg)
    print("The half_time goals of ",x1,"= ",fg1)
    print("The half_time goals of ",x2,"= ",fg2)
    print("------------------------------------")
    print("     (Public Attendance)")
    print("Average public Attendance= ",avg)
    print("------------------------------------")
    print("    (Count of Referee Nationality)")
    print("Nat.     count")
    print(nat_count)


# In[45]:


#w1=str(input("enter first team: "))
#w2=str(input("enter second team:"))
#info(w1,w2)


# # PREDICT

# In[46]:


len(set(df["Referee Nationality"]))


# In[47]:


country=sorted((set(df["Home Team Name"]).union(set(df["Away Team Name"]))).union(set(df["Referee Nationality"])))
len(country)


# In[48]:


country


# In[49]:


homecode=[]
i=0
while i<=963:
    u=0
    while u<=107:
        if df["Home Team Name"][i]==country[u]:
            homecode.append(country.index(country[u]))
            break
        else:
            u+=1
    i+=1
    
df["homecode"]=homecode


# In[50]:


awaycode=[]
i=0
while i<=963:
    u=0
    while u<=107:
        if df["Away Team Name"][i]==country[u]:
            awaycode.append(country.index(country[u]))
            break
        else:
            u+=1
    i+=1
    
df["awaycode"]=awaycode


# In[51]:


rnatcode=[]
i=0
while i<=963:
    u=0
    while u<=107:
        if df["Referee Nationality"][i]==country[u]:
            rnatcode.append(country.index(country[u]))
            break
        else:
            u+=1
    i+=1
    
df["rnatcode"]=rnatcode


# In[52]:


winnercode=[]
i=0
while i<=963:
    t=1
    u=0
    while u<=107:
        if df["Winner"][i]==country[u]:
            winnercode.append(country.index(country[u]))
            t=0
            break
        else:
            u+=1
    if t==0:
        i+=1
    elif t==1:
        winnercode.append(108)
        i+=1
    
df["winnercode"]=winnercode


# In[53]:


df.info()


# ## ALGORITHM

# In[54]:


from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(max_depth=15, max_features=2, random_state=42)


# In[55]:


from sklearn.metrics import confusion_matrix


# In[56]:


from sklearn.metrics import confusion_matrix,f1_score,plot_roc_curve,accuracy_score,roc_curve,roc_auc_score,recall_score


# ## i)X1 GOALS

# In[57]:


x1=df[["homecode","awaycode"]]
y1=df["Home Team Goals"]


# In[58]:


from sklearn.model_selection import train_test_split
x1_train,x1_test,y1_train,y1_test = train_test_split(x1,y1, test_size= 1/3, random_state =42)


# In[59]:


rf.fit(x1_train,y1_train)
rf.score(x1_train,y1_train)


# In[60]:


rf.score(x1_test,y1_test)


# ## ii)X2 GOALS

# In[61]:


x2=df[["homecode","awaycode"]]
y2=df["Away Team Goals"]


# In[62]:


from sklearn.model_selection import train_test_split
x2_train,x2_test,y2_train,y2_test = train_test_split(x2,y2, test_size= 1/3, random_state =42)


# In[63]:


rf.fit(x2_train,y2_train)
rf.score(x2_train,y2_train)


# In[64]:


rf.score(x2_test,y2_test)


# ## iii)EXTRATIME

# In[65]:


x3=df[["homecode","awaycode"]]
y3=df["Extratime"]


# In[66]:


from sklearn.model_selection import train_test_split
x3_train,x3_test,y3_train,y3_test = train_test_split(x3,y3, test_size= 1/3, random_state =42)


# In[67]:


rf.fit(x3_train,y3_train)
rf.score(x3_train,y3_train)


# In[68]:


rf.score(x3_test,y3_test)


# ## iv)Referee Nationality

# In[69]:


x4=df[["homecode","awaycode"]]
y4=df["Referee Nationality"]


# In[70]:


from sklearn.model_selection import train_test_split
x4_train,x4_test,y4_train,y4_test = train_test_split(x4,y4, test_size= 1/3, random_state =42)


# In[71]:


rf.fit(x4_train,y4_train)
rf.score(x4_train,y4_train)


# In[72]:


rf.score(x4_test,y4_test)


# ## v)Winner if equal goals

# In[73]:


df2=df[(df["Winner"] != "tie_match")]


# In[74]:


df2.info()


# In[75]:


x5=df2[["homecode","awaycode"]]
y5=df2["Winner"]


# In[76]:


from sklearn.model_selection import train_test_split
x5_train,x5_test,y5_train,y5_test = train_test_split(x5,y5, test_size= 1/3, random_state =42)


# In[77]:


rf.fit(x5_train,y5_train)
rf.score(x5_train,y5_train)


# In[78]:


rf.score(x5_test,y5_test)


# In[79]:


rf.predict([[1,2]])[0]


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask,jsonify,request
from fifa_world_cup import *
app      = Flask(__name__)
df       = get_data()
df       = preprocess(df)                                                                     #referee
df11=df[["homecode","awaycode","Home Team Goals"]]
df111=df[["awaycode","homecode","Away Team Goals"]]
df111["Home Team Goals"]=df111["Away Team Goals"]
df111=df111.drop(["Away Team Goals"],axis=1)
df1=pd.concat([df11,df111])                                                                   #goals
df2      = df[(df["Stage"] != "Round of groups")]                                             #extratime
x        = df[["homecode","awaycode"]]                                    #referee
x1       = df1[["homecode","awaycode"]]                                   #goals
x2       = df2[["homecode","awaycode"]]                                   #extratime
accuracyg = traing(x1,df1)
accuracyx = trainx(x2,df2)
accuracyr = trainr(x,df)


@app.route('/')        ## Homepage
def home():
    data = {
        'name':'FIFA_World_Cup',
        'page_name':'الصفحة الرئيسيه'
    }
    return jsonify(data)


@app.route('/train') ## train
def fl_train():
    accuracyg = traing(x1,df1)
    accuracyx = trainx(x2,df2)
    accuracyr = trainr(x,df)
    
    data = {
        'name':'FIFA_World_Cup',
        'page_name':'Train',
        'accuracy of team goal':accuracyg,
        'accuracy of extratime':accuracyx,
        'accuracy of referee nationality':accuracyr
    }
    return jsonify(data)



@app.route('/predict') ## predict
def fl_predict():
    t1  = request.args['t1']
    t2  = request.args['t2']
    g   = request.args['g']
    c1  = coding(t1)
    c2  = coding(t2)
    df4 = df[(df["Winner"]==t1) | (df["Winner"]==t2)]                                                #winner
    x4  = df4[["homecode","awaycode"]]                                                                #winner
    accuracyw = trainw(x4,df4)
    print(t1)
    print(t2)
    print(g)
    total = totalmatch(df,t1,t2)
    group = groupmatch(df,t1,t2)
    round16   = r16match(df,t1,t2)
    quarter = quartermatch(df,t1,t2)
    semifinal = semifinalmatch(df,t1,t2)
    third = thirdmatch(df,t1,t2)
    final = finalmatch(df,t1,t2)
    t1win = t1winmatch(df,t1,t2)
    t2win = t2winmatch(df,t1,t2)
    tie = tiematch(df,t1,t2)
    extratime = exmatch(df,t1,t2)
    penalties = penmatch(df,t1,t2)
    totalg = totalgoal(df,t1,t2)
    totalg1 = t1goal(df,t1,t2)
    totalg2 = t2goal(df,t1,t2)
    totalfg = firsttotalgoal(df,t1,t2)
    totalfg1 = firstt1goal(df,t1,t2)
    totalfg2 = firstt2goal(df,t1,t2)
    if total==0:
        avgatt=0
    else:
        avgatt = int(attendance(df,t1,t2)/total)
    refnationality = refnat(df,t1,t2).to_json()
    t1g = predictg(c1,c2)
    t2g = predictg(c2,c1)
    rnat = predictr(c1,c2)
    if g=="group":
        ex = "The Match WITHOUT Extratime"
        p = "The Match WITHOUT Penalties"
        if t1g>t2g:
            w = t1
        elif t2g>t1g:
            w = t2
        else:
            w ="TIE_MATCH"
    elif g=="not_group":
        if t1g>t2g:
            p = "The Match WITHOUT Penalties"
            w = t1
            exc=predictx(c1,c2)
            if exc==0:
                ex = "The Match WITHOUT Extratime"
            else:
                ex = "The Match WITH Extratime"
        elif t2g>t1g:
            p = "The Match WITHOUT Penalties"
            w = t2
            exc=predictx(c1,c2)
            if exc==0:
                ex = "The Match WITHOUT Extratime"
            else:
                ex = "The Match WITH Extratime"
        elif t1g==t2g:
            w = predictw(c1,c2)
            p = "The Match WITH Penalties"
            ex = "The Match WITH Extratime"

            
        
    data = {'0) TOPIC(1)':"(THE INFORMATION OF FIFA WORLD CUP MATCHES BETWEEN ("+t1+") AND ("+t2+") FROM 1930 TO 2022)                                                                    ",
            '00)MATCHES':"                                                                                                                                                                                          ",
            '000)number of All matches is ':str(total)+"                                                                                                                                                    ",
            '001)number of round of group matches is ':str(group)+"                                                                                                                                      ",
            '002)number of round 16 matches is ':str(round16)+"                                                                                                                                          ",
            '003)number of quarter_final matches is ':str(quarter)+"                                                                                                                                     ",
            '004)number of semi_final matches is ':str(semifinal)+"                                                                                                                                      ",
            '005)number of third place matches is ':str(third)+"                                                                                                                                          ",
            '006)number of final matches is ':str(final)+"                                                                                                                                                ",
            '01)----------------------------------------------------------------------------':"                                                                                                                     ",
            '01)RESULTS':"                                                                                                                                                                                           ",
            '010)number of matches that '+t1+' won is':str(t1win)+"                                                                                                                                         ",
            '011)number of matches that '+t2+' won is':str(t2win)+"                                                                                                                                         ",
            '012)number of matches that ended in a tie is ':str(tie)+"                                                                                                                                                     ",
            '013)number of matches that ended with extratime is ':str(extratime)+"                                                                                                                                         ",
            '014)number of matches that ended with penalties is ':str(penalties)+"                                                                                                                                         ",
            '02)----------------------------------------------------------------------------':"                                                                                                                      ",
            '02)GOALS':"                                                                                                                                                                                                         ",
            '020)number of total goals is ':str(totalg)+"                                                                                                                                                ",
            '021)number of total goals to '+t1+' is ':str(totalg1)+"                                                                                                                                          ",
            '022)number of total goals to '+t2+' is ':str(totalg2)+"                                                                                                                                        ",
            '023)number of total halftime goals is ':str(totalfg)+"                                                                                                                                      ",
            '024)number of total halftime goals to '+t1+' is ':str(totalfg1)+"                                                                                                                               ",
            '025)number of total halftime goals to '+t2+' is ':str(totalfg2)+"                                                                                                                                ",
            '03)----------------------------------------------------------------------------':"                                                                                                                        ",
            '03)PUBLIC ATTENDANCE':"                                                                                                                                                                                    ",
            '030)Average Attendance of one match is ':str(avgatt)+"                                                                                                                                                   ",
            '04)----------------------------------------------------------------------------':"                                                                                                                                       ",
            '04)REFEREES NATIONALITIES':"                                                                                                                                                                             ",
            '040)the nationalities of referees is ':refnationality+"                                                                                                                                               ",
            '1)-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------':"  ",
            "1)TOPIC(2)":'THE PREDICTION OF NEXT MATCH BETWEEN ('+t1+') AND ('+t2+')                                                                                                                                ',
            '10)The Prediction goals number to '+t1+' is ':str(t1g)+" goal                                                                                                                                                 ",
            '11)The Prediction goals number to '+t2+' is ':str(t2g)+" goal                                                                                                                                                  ",
            '12)The Prediction Winnig team is ':w+"                                                                                                                                                                    ",
            '13)The Prediction of there is Extratime is ':ex+"                                                                                                                                                                      ",
            '14)The Prediction of there are Penalties is ':p+"                                                                                                                                                              ",
            '15)The Prediction of Referee Nationality is ':rnat+"                                                                                                                                                             "
            
           
           }
    
    return jsonify(data)
app.run()


# In[ ]:





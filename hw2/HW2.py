
import math
from texttable import Texttable
from collections import defaultdict
from operator import itemgetter

#readFile#
def readFile(fileData):
    data=[]
    rates=[]
    f=open(fileData,"r")
    next(f)
    data=f.readlines()
    f.close()
    for line in data:
        dataLine=line.split(",")
        rates.append([int(dataLine[0]),float(dataLine[1]),float(dataLine[2])])
    return rates

#Create a dictionary to generate a data structure for user ratings
#   Input: data set, format: user id\t hard disk id\ ratings
#   output:1.user disk：dic[user id]=[(movie id,rating)...]
#        2.movie disk：dic[movie id]=[user id1,user id2...]#
def createDict(rates):
    user_dict={}
    movie_dict={}
    for i in rates:
        if i[0] in user_dict:
            user_dict[i[0]].append((i[1],i[2]))
        else:
            user_dict[i[0]]=[(i[1],i[2])]
        if i[1] in movie_dict:
            movie_dict[i[1]].append(i[0])
        else:
            movie_dict[i[1]]=[i[0]]
    return user_dict,movie_dict


#Establish item inversion list and calculate item similarity
def itemCF(user_dict):
    N=dict()
    C=defaultdict(defaultdict)
    W=defaultdict(defaultdict)
    for key in user_dict:
        for i in user_dict[key]:
            if i[0] not in N.keys(): #i[0]main is movie_id
                N[i[0]]=0
            N[i[0]]+=1               #N[i[0]]The number of users who have reviewed a movie
            for j in user_dict[key]:
                if i==j:
                    continue
                if j not in C[i[0]].keys():
                    C[i[0]][j[0]]=0
                C[i[0]][j[0]]+=1      #C[i[0]][j[0]]Is the similarity between two movies，
                                      # eg：The number of users who have reviewed both movie 1 and movie 2
    for i,related_item in C.items():
        for j,cij in related_item.items():
            W[i][j]=cij/math.sqrt(N[i]*N[j]) 
    return W

#Sort items according to user preferences
def recommondation(user_id,user_dict,K):
    rank=defaultdict(int)
    l=list()
    W=itemCF(user_dict)
    for i,score in user_dict[user_id]: #iI is the movie id of the specific user, and score is the corresponding score
        for j,wj in sorted(W[i].items(),key=itemgetter(1),reverse=True)[0:K]: #sorted()return list,listIs a tuple
            if j in user_dict[user_id]:
                continue
            rank[j]+=score*wj #Find out the collection of movies that users have commented on，
                              # For each movie id, assume one movie id1, and find the K movies that are most similar to that movie，
                              #Calculate the user's interest in each movie under id1
                             # Then, the whole set of movies reviewed by users is iterated,
                            # weighted sum is calculated, and then sorted. The first n movies can be recommended. I will take 5 movies here
    l=sorted(rank.items(),key=itemgetter(1),reverse=True)[0:5]
    return l
                                

#Get movie list
def getMovieList(item):
    items={}
    f=open(item,"r")
    next(f)
    movie_content=f.readlines()
    f.close()
    for movie in movie_content:
        movieLine=movie.split(",")
        items[int(movieLine[0])]=movieLine[1:]
    return items

#main
if __name__=='__main__':
    itemTemp=getMovieList("movies.csv") #Get movie list
    fileTemp=readFile("ratings.csv")     #read file
    out = open('output.txt', 'w')
    user_dic,movie_dic=createDict(fileTemp)     #create a dic
    a = 1
    user_id = a
    for a in range(1,len(user_dic)+1):
        user_id = a

        print(user_id)

        movieTemp=recommondation(user_id,user_dic,100)      #sort the movies
        rows=[]
        table=Texttable()                          #Create the table and display it
        table.set_deco(Texttable.HEADER)
        rows.append([])

        for i in movieTemp:
            #Because I used the movie name, the standard output mode was too confusing.
            # User-id1 movie-id1 movie-id2 movie-id3 movie-id4 movie-id5
            # My output mode is:
            # User-id1 movie-name1
            # User-id1 movie-name2
            # User-id1 movie-name3
            # User-id1 movie-name4
            # User-id1 movie-name5
            rows.append([user_id,itemTemp[i[0]][0]])
        table.add_rows(rows)
        print("%.3f"%(a/len(user_dic)*100),"%")              #I'm simply going to divide the number of users that are running
                                                        # by the total number of users to get the percentage of progress.
        out.write(table.draw())
        a = a + 1
    else:
        print("Boom!")
    out.close()
    



     


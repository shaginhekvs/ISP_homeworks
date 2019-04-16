import numpy as np
import pandas as pd
import random 

def write_res(file_name,array):
    result_1a_file = open(file_name,'w')
    for movie in array:
        result_1a_file.write(movie.strip()+'\n')

email = 'keshav.singh@epfl.ch'
imdb = pd.read_csv('imdb-1.csv',header=None,quotechar='"',skipinitialspace=True)
com = pd.read_csv('com402-1.csv',header=None,quotechar='"',skipinitialspace=True)

com_grped_by_date = dict([(x.iloc[0,2],x) for _,x in com.groupby(com[2])])
imdb_me = imdb[imdb[0] ==email]
list_potential_movies = []

for i in imdb_me[2]:
    list_potential_movies.append(com_grped_by_date[i])
my_id = None
for elem in list_potential_movies:
    if(len(elem) == 1):
        my_id = elem.iloc[0,0]
my_com_entries = com[com[0] == my_id]


mapping_movies = {}
merged = pd.merge(com,imdb,on= 2)
for _,x in merged.groupby(merged[2]):
    if len(x) == 1:
        mapping_movies[x.iloc[0,1]] = x.iloc[0,5]
my_fav_movies = [mapping_movies.get(x[1],0) for _,x in my_com_entries.iterrows()]
write_res('movies_1a.txt',my_fav_movies)
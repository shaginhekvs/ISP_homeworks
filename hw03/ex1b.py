import numpy as np
import pandas as pd
import random 

def write_res(file_name,array):
    result_1a_file = open(file_name,'w')
    for movie in array:
        result_1a_file.write(movie.strip()+'\n')

email = 'keshav.singh@epfl.ch'
imdb = pd.read_csv('imdb-2.csv',header=None,quotechar='"',skipinitialspace=True)
com = pd.read_csv('com402-2.csv',header=None,quotechar='"',skipinitialspace=True)

count_imdb = imdb[1].value_counts().reset_index()
count_com = com[1].value_counts().reset_index()
concatenated = pd.concat([count_com,count_imdb],axis=1).drop(1,axis = 1)
concatenated.columns = ['hash','movie']
concatenated = concatenated.set_index('hash')
map_hash_movie = concatenated.to_dict()['movie']
map_movie_to_hash = dict([(v,k) for k,v in map_hash_movie.items()])

my_imdb_movies = imdb[imdb[0] ==email]
potential_emails =None
for movie in my_imdb_movies[1].values:
    hash_ = map_movie_to_hash[movie]
    tmp_emails = com[0][com[1] == hash_]
    potential_emails = tmp_emails if potential_emails is None else np.intersect1d(potential_emails,tmp_emails.values)

my_email_hash = potential_emails[0]
my_fav_movies = [map_hash_movie[x] for x in com[1][com[0] == my_email_hash].values]
write_res('movies_1b.txt',my_fav_movies)
    
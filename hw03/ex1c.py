import pandas as pd
from collections import Counter
import itertools
import warnings
warnings.filterwarnings('ignore')
import numpy as np 
from functools import reduce
import hashlib
import random

def write_res(file_name,array):
    result_1a_file = open(file_name,'w')
    for movie in array:
        result_1a_file.write(movie.strip()+'\n')


com_3 = pd.read_csv('com402-3.csv',header=None,quotechar='"',skipinitialspace=True)
imdb_3 = pd.read_csv('imdb-3.csv',header=None,quotechar='"',skipinitialspace=True)
com_3.columns = ['email_salt','movie_salt','date','rating']
imdb_3.columns = ['email','movie','date','rating']

email = 'keshav.singh@epfl.ch'

com_3['date'] = pd.to_datetime(com_3['date'], dayfirst=True)
com_3['min_date'] = com_3['date'] - pd.to_timedelta(13, unit='d')
com_3['max_date'] = com_3['date'] + pd.to_timedelta(13, unit='d')

imdb_3['date'] = pd.to_datetime(imdb_3['date'],dayfirst=True)

random_emails = [email] + list(imdb_3.email.unique()[0:35])

def iterator_movie_dict(com_3,my_subset):

    within_my_dates = pd.DataFrame(columns=['email_salt','movie_salt','date','rating','min_date','max_date','imdb_date','imdb_rating','imdb_movie'])
    for index, row in com_3.iterrows():

        for index_2, row_2 in my_subset.iterrows():

            if row.min_date <= row_2.date <= row.max_date:

                within_my_dates = within_my_dates.append({'email_salt':row.email_salt,
                                                          'movie_salt':row.movie_salt,
                                                          'date':row.date,
                                                          'rating':row.rating,
                                                          'min_date':row.min_date,
                                                          'max_date':row.max_date,
                                                          'imdb_date': row_2.date,
                                                          'imdb_rating': row_2.rating,
                                                          'imdb_movie': row_2.movie},ignore_index=True)

    same_ratings = within_my_dates.loc[within_my_dates['rating'] == within_my_dates['imdb_rating']]
    my_hash = same_ratings['email_salt'].value_counts().index[0]
    print(same_ratings['email_salt'].value_counts()[0])
    my_movies = same_ratings.loc[same_ratings['email_salt']==my_hash]
    my_movies = my_movies.drop_duplicates(subset=['imdb_movie'],keep=False).sort_values(by='imdb_movie')

    dict_movies = pd.Series(my_movies.movie_salt.values,index=my_movies.imdb_movie).to_dict()

    return my_hash, dict_movies



email_hashes = {}
movie_hashes = []

for email_ in random_emails:
    
    
    my_subset = imdb_3.loc[imdb_3['email']==email_]
    
    my_hash, dict_movie = iterator_movie_dict(com_3,my_subset)
    
    print("#########")
    print("The e-mail: {} , The hash: {}".format(email_,my_hash))
    
    email_hashes[email_] = my_hash
    movie_hashes.append(dict_movie)


final_dict = {}
for d in movie_hashes: 
    final_dict.update(d)
    
my_hash = email_hashes[email]
my_movies = com_3.loc[com_3['email_salt']== my_hash]

list_of_movies = []

for movie in my_movies.movie_salt.values:
    for key_, value_ in final_dict.items():
        if movie == value_:
            list_of_movies.append(key_)

write_res('movies_1c.txt',list_of_movies)
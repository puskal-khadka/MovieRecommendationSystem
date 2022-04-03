import pandas as pd
import pickle
import os
from movierecommendation.settings import BASE_DIR

"""
@author: https://github.com/puskal-khadka
"""
def getmovieList():
    moviesDF=getMovieDf()
    return moviesDF['title'].values

def getMovieDf():
    return pd.read_pickle(os.path.join(BASE_DIR,  r'recommendationEngine/movie_df.pkl'))


def recommendMovies(title):
    df=getMovieDf()
    path=os.path.join(BASE_DIR, r'recommendationEngine/cosine_simi.pkl')
    cosine_simi=pickle.load(open(path,'rb'))
    indices=pd.Series(df.index, index=df['title']).drop_duplicates()

    index=indices[title]
    similarity_score=cosine_simi[index]
    enumerated_sim_score= list(enumerate(similarity_score))
    recommended_movieList=sorted(enumerated_sim_score, key=lambda x:x[1],reverse=True)[1:6]
  
    movie_indices=[ i[0] for i in recommended_movieList ]

    originalMovieId=df.iloc[index].id
    recommendedIdList=df.iloc[movie_indices].id

    return originalMovieId,recommendedIdList



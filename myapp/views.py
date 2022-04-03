from django.shortcuts import render
from django.http import HttpResponse


from recommendationEngine.recommend import recommendMovies,getmovieList

from django.shortcuts import render
import requests

from .models import Movie
import random
"""
@author: https://github.com/puskal-khadka
"""

def index(request):
    movieList=getmovieList()
    title=random.choice(movieList)
    return recommend(request,title,True)


def recommendMovie(request):
     if request.method == "POST":
        title=request.POST["movieOptions"]
        return recommend(request,title,False)

def recommend(request,title, isAutoRecommend):
    try:
        originalId,recommended_movie_ID_List=recommendMovies(title)

        mainMovie=getMovieData(originalId)
        recommended_movie_data_List=[]
        for i in recommended_movie_ID_List:
            recommended_movie_data_List.append(getMovieData(i))
        print(recommended_movie_data_List)

        movieTitleList=getmovieList()

        return render(request,'index.html', {
            'allMovieTitleList':movieTitleList,
            'originalMovie':mainMovie,
            "recommendedMovieList":recommended_movie_data_List
            })
    except:
        if isAutoRecommend:
            return HttpResponse()
        else:
            return HttpResponse("Oops! This movie not found at the moment, Go back")




 
def getMovieData(movieId):
    tmbdApikey = "a83888242f103849bed9990ff6139469" #you can use your own tmdb api key here incase mine key expire
    apiUrl=f"https://api.themoviedb.org/3/movie/{movieId}?api_key={tmbdApikey}&language=en-US" 
    response=requests.get(apiUrl)
    movieData=response.json()

    print(movieData)
    obj=Movie()
    obj.movieId=movieId
    obj.title=movieData["original_title"]
    obj.overview=movieData["overview"]
    imgPath=movieData["poster_path"]
    obj.photoPath=f"https://image.tmdb.org/t/p/original/{imgPath}"
    obj.releaseDate=movieData["release_date"]   

    return obj 

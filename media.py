"""Defines the Movie class that contains the details of a movie."""
import webbrowser


class Movie(object):
    """This class provides a way to store movie related information.

    Attributes:
        title: A string to store the title of the movie.
        poster_image_url: A string to store the URL of the movie poster.
        storyline: A string to store the basic plot of the movie.
        id: A string to store the id to indentify the number of Movie
            objects created.
        movie_id : Astring to store the movie id returned by the TMDB API.
        release_date : A string to store the release date of the movie.
        backdrop_path: A string to store url of the backdrop image of
                        the movie.
    """

    def __init__(self, title, image_url, storyline, id, movie_id,
                 movie_release_date, backdrop_path):
        self.title = title
        self.poster_image_url = image_url
        self.storyline = storyline
        self.id = id,
        self.movie_id = movie_id,
        self.release_date = movie_release_date,
        self.backdrop_path = backdrop_path

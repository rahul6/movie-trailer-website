import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet'  type='text/css'>
    <!-- Bootstrap 4 -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css" integrity="sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js" integrity="sha384-3ceskX3iaEnIogmQchP8opvBy3Mi7Ce34nWjpBIwVTHfGYWQS9jwHDVRnpKKHJg7" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.3.7/js/tether.min.js" integrity="sha384-XTs3FgkjiBgo8qjEjBk0tGmf3wPrWtA6coPfQDfFEY8AnYJwjalXCiosYRBIBZX8" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/js/bootstrap.min.js" integrity="sha384-BLiI7JTZm+JWlgKa0M0kGRpJbF2J8q+qreVrKBC47e3K6BW78kGLrCkeRX6I9RoK" crossorigin="anonymous"></script>

    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
            background-color: #333;
            color: #CCC;
        }

        .navbar-fixed-top {
            background-color: #e74c3c;
            border-color: #c0392b;
        }

        .navbar-brand
        {
            color: #373535;
            font-size: 20px;
            font-family: 'Open Sans', sans-serif;
            font-style: italic;
            font-weight: bolder;
        }

        .movie-image {
            opacity: 0.2;
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
        }

        .movie-title {
            color: #000;
        }

        .movie_storyline {
            color: #000;
        }

        .poster_image {
            display: table-cell;
            vertical-align: middle;
        }

        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #444;
            cursor: pointer;
        }
        .movie-tile img {
            box-shadow: 7px 7px 12px #222;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            // Show the loading spinner
            $("#trailer-video-container").empty().html('<h1><i class="fa fa-circle-o-notch" aria-hidden="true"></i> Loading ...</h1>');

            // Get movie info from to display on modal
            var backdrop_path = $(this).attr('data-backdrop-path');
            var movie_poster = $(this).attr('data-poster');
            var movie_storyline = $(this).attr('data-storyline');
            var movie_title = $(this).attr('data-movie-title');
            var movie_id = $(this).attr('data-tmdb-id');
            var movie_release_date = $(this).attr('data-release-date');

            // Set the movie info in HTML elements
            $(".movie-image").css({'background-image':'url('+backdrop_path+')'});
            $(".movie_storyline").text(movie_storyline);
            $('.movie-poster').attr("src", movie_poster);
            $(".movie-title").text(movie_title);

            // Get the youtube id for the trailer from the Movie Database API
            $.getJSON('https://api.themoviedb.org/3/movie/'+movie_id+'/videos?api_key=f72b8cc0f8c7ab0a4ab50a2d5b16f32e', function (data) {
                // Check to make sure the movie has a trailer
                if(typeof data.results[0] !== 'undefined') {
                    var trailerYouTubeId = data.results[0].key;
                    var sourceUrl = 'https://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
                    $("#trailer-video-container").empty().append($("<iframe></iframe>", {
                        'id': 'trailer-video',
                        'type': 'text-html',
                        'src': sourceUrl,
                        'frameborder': 0
                    }));
                } else {
                    $("#trailer-video-container").empty().html("Sorry !! The trailer is unavailable.");
                }
            });

        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container"></div>
          <div style="position: relative;">
            <div class="movie-image"></div>
            <div class="container">
                <img src="" width="150px" style="float: left; margin: 10px;" class="movie-poster">
                <h2 class="movie-title"></h2>
                <p class="movie_storyline"></p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navbar -->
    <nav class="navbar navbar-fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#">
                <img src="icon.jpg" width="50" height="50" alt="Site logo">
                Fresh Tomatoes Movie Trailers
            </a>
        </div>
    </nav>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-xs-6 col-sm-3 movie-tile text-center" data-tmdb-id="{movie_id}" data-movie-title="{movie_title}" data-backdrop-path="{backdrop_path}" data-poster="{poster_image_url}" data-storyline="{movie_storyline}" data-release-date="{movie_release_date}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="200" height="290">
    <p id="title" style="font-size:16px">{movie_title}<br>
    <span style="font-size:14px;">Release date: {movie_release_date}</span>
    </p>
    <div style="position: absolute; bottom: 0; width: 100%; padding: 10px; color: #fff; text-shadow: 2px 2px 0 #000;">
    </div>
</div>
'''

def create_movie_tiles_content(movies):
    """ Creates each movie tile for the fresh tomatoes website. """
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title.encode("ascii", "ignore"),
            poster_image_url=movie.poster_image_url,
            movie_storyline=movie.storyline.encode('utf-8').strip(),
            movie_id=movie.movie_id[0],
            backdrop_path=movie.backdrop_path,
            id=movie.id,
            movie_release_date=movie.release_date[0]
        )
    return content

def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

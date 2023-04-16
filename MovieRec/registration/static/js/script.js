   // Function to handle form submission
   $('#submit-link').on('click', function (event) {
    event.preventDefault();
    var movieName = $('#movie-name').val();
    var emotionText = $('#emotion-text').val();
    var movieData = {
    "movie_name": movieName,
    "emotion_text": emotionText
}
        getMovieSuggestion(movieData);
    });

    // Function to call API and display movie suggestions
    function getMovieSuggestion(movieData) {
        $('#loading-spinner').show();


        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5655/suggest",
            data: JSON.stringify(movieData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                $('#loading-spinner').hide();

                // Update movie details on success
                var movieTitleElement = $('#movie-title');
                movieTitleElement.empty(); // Clear previous movie titles

                var movieImagesContainer = $('#movie-images-container');
                movieImagesContainer.empty(); // Clear previous movie images

                // Create a div element for the movie titles
                var movieTitlesContainer = $('<div>').attr('id', 'movie-titles-container');

                // Loop through movie suggestions and append movie titles and images
                for (var i = 0; i < response.length; i++) {
                    // Create a div element with a class of .card
                    var movieCard = $('<div>').addClass('card');

                    // Set the background image of the .card element to the movie-image URL
                    movieCard.css('background-image', 'url(' + response[i]['movie-image'] + ')');

                    // Create a title element with the movie title and append it to the movie card
                    var movieTitle = $('<h2>').text(response[i]['movie-title']).addClass('movie-title');
                    movieCard.append(movieTitle);

                    movieImagesContainer.append(movieCard);
                }

                // Append the movie titles container to the movie details
                movieTitlesContainer.appendTo('#movie-details');

                // Append the movie titles container to the movie details
                movieTitleElement.append(movieTitlesContainer);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error("Error:", textStatus, errorThrown);
                $('#loading-spinner').hide();

            }
        });
    }
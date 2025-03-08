(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-200px');
        }
    });
    
    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Latest-news-carousel
    $(".latest-news-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            },
            1200:{
                items:4
            }
        }
    });


    // What's New carousel
    $(".whats-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:2
            },
            1200:{
                items:2
            }
        }
    });



    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });



})(jQuery);

document.addEventListener("DOMContentLoaded", function () {
    // 1. Update Date
    function updateDate() {
        const now = new Date();
        const options = { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' };
        document.getElementById("weather-date").innerText = now.toLocaleDateString("en-US", options);
    }
    updateDate();

    // 2. Fetch Live Location & Weather using Tomorrow.io API
    function fetchWeather() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const apiKey = "DlZi5gqlEI1iWp6T3vVaEgT3V6GU6YPF";  // Replace with your Tomorrow.io API key
                const url = `https://api.tomorrow.io/v4/timelines?location=${lat},${lon}&fields=temperature&fields=weatherCode&timesteps=current&units=metric&apikey=${apiKey}`;

                try {
                    const response = await fetch(url);
                    const json = await response.json();
                    
                    // Extract current weather data
                    const data = json.data.timelines[0].intervals[0].values;
                    // Update Weather Icon based on weatherCode
                    const weatherCode = data.weatherCode;
                    const iconMap = {
                        0: "clear-day",        // Clear sky
                        1000: "clear-day",     // Clear, sunny
                        1001: "cloudy",        // Cloudy
                        1100: "partly-cloudy", // Partly Cloudy
                        1101: "partly-cloudy", // Partly Cloudy
                        1102: "cloudy",        // Cloudy
                        4000: "drizzle",       // Drizzle
                        5001: "flurries",      // Flurries
                        5100: "light-snow",    // Light Snow
                        8000: "thunderstorm"   // Thunderstorm
                        // Add more mapping as needed
                    };
                    const iconCode = iconMap[weatherCode] || "unknown";
                    document.getElementById("weather-icon").src = `https://www.tomorrow.io/images/icons/${iconCode}.png`;

                } catch (error) {
                    document.getElementById("temperature").innerText = "Error";
                    document.getElementById("location").innerText = "Weather Unavailable";
                }
            });
        }
    }
    fetchWeather();
});

  // Function to update the date dynamically
    function updateDate() {
        const options = { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' };
        const today = new Date().toLocaleDateString('en-US', options);
        document.getElementById('current-date').textContent = today;
    }

    // Call the function to update the date on page load
    updateDate();

    document.addEventListener("DOMContentLoaded", function () {
        let modal = document.getElementById("exampleModal");
        let modalDialog = modal.querySelector(".custom-modal");
    
        // When modal opens, slide it in
        modal.addEventListener("show.bs.modal", function () {
            modalDialog.style.right = "0";
        });
    
        // When modal closes, slide it back out
        modal.addEventListener("hidden.bs.modal", function () {
            modalDialog.style.right = "-100%";
        });
    });
    
    document.addEventListener("DOMContentLoaded", function () {
        let commentInput = document.querySelector(".comment-input");
    
        commentInput.addEventListener("input", function () {
            this.style.height = "50px"; // Reset height
            this.style.height = this.scrollHeight + "px"; // Expand dynamically
        });
    });
    
    function searchToggle(obj, evt){
        var container = $(obj).closest('.search-wrapper');
            if(!container.hasClass('active')){
                container.addClass('active');
                evt.preventDefault();
            }
            else if(container.hasClass('active') && $(obj).closest('.input-holder').length == 0){
                container.removeClass('active');
                // clear input
                container.find('.search-input').val('');
            }
    }

    //search
    function searchToggle(obj, event) {
        var wrapper = document.querySelector('.search-wrapper');
        if (!wrapper.classList.contains('active')) {
            wrapper.classList.add('active');
            event.stopPropagation();
        } else {
            wrapper.classList.remove('active');
            event.stopPropagation();
        }
    }
    
//shareoption function 
function shareWebsite() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: "Check out this amazing website!",
            url: window.location.href
        }).then(() => {
            console.log("Thanks for sharing!");
        }).catch((error) => {
            console.error("Error sharing:", error);
        });
    } else {
        alert("Sharing is not supported on this browser.");
    }
}
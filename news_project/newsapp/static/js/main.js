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

    // 2. Fetch Live Location & Weather
    function fetchWeather() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const apiKey = "47eed1a31f80d6bd24e9a10c56ab12fa"; 
                const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`;

                try {
                    const response = await fetch(url);
                    const data = await response.json();

                    // Update Temperature
                    document.getElementById("temperature").innerText = `${Math.round(data.main.temp)}°C`;
                    
                    // Update Location (City Name)
                    document.getElementById("location").innerText = data.name + ",";

                    // Update Weather Icon
                    const iconCode = data.weather[0].icon;
                    document.getElementById("weather-icon").src = `https://openweathermap.org/img/wn/${iconCode}.png`;

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
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        dateElement.textContent = today;
    }
}

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

    document.addEventListener('DOMContentLoaded', function() {
        const commentForm = document.getElementById('commentForm');
        const sendButton = document.getElementById('sendButton');
        const commentList = document.getElementById('comment-list');
        console.log("Detail page JS loaded", commentForm, sendButton, commentList);

        sendButton.addEventListener('click', function() {
            console.log("Send button clicked on detail page");
            const formData = new FormData(commentForm);
            fetch(commentForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            })
            .then(response => {
                console.log("Response:", response);
                return response.json();
            })
            .then(data => {
                console.log("Data:", data);
                if (data.success) {

                    const emptyMessage = document.getElementById('no-comments-msg');
                    if (emptyMessage) {
                        emptyMessage.remove();
                    }

                    const newComment = document.createElement('div');
                    newComment.classList.add('detailpage-usercomment');
                    newComment.innerHTML = `
                        <div class="detailpage-user_date">
                            <b><div class="detailpage-user" style="color:rgb(110, 110, 255)">${data.username}</div></b>
                            <div class="detailpage-date" style="font-size: 14px; color: grey">Just now</div>
                        </div>
                        <p>${data.comment}</p>
                    `;
                    commentList.prepend(newComment);
                    commentForm.reset();

                    const commentCountElem = document.getElementById('comment-count');
                    if (commentCountElem) {
                        let currentCount = parseInt(commentCountElem.innerText);
                        if (!isNaN(currentCount)) {
                            commentCountElem.innerText = currentCount + 1;
                        }
                    }

                } else {
                    alert('Failed to submit comment: ' + (data.errors || data.error));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting the comment.');
            });
        });
    });

    

    document.addEventListener("DOMContentLoaded", function () {
        // Get the selected category from the URL
        const urlParams = new URLSearchParams(window.location.search);
        const selectedCategory = urlParams.get('category');

        if (selectedCategory) {
            document.getElementById('selected-category').textContent = selectedCategory;
        }
    });

    // Update the dropdown text when a category is clicked
    document.querySelectorAll('.category-item').forEach(item => {
        item.addEventListener('click', function (event) {
            document.getElementById('selected-category').textContent = this.textContent;
        });
    });

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
    
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM fully loaded');
        
        // Element selections
        const editBtn = document.getElementById('edit-btn');
        const saveBtn = document.getElementById('save-btn');
        const backBtn = document.getElementById('back-btn');
        const wrapper = document.querySelector('.wrapper');
        const profileContainer = document.querySelector('.profile-container');
        const editPicBtn = document.getElementById('edit-pic-btn');
        const profilePicUpload = document.getElementById('profile-pic-upload');
        const profilePic = document.getElementById('profile-pic');
        const front = document.querySelector('.front');
        const back = document.querySelector('.back');
        
        // Debug element presence
        console.log('Elements found:', {
            editBtn: !!editBtn,
            saveBtn: !!saveBtn,
            backBtn: !!backBtn,
            wrapper: !!wrapper,
            profileContainer: !!profileContainer,
            front: !!front,
            back: !!back
        });
        
        // Store original dimensions
        let originalHeight = profileContainer ? profileContainer.offsetHeight + 'px' : '40rem';
        console.log('Original height:', originalHeight);
        
        // Check for error messages
        const hasErrors = document.querySelector('.validation-errors .alert-danger') || 
                         document.querySelector('.toast.error.show');
        console.log('Has errors:', !!hasErrors);
        
        // Function to adjust the container height based on content
        function adjustContainerHeight() {
            if (profileContainer) {
                const backContent = back ? back.offsetHeight : 0;
                const frontContent = front ? front.offsetHeight : 0;
                const maxHeight = Math.max(backContent, frontContent, 600) + 'px';
                console.log('Adjusting container height to:', maxHeight);
                profileContainer.style.minHeight = maxHeight;
                profileContainer.style.marginBottom = '8rem';
            }
        }
        
        // Handle error state - only flip if there are validation errors
        if (hasErrors && wrapper) {
            console.log('Flipping due to errors');
            wrapper.classList.add('flipped');
            
            if (back) {
                back.style.zIndex = '3';
                if (front) front.style.zIndex = '1';
            }
            
            // Adjust container height
            adjustContainerHeight();
        } else {
            console.log('No errors, ensuring front is visible');
            // Ensure we're not flipped if there are no errors
            if (wrapper) {
                wrapper.classList.remove('flipped');
            }
            
            // Make sure front is visible
            if (front) {
                front.style.zIndex = '3';
            }
            
            if (back) {
                back.style.zIndex = '1';
            }
        }
        
        // Handle edit button click
        if (editBtn) {
            editBtn.addEventListener('click', function() {
                console.log('Edit button clicked');
                // Store current height before flipping
                originalHeight = profileContainer ? profileContainer.offsetHeight + 'px' : originalHeight;
                
                // Ensure back has higher z-index during transition
                if (back) {
                    back.style.zIndex = '3';
                    if (front) front.style.zIndex = '1';
                }
                
                // Adjust container height
                adjustContainerHeight();
                
                // Flip the card
                if (wrapper) {
                    wrapper.classList.add('flipped');
                    console.log('Flipped wrapper');
                }
            });
        }
        
        // Handle back button click - make sure this works
        if (backBtn) {
            backBtn.addEventListener('click', function(e) {
                console.log('Back button clicked');
                e.preventDefault();
                
                // Flip back the card
                if (wrapper) {
                    wrapper.classList.remove('flipped');
                    console.log('Unflipped wrapper');
                }
                
                // Reset z-index after transition completes
                setTimeout(function() {
                    if (front) {
                        front.style.zIndex = '3';
                    }
                    if (back) {
                        back.style.zIndex = '1';
                    }
                    console.log('Reset z-indices');
                }, 600);
                
                // Clear any error messages
                const errorElements = document.querySelectorAll('.validation-errors .alert-danger, .toast.error.show');
                errorElements.forEach(el => {
                    el.style.display = 'none';
                });
                console.log('Cleared error messages');
                
                // Restore original height after transition
                if (profileContainer && originalHeight) {
                    setTimeout(function() {
                        profileContainer.style.minHeight = originalHeight;
                        profileContainer.style.marginBottom = '0';
                        console.log('Restored original height:', originalHeight);
                    }, 300);
                }
            });
        }
        
        // Handle profile picture upload
        if (editPicBtn && profilePicUpload) {
            editPicBtn.addEventListener('click', function() {
                profilePicUpload.click();
                console.log('Profile pic upload triggered');
            });
        }
        
        // Preview selected image
        if (profilePicUpload && profilePic) {
            profilePicUpload.addEventListener('change', function(e) {
                if (this.files && this.files[0]) {
                    var reader = new FileReader();
                    
                    reader.onload = function(e) {
                        profilePic.setAttribute('src', e.target.result);
                        console.log('Profile pic preview updated');
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
        
        // Check if we need to force proper state after everything loads
        window.addEventListener('load', function() {
            console.log('Window fully loaded');
            // Force proper z-index after everything else loads
            if (wrapper && wrapper.classList.contains('flipped')) {
                if (back) back.style.zIndex = '3';
                if (front) front.style.zIndex = '1';
            } else {
                if (front) front.style.zIndex = '3';
                if (back) back.style.zIndex = '1';
            }
            
            // Adjust container height again after all assets load
            adjustContainerHeight();
        });
    });
    

//search pagination strat
let page = 2; // Start from the second page since the first 6 are already loaded
let loading = false;
let hasNextPage = true;

async function loadMoreArticles() {
    if (loading || !hasNextPage) return;
    loading = true;
    document.getElementById('loader').style.display = 'block';

    try {
        const query = new URLSearchParams(window.location.search).get('q') || '';
        const response = await fetch(`?q=${query}&page=${page}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (!response.ok) throw new Error('Failed to fetch data');

        const data = await response.json();
        hasNextPage = data.has_next;

        data.articles.forEach(article => {
            const articleHtml = `
                <div class="row-sm-12 mb-4 article scale-hover">
                    <div class="row rounded" style="box-shadow: 5px 4px 5px 2px rgb(121, 121, 121);">
                        <div class="col-sm-5 p-0" style="height: 200px; border-radius: 10px 0 0 10px;">
                            ${article.image_url ? `<img src="${article.image_url}" alt="${article.head_line}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px 0 0 10px;">` : ''}
                        </div>
                        <div class="col-sm-7 p-3" style="height: 200px; border-radius: 0 10px 10px 0; background: linear-gradient(to top right, white, rgb(227, 243, 252));">
                            <h4><a href="/articledetail/${article.id}/">${article.head_line}</a></h4>
                            <p>${article.description.substring(0, 150)}...</p>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('article-container').insertAdjacentHTML('beforeend', articleHtml);
        });

        page++;
    } catch (error) {
        console.error(error);
    } finally {
        document.getElementById('loader').style.display = 'none';
        loading = false;
    }
}

window.addEventListener('scroll', () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
        loadMoreArticles();
    }
});
//search pagination end

let isPlaying = false;
let words = [];
let currentWordIndex = 0;
let utterance = null;

function toggleTTS() {
    let headline = document.querySelector(".h1.display-5").innerText;
    let content = document.getElementById("article-content").innerText;
    let button = document.getElementById("ttsButton");

    if (!isPlaying) {
        startTTS(headline, content, button);
    } else {
        stopTTS(button);
    }
}

function startTTS(headline, content, button) {
    let headlineUtterance = new SpeechSynthesisUtterance(headline);
    let transitionUtterance = new SpeechSynthesisUtterance("Now let's read the content.");
    let contentUtterance = new SpeechSynthesisUtterance(content);
    
    words = content.split(" ");
    currentWordIndex = 0;
    highlightText();

    headlineUtterance.onend = () => {
        speechSynthesis.speak(transitionUtterance);
    };
    
    transitionUtterance.onend = () => {
        speechSynthesis.speak(contentUtterance);
    };

    contentUtterance.rate = 1.0;
    contentUtterance.onboundary = (event) => {
        if (event.name === "word") {
            highlightNextWord();
        }
    };

    contentUtterance.onend = () => {
        isPlaying = false;
        button.innerHTML = '<i class="fa fa-volume-up"></i>Read';
        clearHighlight();
    };
    
    speechSynthesis.speak(headlineUtterance);
    isPlaying = true;
    button.innerHTML = '<i class="fa fa-pause"></i>Stop';
}

function stopTTS(button) {
    speechSynthesis.cancel();
    isPlaying = false;
    button.innerHTML = '<i class="fa fa-volume-up"></i>Read';
    clearHighlight();
}

function highlightText() {
    let article = document.getElementById("article-content");
    article.innerHTML = words.map((word, index) => `<span id='word-${index}'>${word}</span>`).join(" ");
}

function highlightNextWord() {
    if (currentWordIndex > 0) {
        document.getElementById(`word-${currentWordIndex - 1}`)?.classList.remove("highlight");
    }
    if (currentWordIndex < words.length) {
        document.getElementById(`word-${currentWordIndex}`)?.classList.add("highlight");
        currentWordIndex++;
    }
}

function clearHighlight() {
    document.getElementById("article-content").innerHTML = words.join(" ");
}
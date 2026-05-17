/*------------------------------------- Page Loader -------------------------------------*/
$(function () {
    setTimeout(() => {
        $('.page-loader').fadeOut('slow');
    }, 500);
});
/*------------------------------------- Sticky Header -------------------------------------*/
$(document).ready(function () {
    $(window).scroll(function () {
        var scrollPosition = $(window).scrollTop();
        if (scrollPosition >= 20) {
            $('#top-header, #top-navbar').addClass('fixed');
        } else {
            $('#top-header, #top-navbar').removeClass('fixed');
        }
    });
});
/*------------------------------------- Toggle Header Menu -------------------------------------*/
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links-mn');
    const overlay = document.querySelector('.overlay');

    if (navLinks.classList.contains('active')) {
        navLinks.classList.add('closing');
        overlay.classList.remove('active');
        setTimeout(() => {
            navLinks.classList.remove('active', 'closing');
        }, 300);
    } else {
        navLinks.classList.remove('closing');
        navLinks.classList.add('active');
        overlay.classList.add('active');
    }
}

// Close menu when clicking a menu link
document.querySelectorAll('.a-link').forEach(link => {
    link.addEventListener('click', function () {
        toggleMenu();
    });
});

// Close menu when clicking outside
document.addEventListener('click', function (event) {
    const navLinks = document.querySelector('.nav-links-mn');
    const overlay = document.querySelector('.overlay');
    const menuIcon = document.querySelector('.menu-icon');
    if (
        !navLinks.contains(event.target) &&
        !menuIcon.contains(event.target) &&
        overlay.classList.contains('active')
    ) {
        toggleMenu();
    }
});

/*------------- Shop Slider Home Screen ---------------------*/
$(document).ready(function () {
    $('.photo-gallery').slick({
        infinity: true,
        slidesToShow: 6,
        slidesToScroll: 1,
        autoplay: true,
        arrows: false,
        dots: false,
        speed: 1000,
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            }
        ]
    });
});

/*------------------------------------- Infinite Marquee -------------------------------------*/
document.querySelectorAll('.logos').forEach(function (logosContainer) {
    const copy = logosContainer.querySelector('.logos-slide').cloneNode(true);
    logosContainer.appendChild(copy);
});

/*------------- sayAboutSlider ---------------------*/
$(document).ready(function () {
    $('.sayAboutSlider').slick({
        infinity: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        arrows: true,
        dots: false,
        speed: 1000,
        prevArrow: '<button type="button" class="single-slick-arrow slick-prev"><img src="assets/images/svg/white-left-arrow.svg" alt="left-black-arrow"></button>',
        nextArrow: '<button type="button" class="single-slick-arrow slick-next"><img src="assets/images/svg/white-right-arrow.svg" alt="right-half-arrow"></button>',
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    arrows: false,
                }
            }
        ]
    });
});

/*------------- Suggestion Slider ---------------------*/
$(document).ready(function () {
    $('.wrapper').slick({
        infinity: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        arrows: false,
        dots: false,
        speed: 1000,
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    arrows: false,
                }
            }
        ]
    });
});

/*------------- custom-cursor ---------------------*/
document.addEventListener("DOMContentLoaded", function () {
    const cursor = document.createElement("div");
    cursor.classList.add("custom-cursor");

    const arrowImg = document.createElement("img");
    arrowImg.src = "assets/images/svg/arrow-bar-both.svg"; // Update with your correct green arrow image path
    arrowImg.classList.add("cursor-arrow");

    cursor.appendChild(arrowImg);
    document.body.appendChild(cursor);

    const suggBoxes = document.querySelectorAll(".cursor");

    suggBoxes.forEach((box) => {
        box.addEventListener("mouseenter", () => {
            cursor.style.display = "block";
        });

        box.addEventListener("mouseleave", () => {
            cursor.style.display = "none";
        });

        box.addEventListener("mousemove", (e) => {
            cursor.style.left = `${e.clientX}px`;
            cursor.style.top = `${e.clientY}px`;
        });
    });
});

/*------------------------------------- Pricing Tabs btn -------------------------------------*/
$(function () {
    $('.tabs-btn').on('click', 'a', function () {
        var tabId = $(this).attr('data-tab');

        $('.tabs-btn a').removeClass('active');
        $('.Tabcondent').removeClass('active');

        $(this).addClass('active');
        $('#' + tabId).addClass('active');
    });
});

/*------------------------------------- Form Change Toggle -------------------------------------*/
const toggleForm = () => {
    const container = document.querySelector('.container-demo');
    container.classList.toggle('active');
};
/*------------------------------------- Bottom To Top Button -------------------------------------*/
window.addEventListener('scroll', function () {
    var button = document.querySelector('.bottom-top-button');
    if (window.pageYOffset > 100) {
        button.style.display = 'block';

    } else {
        button.style.display = 'none';
    }
});

document.querySelector('.bottom-top-button').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

/*------------------------------------- Toggle Menu Open close acive -------------------------------------*/
$(document).ready(function () {
    function updateActiveLink() {
        var scrollPos = $(document).scrollTop();

        $(".a-link").each(function () {
            var section = $($(this).attr("href"));
            if (section.length) {
                var sectionTop = section.offset().top - 100;
                var sectionBottom = sectionTop + section.outerHeight();

                if (scrollPos >= sectionTop && scrollPos < sectionBottom) {
                    $(".a-link").removeClass("active-link");
                    $(this).addClass("active-link");
                }
            }
        });
    }
    $(window).on("scroll", updateActiveLink);

    $(".menu-icon").on("click", function () {
        $(".nav-links-mn").toggleClass("menu-open");
        updateActiveLink();
    });
});
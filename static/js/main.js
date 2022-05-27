(function ($) {
  "use strict";

  /*
  |--------------------------------------------------------------------------
  | Template Name: Multim
  | Author: Laralink
  | Version: 1.0.0
  |--------------------------------------------------------------------------
  |--------------------------------------------------------------------------
  | TABLE OF CONTENTS:
  |--------------------------------------------------------------------------
  |
  | 1. Preloader
  | 2. Mobile Menu
  | 3. Sticky Header
  | 4. Dynamic Background
  | 5. General Toggle
  | 6. Select 2
  | 7. Slick Slider
  | 8. Isotop Initialize
  | 9. Review
  | 10. Light Gallery
  | 11. Modal Video
  | 12. Hobble Effect
  | 13. Parallax
  | 14. Counter Animation
  | 15. Tabs
  | 16. Accordian
  | 17. Progress Bar
  | 18. Team Member
  | 19. CountDown
  | 20. Round Percent
  | 21. Range slider
  |
  */

  /*--------------------------------------------------------------
    Scripts initialization
  --------------------------------------------------------------*/
  $.exists = function (selector) {
    return $(selector).length > 0;
  };

  $(window).on("load", function () {
    $(window).trigger("scroll");
    $(window).trigger("resize");
    preloader();
    isotopInit();
  });

  $(function () {
    $(window).trigger("resize");
    mainNav();
    onePage();
    stickyHeader();
    dynamicBackground();
    generalToggle();
    select2Init();
    slickInit();
    isotopInit();
    review();
    lightGalleryInit();
    modalVideo();
    hobbleEffect();
    parallaxEffect();
    counterInit();
    tabs();
    accordian();
    progressBar();
    teamMember();
    countDown();
    roundPercentInit();
    rangeSlider();
    if ($.exists(".wow")) {
      new WOW().init();
    }
  });

  $(window).on("resize", function () {
    isotopInit();
  });

  $(window).on("scroll", function () {
    stickyHeader();
    parallaxEffect();
    counterInit();
  });

  /*--------------------------------------------------------------
    1. Preloader
  --------------------------------------------------------------*/
  function preloader() {
    $(".cs-preloader_in").fadeOut();
    $(".cs-preloader").delay(150).fadeOut("slow");
  }

  /*--------------------------------------------------------------
    2. Mobile Menu
  --------------------------------------------------------------*/
  function mainNav() {
    $(".cs-nav").append('<span class="cs-munu_toggle"><span></span></span>');
    $(".menu-item-has-children").append(
      '<span class="cs-munu_dropdown_toggle"></span>'
    );
    $(".cs-munu_toggle").on("click", function () {
      $(this)
        .toggleClass("cs-toggle_active")
        .siblings(".cs-nav_list")
        .slideToggle();
    });
    $(".cs-munu_dropdown_toggle").on("click", function () {
      $(this).toggleClass("active").siblings("ul").slideToggle();
      $(this).parent().toggleClass("active");
    });
    // Mega Menu
    $(".cs-mega-wrapper>li>a").removeAttr("href");
    // Special Nav
    $(".cs-hamburger").on("click", function () {
      $(this).toggleClass("active");
      $(".cs-nav_wrap").toggleClass("active");
      $("body").toggleClass("hamburger_active");
    });
    $(".cs-nav_cross").on("click", function () {
      $(".cs-nav_wrap").removeClass("active");
      $("body").toggleClass("hamburger_active");
    });
    // Search Toggle
    $(".cs-search_toggle").on("click", function () {
      $(this).toggleClass("active");
      $(".cs-search_wrap").toggleClass("active");
    });
    $(".cs-search_close, .cs-nav_overlay").on("click", function () {
      $(".cs-search_toggle").removeClass("active");
      $(".cs-search_wrap").removeClass("active");
    });
    // Sub category Toggle
    $(".cs-subcategory_toggle").on("click", function () {
      $(this).toggleClass("active").siblings("ul").slideToggle();
    });
  }

  // Smoth Animated Scroll
  function onePage() {
    $(".cs-smoth_scroll").on("click", function () {
      var thisAttr = $(this).attr("href");
      if ($(thisAttr).length) {
        var scrollPoint = $(thisAttr).offset().top;
        $("body,html").animate(
          {
            scrollTop: scrollPoint,
          },
          600
        );
      }
      return false;
    });
  }

  /*--------------------------------------------------------------
    3. Sticky Header
  --------------------------------------------------------------*/
  function stickyHeader() {
    var scroll = $(window).scrollTop();
    if (scroll >= 10) {
      $(".cs-sticky-header").addClass("cs-sticky-active");
    } else {
      $(".cs-sticky-header").removeClass("cs-sticky-active");
    }
  }

  /*--------------------------------------------------------------
    4. Dynamic Background
  --------------------------------------------------------------*/
  function dynamicBackground() {
    $("[data-src]").each(function () {
      var src = $(this).attr("data-src");
      $(this).css({
        "background-image": "url(" + src + ")",
      });
    });
  }

  /*--------------------------------------------------------------
    5. General Toggle
  --------------------------------------------------------------*/
  function generalToggle() {
    $(".cs-toggle_btn").on("click", function () {
      $(this).parent().toggleClass("active");
    });

    // Event demo Toggle
    $(".cs-event_toggle_btn").on("click", function () {
      $(this)
        .toggleClass("active")
        .siblings(".cs-event_toggle_body")
        .slideToggle();
    });
    $(".cs-event_toggle_body.active").slideDown();
  }

  /*--------------------------------------------------------------
    6. Select 2
  --------------------------------------------------------------*/
  function select2Init() {
    // Select box
    if ($.exists(".cs-select")) {
      $(".cs-select").select2({
        minimumResultsForSearch: -1,
      });
    }
    if ($.exists(".cs-select2")) {
      if ($.exists(".cs-select2")) {
        $(".cs-select2").select2();
      }
    }
  }

  /*--------------------------------------------------------------
    7. Slick Slider
  --------------------------------------------------------------*/
  function slickInit() {
    if ($.exists(".cs-slider")) {
      $(".cs-slider").each(function () {
        // Slick Variable
        var $ts = $(this).find(".cs-slider_container");
        var $slickActive = $(this).find(".cs-slider_wrapper");
        var $sliderNumber = $(this).siblings(".slider-number");

        // Auto Play
        var autoPlayVar = parseInt($ts.attr("data-autoplay"), 10);
        // Auto Play Time Out
        var autoplaySpdVar = 3000;
        if (autoPlayVar > 1) {
          autoplaySpdVar = autoPlayVar;
          autoPlayVar = 1;
        }
        // Slide Change Speed
        var speedVar = parseInt($ts.attr("data-speed"), 10);
        // Slider Loop
        var loopVar = Boolean(parseInt($ts.attr("data-loop"), 10));
        // Slider Center
        var centerVar = Boolean(parseInt($ts.attr("data-center"), 10));
        // Slider Center
        var variableWidthVar = Boolean(
          parseInt($ts.attr("data-variable-width"), 10)
        );
        // Pagination
        var paginaiton = $(this).children().hasClass("cs-pagination");
        // Slide Per View
        var slidesPerView = $ts.attr("data-slides-per-view");
        if (slidesPerView == 1) {
          slidesPerView = 1;
        }
        if (slidesPerView == "responsive") {
          var slidesPerView = parseInt($ts.attr("data-add-slides"), 10);
          var lgPoint = parseInt($ts.attr("data-lg-slides"), 10);
          var mdPoint = parseInt($ts.attr("data-md-slides"), 10);
          var smPoint = parseInt($ts.attr("data-sm-slides"), 10);
          var xsPoing = parseInt($ts.attr("data-xs-slides"), 10);
        }
        // Fade Slider
        var fadeVar = parseInt($($ts).attr("data-fade-slide"));
        fadeVar === 1 ? (fadeVar = true) : (fadeVar = false);

        // Slick Active Code
        $slickActive.slick({
          autoplay: autoPlayVar,
          dots: paginaiton,
          centerPadding: "0",
          speed: speedVar,
          infinite: loopVar,
          autoplaySpeed: autoplaySpdVar,
          centerMode: centerVar,
          fade: fadeVar,
          prevArrow: $(this).find(".cs-left_arrow"),
          nextArrow: $(this).find(".cs-right_arrow"),
          appendDots: $(this).find(".cs-pagination"),
          slidesToShow: slidesPerView,
          variableWidth: variableWidthVar,
          // slidesToScroll: slidesPerView,
          responsive: [
            {
              breakpoint: 1600,
              settings: {
                slidesToShow: lgPoint,
                // slidesToScroll: lgPoint,
              },
            },
            {
              breakpoint: 1200,
              settings: {
                slidesToShow: mdPoint,
                // slidesToScroll: mdPoint,
              },
            },
            {
              breakpoint: 992,
              settings: {
                slidesToShow: smPoint,
                // slidesToScroll: smPoint,
              },
            },
            {
              breakpoint: 768,
              settings: {
                slidesToShow: xsPoing,
                // slidesToScroll: xsPoing,
              },
            },
          ],
        });
      });
    }

    if ($.exists(".cs-slider_for")) {
      $(".cs-slider_for").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: ".cs-slider_nav",
      });
      $(".cs-slider_nav").slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: ".cs-slider_for",
        dots: false,
        prevArrow: false,
        nextArrow: false,
        focusOnSelect: true,
        vertical: true,
        verticalSwiping: true,
        responsive: [
          {
            breakpoint: 991,
            settings: {
              vertical: false,
              verticalSwiping: false,
            },
          },
        ],
      });
    }

    if ($.exists(".cs-slider_for_1")) {
      $(".cs-slider_for_1").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: ".cs-slider_nav_1",
      });
      $(".cs-slider_nav_1").slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: ".cs-slider_for_1",
        dots: false,
        prevArrow: false,
        nextArrow: false,
        focusOnSelect: true,
        responsive: [
          {
            breakpoint: 991,
            settings: {
              vertical: false,
              verticalSwiping: false,
            },
          },
        ],
      });
    }
  }

  /*--------------------------------------------------------------
    8. Isotop Initialize
  --------------------------------------------------------------*/
  function isotopInit() {
    if ($.exists(".cs-isotop")) {
      $(".cs-isotop").isotope({
        itemSelector: ".cs-isotop_item",
        transitionDuration: "0.60s",
        percentPosition: true,
        masonry: {
          columnWidth: ".cs-grid_sizer",
        },
      });
      /* Active Class of Portfolio*/
      $(".cs-isotop_filter ul li").on("click", function (event) {
        $(this).siblings(".active").removeClass("active");
        $(this).addClass("active");
        event.preventDefault();
      });
      /*=== Portfolio filtering ===*/
      $(".cs-isotop_filter ul").on("click", "a", function () {
        var filterElement = $(this).attr("data-filter");
        $(this).parents(".cs-isotop_filter").next().isotope({
          filter: filterElement,
        });
      });
    }
  }

  /*--------------------------------------------------------------
    9. Review
  --------------------------------------------------------------*/
  function review() {
    $(".cs-review").each(function () {
      var review = $(this).data("review");
      var reviewVal = review * 20 + "%";
      $(this).find(".cs-review_in").css("width", reviewVal);
    });
  }

  /*--------------------------------------------------------------
    10. Light Gallery
  --------------------------------------------------------------*/
  function lightGalleryInit() {
    $(".cs-lightgallery").each(function () {
      $(this).lightGallery({
        selector: ".cs-lightbox-item",
        subHtmlSelectorRelative: false,
        thumbnail: false,
        mousewheel: true,
      });
    });
  }

  /*--------------------------------------------------------------
    11. Modal Video
  --------------------------------------------------------------*/
  function modalVideo() {
    $(document).on("click", ".cs-video_open", function (e) {
      e.preventDefault();
      var video = $(this).attr("href");
      $(".cs-video_popup_container iframe").attr("src", video);
      $(".cs-video_popup").addClass("active");
    });
    $(".cs-video_popup_close, .cs-video_popup_layer").on("click", function (e) {
      $(".cs-video_popup").removeClass("active");
      $("html").removeClass("overflow-hidden");
      $(".cs-video_popup_container iframe").attr("src", "about:blank");
      e.preventDefault();
    });
  }

  /*--------------------------------------------------------------
    12. Hobble Effect
  --------------------------------------------------------------*/
  function hobbleEffect() {
    $(document)
      .on("mousemove", ".cs-hobble", function (event) {
        var halfW = this.clientWidth / 2;
        var halfH = this.clientHeight / 2;
        var coorX = halfW - (event.pageX - $(this).offset().left);
        var coorY = halfH - (event.pageY - $(this).offset().top);
        var degX1 = (coorY / halfH) * 8 + "deg";
        var degY1 = (coorX / halfW) * -8 + "deg";
        var degX2 = (coorY / halfH) * -50 + "px";
        var degY2 = (coorX / halfW) * 70 + "px";
        var degX3 = (coorY / halfH) * -10 + "px";
        var degY3 = (coorX / halfW) * 10 + "px";
        var degX4 = (coorY / halfH) * 15 + "deg";
        var degY4 = (coorX / halfW) * -15 + "deg";
        var degX5 = (coorY / halfH) * -30 + "px";
        var degY5 = (coorX / halfW) * 60 + "px";

        $(this)
          .find(".cs-hover_layer1")
          .css("transform", function () {
            return (
              "perspective( 800px ) translate3d( 0, 0, 0 ) rotateX(" +
              degX1 +
              ") rotateY(" +
              degY1 +
              ")"
            );
          });
        $(this)
          .find(".cs-hover_layer2")
          .css("transform", function () {
            return (
              "perspective( 800px ) translateY(" +
              degX2 +
              ") translateX(" +
              degY2 +
              ")"
            );
          });
        $(this)
          .find(".cs-hover_layer3")
          .css("transform", function () {
            return (
              "perspective( 800px ) translateX(" +
              degX3 +
              ") translateY(" +
              degY3 +
              ") scale(1.02)"
            );
          });
        $(this)
          .find(".cs-hover_layer4")
          .css("transform", function () {
            return (
              "perspective( 800px ) translate3d( 0, 0, 0 ) rotateX(" +
              degX4 +
              ") rotateY(" +
              degY4 +
              ")"
            );
          });
        $(this)
          .find(".cs-hover_layer5")
          .css("transform", function () {
            return (
              "perspective( 800px ) translateY(" +
              degX5 +
              ") translateX(" +
              degY5 +
              ")"
            );
          });
      })
      .on("mouseout", ".cs-hobble", function () {
        $(this).find(".cs-hover_layer1").removeAttr("style");
        $(this).find(".cs-hover_layer2").removeAttr("style");
        $(this).find(".cs-hover_layer3").removeAttr("style");
        $(this).find(".cs-hover_layer4").removeAttr("style");
        $(this).find(".cs-hover_layer5").removeAttr("style");
      });
  }

  /*--------------------------------------------------------------
    13. Parallax
  --------------------------------------------------------------*/
  function parallaxEffect() {
    $(".cs-parallax").each(function () {
      var windowScroll = $(document).scrollTop(),
        windowHeight = $(window).height(),
        barOffset = $(this).offset().top,
        barHeight = $(this).height(),
        barScrollAtZero = windowScroll - barOffset + windowHeight,
        barHeightWindowHeight = windowScroll + windowHeight,
        barScrollUp = barOffset <= windowScroll + windowHeight,
        barSctollDown = barOffset + barHeight >= windowScroll;

      if (barSctollDown && barScrollUp) {
        var calculadedHeight = barHeightWindowHeight - barOffset;
        var largeEffectPixel = calculadedHeight / 5;
        var mediumEffectPixel = calculadedHeight / 20;
        var miniEffectPixel = calculadedHeight / 10;

        $(this)
          .find(".cs-to_left")
          .css("transform", `translateX(-${miniEffectPixel}px)`);
        $(this)
          .find(".cs-to_right")
          .css("transform", `translateX(${miniEffectPixel}px)`);
        $(this)
          .find(".cs-to_up")
          .css("transform", `translateY(-${miniEffectPixel}px)`);
        $(this)
          .find(".cs-to_down")
          .css("transform", `translateY(${miniEffectPixel}px)`);
        $(this)
          .find(".cs-to_right_up")
          .css(
            "transform",
            `translate(${miniEffectPixel}px, -${miniEffectPixel}px)`
          );
        $(this)
          .find(".cs-to_left_up")
          .css(
            "transform",
            `translate(-${miniEffectPixel}px, -${miniEffectPixel}px)`
          );
        $(this)
          .find(".cs-to_right_down")
          .css(
            "transform",
            `translate(-${miniEffectPixel}px, ${miniEffectPixel}px)`
          );
        $(this)
          .find(".cs-to_left_down")
          .css(
            "transform",
            `translate(${miniEffectPixel}px, ${miniEffectPixel}px)`
          );
        $(this)
          .find(".cs-to_rotate")
          .css("transform", `rotate(${mediumEffectPixel}deg)`);
        $(this)
          .find(".cs-to_rotate_2")
          .css("transform", `rotate(-${mediumEffectPixel}deg)`);
        $(this)
          .find(".cs-bg_parallax")
          .css("background-position", `center -${largeEffectPixel}px`);
      }
    });
  }

  /*--------------------------------------------------------------
    14. Counter Animation
  --------------------------------------------------------------*/
  function counterInit() {
    if ($.exists(".odometer")) {
      $(window).on("scroll", function () {
        function winScrollPosition() {
          var scrollPos = $(window).scrollTop(),
            winHeight = $(window).height();
          var scrollPosition = Math.round(scrollPos + winHeight / 1.2);
          return scrollPosition;
        }

        $(".odometer").each(function () {
          var elemOffset = $(this).offset().top;
          if (elemOffset < winScrollPosition()) {
            $(this).html($(this).data("count-to"));
          }
        });
      });
    }
  }

  /*--------------------------------------------------------------
    15. Tabs
  --------------------------------------------------------------*/
  function tabs() {
    $(".cs-tabs.cs-fade_tabs .cs-tab_links a").on("click", function (e) {
      var currentAttrValue = $(this).attr("href");
      $(".cs-tabs " + currentAttrValue)
        .fadeIn(400)
        .siblings()
        .hide();
      $(this).parents("li").addClass("active").siblings().removeClass("active");
      e.preventDefault();
    });
  }

  /*--------------------------------------------------------------
    16. Accordian
  --------------------------------------------------------------*/
  function accordian() {
    $(".cs-accordian").children(".cs-accordian-body").hide();
    $(".cs-accordian.active").children(".cs-accordian-body").show();
    $(".cs-accordian_head").on("click", function () {
      $(this)
        .parent(".cs-accordian")
        .siblings()
        .children(".cs-accordian-body")
        .slideUp(250);
      $(this).siblings().slideDown(250);
      /* Accordian Active Class */
      $(this).parents(".cs-accordian").addClass("active");
      $(this).parent(".cs-accordian").siblings().removeClass("active");
    });
  }

  /*--------------------------------------------------------------
    17. Progress Bar
  --------------------------------------------------------------*/
  function progressBar() {
    $(".cs-progress").each(function () {
      var progressPercentage = $(this).data("progress") + "%";
      $(this).find(".cs-progress_in").css("width", progressPercentage);
    });
  }

  /*--------------------------------------------------------------
    18. Team Member
  --------------------------------------------------------------*/
  function teamMember() {
    $(".cs-member_social_toggle").on("click", function () {
      $(this).toggleClass("active");
    });

    $(".cs-team_member.cs-style5").hover(function () {
      $(this).addClass("active").siblings().removeClass("active");
    });
  }

  /*--------------------------------------------------------------
    19. CountDown
  --------------------------------------------------------------*/
  function countDown() {
    if ($.exists(".cs-countdown")) {
      $(".cs-countdown").each(function () {
        var _this = this;
        var el = $(_this).data("countdate");
        var countDownDate = new Date(el).getTime();
        var x = setInterval(function () {
          var now = new Date().getTime();
          var distance = countDownDate - now;
          var days = Math.floor(distance / (1000 * 60 * 60 * 24));
          var hours = Math.floor(
            (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
          );
          var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
          var seconds = Math.floor((distance % (1000 * 60)) / 1000);
          $(_this).find("#cs-count-days").html(days);
          $(_this).find("#cs-count-hours").html(hours);
          $(_this).find("#cs-count-minutes").html(minutes);
          $(_this).find("#cs-count-seconds").html(seconds);

          if (distance < 0) {
            clearInterval(x);
            $(_this).html("<div class='cs-token_expired'>TOKEN EXPIRED<div>");
          }
        }, 1000);
      });
    }
  }
  /*--------------------------------------------------------------
    20. Round Percent
  --------------------------------------------------------------*/
  function roundPercentInit() {
    if ($.exists(".cs-round_percentage")) {
      $(window).on("scroll", function () {
        function winScrollPosition() {
          var scrollPos = $(window).scrollTop(),
            winHeight = $(window).height();
          var scrollPosition = Math.round(scrollPos + winHeight / 1.2);
          return scrollPosition;
        }

        $(".cs-round_percentage").each(function () {
          var roundEffect = $(this).offset().top;
          if (roundEffect < winScrollPosition()) {
            $(this).each(function () {
              let roundRadius = $(this).find("circle").attr("r");
              let roundPercent = $(this).data("percent");
              let roundCircum = 2 * roundRadius * Math.PI;
              let roundDraw = (roundPercent * roundCircum) / 100 - 3;
              $(this).css("stroke-dasharray", roundDraw + " 999");
            });
          }
        });
      });
    }
  }
  /*--------------------------------------------------------------
    21. Range slider
  --------------------------------------------------------------*/
  function rangeSlider() {
    if ($.exists("#slider-range")) {
      $("#slider-range").slider({
        range: true,
        min: 0,
        max: 500,
        values: [75, 300],
        slide: function (event, ui) {
          $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
        },
      });
      $("#amount").val(
        "$" +
          $("#slider-range").slider("values", 0) +
          " - $" +
          $("#slider-range").slider("values", 1)
      );
    }
  }
})(jQuery); // End of use strict

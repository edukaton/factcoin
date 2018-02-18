$(document).ready(function () {
  var evalAuthor = $('#eval-author');
  var evalRelevance = $('#eval-relevance');
  var evalSimilar = $('#eval-similar');
  var evalClickbaits = $('#eval-clickbaits');

  var processSearching = function () {
    $('.criteria-unknown').hide();
    $('.criteria-false').hide();
    $('.criteria-true').hide();
    $('.criteria-spinner').show();
    var top = $('#fact-analysis').offset().top - 90;
    $('html, body').animate({ scrollTop: top }, 'slow');
  };

  var processFound = function (result) {
    $('.criteria-spinner').hide();

    console.log(result);
    if (parseInt(result['authors_score']) === 1) {
      evalAuthor.find('.criteria-true').show();
    }
    else {
      evalAuthor.find('.criteria-false').show();
    }

    evalRelevance.find('.criteria-unknown').show();

    if (parseInt(result['neighbours_count']) >= 1) {
      evalSimilar.find('.criteria-true').show();
    }
    else {
      evalSimilar.find('.criteria-false').show();
    }

    if (parseFloat(result['clickbait_score']) >= 0.5) {
      evalClickbaits.find('.criteria-true').show();
    }
    else {
      evalClickbaits.find('.criteria-false').show();
    }
  };

  var processNotFound = function (rb) {
    evalAuthor.find('.criteria-unknown').show();
    evalRelevance.find('.criteria-unknown').show();
    evalSimilar.find('.criteria-unknown').show();
    evalClickbaits.find('.criteria-unknown').show();
  };

  $('#search-form').on('submit', function (e) {
    processSearching();
    e.preventDefault();
    $.ajax({
      type: "get",
      url: "api/document/evaluation",
      data: {
        url: $(this).find('input[type=text]').val()
      },
      success: function (result) {
        processFound(result);
      },
      error: function (rb) {
        processNotFound(rb);
      }
    });
  });
});
$(document).ready(function () {
  var factAnalysis = $('div#fact-analysis');
  var footer = $('div#footer');

  var evalAuthor = $('#eval-author');
  var evalRelevance = $('#eval-relevance');
  var evalSimilar = $('#eval-similar');
  var evalClickbaits = $('#eval-clickbaits');

  var init = function () {
    factAnalysis.hide();
    footer.hide();
  };

  var processSearching = function () {
    factAnalysis.show();
    footer.show();

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

    /**
     * Criteria
     */
    if (result['authors_score'] === null) {
      evalAuthor.find('.criteria-unknown').show();
    }
    else if (parseInt(result['authors_score']) === 1) {
      evalAuthor.find('.criteria-true').show();
    }
    else {
      evalAuthor.find('.criteria-false').show();
    }

    evalRelevance.find('.criteria-unknown').show();

    if (result['neighbours_count'] === null) {
      evalSimilar.find('.criteria-unknown').show();
    }
    else if (parseInt(result['neighbours_count']) >= 1) {
      evalSimilar.find('.criteria-true').show();
    }
    else {
      evalSimilar.find('.criteria-false').show();
    }

    if (result['clickbait_score'] === null) {
      evalClickbaits.find('.criteria-unknown').show();
    }
    else if (parseFloat(result['clickbait_score']) >= 0.5) {
      evalClickbaits.find('.criteria-true').show();
    }
    else {
      evalClickbaits.find('.criteria-false').show();
    }

    /**
     * Analyzed article
     */
    $('h4#analyzed-header').text(result['title']);
    $('div#analyzed-text').html(result['text'].replace(/(?:\r\n|\r|\n)/g, '<br />'));
  };

  var processNotFound = function (rb) {
    evalAuthor.find('.criteria-unknown').show();
    evalRelevance.find('.criteria-unknown').show();
    evalSimilar.find('.criteria-unknown').show();
    evalClickbaits.find('.criteria-unknown').show();
  };

  init();

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
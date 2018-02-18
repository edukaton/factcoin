$(document).ready(function () {
  $('#search-form').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
      type: "get",
      url: "",
      data: {
        url: $(this).find('input[type=text]').val()
      },
      success: function (result) {
        console.log(result);
      },
      error: function (rb) {
        console.log(rb);
      }
    });
  });
});
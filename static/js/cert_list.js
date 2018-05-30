$(function () {
  $('#side-menu>li:nth-of-type(5)').addClass('active')
  $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

  $("#filterName").keyup(function(e) {
      $(".file-manager>ul>li")
        .hide()
        .filter(":contains('" + ($(this).val()).trim() + "')")
        .show();
      if($(this).val().trim() == "") {
        $(".file-manager>ul>li")
        .show()
      }
  });
})
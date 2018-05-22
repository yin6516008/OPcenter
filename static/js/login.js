$(function () {
  $('p').css('fontWeight','bold')
  if($('p').text().trim() == ''){
    $('p').hide()
  }else {
    $('p').show()
  }
})
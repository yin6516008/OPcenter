$(function () {
  $('#side-menu>li:nth-of-type(5)').addClass('active')
  $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

  $('#getTXT').click(function () {
      var domain = $('.input-lg').val()
      console.log(domain)
      $.ajax({
          url:'/cert/apply/postdomain/',
          data:{'domain':domain},
          type:'post',
          success:function (result) {
              $('#TXT_info').html(result)
          }
      })
  })


})
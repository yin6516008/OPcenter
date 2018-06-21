$(function () {
  // 左侧边栏
  $('#side-menu>li:nth-of-type(2)').addClass('active')
  $('#side-menu>li:nth-of-type(2)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('in')

    // 改变翻页的样式
  var re = /(\d+)\/$/.exec(window.location.pathname)
  if (re == null){
  var paramNum = 1
  }else{
  var paramNum = re[1]
  }
  $('#pageUl').find('li').children().each(function () {
    if($(this).text() == paramNum) { //页数等于地址栏参数
      $(this).css({ "backgroundColor": "#C6C6C7", "color": "#0d71c7" })
      // 分页过多以···显示
      $(this).parent().prev().prev().prev().prevAll().hide() //当页之前 除邻近3项 全部隐藏
      $(this).parent().next().next().next().nextAll().hide() //当页之后 除邻近3项 全部隐藏
      $(this).parent().prev().prev().prev().children().text('···')
      $(this).parent().next().next().next().children().text('···')
    }
  })
  $('#previous').parent().show().children().html('&laquo;')
  $('#next').parent().show().children().html('&raquo;')
})

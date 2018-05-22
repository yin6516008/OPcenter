$(function () {
  // ==========页码区域==========
  var id = null
  var idMax = null
  var idMin = null
  var pageNum = null
  var totalPagesNum = Math.ceil($('tbody>tr').length / 20)  //总页数
  // 若总页数等于1 隐藏页码区域
  if(totalPagesNum === 1) {
    $('.tableArea>nav').hide()
  }
  for(var i=totalPagesNum; i>=1; i--) {
    $('<li><a href="#" class="pageClick">'+i+'</a></li>').insertAfter('#nodeLi')
  }
  // 页面一加载 设置页码1的背景色
  $('#nodeLi').next().children().css({ "backgroundColor": "#999", "color": "#0d71c7" })
  // 页面一加载 若tr的id大于20 则隐藏
  $('tbody>tr').each(function () {
    id = Number($(this).attr('id'))
    if(id > 20) {
      $(this).hide()
    }
  })

  // 设置页码的点击事件
  $('.pageClick').click(function () {
    pageNum = Number($(this).text())
    idMax = pageNum * 20
    idMin = idMax - 19
    $('tbody>tr').each(function () {
      id = Number(($(this).attr('id')))
      if(idMin<=id & idMax>=id) {
        $(this).show()
      }else {
        $(this).hide()
      }
    })
    // 被点击的样式
    $('.pageClick').css({ "backgroundColor": "", "color": "" })    
    $(this).css({ "backgroundColor": "#999", "color": "#0d71c7" })
  })

  // 下一页的点击事件
  $('#next').click(function () {
    // 不点击页码 直接点击下一页的情况
    if(idMax === null) {
      idMax = 20
      idMin = 1
      pageNum++
    }
    // 获取到当前页展示的id 然后根据这个id往后加上20项显示
    console.log(idMax,id)
    if(idMax >= id) {
      return false
    }
    idMax += 20
    idMin += 20
    $('tbody>tr').each(function () {
      id = Number(($(this).attr('id')))
      if(idMin<=id & idMax>=id) {
        $(this).show()
      }else {
        $(this).hide()
      }
    })
    // 下一页按钮被点击的样式
    pageNum++
    $('.pageClick').each(function () {
      if(pageNum === Number($(this).text())){
        $(this).css({ "backgroundColor": "#999", "color": "#0d71c7" })
      }else {
        $(this).css({ "backgroundColor": "", "color": "" })
      }
    })
  })

  // 上一页的点击事件
  $('#previous').click(function () {
    // 不点击页码 直接点击上一页的情况
    if(idMax === null) {
      idMax = 20
      idMin = 1
      pageNum--
    }
    if(idMin == 1) {
      return false
    }
    idMax -= 20
    idMin -= 20
    $('tbody>tr').each(function () {
      id = Number(($(this).attr('id')))
      if(idMin<=id & idMax>=id) {
        $(this).show()
      }else {
        $(this).hide()
      }
    })
    // 上一页按钮被点击后的样式
    pageNum--
    $('.pageClick').each(function () {
      if(pageNum === Number($(this).text())){
        $(this).css({ "backgroundColor": "#999", "color": "#0d71c7" })
      }else {
        $(this).css({ "backgroundColor": "", "color": "" })
      }
    })
  })


})

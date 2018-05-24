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
  $('#nodeLi').next().children().css({ "backgroundColor": "#C6C6C7", "color": "#0d71c7" })
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
    $(this).css({ "backgroundColor": "#C6C6C7", "color": "#0d71c7" })
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
        $(this).css({ "backgroundColor": "#C6C6C7", "color": "#0d71c7" })
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
        $(this).css({ "backgroundColor": "#C6C6C7", "color": "#0d71c7" })
      }else {
        $(this).css({ "backgroundColor": "", "color": "" })
      }
    })
  })

// ================消息提示框================
$('#btn_confirm').click(function (e) {
var search_url = $('#inputSearch').val()
if ( search_url == '' ){
    $('#search_tip').text('请输入域名')
    $('.alert-danger').css("display", "block").addClass('fadeInRight')
    setTimeout(function () {
    $('.alert-danger').fadeOut()
    }, 2000)
}else {
    $.ajax({
        type: "POST",
        url: "/webmoni/tables/search/",
        data: {
            'url': search_url,
        },
        success: function (url_id) {
            if (url_id == 'no') {
                $('#search_tip').text('没有这个域名！')
                $('.alert-danger').css("display", "block").addClass('fadeInRight')
                setTimeout(function () {
                    $('.alert-danger').fadeOut()
                }, 2000)
            } else {
                console.log(url_id)
                window.location.href = "/webmoni/tables/search-" + url_id + '/';
            }
        }
    })
    }
})

// 删除按钮
$('[data-target="#delDomain"]').click(function () {
  var node = $(this).parent().parent().parent()
  .parent().parent()
  // 获取到对应的tr的节点号 --> 填充到隐藏域value
  var nodeNum = node.attr("data-id")
  $('#delete').val(nodeNum)

  // 确认删除模态框中添加对应节点名
  var nodeDomain = node.find('td:nth-of-type(3)').text()
  $('#delModalLabel').text('确认删除域名 "'+ nodeDomain + '" 吗?')
})

// =========删除的模态框==========
$('#confirmDel').click(function () { //点击确认按钮
  // $('.modal-backdrop').click(function () { //使点击遮罩失效
  //   $('#waving').show()
  // })
  

  var $that = $(this).siblings('input').val()
  // $('tbody>tr[data-id='+ $that +']').remove()
  // 请求数据
  $.ajax({
    type: "POST",
    url: "/webmoni/tables/delete/",
    data: {'url_id': $('#delete').val()},
    success: function (result) {
      if (result == 'OK') {
        $('tbody>tr[data-id='+ $that +']').remove()
      }
    }
  })
})



// 编辑按钮
$('[data-target="#editDomain"]').click(function () {
  var node = $(this).parent().parent().parent()
  .parent().parent()
  // 隐藏域value值
  var nodeNum = node.attr('data-id')
  $('#edit').val(nodeNum)
  $('#itemDetail_cate').val(node.find('td:nth-of-type(2)').text())
  $('#itemDetail_edit').val(node.find('td:nth-of-type(3)').text())
})
// 关闭编辑模态框 清除选中的值
$('#btn_close_bottom_edit,#btn_close_top_edit').click(function () {
  $('#edit_notadd,#edit_notwarn').attr('checked',false)
})
})

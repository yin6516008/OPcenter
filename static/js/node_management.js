$(function () {
  // 左侧边栏
  $('#side-menu>li:nth-of-type(2)').addClass('active')
  $('#side-menu>li:nth-of-type(2)>ul').removeClass('ulhide')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('collapse')
  $('#side-menu>li:nth-of-type(2)>ul').addClass('in')

  // 新增节点模态框
  // 关闭模态框时，清除模态框内文字
  $('#addNodeClose,#close').click(function () {
    $('#nodeNames,#nodeDetail,#addNodeDes').val('')
  })
  // 模态框表单验证
  $('#addNodeSave').attr('disabled', 'true')
  $('#nodeNames,#nodeDetail').keyup(function () {
    if(($('#nodeNames').val().trim() != '') && ($('#nodeDetail').val().trim() != '')) {
      $('#addNodeSave').removeAttr("disabled")
    }else {
      $('#addNodeSave').attr('disabled', 'true')
    }
  })

  // 删除按钮
  $('[data-target="#delNode"]').click(function () {
    var node = $(this).parent().parent().parent()
    .parent().parent()
    // 获取到对应的tr的节点号 --> 填充到隐藏域value
    var nodeNum = node.find('td:nth-of-type(1)').text()
    $('[type="hidden"]').val(nodeNum)

    // 确认删除模态框中添加对应节点名
    var nodePlace = node.find('td:nth-of-type(2)').text()
    $('#delModalLabel').text('确认删除 "'+ nodePlace + '" 节点吗?')
  })

})
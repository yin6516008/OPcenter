$(function () {
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




})
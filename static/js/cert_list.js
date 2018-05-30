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

    $('.folder-list>li').click(function () {
        var domain = $(this).attr('data-id')
        $.ajax({
            url:'/cert/getfile/',
            type:'post',
            data:{'domain':domain},
            success:function (msg) {
                var files = JSON.parse(msg)
                $('#file_table').html('')
                for (i in files){
                   var file = "<div class='file-box'>\
                        <div class='file'>\
                        <a href='/cert/download/" + domain + "/" + files[i] +"'>\
                        <span class='corner'></span>\
                        <div class='icon'>\
                        <i class='fa fa-file'></i>\
                        </div>\
                        <div class='file-name'>" + files[i] + "\
                        <br/>\
                    </div>\
                    </a>\
                </div>";
                $('#file_table').append(file)

                }
            }
        })
    })
})
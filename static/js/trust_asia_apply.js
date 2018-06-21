$(function () {
    $('#side-menu>li:nth-of-type(5)').addClass('active')
    $('#side-menu>li:nth-of-type(5)>ul').removeClass('ulhide')
    $('#side-menu>li:nth-of-type(5)>ul').addClass('collapse')
    $('#side-menu>li:nth-of-type(5)>ul').addClass('in')

    $('#getTXT').click(function () {
        $('#wave').show() // 点击按钮 显示动画
        $('#TXT_info').hide()
        $('#err').hide()
        $('.download-box').hide()
        $('#certList').remove()
        $('#record').text('系统操作信息：')
        var domain = $('#inputBox').val()
        var algorithm = $('input[name="algorithm"]').val()
        console.log(algorithm)
        $.ajax({
            url:'/cert/TrustAsia_apply/create_order/',
            data:{'domain':domain,'algorithm':algorithm},
            type:'post',
            success:function (msg) {
                $('#wave').hide()
                var result = JSON.parse(msg)
                if ( result.code == 0 ){
                    auth_info = result["msg"]["auth_info"][0]
                    $('#mediaId').html(result["msg"]["order_id"])
                    $('#mediaId').attr("name",auth_info["auth_key"])
                    var TXT = auth_info["auth_value"]
                    var host = auth_info["auth_path"]
                    $('#TXT_info').show()
                    $('#hostname').text(host)
                    $('#TXTval').text(TXT)
                }else{
                    var sys_info = result.msg//后台记录
                    $('#record').append('<hr/>').append(sys_info)  //后台记录添加到右侧
                }


            }
        })


    })


    $('#generateCert').click(function () {
        $('#err').hide()
        $('.download-box').hide()
        $('#wave').show()
        $('#wave>h3').text('证书生成中，请稍后···')
        var order = $('#mediaId').html()
        var domain = $('#mediaId').attr("name")
        console.log(domain)
        console.log(order)
        $.ajax({
            url: '/cert/TrustAsia_apply/Order_Authz/',
            data: {'order':order,"domain":domain},
            type: 'post',
            success: function (msg) {
                $('#wave').hide()
                var result = JSON.parse(msg)
                console.log(result)
                if ( result.code == 0 ){
                    $('.download-box').show()
                    $('#nginx').attr("href","/cert/TrustAsia_apply/download/nginx/"+ domain +"/")
                    $('#iis').attr("href","/cert/TrustAsia_apply/download/iis/"+ domain +"/")
                }else{
                    $('#record').append('<hr/>').append(result["msg"])
                }
            }
        })
    })

    // 监听输入框回车事件
    $('#inputBox').keyup(function (e) {
        if(e.keyCode == 13) {
            $('#getTXT').click()
        }
    })
    // 点击复制
    $('#copyHostname').click(function () {
        copyContent('hostname')
        $(this).after($('<span>复制成功！</span>'))
        $(this).next().css({'padding-left': '10px', 'padding-bottom':'0', 'color':'#f10b0b', 'font-size':'15px'})
        setTimeout(function () {
            $('#copyHostname').next().hide()
        }, 1500)
    })
    $('#copyTxtval').click(function () {
        copyContent('TXTval')
        $(this).after($('<span>复制成功！</span>'))
        $(this).next().css({'padding-bottom':'0', 'color':'#f10b0b', 'font-size':'15px'})
        setTimeout(function () {
            $('#copyTxtval').next().hide()
        }, 1500)
    })
    function copyContent(sourceId) {
        var Url2=document.getElementById(sourceId).innerText;
        var oInput = document.createElement('input')
        oInput.value = Url2
        document.body.appendChild(oInput)
        oInput.select()
        document.execCommand("Copy")
        oInput.className = 'oInput'
        oInput.style.display='none'
    }
})
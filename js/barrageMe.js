$(document).ready(function(){
    $("#submit-button").animate({backgroundColor:"#FFC107"},100);
})

function changeColor(){
	var nowColor = $('#bcolor').val();
	if (nowColor == '#ffffff'){
//		$("#submit-button").animate({color:"#000000"},200);
		$("#submit-button").animate({backgroundColor:"#FFC107"},100);
		$("#submit-button").css({"color":"black"})
		return;
	}
	else if (nowColor == '#99ffff'){
		$("#submit-button").animate({color:"#000000"},100);
		$("#submit-button").animate({backgroundColor:nowColor},100);
		return;
	}
	else{
		$("#submit-button").animate({backgroundColor:nowColor},100);
		$("#submit-button").animate({color:"#ffffff"},100);
	}
}

function sendBarrage(){
    if ($('#barrage').val().length > 32 || $('#barrage').val().length == 0){
        mdui.snackbar({
            message: 'Σ(ﾟдﾟlll)似乎出了点问题……'
        });
        if ($('#barrage').val().length >= 32){
            $("#errMsg").html("你输入的内容太长啦(╯‵□′)╯︵┻━┻");
        }
        else if ($('#barrage').val().length == 0){
            $("#errMsg").html("你总得说点什么吧(ˊ･ω･ ˋ)");
        }
        else{
            $("#errMsg").html("开发者也不知道出了什么问题_(:з」∠)_");
        }
        $('#binput').addClass("mdui-textfield-invalid")
        return false;
    }
    $("#progress").fadeIn();
    $("#submit-button").attr("disabled","disabled");
	$("#bform").ajaxSubmit({
		type:'post',
		url:'cgi-bin/backend_post.py',
		data:{
			btext:$('#barrage').val(),
			bcolor:$('#bcolor').val()
		},
		success:function(){

		},
		error:function(){
			mdui.snackbar({
                message: '发送失败'
            });
            return false;
		}
	});
    setTimeout('$("#submit-button").delay("2000").removeAttr("disabled")', 2000); 
//    $("#submit-button").delay("2000").removeAttr("disabled");
    $("#progress").delay("2000").fadeOut();
    setTimeout('mdui.snackbar({message: "发送成功！"});', 2000); 
    $("#barrage").val("");
//	alert(${pageContext.request.contextPath})
	return false;
}
function isEmpty(){
    if ($('#barrage').val().length <= 32 && $('#barrage').val().length != 0){
        $('#binput').removeClass("mdui-textfield-invalid")
    }
}
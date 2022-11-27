$(document).ready(function () {
    $("#btnclk").click(function() {
        username = $('#username').val();
        sessionStorage.setItem('myusername',username);
        userid=$('#uid').val();
        sessionStorage.setItem('myuid',userid);
       
    });
    $('#my_name').append(sessionStorage.getItem('myusername'));

});

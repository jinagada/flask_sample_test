// 오류 발생 시 처리
function common_ajaxFailProcess(e) {
    if (e.status == 403) {
        alert('Forbidden');
        location.href = e.responseJSON.error_msg;
    } else if (e.status == 404) {
        alert('Not Foundn');
        location.href = '/';
    } else {
        if ($(e.responseText).find('#error_msg')[0]) {
            alert($(e.responseText).find('#error_msg').text());
        } else {
            alert('System Error');
        }
    }
}

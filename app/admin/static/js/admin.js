function load_content(content, elem) {
    elem.textContent = content;
}

$("#postFile").change(function() {
    var fr = new FileReader();
    var text = $('#postText')[0];
    // On successful load of content, put into textarea
    fr.onload = function() {
        load_content(fr.result, text);
    }
    fr.readAsText($(this).prop('files')[0]);
});

function renderPreview(response) {
    if( response['message'] === 'success') {
        var preview = $('#preview');
        preview.empty();
        preview.html(response['content']);
    }
    else {
        alert('Bad input or no input!');
    }
};

$("#getPreview").click(function() {
    var text = $('#postText')[0].value;
    $.ajax({
        url: $SCRIPT_ROOT + 'admin/_preview',
        dataType: 'json',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({'postText': text}),
        success: function(response) {
            renderPreview(response);
        }
    });
})
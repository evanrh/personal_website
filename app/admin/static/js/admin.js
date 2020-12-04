var newPostMDE = new SimpleMDE({ element: document.getElementById('postText')})
var editPostMDE = new SimpleMDE({ element: document.getElementById('postContent') })

function load_content(content, editor) {
    editor.value(content);
}

$("#postFile").change(function() {
    var fr = new FileReader();
    // On successful load of content, put into textarea
    fr.onload = function() {
        load_content(fr.result, newPostMDE);
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

$("button[name='render']").click(function() {
    var text = newPostMDE.value();
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
});

function modal_content(response, modal, mde) {
    load_content(response['content'], mde);
    modal.querySelector('input[name="title"]').value = response['title'];
    modal.querySelector('textarea[name="preview"]').value = response['preview'];
}
$('button[name="editPost"]').click(function() {
    document.getElementById('editPostModal').querySelector('.modal-footer > div[name="id"]').innerText = this.dataset.id;
    $.ajax({
        url: $SCRIPT_ROOT + 'admin/_post-content',
        dataType: 'json',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({'id': this.dataset.id }),
        success: function(response) {
            modal_content(response, document.getElementById('editPostModal'), editPostMDE);
        }
    })
});

$('button[name="save"]').click(function() {
    // Send post data off to database
    var parent = this.parentElement.previousElementSibling;
    var title = parent.querySelector('input[name="title"]').value;
    var preview = parent.querySelector('textarea[name="preview"]').value;
    var body = this.dataset.mde === 'edit' ? editPostMDE.value() : newPostMDE.value();
    var arr = {'title': title, 'preview': preview, 'body': body};
    if( this.dataset.mde === 'edit' ) {
        var id = this.parentElement.querySelector('div[name="id"]').innerText;
        arr['id'] = id;
    }
    $.ajax({
        url: $SCRIPT_ROOT + 'admin/_update-post',
        dataType: 'json',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(arr),
        success: function(response) {
            if( response['message'] === 'success') {
                window.location.reload();
            }
            else {
                alert('Something went wrong');
            }
        }
    });
});
var newPostMDE = new SimpleMDE({ element: document.getElementById('postText')})
var editPostMDE = new SimpleMDE({ element: document.getElementById('postContent') })

function remove_all_child_nodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

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
    var categories = modal.querySelector('ul');
    remove_all_child_nodes(categories);

    for(var i = 0; i < response['categories'].length; i++) {
        add_category_button(categories, response['categories'][i]);
    }
}
$('button[name="editPost"]').click(function() {
    var id_tool = document.getElementById('editPostForm').querySelector('input[id="id"]');
    id_tool.value = this.dataset.id;
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

function remove_parent(elem) {
    elem.parentElement.remove();
}

function add_category_button(ul, value='') {
    var num = ul.children.length;
    var div = document.createElement('div');
    var btn = document.createElement('button');
    btn.innerHTML = '&times;';
    btn.name = 'removeCategory';
    btn.type = 'button';
    btn.onclick = function() {
        remove_parent(btn);
    };
    var node = document.createElement('input');
    node.value = value;
    node.className = 'form-control col-md-2';
    node.name = 'categories-' + num;
    div.appendChild(btn);
    div.appendChild(node);
    ul.appendChild(div);
}
// Add category button to list
$('button[name="addCategory"]').click(function() {
    var parent = this.parentElement;
    var ul = parent.querySelector('ul');
    add_category_button(ul);
});

function upload_new_post(form_id) {
    var form = $('#' + form_id);

    // Add submit button to form data
    var submit = $('input[type="submit"]', form);

    $.ajax({
        data: form.serialize() + '&' + encodeURI( $(submit).attr('name') ) + '=' + encodeURI( $(submit).val() ),
        type: 'POST',
        url: $SCRIPT_ROOT + 'admin/_post-edit',
        contentType: 'application/x-www-form-urlencoded; charset=utf-8',
        dataType: 'json'
    }).done(function(data) {
        window.location.reload();
    });
}

$('#newPostForm').on('submit', function(event) {
    event.preventDefault();
    upload_new_post('newPostForm');
    return false;
})

$('#editPostForm').on('submit', function(event) {
    event.preventDefault();
    upload_new_post('editPostForm');
    return false;
});

$('')
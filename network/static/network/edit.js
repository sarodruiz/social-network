document.addEventListener('DOMContentLoaded', () => {    
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.onclick = function (event) {
            on_edit(this.dataset.id);
        }
    });

    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.onclick = function (event) {
            save(this.dataset.id);
        }
    });
});

function on_edit(post_id) {
    const content = document.querySelector(`#post${post_id}-content`);
    const edit_form = document.querySelector(`#post${post_id}-edit-form`);
    const edit_text = document.querySelector(`#post${post_id}-edit-text`);
    const edit_btn = document.querySelector(`#edit-btn${post_id}`);
    const save_btn = document.querySelector(`#save-btn${post_id}`);

    edit_form.style.display = 'block';
    save_btn.style.display = 'block'
    edit_text.value = content.innerHTML;
    content.style.display = 'none';
    edit_btn.style.display = 'none';
}

function save(post_id) {
    const content = document.querySelector(`#post${post_id}-content`);
    const edit_form = document.querySelector(`#post${post_id}-edit-form`);
    const edit_text = document.querySelector(`#post${post_id}-edit-text`);
    const edit_btn = document.querySelector(`#edit-btn${post_id}`);
    const save_btn = document.querySelector(`#save-btn${post_id}`);

    if (edit_text.value != "") {
        fetch('/edit', {
            method: 'PUT',
            body: JSON.stringify({
                id: post_id,
                content: edit_text.value
            })
        })
        .then(response => response.json())
        .then(data => {
            document.querySelector(`#post${post_id}-content`).innerHTML = `${data.content}`;
        });
    }

    edit_form.style.display = 'none';
    save_btn.style.display = 'none'
    content.style.display = 'block';
    edit_btn.style.display = 'block';
}
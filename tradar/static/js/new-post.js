function activateNewPostForm() {
  this.getElementsByClassName('post-header')[0].classList.remove('hidden');
  this.getElementsByClassName('post-footer')[0].classList.remove('hidden');
  this.removeEventListener('focus', activateNewPostForm, true);
};

function deactivateNewPostForm() {
  var form = this.parentForm;
  form.getElementsByClassName('post-header')[0].classList.add('hidden');
  form.getElementsByClassName('post-footer')[0].classList.add('hidden');
  form.addEventListener('focus', activateNewPostForm, true);
}

window.addEventListener('load',
  function() {
    var forms = document.getElementsByClassName('new-post');
    for (i=0; i < forms.length; i++) {
      var form = forms.item(i);
      close_button = form.getElementsByClassName('post-close')[0];
      close_button.parentForm = form;
      close_button.addEventListener('click', deactivateNewPostForm);

      // hide extra post controls
      form.getElementsByClassName('post-header')[0].classList.add('hidden');
      form.getElementsByClassName('post-footer')[0].classList.add('hidden');
      form.addEventListener('focus', activateNewPostForm, true);
    };
  });

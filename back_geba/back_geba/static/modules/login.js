document.addEventListener("DOMContentLoaded", function(event) {
   authVerifyLogin();
});

document.querySelector('#password').addEventListener("keyup", (e) => {
  const mPressed = e.keyCode || e.which;
  if(mPressed === 9 || mPressed === 13) {
    acceder();
  }
  return true;
});

function acceder() {
    clearMessage();
    let username = getValue('username');
    let password = getValue('password');
    postData('/api/token/', {username, password}).then((response) => {
      if(typeof response.status !== undefined && response.status > 201) {
        showMessage('danger', response.message, true, 5000);
        return;
      }
      saveToken(response);
      saveCurrentUser(response);
      redirect('/mis-cuentas');
    });
}

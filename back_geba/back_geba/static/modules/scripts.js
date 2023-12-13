/*
 * Utiles
 **/
 document.addEventListener("DOMContentLoaded", function(event) {
    let currentUser = getCurrentUser();
    if(currentUser != null) {
        let username = currentUser.username;
        document.querySelector('#lblCurrentUser').innerHTML = `<span class="icon-person text-primary" style="margin-left: 10px;margin-top:8px;margin-bottom:3px;"></span> ${username} `;

        if(currentUser.is_superuser) {
            document.querySelector('.nav-admin').style.display = 'block';
            document.querySelector('.nav-cliente').style.display = 'none';
        } else {
            document.querySelector('.nav-admin').style.display = 'none';
            document.querySelector('.nav-cliente').style.display = 'block';
        }
    } else {
        document.querySelector('#menuAuth').style.display = 'none';
    }
});

 function authVerifyLogin() {
    let token = getToken();
    if(token != null) {
        redirect('/mis-cuentas');
    }
 }

  function authVerifyPage() {
    let token = getToken();
    if(token == null) {
        redirect('/login');
    }
 }

 function saveToken(data) {
    if(data != null) {
        localStorage.setItem("gebaToken", data.access);
    }
 }

 function getToken() {
    console.log('getToken');
    if(localStorage.getItem("gebaToken") != undefined
    && localStorage.getItem("gebaToken") != null
    && localStorage.getItem("gebaToken") != "") {
        return localStorage.getItem("gebaToken");
    }
    return null;
 }

 function saveCurrentUser(data) {
    if(data != null) {
        let user = {
            id: data.id,
            idCliente: data.id_cliente,
            username: data.username,
            firstName: data.first_name,
            lastName: data.last_name,
            email: data.email,
            is_superuser: data.is_superuser
        };
        localStorage.setItem("gebaUser", JSON.stringify(user));
    }
 }

 function logout() {
    localStorage.setItem("gebaToken", '');
    localStorage.setItem("gebaUser", '');
    redirect('/login');
 }

 function getCurrentUser() {
    if(localStorage.getItem("gebaUser") != undefined
    && localStorage.getItem("gebaUser") != null
    && localStorage.getItem("gebaUser") != "") {
        return JSON.parse(localStorage.getItem("gebaUser"));
    }
    return null;
 }

function redirect(page) {
  window.location.href = page;
}

 async function postData(url = '', data = {}) {
   let headers = { 'Content-Type': 'application/json' };
   let token = getToken();
   if(token != null) {
      headers = headers = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` };
   }
  const response = await fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    let jsonError = await response.json();
    let message = jsonError.message;
    if(response.status == 401) { message = 'Credenciales inválidas'; }
    return {status: response.status, message: message};
  }
  return response.json();
}

 async function getData(url = '') {
   let headers = { 'Content-Type': 'application/json' };
   let token = getToken();
   if(token != null) {
      headers = headers = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` };
   }
  const response = await fetch(url, {
    method: 'GET',
    headers: headers
  });
  if (!response.ok) {
    let jsonError = await response.json();
    let message = jsonError.message;
    if(response.status == 401) { message = 'Credenciales inválidas'; }
    return {status: response.status, message: message};
  }
  return response.json();
}

function getValue(key) {
  const data = document.querySelector('#'+key);
  if(data != null) {
    return data.value;
  }
  return null;
}

function setValue(key, value) {
  document.querySelector('#'+key).value = value;
}

function clearMessage() {
   document.querySelector('#message').innerHTML = '';
}

function showMessage(tipo, msg, isTitle, timeout) {
  const message = msg.replace(/["]/g, "");
  const messageHTML = `<div class="alert alert-${tipo}">${ isTitle ? '<strong>¡Atención! </strong> ':''} ${message}</div>`;
  document.querySelector('#message').innerHTML = messageHTML;
  if(timeout != null) {
      setTimeout(function() {
         document.querySelector('#message').innerHTML = '';
      }, timeout);
  }
}


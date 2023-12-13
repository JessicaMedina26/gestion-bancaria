var idCuenta = 0;
var nroCuenta = 0;
document.addEventListener("DOMContentLoaded", function(event) {
    authVerifyPage();
    getParams();
    verMisMovimientos();
});

function getParams() {
    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams == undefined || urlParams == null) {
        redirect('/mis-cuentas/');
        return;
    }

    idCuenta = urlParams.get('id');
    nroCuenta = urlParams.get('cuenta');
    if(idCuenta == undefined || idCuenta == null || nroCuenta == undefined || nroCuenta == null) {
        redirect('/mis-cuentas/');
        return;
    }
}

function redirectTab(url) {
    redirect(`${url}?id=${idCuenta}&cuenta=${nroCuenta}`);
}

function verMisMovimientos() {
    let currentUser = getCurrentUser();
    if(currentUser == null) return;

    getData(`/api/movimiento/all/?cuenta=${idCuenta}`).then((response) => {
      if(typeof response.status !== undefined && response.status > 201) {
        document.querySelector('#sectionPage').style.display = 'none';
        showMessage('danger', response.message, true, null);
      }
      console.log('ddd',{ response });
      document.querySelector('#lista').innerHTML = previewDetail(response);
    });
}

function previewDetail(response) {
    let htmlView = '';
    response.forEach((row) => {
        htmlView+= `<tr>
            <td><span style="font-size:15px;padding:10px" class="badge badge-soft-primary">${Math.round(row.cuenta_origen)}</span></td>
            <td><span style="font-size:15px;padding:10px" class="badge badge-soft-primary">${Math.round(row.cuenta_destino)}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.tipo_movimiento}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.saldo_anterior}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.monto_movimiento}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.saldo_actual}</span></td>
        </tr>`;
    });
    return htmlView;
}

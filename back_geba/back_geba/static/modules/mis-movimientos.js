var id_cuenta = 0;
var nro_cuenta = 0;
document.addEventListener("DOMContentLoaded", function(event) {
    authVerifyPage();

    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams == undefined || urlParams == null) {
        redirect('/mis-cuentas/');
        return;
    }
    id_cuenta = urlParams.get('id');
    nro_cuenta = urlParams.get('cuenta');
    if(id_cuenta == undefined || id_cuenta == null || nro_cuenta == undefined || nro_cuenta == null) {
        redirect('/mis-cuentas/');
        return;
    }

    verMisMovimientos(id_cuenta);
});

function redirectTab(url) {
    redirect(`${url}?id=${id_cuenta}&cuenta=${nro_cuenta}`);
}

function verMisMovimientos(id_cuenta) {
    let currentUser = getCurrentUser();
    if(currentUser == null) return;

    getData(`/api/movimiento/all/?cuenta=${id_cuenta}`).then((response) => {
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

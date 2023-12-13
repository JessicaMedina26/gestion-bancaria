var cuenta = 0;
document.addEventListener("DOMContentLoaded", function(event) {
    authVerifyPage();

    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams == undefined || urlParams == null) {
        redirect('/mis-cuentas/');
        return;
    }
    cuenta = urlParams.get('cuenta');
    if(cuenta == undefined || cuenta == null) {
        redirect('/mis-cuentas/');
        return;
    }

    verMisMovimientos(cuenta);
});


function redirectTab(page) {
    redirect(`${page}?cuenta=${cuenta}`);
}


function verMisMovimientos(cuenta) {
    let currentUser = getCurrentUser();
    if(currentUser == null) return;

    getData(`/api/movimiento/all/?cuenta=${cuenta}`).then((response) => {
      if(typeof response.status !== undefined && response.status > 201) {
        document.querySelector('#sectionPage').style.display = 'none';
        showMessage('danger', response.message, true, null);
      }
      console.log('ddd',{ response });
      document.querySelector('#lista').innerHTML = previewDetail(response);
    });
}

function deposito(id_movimiento){
    console.log(id_movimiento);
}

function transferencia(id_movimiento){
    console.log(id_movimiento);
}

function extraccion(id_movimiento){
    console.log(id_movimiento);
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

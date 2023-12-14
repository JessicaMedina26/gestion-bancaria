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
        let movimiento = '';
        let movimientoBadge = 'badge-soft-primary';
        let ctaOrigen = Math.round(row.cuenta_origen);
        let ctaDestino = Math.round(row.cuenta_destino);

        if(ctaOrigen == 0) {
            ctaOrigen = '-';
            movimiento = 'Depósito';
            movimientoBadge = 'badge-soft-success';
        }
        if(ctaDestino == 0) {
             ctaDestino = '-';
             movimiento = 'Extracción';
             movimientoBadge = 'badge-soft-danger';
        }
        if(ctaOrigen > 0 && ctaDestino > 0) {
            movimiento = 'Transferencia';
            movimientoBadge = 'badge-soft-primary';
        }

        htmlView+= `<tr>
            <td><span style="font-size:15px;padding:10px" class="badge ${movimientoBadge}">${movimiento}</span></td>
            <td><span style="font-size:15px;padding:10px;font-weight:bold;">${ctaOrigen}</span></td>
            <td><span style="font-size:15px;padding:10px;font-weight:bold;">${ctaDestino}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.tipo_movimiento}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.saldo_anterior}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.monto_movimiento}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.saldo_actual}</span></td>
        </tr>`;
    });
    return htmlView;
}

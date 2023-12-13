var idCuenta = 0;
var nroCuenta = 0;
document.addEventListener("DOMContentLoaded", function(event) {
    authVerifyPage();
    getParams();
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

    setValue('nro_cuenta_origen', nroCuenta);
    setValue('moneda', 'GS');
}

function redirectTab(url) {
    redirect(`${url}?id=${idCuenta}&cuenta=${nroCuenta}`);
}

function procesar() {
    clearMessage();
    const body = {
        moneda: getValue('moneda'),
        monto: getValue('monto'),
        nro_cuenta_origen: nroCuenta,
        nro_cuenta_destino: getValue('nro_cuenta_destino'),
        canal: 'WEB'
    };
    postData('/api/movimiento/deposit/', body).then((response) => {
      if(typeof response.status !== undefined && response.status > 201) {
        showMessage('danger', response.message, true, 5000);
        return;
      }
      showMessage('success', response.message, true, 5000);
    });
}

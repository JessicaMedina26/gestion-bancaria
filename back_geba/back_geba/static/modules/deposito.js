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
});

function redirectTab(url) {
    redirect(`${url}?id=${id_cuenta}&cuenta=${nro_cuenta}`);
}


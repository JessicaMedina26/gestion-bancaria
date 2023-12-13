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

});

function redirectTab(page) {
    redirect(`${page}?cuenta=${cuenta}`);
}
document.addEventListener("DOMContentLoaded", function(event) {
    authVerifyPage();
    verMisCuentas();
});


function verMisCuentas() {
    let currentUser = getCurrentUser();
    if(currentUser == null) return;

    getData(`/api/cuenta/all/?cliente=${currentUser.idCliente}`).then((response) => {
      if(typeof response.status !== undefined && response.status > 201) {
        document.querySelector('#sectionPage').style.display = 'none';
        showMessage('danger', response.message, true, null);
      }
      console.log('ddd',{ response });
      document.querySelector('#lista').innerHTML = previewDetail(response);
    });
}

function redirectMovimiento(id_cuenta, nro_cuenta){
    redirect(`/mis-movimientos/?cuenta=${id_cuenta}`);
}

function previewDetail(response) {
    let htmlView = '';
    response.forEach((row) => {
        htmlView+= `<tr>
            <td><span style="font-size:15px;padding:10px" class="badge badge-soft-primary">${row.nro_cuenta}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.nro_contrato}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.tipo_cuenta}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.saldo}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.moneda}</span></td>
            <td>
                <button type="button" class="btn"
                    onclick="redirectMovimiento('${row.id_cuenta}','${row.nro_cuenta}')">
                    <i class="icon-arrow-right text-primary" style="font-size:20px"></i>
                </button>
            </td>
        </tr>`;
    });
    return htmlView;
}

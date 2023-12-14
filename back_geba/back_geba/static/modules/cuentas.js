document.addEventListener("DOMContentLoaded", function(event) {
    authVerifyPage();
    listarCuentas();
});

function listarCuentas() {
    let currentUser = getCurrentUser();
    if(currentUser == null) return;

    getData(`/api/cuenta/all/`).then((response) => {
      if(typeof response.status !== undefined && response.status > 201) {
        document.querySelector('#sectionPage').style.display = 'none';
        showMessage('danger', response.message, true, null);
      }
      document.querySelector('#lista').innerHTML = previewDetail(response);
    });
}

function changeStatus(id_cuenta, nro_cuenta, estado) {
    clearMessage();
    const estadoFinal = estado != 'BLOQUEADO' ? 'BLOQUEADO' : 'ACTIVO';
    if (confirm(`Confirma ${estadoFinal == 'BLOQUEADO' ? 'bloquear' : 'activar'} el Nro. de cuenta ${nro_cuenta}?`)) {
        putData(`/api/cuenta/item/${id_cuenta}/changeStatus/`, { "estado": estadoFinal }).then((response) => {
          if(typeof response.status !== undefined && response.status > 201) {
            showMessage('danger', response.message, true, 5000);
            return;
          }
          listarCuentas();
        });
    }
}


function previewDetail(response) {
    let htmlView = '';
    response.forEach((row) => {
        let cuentaBadge = 'badge-soft-success';
        let estadoIcon = 'icon-check';
        if(row.estado == 'BLOQUEADO') cuentaBadge = 'badge-soft-danger';
        if(row.estado == 'ACTIVO') cuentaBadge = 'badge-soft-success';
        if(row.estado == 'INACTIVO') cuentaBadge = 'badge-soft-primary';

        if(row.estado != 'BLOQUEADO') {
            estadoIcon = 'icon-lock';
        }
        htmlView+= `<tr>
            <td><span style="font-size:15px;padding:10px" class="badge badge-soft-primary">${row.nro_cuenta}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.nro_contrato}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.tipo_cuenta}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.saldo}</span></td>
            <td><span style="font-size:15px;padding:10px">${row.moneda}</span></td>
            <td><span style="font-size:15px;padding:10px" class="${cuentaBadge}">${row.estado}</span></td>
            <td>
                <button type="button" class="btn" onclick="changeStatus('${row.id_cuenta}', '${row.id_cuenta}', '${row.estado}')">
                    <i class="${estadoIcon} text-primary" style="font-size:20px"></i>
                </button>
            </td>
        </tr>`;
    });
    return htmlView;
}

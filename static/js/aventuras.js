document.addEventListener("DOMContentLoaded", function () {
    if (window.jQuery && $.fn.DataTable) {
        $('.datatable').DataTable({
            pageLength: 10,
            language: {
                search: "Buscar:",
                lengthMenu: "Mostrar _MENU_ registros",
                info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
                infoEmpty: "No hay registros disponibles",
                zeroRecords: "No se encontraron resultados",
                paginate: { first: "Primero", last: "Último", next: "Siguiente", previous: "Anterior" }
            }
        });
    }
});

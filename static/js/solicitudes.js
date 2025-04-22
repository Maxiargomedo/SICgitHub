document.addEventListener('DOMContentLoaded', function() {
    // Elementos del formulario
    const esMuestraCheckbox = document.getElementById('esMuestra');
    const formularioCompra = document.getElementById('formularioCompra');
    const formularioMuestra = document.getElementById('formularioMuestra');
    const mainForm = document.getElementById('mainForm');
    
    if (esMuestraCheckbox && formularioCompra && formularioMuestra && mainForm) {
        // Manejar el cambio en el checkbox
        esMuestraCheckbox.addEventListener('change', function() {
            if(this.checked) {
                // Activar modo muestra
                formularioCompra.classList.add('form-disabled');
                formularioMuestra.style.display = 'block';
                
                // Deshabilitar validación en formulario de compra
                const compraFields = formularioCompra.querySelectorAll('[required]');
                compraFields.forEach(field => {
                    field.removeAttribute('required');
                });
                
                // Habilitar validación en formulario de muestra
                const muestraFields = formularioMuestra.querySelectorAll('input, textarea, select');
                muestraFields.forEach(field => {
                    field.setAttribute('required', '');
                });
            } else {
                // Desactivar modo muestra
                formularioCompra.classList.remove('form-disabled');
                formularioMuestra.style.display = 'none';
                
                // Restaurar validación en formulario de compra
                const compraRequiredFields = ['descripcion', 'especificaciones', 'cantidad', 'unidad'];
                compraRequiredFields.forEach(fieldId => {
                    const field = document.getElementById(fieldId);
                    if (field) field.setAttribute('required', '');
                });
                
                // Deshabilitar validación en formulario de muestra
                const muestraFields = formularioMuestra.querySelectorAll('[required]');
                muestraFields.forEach(field => {
                    field.removeAttribute('required');
                });
            }
        });
        
        // Validación del formulario principal
        mainForm.addEventListener('submit', function(e) {
            if(!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        }, false);
    }
});
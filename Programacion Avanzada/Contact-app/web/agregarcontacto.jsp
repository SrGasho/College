<%-- 
    Document   : agregarcontacto
    Created on : 30/05/2024, 4:49:50 p. m.
    Author     : DANI
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <!-- ${usuario.nombre}, ${usuario.celular} ,${usuario.pass} -->
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mostrar Divs</title>
        <style>
            .hidden {
                display: none;
            }
        </style>
    </head>
    <body>
        
        <form action="GuardarNewContacto" method="post">
            <input type="hidden" name="usuarioID" id="usuarioID" value="${usuario.id}">
            
            <input type="hidden" name="celLogin" value="${usuario.celular}">
            <input type="hidden" name ="passLogin" value="${usuario.pass}">
            <div class="contenedor_principal">
                <div class="elementos">
                    <label>Nombre</label>
                    <input type="text" name="nombreNewContacto">
                </div>

                <div class="elementos">
                    <label>Apellido</label>
                    <input type="text" name="apellidoNewContacto">
                </div>

                <div class="elementos">
                    <label>Numero celular</label>
                    <input type="number" name="celularNewContacto">
                </div>

                <div class="elementos">
                    <select name="tipoContacto" id="tipoContacto">
                        <option value="">Seleccione tipo de contacto</option>
                        <option value="lab">Laboral</option>
                        <option value="fam">Familiar</option>
                        <option value="neg">Negocios</option>
                    </select>
                </div>
                <div class="diLab hidden" id="diLab">
                    <div class="elementos">
                        <label>Segundo numero de celular</label>
                        <input type="number" name="segundoNumeroNewContactoLab">
                    </div>

                    <div class="elementos">
                        <label>Posición laboral</label>
                        <input type="text" name="posicionNewContactoLab">
                    </div>

                    <div class="elementos">
                        <label>Empresa</label>
                        <input type="text" name="empresaNewContactoLab">
                    </div>
                </div>
                <div class="diFam hidden" id="diFam">
                    <div class="elementos">
                        <label>Tipo familiar</label>
                        <input type="text" name="tipoFamiliarNewContactoFam">
                    </div>

                    <div class="elementos">
                        <label>Direccion</label>
                        <input type="text" name="direccionNewContactoFam">
                    </div>
                </div>
                <div class="diNeg hidden" id="diNeg">
                    <div class="elementos">
                        <label>Segundo numero de celular</label>
                        <input type="number" name="segundoNumeroNewContactoNeg">
                    </div>

                    <div class="elementos">
                        <label>Posición laboral</label>
                        <input type="text" name="posicionNewContactoNeg">
                    </div>

                    <div class="elementos">
                        <label>Empresa</label>
                        <input type="text" name="empresaNewContactoNeg">
                    </div>

                    <div class="elementos">
                        <label>Direccion de oficina</label>
                        <input type="text" name="direccionOficinaNewContactoNeg">
                    </div>
                </div>
            </div>
            <input type="submit" value="AGREGAR">
        </form>
        <script>
            alert(document.getElementById("usuarioID"))
            document.addEventListener('DOMContentLoaded', function () {
                const selectElement = document.getElementById('tipoContacto');
                const divLab = document.getElementById('diLab');
                const divFam = document.getElementById('diFam');
                const divNeg = document.getElementById('diNeg');

                selectElement.addEventListener('change', function () {
                    // Ocultar todos los divs
                    divLab.classList.add('hidden');
                    divFam.classList.add('hidden');
                    divNeg.classList.add('hidden');

                    // Mostrar el div correspondiente a la opción seleccionada
                    const selectedOption = selectElement.value;
                    if (selectedOption === 'lab') {
                        divLab.classList.remove('hidden');
                    } else if (selectedOption === 'fam') {
                        divFam.classList.remove('hidden');
                    } else if (selectedOption === 'neg') {
                        divNeg.classList.remove('hidden');
                    }
                });
            });
        </script>
    </body>
</html>

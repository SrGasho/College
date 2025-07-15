
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <title>INICIO DE SESION</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div class="conetenedor_principal">
            <label>POR FAVOR INGRESE:</label>
            <form action="LobbyServlet">
                <div class="elementos">
                    <label>NUMERO DE CELULAR</label>
                    <input type="number" name="celLogin" id="celLogin">
                </div>
                <div>
                    <label>CONTRASEÑA</label>
                    <input type="password" name="passLogin" id="passLogin">
                </div>
                <div class="elementos">
                    <p>
                        <%
                            String resultado = (String)request.getAttribute("mensaje");
                            String mensaje = "";
                            if(resultado != null){
                                mensaje = resultado;
                            }
                        %>
                        <%=mensaje%>
                    </p>
                </div>
                <input type="submit" value="INGRESAR">
            </form>
        </div>
    </body>
</html>

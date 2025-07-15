/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/JSP_Servlet/Servlet.java to edit this template
 */
package Sevlets;

import Contactos.ContactoFamiliar;
import Datos.ConsultasSQL;
import Usuarios.Usuario;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author DANI
 */
@WebServlet(name = "LobbyServlet", urlPatterns = {"/LobbyServlet"})
public class LobbyServlet extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            response.setContentType("text/html;charset=UTF-8");
            
            //REALIZA LA AUTENTICACION DE USUARIO
            String celLogin = request.getParameter("celLogin");
            String pass = request.getParameter("passLogin");
            
            ConsultasSQL sqlconsultas = new ConsultasSQL();
            Usuario usuario = sqlconsultas.getLoginUsuarios(celLogin, pass);
            
            if(usuario == null){
                request.setAttribute("mensaje", "ERROR USUARIO Y/O CLAVE NO COINCIDEN");
                request.getRequestDispatcher("iniciosesion.jsp").forward(request, response);
            }else{
              try (PrintWriter out = response.getWriter()) {

                out.println("<!DOCTYPE html>");
                out.println("<html>");
                out.println("<head>");
                out.println("<title>AUTENTICADO</title>");
                out.println("</head>");
                out.println("<body>");
                out.println("<div class='encabezado'>");
                out.println("<label>BIENVENIDO "+usuario.getNombre()+ usuario.getId()+"</label>");
                out.println("<form action='RedirectNewContacto'>");
                out.println("<input type='hidden' name='usuarioID' value='"+usuario.getId()+"'>");
                out.println("<input type='hidden' name='usuarioCelular' value='"+usuario.getCelular()+"'>");
                out.println("<input type='hidden' name='usuarioPass' value='"+usuario.getPass()+"'>");
                out.println("<input type='submit' value='AGREGAR CONTACTO'>");
                out.println("</form>");

                out.println("</div>");
                out.println("<div class='contenedor_principal'>");
                List<ContactoFamiliar> contactosFamiliares = sqlconsultas.recuperarContactosFamiliares(usuario.getId());
                
                for(int i=0;i<contactosFamiliares.size();i++){
                    
                    out.println("<div class='contactos'>");
                    out.println("<label>Nombre: "+contactosFamiliares.get(i).getNombres()+"</label>");
                    out.println("<label>Apellidos: "+contactosFamiliares.get(i).getApellido()+"</label>");
                    out.println("<label>Celular: "+contactosFamiliares.get(i).getCelular()+"</label>");
                    out.println("<label>Familiar: "+contactosFamiliares.get(i).getTipoFamiliar()+"</label>");
                    out.println("<label>Direccion: "+contactosFamiliares.get(i).getDireccion()+"</label>");
                    out.println("</div>");
                    out.println("<br>");
                }
                out.println("<div class='contactos'>");
                out.println("<h1>AQUI VAN LOS CONTATOS 1</h1>");
                out.println("</div>");
                
                out.println("</div>");
                out.println("</body>");
                out.println("</html>");
            }  
            }
            /*
            
            */
        } catch (SQLException ex) {
            Logger.getLogger(LobbyServlet.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}

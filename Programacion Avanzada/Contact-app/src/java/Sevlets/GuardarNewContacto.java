/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/JSP_Servlet/Servlet.java to edit this template
 */
package Sevlets;

import Contactos.Contacto;
import Contactos.ContactoFamiliar;
import Contactos.ContactoLaboral;
import Contactos.ContactoNegocios;
import Datos.ConsultasSQL;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 *
 * @author DANI
 */
@WebServlet(name = "GuardarNewContacto", urlPatterns = {"/GuardarNewContacto"})
public class GuardarNewContacto extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    //APLICANDO LISKOV
    public static Contacto nuevoConctacto;

    public static void liskovContactoFamiliar(ContactoFamiliar c, int usrid, String nom,
            String ap, String celular, String tf, String direccion) {

        c.setUsuarioID(usrid);
        c.setNombres(nom);
        c.setApellido(ap);
        c.setCelular(celular);
        c.setTipoFamiliar(tf);
        c.setDireccion(direccion);

        nuevoConctacto = c;

    }

    public static void liskovContactoLaboral(ContactoLaboral c, int usrid, String nom,
            String ap, String celular, String pl, String sn, String e) {

        c.setUsuarioID(usrid);
        c.setNombres(nom);
        c.setApellido(ap);
        c.setCelular(celular);
        c.setPosicionLaboral(pl);
        c.setSegundoNumero(sn);
        c.setEmpresa(e);

        nuevoConctacto = c;
    }

    public static void liskovContactoNegocios(ContactoNegocios c, int usrid, String nom,
            String ap, String celular, String sn, String pl, String e, String dirO) {

        c.setUsuarioID(usrid);
        c.setNombres(nom);
        c.setApellido(ap);
        c.setCelular(celular);
        c.setPosicionLaboral(pl);
        c.setSegundoNumero(sn);
        c.setEmpresa(e);
        c.setDireccionOficina(dirO);
        nuevoConctacto = c;
    }

    /////////////////
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        int usuarioID = Integer.parseInt(request.getParameter("usuarioID"));
        String nombres = request.getParameter("nombreNewContacto");
        String apellidos = request.getParameter("apellidoNewContacto");
        String celular = request.getParameter("celularNewContacto");
        String tipoContacto = request.getParameter("tipoContacto");

        ConsultasSQL consutlasDB = new ConsultasSQL();

        //REGISTRA CONTACTSO FAMILIARES
        if ("fam".equals(tipoContacto)) {
            try {
                //aplicando liskov:
                String tipoFamiliar = request.getParameter("tipoFamiliarNewContactoFam");
                String direccion = request.getParameter("direccionNewContactoFam");
                ContactoFamiliar cf = new ContactoFamiliar();

                liskovContactoFamiliar(cf, usuarioID, nombres, apellidos, celular, tipoFamiliar, direccion);

                consutlasDB.registrarContactoFamiliar((ContactoFamiliar) nuevoConctacto);
            } catch (SQLException ex) {
                Logger.getLogger(GuardarNewContacto.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

        //REGISTRA CONTACTOS LABORALES
        if ("lab".equals(tipoContacto)) {
            try {
                String segundoNumero = request.getParameter("segundoNumeroNewContactoLab");
                String posicionlab = request.getParameter("posicionNewContactoLab");
                String empresa = request.getParameter("empresaNewContactoLab");

                ContactoLaboral cl = new ContactoLaboral();
                liskovContactoLaboral(cl, usuarioID, nombres, apellidos, celular, posicionlab, segundoNumero, empresa);

                consutlasDB.registrarContactoLaboral((ContactoLaboral) nuevoConctacto);
            } catch (SQLException ex) {
                Logger.getLogger(GuardarNewContacto.class.getName()).log(Level.SEVERE, null, ex);
            }

        }

        if ("neg".equals(tipoContacto)) {
            try {
                String segundoNumero = request.getParameter("segundoNumeroNewContactoNeg");
                String posicionLab = request.getParameter("posicionNewContactoNeg");
                String empresa = request.getParameter("empresaNewContactoNeg");
                String direccionOficina = request.getParameter("direccionOficinaNewContactoNeg");

                ContactoNegocios cn = new ContactoNegocios();
                liskovContactoNegocios(cn, usuarioID, nombres, apellidos, celular, segundoNumero, posicionLab, empresa, direccionOficina);

                consutlasDB.registrarContactoNegocios((ContactoNegocios) nuevoConctacto);

                try (PrintWriter out = response.getWriter()) {
                    /* TODO output your page here. You may use following sample code. */
                    out.println("<!DOCTYPE html>");
                    out.println("<html>");
                    out.println("<head>");
                    out.println("<title>GUARDADO EXITOSO</title>");
                    out.println("</head>");
                    out.println("<body>");
                    out.println("<h1>SE GUARDO EL CONTACTO CON EXITO</h1>");
                    out.println("<a href='LobbyServlet'>VOLVER</a>");
                    out.println("</body>");
                    out.println("</html>");
                }
            } catch (SQLException ex) {
                Logger.getLogger(GuardarNewContacto.class.getName()).log(Level.SEVERE, null, ex);

                try (PrintWriter out = response.getWriter()) {
                    /* TODO output your page here. You may use following sample code. */
                    out.println("<!DOCTYPE html>");
                    out.println("<html>");
                    out.println("<head>");
                    out.println("<title>ERROR AL GUARDAR EL CONTACTO</title>");
                    out.println("</head>");
                    out.println("<body>");
                    out.println("<h1>SE PRODUJO UN ERROR AL GUARDAR EL CONTACTO</h1>");
                    out.println("<a href='LobbyServlet'>VOLVER</a>");
                    out.println("</body>");
                    out.println("</html>");
                }
            }
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

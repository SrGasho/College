/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Datos;

import Contactos.Contacto;
import Contactos.ContactoFamiliar;
import Contactos.ContactoLaboral;
import Contactos.ContactoNegocios;
import Usuarios.Usuario;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author DANI
 */
public class ConsultasSQL {

    ConexionSQL conexion;

    public ConsultasSQL() {
        conexion = new ConexionSQL();
    }

    //-----------METODOS GUIA PARA REALIZAR EL MANEJO DE LOS DATOS---------------//
    //---------METODO PARA LEER CONTENIDO DE LAS TABLAS DE LA DB--------
    public Usuario getLoginUsuarios(String cel, String pass) throws SQLException {
        Usuario usuario = null;
        String sql = "SELECT U.id, U.nombre, U.celular, U.contrasena FROM registros_usuarios U WHERE U.celular = ? AND U.contrasena = ?";
        PreparedStatement pstm = conexion.conectar().prepareStatement(sql);
        pstm.setString(1, cel);
        pstm.setString(2, pass);
        ResultSet res = pstm.executeQuery();

        while (res.next()) {

            usuario = new Usuario();
            usuario.setId(res.getInt("id"));
            usuario.setNombre(res.getString("nombre"));
            usuario.setCelular(res.getString("celular"));
            usuario.setPass(res.getString("contrasena"));
            System.out.println(usuario.getId());
            System.out.println(usuario.getCelular());
            System.out.println(usuario.getPass());
        }
        return usuario;
    }

    //////////////////////////////////////////////////////////////
    //--------METODO PARA ESCRIBIR EN LA TABLA DE LA DB-------------------
    public void setRegistrarUsuario(Usuario u) throws SQLException {
        String sql = "INSERT INTO registros_usuarios (nombre, celular , contrasena) VALUES (?,?,?)";
        PreparedStatement pstm = conexion.conectar().prepareStatement(sql);
        pstm.setString(1, u.getNombre());
        pstm.setString(2, u.getCelular());
        pstm.setString(3, u.getPass());

        pstm.executeUpdate();
    }

    public void registrarContactoFamiliar(ContactoFamiliar c) throws SQLException {
        String sql = "INSERT INTO contactos_familiares (usuario_id, nombre, apellido,"
                + " celular, tipo_familiar, direccion) VALUES (?,?,?,?,?,?)";

        PreparedStatement pstm = conexion.conectar().prepareStatement(sql);
        pstm.setInt(1, c.getUsuarioID());
        pstm.setString(2, c.getNombres());
        pstm.setString(3, c.getApellido());
        pstm.setString(4, c.getCelular());
        pstm.setString(5, c.getTipoFamiliar());
        pstm.setString(6, c.getDireccion());

        pstm.executeUpdate();
    }

    public void registrarContactoLaboral(ContactoLaboral c) throws SQLException {
        String sql = "INSERT INTO contactos_laborales (usuario_id, nombre, apellido,"
                + " celular, segundo_numero, posicion_laboral, empresa) VALUES (?,?,?,?,?,?,?)";

        PreparedStatement pstm = conexion.conectar().prepareStatement(sql);
        pstm.setInt(1, c.getUsuarioID());
        pstm.setString(2, c.getNombres());
        pstm.setString(3, c.getApellido());
        pstm.setString(4, c.getCelular());
        pstm.setString(5, c.getSegundoNumero());
        pstm.setString(6, c.getPosicionLaboral());
        pstm.setString(7, c.getEmpresa());

        pstm.executeUpdate();
    }

    public void registrarContactoNegocios(ContactoNegocios c) throws SQLException {
        String sql = "INSERT INTO contactos_negocios (usuario_id, nombre, apellido,"
                + " celular, segundo_numero, posicion_laboral, empresa, direccion_oficina) VALUES (?,?,?,?,?,?,?,?)";

        PreparedStatement pstm = conexion.conectar().prepareStatement(sql);
        pstm.setInt(1, c.getUsuarioID());
        pstm.setString(2, c.getNombres());
        pstm.setString(3, c.getApellido());
        pstm.setString(4, c.getCelular());
        pstm.setString(5, c.getSegundoNumero());
        pstm.setString(6, c.getPosicionLaboral());
        pstm.setString(7, c.getEmpresa());
        pstm.setString(8, c.getDireccionOficina());

        pstm.executeUpdate();
    }

    public List<ContactoFamiliar> recuperarContactosFamiliares(int usuarioID) throws SQLException {

        String sql = "SELECT * FROM contactos_familiares WHERE usuario_id = ?";
        List<ContactoFamiliar> contactos = new ArrayList<>();
        PreparedStatement pstm = conexion.conectar().prepareStatement(sql);
        pstm.setInt(1, usuarioID);
        ResultSet res = pstm.executeQuery();

        while (res.next()) {
            ContactoFamiliar cf = new ContactoFamiliar();
            cf.setId(res.getInt("id"));
            cf.setUsuarioID(res.getInt("usuario_id"));
            cf.setApellido(res.getString("apellido"));
            cf.setCelular(res.getString("celular"));
            cf.setTipoFamiliar(res.getString("tipo_familiar"));
            cf.setDireccion(res.getString("direccion"));
        }

        return contactos;

    }
    //////////////////////////////

}

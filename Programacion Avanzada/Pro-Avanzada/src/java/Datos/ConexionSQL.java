/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Datos;




import java.sql.*;
import java.util.logging.Level;
import java.util.logging.Logger;



/**
 *
 * @author DANI
 */
public class ConexionSQL {
    String db="contactos";
    String url="jdbc:mysql://localhost:3306/"+db;
    String user="root";
    String password="";
    String driver="com.mysql.cj.jdbc.Driver";
    Connection cx;
    
    public ConexionSQL(){
        
    }
    
    public Connection conectar(){
        try {
            Class.forName(driver);
            cx = DriverManager.getConnection(url, user, password);
            System.out.println("SE HA CONECTADO A LA BASE DE DATOS"+db);
        } catch (ClassNotFoundException | SQLException ex) {
            System.out.println("NO SE HA CONECTADO A LA BASE DE DATOS"+db);
            Logger.getLogger(ConexionSQL.class.getName()).log(Level.SEVERE, null, ex);
        }
     return cx;
    }
    
    public void desconectar(){
        try {
            cx.close();
        } catch (SQLException e) {
            Logger.getLogger(ConexionSQL.class.getName()).log(Level.SEVERE, null, e);
        }
    }
    
}

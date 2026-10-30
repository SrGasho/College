/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Contactos;

/**
 *
 * @author DANI
 */
public class ContactoLaboral extends Contacto{
    private String segundoNumero;
    private String posicionLaboral;
    private String empresa;
    
    public ContactoLaboral() {
        super();
    }

    public String getPosicionLaboral() {
        return posicionLaboral;
    }

    public void setPosicionLaboral(String posicionLaboral) {
        this.posicionLaboral = posicionLaboral;
    }

    public String getSegundoNumero() {
        return segundoNumero;
    }

    public void setSegundoNumero(String segundoNumero) {
        this.segundoNumero = segundoNumero;
    }

    public String getEmpresa() {
        return empresa;
    }

    public void setEmpresa(String empresa) {
        this.empresa = empresa;
    }
    
    
}

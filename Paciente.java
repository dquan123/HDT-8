public class Paciente implements Comparable<Paciente> {

    private String nombre;
    private String sintoma;
    private String codigo_emergencia;

    public Paciente(String nombre, String sintoma, String codigo_emergencia){
        this.nombre = nombre;
        this.sintoma = sintoma;
        this.codigo_emergencia = codigo_emergencia;
    }

    public String getNombre(){
        return nombre;
    }

    public String getSintoma(){
        return sintoma;
    }

    public String getCodigoEmergencia(){
        return codigo_emergencia;
    }

    @Override
    public int compareTo(Paciente otro) {
        return this.codigo_emergencia.compareTo(otro.codigo_emergencia);
    }

    @Override
    public String toString() {
        return nombre + ", " + sintoma + ", " + codigo_emergencia;
    }
}

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Scanner;

public class PrincipalJCF {

    public static void main(String[] args) {

        String ruta = "C:\\Users\\dquan\\OneDrive\\Documentos\\Diego Quan\\UVG\\Ciclo 3\\Algoritmos y Estructura de datos\\Hoja de trabajo 9\\HDT-8\\pacientes.txt";

        // PriorityQueue con Comparator personalizado para que A tenga más prioridad que B, C, etc.
        PriorityQueue<Paciente> colaPrioridad = new PriorityQueue<>(new Comparator<Paciente>() {
            
            @Override
            public int compare(Paciente p1, Paciente p2) {
                return p1.getCodigoEmergencia().compareTo(p2.getCodigoEmergencia());
            }
        });

        // Leer archivo y llenar la cola
        try (BufferedReader br = new BufferedReader(new FileReader(ruta))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                String[] datos = linea.split(",");
                if (datos.length == 3) {
                    String nombre = datos[0].trim();
                    String sintoma = datos[1].trim();
                    String codigo = datos[2].trim();

                    Paciente paciente = new Paciente(nombre, sintoma, codigo);
                    colaPrioridad.add(paciente);
                }
            }
        } catch (IOException e) {
            System.out.println("Error al leer el archivo: " + e.getMessage());
            return;
        }

        // Menú interactivo
        Scanner scanner = new Scanner(System.in);
        int opcion = 0;

        System.out.println("=== SISTEMA DE ATENCIÓN DE EMERGENCIAS (JCF) ===");

        while (!colaPrioridad.isEmpty()) {
            System.out.println("\nSeleccione una opción:");
            System.out.println("1. Siguiente paciente");
            System.out.println("2. Salir");

            boolean entradaValida = false;
            while (!entradaValida) {
                System.out.print(">> ");
                String entrada = scanner.nextLine().trim();

                try {
                    opcion = Integer.parseInt(entrada);
                    if (opcion == 1 || opcion == 2) {
                        entradaValida = true;
                    } else {
                        System.out.println("Opción inválida. Ingrese 1 o 2.");
                    }
                } catch (NumberFormatException e) {
                    System.out.println("Entrada inválida. Ingrese un número (1 o 2).");
                }
            }

            if (opcion == 1) {
                Paciente paciente = colaPrioridad.poll(); // poll saca el elemento con mayor prioridad
                System.out.println("Turno de: " + paciente);
            } else if (opcion == 2) {
                break;
            }
        }

        if (colaPrioridad.isEmpty()) {
            System.out.println("\n¡No quedan pacientes por atender!");
        }

        scanner.close();
    }
}

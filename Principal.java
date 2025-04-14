import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class Principal {

    public static void main(String[] args) {

        String ruta = "C:\\Users\\dquan\\OneDrive\\Documentos\\Diego Quan\\UVG\\Ciclo 3\\Algoritmos y Estructura de datos\\Hoja de trabajo 9\\HDT-8\\pacientes.txt";

        HeapUsingIterativeBinaryTree<String, Paciente> colaPrioridad =
                new HeapUsingIterativeBinaryTree<>(new ComparadorPrioridad());

        // Leer archivo y llenar el heap
        try (BufferedReader br = new BufferedReader(new FileReader(ruta))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                String[] datos = linea.split(",");
                if (datos.length == 3) {
                    String nombre = datos[0].trim();
                    String sintoma = datos[1].trim();
                    String codigo = datos[2].trim();

                    Paciente paciente = new Paciente(nombre, sintoma, codigo);
                    colaPrioridad.Insert(codigo, paciente);
                }
            }
        } catch (IOException e) {
            System.out.println("Error al leer el archivo: " + e.getMessage());
            return;
        }

        // Menú interactivo con validación
        Scanner scanner = new Scanner(System.in);
        int opcion = 0;

        System.out.println("=== SISTEMA DE ATENCIÓN DE EMERGENCIAS ===");

        while (!colaPrioridad.isEmpty()) {
            System.out.println("\nSeleccione una opción:");
            System.out.println("1. Siguiente paciente");
            System.out.println("2. Salir");

            // Validar entrada
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
                Paciente paciente = colaPrioridad.remove();
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

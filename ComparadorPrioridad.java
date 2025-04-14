import java.util.Comparator;

public class ComparadorPrioridad implements Comparator<String> {

    @Override
    public int compare(String o1, String o2) {
        // Prioridad más alta = letra más cercana a 'A'
        return o2.compareTo(o1); // A < B < C < D < E
    }
}

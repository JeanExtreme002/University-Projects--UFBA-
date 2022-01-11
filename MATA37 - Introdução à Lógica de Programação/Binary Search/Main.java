import java.io.File;
import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws IOException {

        // Deve ser passado como argumento o nome do arquivo, a quantidade de valores e o valor alvo.
        if (args.length < 3) {
            System.out.println("You must pass the target value, filename and length as an argument.");
            System.exit(1);
        }

        String target = args[0];
        String filename = args[1];
        int length = Integer.parseInt(args[2]);

        // Obtém todos os valores do arquivo.
        Scanner scanner = new Scanner(new File(filename));
        String[] values = new String[length];

        for (int index = 0; index < length; index++) {
            values[index] = scanner.nextLine();
        }

        // Faz a busca binária e imprime o índice do valor, se encontrado.
        int index = BinarySearch.<String>search(target, values);
        System.out.println("Index: " + (index >= 0 ? index : "Not Found"));
    }
}

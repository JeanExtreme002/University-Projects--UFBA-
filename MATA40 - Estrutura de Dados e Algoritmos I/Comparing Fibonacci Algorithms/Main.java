class Main {
    public static void main(String[] args) {

        // Verifica se recebeu a posição como argumento.
        if (args.length < 1) {
            System.out.println("Informe a posição da sequência de Fibonacci a ser calculada!");
            return;
        }

        // Obtém as posições do array no tipo inteiro.
        int position1 = Integer.parseInt(args[0]);
        int position2 = (args.length > 1) ? Integer.parseInt(args[1]) : position1;

        // Calcula o valor na posição N da sequência de Fibonacci usando uma função linear.
        System.out.println("Resultado para a posição " + position1 + ":");
        System.out.println("Algoritmo Linear: " + new Linear().run(position1) + " millisegundos.");

        System.out.println("-".repeat(60));

        // Calcula o valor na posição N da sequência de Fibonacci usando uma função quadrática.
        System.out.println("Resultado para a posição " + position2 + ":");
        System.out.println("Algoritmo Quadrático: " + new Quadratic().run(position2) + " millisegundos.");
    }
}
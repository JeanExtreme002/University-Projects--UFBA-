class Linear extends Tester {
    /**
    Calcula um valor da sequência de Fibonacci, dado uma posição,
    utilizando um único laço de repetição.
    */
    public long executable(int position) {
        if (position <= 2) {
            return 1;
        }

        long sum = 0;
        long before = 1;
        long after = 1;
        
        for (int index = 0; index <= position; index++) {
            sum = before + after;
            after = before;
            before = sum;
        }

        return sum; 
    }
}
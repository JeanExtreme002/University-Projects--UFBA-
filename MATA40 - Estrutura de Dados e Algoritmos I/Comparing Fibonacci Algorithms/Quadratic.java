class Quadratic extends Tester {
    /**
    Calcula um valor da sequência de Fibonacci, 
    dado uma posição, recursivamente.
    */
    public long executable(int position) {
        if (position <= 2) {
            return 1;
        }
        return this.executable(position - 1) + this.executable(position - 2);
    }
}
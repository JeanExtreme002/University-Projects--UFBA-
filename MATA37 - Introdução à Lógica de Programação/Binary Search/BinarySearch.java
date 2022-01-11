public class BinarySearch {
	public static <T extends Comparable> int search(T value, T[] array) {

		int left = 0;
		int right = array.length;

		while (left < right) {

			// Obtém o índice do centro do range e compara os dois valores.
			int index = (left + right) / 2;
			int result = value.compareTo(array[index]);

			// Se forem iguais, retorna o índice.
			if (result == 0) {
				return index;
			}
			// Se o valor for menor que o encontrado, o range é reduzido na direita.
			else if (result < 0) {
				right = index;
			}
			// Se o valor for maior que o encontrado, o range é reduzido na esquerda.
			else {
				left = index + 1;
			}
		}

		return -1;
	}
}

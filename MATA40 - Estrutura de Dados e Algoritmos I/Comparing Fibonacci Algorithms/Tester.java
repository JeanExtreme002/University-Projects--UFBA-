import java.util.Date;

abstract class Tester {
	public abstract long executable(int position);

	public long run(int position) {
		long start = new Date().getTime();
		this.executable(position);
		return new Date().getTime() - start;
	}
}
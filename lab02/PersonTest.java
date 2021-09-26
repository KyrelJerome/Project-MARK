package lab02;

import static org.junit.Assert.*;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

class PersonTest {
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
	}

	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	@Test(timeout=5)
	void testName() {
		Person kyrel = new Person("Kyrel");
		String kyString = kyrel.toString();
		assertTrue("I am Kyrel, and I am very thirsty".equals(kyString));
	}

	@Test(timeout=5)
	void testUnOpened() {
		SodaCan s = new SodaCan("Roots");
		Person ilir = new Person("Ilir");

		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);

		String ilirString = ilir.toString();
		assertTrue("I am Ilir, and I am very thirsty".equals(ilirString));
	}
	@Test(timeout=5)
	void testOpenedThirsty() {
		SodaCan s = new SodaCan("Roots");
		s.open();
		Person ilir = new Person("Ilir");

		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);

		String ilirString = ilir.toString();
		assertTrue("I am Ilir, and I am thirsty".equals(ilirString));
	}

	@Test(timeout=5)
	void testOpenedVeryThirsty() {
		SodaCan s = new SodaCan("Roots");
		SodaCan s2 = new SodaCan("Roots");
		s.open();
		s2.open();
		
		Person ilir = new Person("Ilir");

		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s);
		ilir.gulpFrom(s2);
		ilir.gulpFrom(s2);
		ilir.gulpFrom(s2);
		ilir.gulpFrom(s2);
		ilir.gulpFrom(s2);

		String ilirString = ilir.toString();
		assertTrue("I am Ilir, and I am satisfied".equals(ilirString));
	}
}

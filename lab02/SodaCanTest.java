package lab02;
import edu.toronto.cs.jam.annotations.Description;

import static org.junit.Assert.*;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;


class SodaCanTest {

	@Test(timeout=10)
	@Description(description="Testing Soda Can Opening")
	void testOpen() {
		SodaCan s = new SodaCan("Roots");
		s.sip();
		assertTrue(s.isOpen() == false);
		s.open();
		assertTrue(s.isOpen() == true);

		assertTrue(s.getAmount()==250);
		s.sip();
		assertTrue(s.getAmount()==240);
	}

	@Test(timeout=10)
	@Description(description="Testing Soda Can Name")
	void testName() {
		SodaCan s = new SodaCan("Roots");
		SodaCan s2 = new SodaCan("Roots");
		s.sip();
		s.open();
		assertTrue(s.getAmount()==250);
		s.sip();
		assertTrue(s.getAmount()==240);
	}

}

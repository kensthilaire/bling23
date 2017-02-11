import java.util.Scanner;
public class BlingRunnerTwo {

	public static void main(String[] args) {

		Bling lights = new Bling();
		boolean isOn = true;
		Scanner oper = new Scanner(System.in);
		
		while(isOn)
		{
			System.out.println("What pattern do you want to run?");
			String answer = oper.next(); 
			
			if(answer.equalsIgnoreCase("c"))
			{
				lights.setPattern("ColorFade", "teamcolors", "all", "fast", 0, 100);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("f"))
			{
				lights.setPattern("RainbowHalves", "red", "all", "fast", 0, 100);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("fc"))
			{
				lights.setPattern("colorPattern", "teamcolors", "all", "medium", 0, 100);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("l"))
			{
				lights.setPattern("ColorWipe", "green", "left", "fast", 0, 100);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("r"))
			{
				lights.setPattern("ColorWipe", "green", "right", "fast", 0, 100);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("d"))
			{
				lights.setPattern("solid", "blue", "all", "medium", 0, 100);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("b"))
			{
				lights.setPattern("blinking", "yellow", "all", "medium", 0, 100);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("off"))
			{
				lights.disableLeds();
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("done") || answer.equalsIgnoreCase("q"))
			{
				isOn = false;
			}
		}
	}
}
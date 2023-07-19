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
				lights.sendClimbing();
			}
			
			else if(answer.equalsIgnoreCase("f"))
			{
				lights.sendFinished();
			}
			
			else if(answer.equalsIgnoreCase("fc"))
			{
				lights.sendFinishedClimbing();
			}
			
			else if(answer.equalsIgnoreCase("l"))
			{
				lights.sendLeftTurning();
			}
			
			else if(answer.equalsIgnoreCase("r"))
			{
				lights.sendRightTurning();
			}
			
			else if(answer.equalsIgnoreCase("d"))
			{
				lights.sendDrive();
			}
			
			else if(answer.equalsIgnoreCase("b"))
			{
				lights.sendBackup();
			}
			
			else if(answer.equalsIgnoreCase("e"))
			{
				lights.sendEnd();
			}
			
			else if(answer.equalsIgnoreCase("off") || answer.equalsIgnoreCase("o"))
			{
				lights.sendOff();
			}
			
			else if(answer.equalsIgnoreCase("done") || answer.equalsIgnoreCase("q"))
			{
				isOn = false;
			}
		}
	}
}

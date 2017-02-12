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
				lights.sendClimbingPattern();
			}
			
			else if(answer.equalsIgnoreCase("f"))
			{
				lights.sendFinishedPattern();
			}
			
			else if(answer.equalsIgnoreCase("fc"))
			{
				lights.sendFinishedClimbingPattern();
			}
			
			else if(answer.equalsIgnoreCase("l"))
			{
				lights.sendLeftTurningPattern();
			}
			
			else if(answer.equalsIgnoreCase("r"))
			{
				lights.sendRightTurningPattern();
			}
			
			else if(answer.equalsIgnoreCase("d"))
			{
				lights.sendDrivePattern();
			}
			
			else if(answer.equalsIgnoreCase("b"))
			{
				lights.sendBackupPattern();
			}
			
			else if(answer.equalsIgnoreCase("e"))
			{
				lights.sendEndPattern();
			}
			
			else if(answer.equalsIgnoreCase("off") || answer.equalsIgnoreCase("o"))
			{
				lights.sendOffPattern();
			}
			
			else if(answer.equalsIgnoreCase("done") || answer.equalsIgnoreCase("q"))
			{
				isOn = false;
			}
		}
	}
}

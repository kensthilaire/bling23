//package edu.wpi.first.wpilibj.templates;
import edu.wpi.first.wpilibj.networktables.NetworkTable;
import java.util.Scanner;
public class BlingRunner {

	public static void main(String[] args) {
	
		String tell = "", light = "", segment = "", speed = "";
		int min = 0, max = 100;
		
		Bling lights = new Bling();
		boolean isGo = true;
		Scanner input = new Scanner(System.in);
		
		while(isGo)
		{
			System.out.println("What do you want to do? (B)uild manually, (S)pecific blinking, (C)olor change, or (Q)uit code");
			String answer = input.next();
			if(answer.equalsIgnoreCase("B"))
				{
				
				lights.disableLeds();
				System.out.println("What pattern do you want to select?");
				tell = input.next();
			
				System.out.println("What color do you want the strips to light up?");
				light = input.next();
				
				System.out.println("What segment of the strips do you want to light up?");
				segment = input.next();
				
				System.out.println("What speed do you want to run at?");
				speed = input.next();
				
				System.out.println("What minimum light do you want to activate?");
				min = input.nextInt();
							
				System.out.println("What maximum light do you want to activate?");
				max = input.nextInt();
				
				
				System.out.println(lights.setPattern(tell, light, segment, speed, min, max));
				
				System.out.print("Do you want to push this code? (Y)es or (N)o ");
				String tell2 = input.next();
				
				if(tell2.equalsIgnoreCase("n"))
					System.out.println("The code was not pushed.");
					
				else
					System.out.println("The code was pushed successfully");
					lights.send();
				}
			
			else if(answer.equalsIgnoreCase("C"))
			{
				System.out.println("What color would you like to change the lights to?");
				String newCol = input.next();
				lights.setPattern(tell, newCol, segment, speed, min, max);
				lights.send();
			}
			
			else if(answer.equalsIgnoreCase("S"))
			{
				System.out.println("What do you want to do? Blink the (L)eft of (R)ight? ");
				String answer2 = input.next();
				
				if(answer2.equalsIgnoreCase("L"))
				{
					System.out.println("What color do you want the lights to blink?");
					String lights2 = input.next();
					System.out.println("Do you want to change the speed? (Y)es or (N)o");
					String answer3 = input.next();
					
					if(answer3.equalsIgnoreCase("Y"))
					{
						System.out.println("What color would you like to change the lights to?");
						speed = input.next();
						lights.setPattern("blinking", lights2, "left", speed, min, max);
					}
					
					System.out.println(lights.setPattern("blinking", lights2, "left", speed, min, max));
					System.out.println("Do you want to push this code? (Y)es or (N)o");
					String tell2 = input.next();
					
					if(tell2.equalsIgnoreCase("n"))
						System.out.println("The code was not pushed.");
						
					else
						System.out.println("The code was pushed successfully");
						lights.send();
				}
				
				else if(answer2.equalsIgnoreCase("R"))
				{
					System.out.println("What color do you want the lights to blink?");
					String lights3 = input.next();
					System.out.println("Do you want to change the speed? (Y)es or (N)o");
					String answer3 = input.next();
					
					if(answer3.equalsIgnoreCase("Y"))
					{
						System.out.println("What speed would you like to change the lights to?");
						speed = input.next();
						lights.setPattern("blinking", lights3, "right", speed, min, max);
					}
					
					System.out.println(lights.setPattern("blinking", lights3, "right", speed, min, max));
					System.out.println("Do you want to push this code? (Y)es or (N)o");
					String tell2 = input.next();
					if(tell2.equalsIgnoreCase("n"))
						System.out.println("The code was not pushed.");
						
					else
						System.out.println("The code was pushed successfully");
						lights.send();
				}
			}
			
			else
			{
				lights.disableLeds();
				lights.send();
				System.out.println("The lights should be turned off.");
				//isGo = false;
			}
		}
	}
}
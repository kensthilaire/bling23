import edu.wpi.first.wpilibj.networktables.NetworkTable;

public class Bling 
{
	NetworkTable newtable;
	
	
	//Instance Variables
	private String color;
	private String speed;
	private int min;
	private int max;
	private String pattern;
	private String segment;
	private String put;
	private String put2;
	
	//Constructor
	public Bling()
	{
		newtable = NetworkTable.getTable("Bling");
		NetworkTable.initialize();
	}
	
	//Methods
	public String setPattern(String patt, String col, String seg, String spd, int mini, int maxi)
	{
		pattern = patt;
		color = col;
		segment = seg;
		speed = spd;
		min = mini;
		max = maxi;
		put = "Pattern=" + pattern + "," + "Color=" + color + "," + "Segment=" + segment + "," + "Speed=" + speed + "," + "Min=" + min + "," + "Max=" + max; 
		return put;
	}
	
	public void disableLeds()
	{
		put = "Pattern=" + "off" + "," + "Color=" + color + "," + "Segment=" + segment + "," + "Speed=" + speed + "," + "Min=" + min + "," + "Max=" + max; 
	}
	
	public void send()
	{
		newtable.putString("command", put);
	}

    /** Set of API functions that can be called from the robot code to send and
        pattern to the bling **/

    public void sendRobotInit()
    {
		setPattern("RainbowHalves", "red", "all", "medium", 0, 100);
		send();
    }

	public void sendClimbing()
	{
		setPattern("ColorFade", "teamcolors", "all", "fast", 0, 100);
		send();
	}

	public void sendFinished()
	{
		setPattern("RainbowHalves", "red", "all", "fast", 0, 100);
		send();
	}
			
	public void sendFinishedClimbing()
	{
	    setPattern("colorPattern", "teamcolors", "all", "medium", 0, 100);
		send();
	}
			
	public void sendLeftTurning()
	{
		setPattern("ColorWipe", "green", "left", "fast", 0, 100);
	    send();
	}
			
	public void sendRightTurning()
	{
		setPattern("ColorWipe", "green", "right", "fast", 0, 100);
		send();
	}
	public void sendDrive()
	{
		setPattern("solid", "blue", "all", "medium", 0, 100);
		send();
	}
	public void sendBackup()
	{
		setPattern("blinking", "yellow", "all", "medium", 0, 100);
		send();
	}
	public void sendEnd()
	{
		setPattern("fireflies", "rainbow", "all", "medium", 0, 100);
		send();
	}
	public void sendOff()
	{
		disableLeds();
		send();
	}

}

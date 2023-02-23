package frc.lib.util;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;

public class Limelight {

    //create NetworkTable objects
    NetworkTableInstance nInstance;
    NetworkTable table; 
    
    //limelight values
    private NetworkTableEntry ta; 
    private NetworkTableEntry tv; 
    private NetworkTableEntry ty;
    private NetworkTableEntry tx; 
    private NetworkTableEntry tid; 
    private double[] tagpose, botpose; 
    private int pipeline; 
    

    
    public Limelight() {
        nInstance = NetworkTableInstance.getDefault();

        table = nInstance.getTable("limelight");
        ta = table.getEntry("ta");
        tv = table.getEntry("tv");
        tx = table.getEntry("tx");
        ty = table.getEntry("ty");
        tid = table.getEntry("tid");
        tagpose = table.getEntry("targetpose_robotspace").getDoubleArray(new double[6]); 
        botpose = table.getEntry("robotpose_targetspace").getDoubleArray(new double[6]); 
    
    }

    public Pose2d getTagPose() { 
        return new Pose2d(tagpose[0], tagpose[1], new Rotation2d(tagpose[5]));
    }

    public Pose2d getBotPose() {  
        return new Pose2d(botpose[0], botpose[1], new Rotation2d(botpose[5]));
    }

    public double getTa() {
        return ta.getDouble(0); 
    }

    public double getTv() {
        return tv.getDouble(0); 
    }

    public double getTx() {
        return tx.getDouble(0); 
    }

    public double getTy() {
        return ty.getDouble(0); 
    }

    public double getTid() {
        return tid.getDouble(0); 
    }

    public String getPipeline() {
        return "Currently using pipeline " + pipeline; 
    }

    public void setPipeline(int pipeline) {
        this.pipeline = pipeline;
        table.getEntry("pipeline").setNumber(pipeline);
        System.out.println("Pipeline changed to " + pipeline); 
    } 

}

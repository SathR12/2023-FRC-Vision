package frc.lib.util;

import java.util.List;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.trajectory.Trajectory;
import edu.wpi.first.math.trajectory.TrajectoryConfig;
import edu.wpi.first.math.trajectory.TrajectoryGenerator;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;
import frc.robot.Constants;
import frc.robot.RobotContainer;

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

    //trajectory fields
    private Trajectory trajectory;
    private TrajectoryConfig config; 

    public Limelight() {
        System.out.println("Limelight object initialized");

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

    public Trajectory generateTargetTrajectory() {
        System.out.println("Trajectory generated successfully"); 
        config = new TrajectoryConfig(
           Constants.AutoConstants.kMaxSpeedMetersPerSecond,
           Constants.AutoConstants.kMaxAccelerationMetersPerSecondSquared)
           .setKinematics(Constants.Swerve.swerveKinematics);
        
        //set tag pose as the current origin 
        Pose2d origin = this.getTagPose();

        RobotContainer.s_Swerve.resetOdometry(origin);
    
        trajectory = TrajectoryGenerator.generateTrajectory(
            // robot pose -> target space 
            RobotContainer.s_Swerve.getPose(),
            // Pass through no interior points 
            List.of(),
            // End at apriltag pose 
            origin,
            config);

        return trajectory; 
    
    }


}

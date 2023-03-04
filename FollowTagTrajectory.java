// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.math.controller.PIDController;
import edu.wpi.first.math.controller.ProfiledPIDController;
import edu.wpi.first.math.trajectory.Trajectory;
import edu.wpi.first.math.trajectory.TrajectoryConfig;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandBase;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.SwerveControllerCommand;
import frc.lib.util.Limelight;
import frc.robot.Constants;
import frc.robot.RobotContainer;

public class FollowTagTrajectory extends CommandBase {
  /** Creates a new FollowTagTrajectory. */
  Limelight limelight  = new Limelight(); 
  TrajectoryConfig config;
  public FollowTagTrajectory() {
    // Use addRequirements() here to declare subsystem dependencies.
    addRequirements(RobotContainer.s_Swerve);
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {

  }

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
     config = new TrajectoryConfig(
      Constants.AutoConstants.kMaxSpeedMetersPerSecond,
      Constants.AutoConstants.kMaxAccelerationMetersPerSecondSquared)
      .setKinematics(Constants.Swerve.swerveKinematics);
    
    
      loadCommand(limelight.generateTargetTrajectory(config));
      
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {

  }

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    return false;
  }

  public Command loadCommand(Trajectory trajectory) {
    var thetaController = new ProfiledPIDController(Constants.AutoConstants.kPThetaController, 0, 0, Constants.AutoConstants.kThetaControllerConstraints);
    thetaController.enableContinuousInput(-Math.PI, Math.PI);

    SwerveControllerCommand swerveControllerCommand =
    new SwerveControllerCommand(
      trajectory, // PUT TRAJECTORY HERE
      RobotContainer.s_Swerve::getPose,
      Constants.Swerve.swerveKinematics,
      new PIDController(Constants.AutoConstants.kPController, Constants.AutoConstants.kIController, Constants.AutoConstants.kDController),
      new PIDController(Constants.AutoConstants.kPController, Constants.AutoConstants.kIController, Constants.AutoConstants.kDController),
      thetaController,
      RobotContainer.s_Swerve::setModuleStates,
      RobotContainer.s_Swerve);
        
      // return swerveControllerCommand;
      return new InstantCommand(() -> RobotContainer.s_Swerve.resetOdometry(trajectory.getInitialPose())).andThen(swerveControllerCommand);
  }
  
}

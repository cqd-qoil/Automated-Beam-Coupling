import ZaberMotor

#Motor initialisation
motors = ZaberMotor.ZaberMotor()

try:
    motors.open_motor_connection()
    # print("Coordinates: ", motors.get_motor_coordinates())
    # motors.close_motor_connection()

    # Coordinates:  [7632.0, 14132.0, -5695.0, -6508.0]
    paired = [7632.0, 14132.0, -5695.0, -6508.0]
    # motors.reset_motor_axis()
    motors.move_to_array(paired)
finally:
    motors.close_motor_connection()


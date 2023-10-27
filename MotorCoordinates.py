import ZaberMotor

#Motor initialisation
motors = ZaberMotor.ZaberMotor()
motors.open_motor_connection()
# print("Coordinates: ", motors.get_motor_coordinates())
# motors.close_motor_connection()

# Coordinates:  [7632.0, 14132.0, -5695.0, -6508.0]
paired = [7632.0, 14132.0, -5695.0, -6508.0]
motors.move_to_array(paired)
motors.close_motor_connection()


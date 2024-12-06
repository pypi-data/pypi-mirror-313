class InitMissing(Exception):
    def __str__(self):
        return "Incomplete settings, please initialize"

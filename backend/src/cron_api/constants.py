WHITESPACE = " \n\t\r"

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

LIST_CRONTAB = "crontab -l"

APPEND_CRONJOB_CMD = '(crontab -l 2>/dev/null ; echo "{cronjob}") | crontab -'

DELETE_CRONJOB_CMD = "crontab -l | grep -F -v '{cronjob}' | crontab -"

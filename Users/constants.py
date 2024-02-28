LOGIN_TEMPLATE = 'Users/login.html'
REGISTER_TEMPLATE = 'Users/register.html'
PROFILE_TEMPLATE = 'Users/profile.html'
FOLLOWERS_TEMPLATE = 'Users/followers.html'
LIST_OF_USER_TEMPLATE = 'Users/listUser.html'
FOLLOWING_TEMPLATE = 'Users/following.html'
DISPLAY_PROFILE_ONLY_TEMPLATE = 'Users/display_profile.html'

# messages
USER_EXISTS = "User with {} is already exists. Please check inbox."
USER_CREATED = "User: {} created Successfully."
INVALID_DETAILS_FORMAT = "Please enter details with proper format"
INVALID_USERNAME_FORMAT = "Invalid Username format."
INVALID_PASSWORD_FORMAT = "Invalid Password format."
INVALID_EMAIL_FORMAT = "Invalid Email format."
FIELDS_MISSING = "Fields Missing."
SOMETHING_WENT_WRONG = "Something Went Wrong."
ACCOUNT_DISABLED = "Your account is disabled. Please contact to Administrator."
INVALID_CREDENTIALS = "Invalid Username or Password. Please Try Again."

# Regex
PASSWORD_PATTERN = "^(?!.*\s)(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{10,}$"
USERNAME_PATTERN = "^(?!.*\s)(?=.*[a-z])[a-z0-9-_.]{7,30}$"
EMAIL_PATTERN = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$"
MOBILE_NUMBER_PATTERN = "[0-9]{10}"

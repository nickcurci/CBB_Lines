# authorization: ZWFmNzdmMTI3ZWEwMDNkNGUyNzVhM2VkMDdkNmY1Mjc6

import southpaw

basic_auth_token = 'Basic ZWFmNzdmMTI3ZWEwMDNkNGUyNzVhM2VkMDdkNmY1Mjc6'

fanduel_email = 'nickcurci2012@gmail.com'

fanduel_password = 'Tnt8675309!'

fd = southpaw.Fanduel(fanduel_email, fanduel_password, basic_auth_token)

upcoming = fd.get_contests()
print(upcoming)
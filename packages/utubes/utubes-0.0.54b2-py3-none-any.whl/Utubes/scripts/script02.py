class Rttps(object):

    DATA01 = r"^((?:https?:)?\/\/)"
    DATA02 = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"
    DATA03 = r"^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9\-_]*)"

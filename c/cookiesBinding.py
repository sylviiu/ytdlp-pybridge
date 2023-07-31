class cookiesBinding():
    def __init__(self, cookies):
        self.cookies = str(cookies).splitlines()
        
        while "" in self.cookies:
            self.cookies.remove("")

        print("Cookies: ", self.cookies)
    
    def readline(self):
        if len(self.cookies) > 0:
            return self.cookies.pop(0) + "\n"
        else:
            return ""
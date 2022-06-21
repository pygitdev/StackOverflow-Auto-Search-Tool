from subprocess import Popen, PIPE, DEVNULL
import requests
import webbrowser
from colorama import init, Fore


class StackOverflow:
    def __init__(self, cmd, AutoSearch=True, language="python", Limit=6):
        init(autoreset=True)
        self.CMD = cmd
        self.LANGUAGE = language
        self.returncode = None
        self.limit = Limit
        if AutoSearch:
            self.__start__()

    def extract_error(self):
        problem_finder = Popen(self.CMD, shell=True, encoding="UTF-8", stdout=PIPE, stderr=PIPE)
        output, raw_error = problem_finder.communicate()
        self.returncode = problem_finder.returncode
        if self.returncode == 1:
            """We only need the type of raw_error"""
            errors = raw_error.strip().split("\n")
            TypeOfError = ""
            for error in errors:
                if "Error" in error:
                    TypeOfError = error
            return TypeOfError
        elif self.returncode == 0 and raw_error == "":
            """if file run successfully"""
            return f"{Fore.GREEN}output : {output} \nsuccessfully run"
        else:
            """if given cmd or directory is wrong"""
            return Fore.RED + raw_error

    def get_request(self):
        """sending get request to stackoverflow"""
        url = "https://api.stackexchange.com/"+"/2.3/search?order=desc&tagged={}&sort=activity&intitle={}&site=stackoverflow"
        ERROR = self.extract_error()
        print(ERROR)
        req = requests.get(url.format(self.LANGUAGE, ERROR))
        return req.json()

    def get_answered_urls(self):
        """filtering the answered urls"""
        answered_link = []
        raw_data = self.get_request()
        for data in raw_data["items"]:
            if data["is_answered"]:
                answered_link.append(data['link'])
        return answered_link

    def open_web(self):
        """open the browser tabs if answer is find"""
        urls = self.get_answered_urls()
        limit = 0
        if len(urls) != 0:
                for url in urls:
                    if limit != self.limit:
                        webbrowser.open(url)
                        limit += 1
                    else:
                        break

                print(Fore.LIGHTGREEN_EX+"Stackoverflow opened")
        else:
            print(Fore.YELLOW+"oop! answer not found")

    def __start__(self):
        output = self.extract_error()

        if self.returncode == 1:
            self.open_web()
        else:
            print(output)




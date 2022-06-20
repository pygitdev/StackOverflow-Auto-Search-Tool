from subprocess import Popen, PIPE, DEVNULL
import requests
import webbrowser
from colorama import init, Fore


class StackOverflow:
    def __init__(self, cmd, AutoSearch=True, language="python"):
        init(autoreset=True)
        self.CMD = cmd
        self.LANGUAGE = language
        self.returncode = None
        if AutoSearch:
            self.__start__()

    def extract_error(self):
        problem_finder = Popen(self.CMD, shell=True, encoding="UTF-8", stdout=PIPE, stderr=PIPE)
        output, error = problem_finder.communicate()
        self.returncode = problem_finder.returncode
        if self.returncode == 1:
            """We only need the type of error"""
            error = error.strip().split("\n")
            TypeOfError = error[-1]
            return TypeOfError
        elif self.returncode == 0 and error == "":
            """if file run successfully"""
            return f"{Fore.GREEN}output : {output} \nsuccessfully run"
        else:
            """if given cmd or directory is wrong"""
            return Fore.RED + error

    def get_request(self):
        """sending get request to stackoverflow"""
        url = "https://api.stackexchange.com/2.3/search?order=desc&tagged={}&sort=activity&intitle={}&site=stackoverflow"
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
        if len(urls) != 0:
            for url in urls:
                webbrowser.open(url)
            print(Fore.LIGHTGREEN_EX+"Stackoverflow opened")
        else:
            print(Fore.YELLOW+"oop! answer not found")

    def __start__(self):
        output = self.extract_error()
        if self.returncode == 1:
            self.open_web()
        else:
            print(output)




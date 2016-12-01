"""


Dostepne opcje:
   -c, --console              pobieranie napisow z konsoli
   -q, --quiet                pobiera napisy nie wypisujac zadnych komunikatow
                              ani nie pokazujac zadnych okien (implikuje -d)

   -s, --show-list            pokazuj liste napisow (dziala tylko z -c)
   -d, --dont-show-list       nie pokazuj listy napisow (dziala tylko z -c)

   -l, --lang [jezyk]         preferowany jezyk napisow
   -lb,--lang-backup [jezyk]  zapasowy jezyk napisow

   -o, --options              wywoluje okno konfiguracji programu (tylko GUI)

   -h, --help                 pokazuje tekst pomocy
   -hl,--help-languages       listuje jezyki, w jakich mozna pobierac napisy

"""
import re
STATUS_OK = ' ✓ '
STATUS_NOK = ' × '


# TODO: allow to set parameters for qnapi
class QNapiWrapper:
    """QNapiWrapper class"""

    primary_lang = "pl"
    backup_lang = "en"

    def set_primary_lang(self, lang):
        """Set primary lang
        :type lang: str
        :param lang: name of the lang
        """
        self.primary_lang = lang

    def set_backup_lang(self, lang):
        """Set backup lang
        :type lang: str
        :param lang: name of the lang
        """
        self.backup_lang = lang

    def build_console_cmd(self, argument):
        """Build console command
        :type argument: str
        :param argument: filepath to movie
        :rtype: list
        :return: Returns built command line to execute
        """
        return ["qnapi", '-c',
                "{}".format(argument),
                "-l", "{}".format(self.primary_lang),
                "-lb", "{}".format(self.backup_lang)]

    @classmethod
    def parse_response(cls, response):
        """Parse given response
        :type response: list
        :param response: std output
        :rtype: (int, string)
        :return: Returns status code and parsed response
        """
        parsed_msg = ""
        status = 1

        qnapi_ver_pattern = r"QNapi.+?(?=,)"
        qnapi_sub_found_pattern = r"Rozpakowywanie napisow..."

        qnapi_ver = re.search(qnapi_ver_pattern, str(response))
        if qnapi_ver:
            parsed_msg = qnapi_ver.group()

        match = re.search(qnapi_sub_found_pattern, str(response))
        if match:
            parsed_msg += ">> Subtitles downloaded" + STATUS_OK
            status = 0
        else:
            parsed_msg += ">> Subtitles not found" + STATUS_NOK
            status = 1

        return status, parsed_msg

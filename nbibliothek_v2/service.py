from nbibliothek_v1.service import BibliothekService


class BibliothekService2(BibliothekService):
    def get_lang_pack(self):
        if self.get_lang() == "EN":
            return self._lang_key["EN"]
        else:
            return super().get_lang_pack()

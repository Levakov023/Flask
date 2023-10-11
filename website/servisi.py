from abc import ABC, abstractmethod
from .models import db, Sud, SudskaOdluka

class DodajServis(ABC):
    @abstractmethod
    def dodaj(self, *args, **kwargs):
        pass



class DodajSudServis(DodajServis):
    def dodaj(self, naziv, mesto):
        if not naziv or not mesto:
            return False

        novi_sud = Sud(naziv=naziv, mesto=mesto)
        db.session.add(novi_sud)
        db.session.commit()
        return True


class DodajSudskuOdlukuServis(DodajServis):
    def dodaj(self, naslov, sadrzaj, jmbg_list_str, sud_ime):
        sud = Sud.query.filter_by(naziv=sud_ime).first()

        if sud:
            jmbg_list = [jmbg.strip() for jmbg in jmbg_list_str.split(',') if jmbg.strip()]
            nova_odluka = SudskaOdluka(Naslov=naslov, Sadrzaj=sadrzaj, JMBG_list=jmbg_list, sud=sud)
            db.session.add(nova_odluka)
            db.session.commit()
            return True
        else:
            return False



class AzuriranjeServis(DodajServis):
    def dodaj(self, odluka, naslov, sadrzaj, jmbg_list_str, sud_id):
        if not naslov or not sadrzaj or not jmbg_list_str or not sud_id:
            return False

        odluka.Naslov = naslov
        odluka.Sadrzaj = sadrzaj
        odluka.sud_id = sud_id

        jmbg_list = [jmbg.strip() for jmbg in jmbg_list_str.split(',') if jmbg.strip()]
        odluka.JMBG_list = jmbg_list

        db.session.commit()
        return True